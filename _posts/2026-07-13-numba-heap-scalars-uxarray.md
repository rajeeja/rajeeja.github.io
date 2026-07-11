---
title: "Where Your Numbers Live: Killing Hidden Heap Allocations in a Numba Hot Path"
date: 2026-07-13
permalink: /blog/numba-heap-scalars-uxarray/
categories:
  - blog
tags:
  - python
  - numba
  - numpy
  - performance
  - scientific-computing
  - uxarray
  - memory-management
  - cpp
excerpt: "A 1.67× speedup in a spherical-geometry kernel came not from better math but from where the numbers lived. A ground-up look at heap vs. registers, why NumPy's ndarray is always heap while C++'s std::array is not, and how scalarizing a Numba hot path recovered the performance the reference C++ design assumed."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">Performance engineering &middot; 2026</p>
  <h1 class="article-title">Where Your Numbers Live: Killing Hidden Heap Allocations in a Numba Hot Path</h1>
  <p class="article-dek">A 1.67× speedup in a spherical-geometry kernel that had nothing to do with the math and everything to do with memory. A ground-up tour of the stack, the heap, and why a faithful C++-to-Python port can silently get slow.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">Numba</span>
  <span class="post-tag post-tag--violet">NumPy</span>
  <span class="post-tag post-tag--green">memory management</span>
  <span class="post-tag post-tag--amber">C++ interop</span>
  <span class="post-tag post-tag--red">UXarray</span>
</div>

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">1.67×</span>
    <span class="stat-card__label">faster on the constant-latitude intersection dispatcher</span>
  </div>
  <div class="stat-card stat-card--green">
    <span class="stat-card__value">5 → 1</span>
    <span class="stat-card__label">heap allocations per call</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">0.0</span>
    <span class="stat-card__label">change in output — byte-identical across 502 cases</span>
  </div>
</div>

Every so often a performance problem turns out to be a lesson in computer science fundamentals wearing a domain costume. This is one of those. The domain is [UXarray](https://github.com/UXARRAY/uxarray) — a Python library for working with unstructured climate grids — and the specific function computes where an edge of a grid cell (a great-circle arc) crosses a line of constant latitude. It is called once per edge, over meshes with millions of edges. Classic hot path.

The speedup I want to walk through — from ~232 nanoseconds per call down to ~139 — did not come from a cleverer algorithm. The math was already correct and already carefully written. It came from changing *where the intermediate numbers lived* in memory. That is the entire story, and it is worth telling slowly, because the same mistake is easy to make anywhere you port array-oriented code into a `@njit` inner loop.

## The basics: the stack, registers, and the heap

Before any code, the two concepts everything else hangs on.

When a program runs, the operating system hands it a few different regions of memory. Two of them matter here.

**The stack (and registers).** The *stack* is a contiguous block of memory that the CPU manages with a single pointer. "Allocating" a local variable means subtracting a few bytes from that pointer — one instruction. Freeing it means adding them back when the function returns. There is no searching, no bookkeeping, no cleanup step. One level faster still are **registers**: roughly sixteen named slots that live physically inside the CPU core (`rax`, `xmm0`, and friends). A value in a register requires *zero* memory traffic — the arithmetic units read it directly. When a compiler can prove a value is a fixed-size scalar, it keeps it in a register or on the stack.

**The heap.** The *heap* is a general-purpose pool for objects whose size or lifetime is not known at compile time. Asking for heap memory (`malloc` in C, or implicitly `np.empty` in Python) forces the runtime to walk a free-list, find a block that fits, mark it as used, and hand back a *pointer* to it. Later, something has to give that memory back — in C you call `free`; in Python the reference-counter or garbage collector does it for you, but it is not free of cost. And every time you *read* a heap object you go *through* the pointer — an indirection that can miss the CPU cache.

A rough analogy: a register is a pen already in your hand. The stack is a scratchpad on your desk. The heap is a file you request from the archive room downstairs — and then must remember to return.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/numba-stack-vs-heap.svg" alt="Comparison diagram: scalar values px, py, nx, ny living in CPU registers with roughly zero overhead, versus a NumPy ndarray on the heap with a header, a separate data buffer reached by a pointer, and garbage-collection cost of 20 to 30 nanoseconds each." style="width:100%;max-width:1100px;" />
  <figcaption>A three-element vector can be three registers (effectively free) or a full heap object. Same numbers; very different price.</figcaption>
</figure>

The punchline you can already feel: a stack/register value costs approximately nothing, and a heap allocation costs on the order of 20–30 nanoseconds. If a function does *five* heap allocations and only a few nanoseconds of actual arithmetic, then almost all of its runtime is memory bookkeeping. In a loop that runs millions of times, that bookkeeping *is* your runtime.

## The tools, and one crucial detail about each

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/numba-stack-timing.svg" alt="Badges for Python, NumPy, Numba, and a C++ reference, above a bar chart showing the dispatcher dropping from 232 nanoseconds per call before to 139 nanoseconds after, a 1.67 times speedup." style="width:100%;max-width:1100px;" />
  <figcaption>The stack, and the measured result. The C++ reference matters more than it looks — see below.</figcaption>
</figure>

**Python** is the expressive glue that scientists actually write in. It is also, on its own, far too slow for a per-edge geometry kernel.

**NumPy** gives Python its array vocabulary — `ndarray`, vectorized operations, the whole scientific ecosystem. The crucial detail: **a NumPy `ndarray` is *always* a heap object.** Even a three-element array carries a full Python object header (shape, strides, dtype, a reference count) plus a *separate* data buffer that the header points to. There is no such thing as a "small, cheap, on-the-stack" NumPy array. `np.empty(3)` is a heap allocation, full stop.

**Numba** is what makes the Python fast. Its `@njit` decorator compiles a Python function down to native machine code through the LLVM compiler. Numba is genuinely good at this — it will keep scalars in registers and vectorize arithmetic. But it cannot perform miracles it is not allowed to perform: **if your code creates a NumPy array, Numba must emit a real heap allocation for it.** The array type carries a buffer that has to live somewhere addressable and be freed later. There is no way to express "`ndarray`" without a backing allocation.

That last sentence is the whole bug in one line. Nothing was wrong with Numba, or NumPy, or the math. The code simply *asked* for arrays it did not need, and Numba faithfully allocated them.

## The code, before

The intersection routine was written in three clean layers, mirroring a well-structured C++ reference implementation. Each layer returned a NumPy array:

```python
# Layer 1 — the numerical kernel
def _accux_constlat(x1, x2, const_z):
    px, py, nxo, nyo = _accux_constlat_scalar(...)   # computes 4 floats
    pos = np.empty(3)        # allocation #1
    pos[0] = px; pos[1] = py; pos[2] = const_z
    neg = np.empty(3)        # allocation #2
    neg[0] = nxo; neg[1] = nyo; neg[2] = const_z
    return pos, neg

# Layer 2 — validity masks + point selection
def _try_gca_const_lat_intersection(gca_cart, const_z):
    pos, neg = _accux_constlat(x1, x2, const_z)
    ...
    point = np.empty(3)      # allocation #3
    ...
    return point, status, pos, neg

# Layer 3 — dispatcher, returns UXarray's (2, 3) format
def gca_const_lat_intersection(gca_cart, const_z):
    res = np.empty((2, 3))   # allocation #4
    res.fill(np.nan)
    point, status, pos, neg = _try_gca_const_lat_intersection(...)
    ...
    out = _snap_const_lat_endpoint(...)   # allocation #5 inside
    ...
    return res
```

That is **five heap allocations per call**. And notice what most of them are: temporary, three-element vectors that exist only to carry four numbers from one layer to the next. They are born on the heap, read once, and thrown away.

A benchmark made the damage explicit. I timed each layer separately, in a batched in-kernel loop (so the measurement reflects steady-state throughput, not Python overhead). The pure arithmetic — the actual compensated-precision math — was around 5 ns. A full dispatcher call was around 232 ns. Roughly **97% of the time was plumbing**: allocating and freeing those little arrays, not computing anything.

> The benchmark was not there to produce a number. It was a *diagnostic*. By timing each layer with the real math body and then with a trivial body, I could show that the overhead was **independent of the math** — it lived entirely in the array plumbing. That told me exactly where to cut without touching a single line of the verified numerical core.

## The fix: scalarization

The technique has a plain name: **scalarization**. Instead of passing a three-element array between functions, pass the three (or here, four) components as individual scalar arguments. Scalars are exactly the thing Numba keeps in registers. No array type means no allocation — guaranteed by the type system, not by hope.

The kernel already had a scalar-returning variant (`_accux_constlat_scalar`, returning four floats). What was missing were scalar forms of the *predicates* it relied on — the "is this point on the minor arc?" test and the endpoint-snapping helper — which still demanded arrays. So I added scalar cores for those, and, importantly, made the existing array versions delegate to them:

```python
# Logic lives ONCE, in the scalar core:
@njit(cache=True, inline="always")
def _on_minor_arc_xyz(q0, q1, q2, a0, a1, a2, b0, b1, b2, tol=...):
    # ... the real test, all scalars, no arrays ...

# The old array-taking function becomes a thin adapter:
def on_minor_arc(q, a, b, tol=...):
    return _on_minor_arc_xyz(q[0], q[1], q[2],
                             a[0], a[1], a[2],
                             b[0], b[1], b[2], tol)
```

This is the *facade* pattern, and it matters for maintainability: the mathematics is written in exactly one place. The array version is a one-line unpack-and-forward with no logic of its own, so the two can never drift apart.

Then the dispatcher (Layer 3) was rewritten as one flat function that keeps everything in scalars and allocates only the single `(2, 3)` array it is contractually required to return:

```python
@njit(cache=True)
def gca_const_lat_intersection(gca_cart, const_z):
    res = np.empty((2, 3))          # the ONLY allocation — it's the return value
    res.fill(np.nan)

    a0, a1, a2 = gca_cart[0, 0], gca_cart[0, 1], gca_cart[0, 2]
    b0, b1, b2 = gca_cart[1, 0], gca_cart[1, 1], gca_cart[1, 2]

    px, py, nx, ny = _accux_constlat_scalar(a0, a1, a2, b0, b1, b2, const_z)

    pos_valid = math.isfinite(px) and math.isfinite(py) and \
                _on_minor_arc_xyz(px, py, const_z, a0, a1, a2, b0, b1, b2)
    neg_valid = math.isfinite(nx) and math.isfinite(ny) and \
                _on_minor_arc_xyz(nx, ny, const_z, a0, a1, a2, b0, b1, b2)

    # ... scalar snap + write results into res ...
    return res
```

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/numba-alloc-before-after.svg" alt="Two-column diagram. Left: the old three-layer design with five np.empty allocations totalling 232 nanoseconds per call. Right: the scalarized version where intermediates are returned as scalars and only the final (2,3) array is allocated, totalling 139 nanoseconds per call and byte-identical output." style="width:100%;max-width:1100px;" />
  <figcaption>Four of the five allocations were temporary vectors carrying a handful of numbers between layers. Scalarizing removes them; only the required output array survives.</figcaption>
</figure>

The four intermediate arrays are gone. Their values never leave registers between calls. This is, in effect, *manual inlining* — exactly what an aggressive optimizing compiler would do on its own, except that array return values blocked Numba from doing it automatically.

## The C++ angle: why the port got slow in the first place

Here is the part I find genuinely instructive, and it reframes the whole thing from "a bug" to "a language impedance mismatch."

The reference implementation this code was ported from is written in C++. Its vector type is:

```cpp
template <typename T>
using Vec3 = std::array<T, 3>;
```

`std::array<double, 3>` is **not** `std::vector`. A `std::vector` is heap-backed and dynamically sized. A `std::array` is a **fixed-size, stack-allocated value type** — it is, quite literally, three doubles in a box, with no separate buffer and no allocation. C++ passes these by `const&` and returns small structs by value, and the compiler keeps them in registers or on the stack, frequently eliding copies entirely (return-value optimization).

So in the C++ original, the three-layer design was already free of heap traffic. `Vec3` *looks* like an array but *behaves* like three scalars. The layering cost essentially nothing, because the compiler saw through it.

The Python port was algorithmically faithful — it mirrored `Vec3` with `np.empty(3)`. But that single modeling choice quietly converted a free, stack-resident value into an expensive heap object at every layer boundary. **Same code shape, opposite memory behavior**, because `std::array` is a stack type and `np.ndarray` is a heap type.

Seen this way, scalarization is not a hack. It is *restoring the C++ semantics in Python*: pass the components directly, the way `std::array` lives in registers, instead of allocating an `ndarray`. The optimization recovers exactly the performance the reference design already assumed. It closes the impedance gap between the two languages.

## How do we *know* it's correct — and that it's actually the heap?

Two claims need evidence: that the values really do move from heap to registers, and that the output did not change.

**On the memory claim.** This is not a matter of trust. Numba can print the LLVM intermediate representation it generates (`.inspect_llvm()`). The array version contains calls to Numba's runtime allocator (`NRT_MemInfo_alloc`); the scalar version contains none. The type decides the code path, mechanically and inspectably — an `ndarray` type *must* allocate, a `float` type *cannot*.

**On the correctness claim.** A performance change that alters results is a bug, not an optimization. So I dumped the output of the old and new dispatchers over 502 cases — deliberately including the tricky branches: endpoints sitting exactly on the target latitude (which trigger the snapping logic) and arcs that cross the latitude twice (the dual-intersection case). The comparison was **byte-identical**: maximum absolute difference 0.0, and the not-a-number patterns matched exactly. The full geometry test suite (255 tests) and the downstream integration and zonal-average tests all pass unchanged.

The result, on the same benchmark harness:

| | Before | After |
|---|--:|--:|
| Time per call | 232 ns | **139 ns** |
| Heap allocations / call | 5 | **1** |
| Output | — | **identical** |

A **1.67× speedup** on a function in the inner loop of every zonal-mean and conservative-integration call over a mesh.

## What to take away

The algorithmic complexity here never changed — it was O(1) per edge before and after, O(n) over a grid. This was purely a **constant-factor** win. But on a hot path, the constant factor is precisely what you feel, and a 1.67× constant compounds across every mesh, every timestep, every analysis.

A few things I'd carry to the next port:

- **Small fixed-size vectors are a trap when you cross from a stack-typed language to a heap-typed one.** `std::array` → `np.ndarray` looks like a clean translation and is a silent performance regression. Watch for it explicitly.
- **In a Numba hot path, count your `np.empty` calls.** Each one is a heap allocation the JIT cannot remove. If an array exists only to pass a handful of numbers between functions, return scalars instead.
- **Keep the public array API; scalarize the internals.** Callers never saw the change. The `(2, 3)` return shape — the actual contract — stayed exactly as it was.
- **Use benchmarks as diagnostics, not scoreboards.** The measurement that mattered wasn't "how fast is it"; it was "*where* does the time go." Localizing the cost to plumbing rather than math is what made the fix safe and obvious.
- **Prove equivalence.** Byte-for-byte output comparison over the hard cases is cheap insurance that a speedup is really a refactor.

The work described here lives on the [`rajeeja/accusphere` branch](https://github.com/UXARRAY/uxarray/tree/rajeeja/accusphere) of UXarray ([PR #1513](https://github.com/UXARRAY/uxarray/pull/1513)), which ports a set of accurate spherical-geometry kernels based on error-free-transformation (compensated) arithmetic. The precision story in that PR is worth its own post; this one was only about where the numbers live. Sometimes that is the whole game.
