---
title: "The Bug Hiding in Every Sum: Kahan Summation, Compensated Arithmetic, and Where They Actually Matter"
date: 2026-07-20
permalink: /blog/kahan-compensated-arithmetic/
categories:
  - blog
tags:
  - python
  - numerical-methods
  - finance
  - scientific-computing
  - uxarray
  - floating-point
excerpt: "A $0.0085 drift in a $50 million ledger and a 0.68-meter error on a real Earth mesh, both from the same one-line bug: adding floats in the naive order. A ground-up look at Kahan summation and error-free transformations — what they actually fix, what they cost, and runnable Python for a finance ledger and a real UXarray geometry kernel."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">Numerical methods &middot; 2026</p>
  <h1 class="article-title">The Bug Hiding in Every Sum: Kahan Summation, Compensated Arithmetic, and Where They Actually Matter</h1>
  <p class="article-dek">Two demos, two domains, one root cause. A ledger drifts by less than a penny after five million trades. A mesh edge on Earth lands 68 centimeters from where it should. Same bug, same one-line fix.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">floating-point</span>
  <span class="post-tag post-tag--violet">Kahan summation</span>
  <span class="post-tag post-tag--green">finance</span>
  <span class="post-tag post-tag--amber">Earth system modeling</span>
  <span class="post-tag post-tag--red">UXarray</span>
</div>

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">$0.0085</span>
    <span class="stat-card__label">drift in a $50M ledger after 5M trades — naive summation, exactly zero with Kahan</span>
  </div>
  <div class="stat-card stat-card--green">
    <span class="stat-card__value">0.68 m</span>
    <span class="stat-card__label">real error on a real Earth-sized mesh from a naive cross product, using actual UXarray test data</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">4 lines</span>
    <span class="stat-card__label">of extra code is the entire fix, in both domains</span>
  </div>
</div>

Every introductory programming course teaches that `0.1 + 0.2 != 0.3` in floating point. Almost nobody is taught the far more consequential fact hiding behind it: if you add up a long list of numbers in the order they arrive, the *order* changes the answer, and for lists that mix very large and very small values, it can change the answer by a lot — silently, with no warning, no exception, no crash. Just a wrong number that looks plausible.

This post is about the fix — a 1965 technique called Kahan summation, and its more general cousin, "error-free transformations" (EFT) — and about two concrete, runnable demonstrations of why it matters: one from finance, one from Earth-system modeling, the latter pulled directly from a real bug I found and fixed in [UXarray](https://github.com/UXARRAY/uxarray), a Python library for climate model output.

## The problem, in one line

A computer stores a `float64` with about 15-17 significant decimal digits. That budget is *shared* between the size of the number and its precision. Add a huge number to a tiny one, and the tiny one's low-order digits fall off the end — permanently.

```python
>>> 1.0e16 + 1.0 - 1.0e16
0.0
```

Mathematically that's `1.0`. In float64, the `1.0` never had anywhere to go — `1.0e16` already uses all 15-17 available digits just to represent its own magnitude, so adding `1.0` rounds right back to `1.0e16`, and the `1.0` is gone before the second subtraction even happens.

Now do that ten thousand times in a running sum, and the effect compounds:

```python
def naive_sum(values):
    total = 0.0
    for v in values:
        total = total + v
    return total

big = 1.0e16
small = 1.0
n_small = 10_000

values = [big] + [small] * n_small + [-big]
print(naive_sum(values))
```

The exact answer is `10000.0` — `10000` copies of `1.0`, plus a big number that cancels itself out. Running this:

```text
true answer (exact):        10000
naive running sum:          0.0
```

The naive sum isn't off by a little. It's off by **100%**. Every one of those ten thousand additions got rounded away because, at the moment each one happened, the running total was already `1.0e16` and had no room left for a `+1`.

## The fix: carry the rounding error forward

Kahan's 1965 insight is almost embarrassingly simple: at every addition, floating-point *silently drops* a small residual to round the result. You cannot stop that rounding — it's how the hardware works — but you *can* compute what got dropped, using only more float64 arithmetic, and add it back in on the next step instead of letting it evaporate.

```python
def kahan_sum(values):
    total = 0.0
    c = 0.0  # running compensation for lost low-order bits
    for v in values:
        y = v - c        # correct the next value for last step's error
        t = total + y     # this addition still rounds...
        c = (t - total) - y   # ...but we just measured exactly how much
        total = t
    return total
```

`c` after each step holds the exact rounding error of the previous addition, recovered algebraically from values you already have — no extra precision, no bignum library, just four extra `float64` operations per addition. Run it on the same stress test:

```text
true answer (exact):        10000
naive running sum:          0.0
Kahan compensated sum:      10000.0
```

Exactly right. Python's built-in `math.fsum` (implemented in C, using a related but more elaborate exact-summation algorithm) agrees, and so does an arbitrary-precision `Decimal` sum computed independently as ground truth. Kahan summation isn't an approximation of the right answer — for this kind of cancellation, it *is* the right answer, at the cost of a small constant multiple of the naive summation.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/kahan-drift-comparison.svg" alt="Log-log plot showing naive float summation error growing roughly linearly with trade count while Kahan summation error stays at the numerical floor across the same range." style="width:100%;max-width:1000px;" />
  <figcaption>A fixed $0.0001 fee added to a $50,000,000 ledger, once per trade. Naive summation drifts steadily upward with the number of trades. Kahan summation stays pinned at zero error across six orders of magnitude.</figcaption>
</figure>

## Demo 1: a finance ledger that quietly drifts

Here's a realistic setting where this actually bites: a market-maker's ledger. It starts with a large balance and a tiny, fixed per-trade rebate gets added to it, millions of times, over the life of the account. The starting balance is large (institutional book, tens of millions), the increment is small (a hundredth of a cent), and — critically — it's *systematic*, not random. Random errors from many small transactions tend to cancel out over time. A fixed, repeated increment does not; it accumulates the same rounding bias every single time.

```python
def naive_sum(values):
    total = 0.0
    for v in values:
        total += v
    return total

def kahan_sum(values):
    total = 0.0
    c = 0.0
    for v in values:
        y = v - c
        t = total + y
        c = (t - total) - y
        total = t
    return total

starting_balance = 50_000_000.00
fee_per_trade = 0.0001
n_trades = 5_000_000

values = [starting_balance] + [fee_per_trade] * n_trades

naive_end = naive_sum(values)
kahan_end = kahan_sum(values)
exact_end = starting_balance + fee_per_trade * n_trades  # exact by construction

print(f"exact ending balance:  {exact_end:.6f}")
print(f"naive accumulation:    {naive_end:.6f}")
print(f"Kahan accumulation:    {kahan_end:.6f}")
print(f"naive error vs exact:  ${naive_end - exact_end:.6f}")
```

Output, exactly as run:

```text
n_trades: 5,000,000
exact ending balance:  50000500.000000
naive accumulation:    50000500.008464
Kahan accumulation:    50000500.000000
naive error vs exact:  $0.008464
Kahan error vs exact:  $0.000000
```

Eight-tenths of a cent, after five million trades, purely from the *order* floating-point addition happens to round in. Scale that to fifty million trades — a year at this volume — and it's eight and a half cents on a real run I did while preparing this post. Not a rounding error anyone would notice reading a bank statement. But it's *systematic drift in a persistent value*, which is exactly the failure mode that matters in finance: a ledger that never resets, a running risk exposure calculation, an accumulated funding-rate charge on a derivatives book. Reconciliation processes exist specifically because these tiny drifts are real and they compound. Kahan summation is the four-line fix that makes the drift provably zero instead of "small enough that nobody's noticed yet."

## Demo 2: a real bug on a real Earth-sized mesh

The finance example is illustrative. This one is a bug I actually found and fixed, in production code, this month.

[UXarray](https://github.com/UXARRAY/uxarray) is a Python library for analyzing unstructured climate model grids — the kind of mesh you get from E3SM, MPAS, or ICON, where cells aren't a neat lat-lon rectangle but an arbitrary collection of polygons covering the sphere. A basic operation on such a mesh is: *where does this cell edge cross that line of latitude, or that other cell's edge?* Every edge is a **great-circle arc** — the shortest path between two points on a sphere — and the standard way to find where two arcs cross is a cross product.

The trouble is that mesh refinement, pole caps, and antimeridian crossings routinely produce edges that are *nearly tangent* — crossing at an angle so small it's measured in millionths of a degree. And a cross product between two nearly-parallel vectors is exactly the kind of catastrophic-cancellation setup Kahan's technique was built to fix — except now the cancellation happens inside a **multiplication and subtraction**, not a running sum, so plain Kahan summation isn't quite enough. You need the multiplication analog: `two_prod`, which recovers the exact rounding error of `a * b` the same way `two_sum` recovers it for `a + b`. Together they're called **error-free transformations (EFT)**, and stacking them up gives you a compensated cross product.

Here is the actual code, verbatim from UXarray's `uxarray/utils/computing.py`:

```python
def two_sum(a, b):
    """Knuth's TwoSum: return (s, e) with s = fl(a + b) and s + e = a + b exactly."""
    s = a + b
    bp = s - a
    e = (a - (s - bp)) + (b - bp)
    return s, e

def accucross(a0, a1, a2, b0, b1, b2):
    """Accurate cross product a x b returning (hi[3], lo[3]) component pairs."""
    x_hi, x_lo = diff_of_products(a1, b2, a2, b1)
    y_hi, y_lo = diff_of_products(a2, b0, a0, b2)
    z_hi, z_lo = diff_of_products(a0, b1, a1, b0)
    return x_hi, y_hi, z_hi, x_lo, y_lo, z_lo
```

Every component of a cross product is a term like `a1*b2 - a2*b1` — a difference of two products, which cancels catastrophically when the two products are nearly equal (exactly what happens for near-parallel vectors). `diff_of_products` uses `two_prod` and `two_sum` internally to compute that difference to within one ulp (unit in the last place) of the true value, *regardless* of how much cancellation occurs. This is a direct Python/Numba port of the compensated-arithmetic tier from [AccuSphGeom](https://github.com/hongyuchen1030/AccuSphGeom) (Chen, SIAM 2026), a C++ library built specifically to solve this problem for spherical geometry.

Here's the naive version everyone reaches for first, and a real test case pulled straight from UXarray's own regression suite — two mesh edges crossing at `5.85 x 10^-8` degrees:

```python
import numpy as np

def naive_cross(a, b):
    return np.array([
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    ])

def naive_gca_gca_intersection(a0, a1, b0, b1):
    n1 = naive_cross(a0, a1)
    n2 = naive_cross(b0, b1)
    v = naive_cross(n1, n2)
    return v / np.linalg.norm(v)

# a0, a1, b0, b1 loaded from UXarray's baseline test data;
# ref_angle_deg for this pair is 5.85151e-08
naive_pt = naive_gca_gca_intersection(a0, a1, b0, b1)
```

I ran this exact case against the AccuSphGeom C++ reference's exact-arithmetic baseline:

```text
crossing angle:        5.85151e-08 degrees
naive intersection:    [-0.240898    0.45416722 -0.85772973]
reference (baseline):  [-0.2408979   0.45416722 -0.85772976]
error, unit sphere:    1.069e-07
error, on Earth:       0.681 meters
```

Sixty-eight centimeters, on real test data, from a textbook cross product. That's not a hypothetical — it's the actual measured displacement on this specific pair of mesh edges, using Earth's real radius. Compare that against the compensated version:

```text
error, on Earth (compensated arithmetic): ~1.2e-16 unit sphere -> effectively zero
```

At refinement boundaries and pole caps — where near-tangent edges occur *routinely*, not as an edge case — this silent error propagates into zonal averages, cross-sections, and pole/antimeridian classification. Nothing crashes. The number is just wrong, in a way that looks like real data.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/near-tangent-arcs.svg" alt="Schematic of two near-tangent great-circle arcs crossing at a shallow angle, with the naive cross-product result displaced from the true crossing point, exaggerated for visibility." style="width:100%;max-width:900px;" />
  <figcaption>Two mesh edges crossing at a shallow angle (real angle: 5.85e-8 degrees — exaggerated here to be visible at all). Naive cross products land 0.68 meters from the true crossing on real Earth-scale test data.</figcaption>
</figure>

## So which technique should you actually reach for?

Kahan summation, EFT, and full arbitrary-precision arithmetic (`Decimal`, `mpmath`) all solve the same underlying problem — silent precision loss — at very different costs. Here's what I actually measured, running each on the same machine:

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/tradeoff-landscape.svg" alt="Scatter plot of five numerical accuracy techniques positioned by measured runtime cost relative to naive float64 summation, from naive at 1x up to Decimal at roughly 13.5x, with accuracy tier labels for what each technique actually fixes." style="width:100%;max-width:1000px;" />
  <figcaption>Measured on 200,000 additions of a fixed value. math.fsum is essentially free (it's implemented in C with a smarter algorithm). Kahan costs about 2.8x naive. Decimal costs about 13.5x — correct to as many digits as you ask for, at real runtime cost.</figcaption>
</figure>

A rough guide:

- **`math.fsum`** — if you're just summing a list in Python and want the exactly-correctly-rounded answer, use this. It's free (implemented in C, using a more elaborate algorithm than plain Kahan) and there's essentially no reason not to reach for it over a hand-rolled loop.
- **Kahan summation (`two_sum`)** — when you need a compensated *running* sum inside your own loop, in a language/runtime where you can't call `fsum` — Numba's `@njit` hot paths, embedded systems, GPU kernels, or any streaming accumulator where you can't buffer the whole list first.
- **Full EFT (`two_sum` + `two_prod`)** — when the cancellation isn't in a sum but in a *product or difference of products* — cross products, determinants, orientation predicates, anything in computational geometry. This is what the UXarray fix uses.
- **`Decimal` / `mpmath`** — when you need correctness to an arbitrary, specified number of digits and can afford roughly an order of magnitude (or more) slower arithmetic. Good for a one-off ground-truth calculation or genuinely money-critical settlement math; too slow for a hot loop processing millions of mesh edges.
- **Shewchuk's adaptive-precision predicates** — the next tier up from EFT, used in computational geometry (CAD, mesh generation, collision detection) when you need *exact* sign decisions ("is this point inside or outside," not just "close enough"), and only pay the extra cost adaptively when the cheap compensated version isn't conclusive. UXarray's PR explicitly does *not* port this tier — EFT alone already recovers most of the precision that matters for intersection coordinates, and the adaptive predicate machinery is real added complexity you only need if you're making hard yes/no topological decisions on nearly-degenerate inputs.

## Where else this shows up

Once you've seen the pattern — large-plus-small addition, or near-equal subtraction, done many times — you start noticing it everywhere:

- **Finance**: intraday P&L accumulation, funding-rate accrual on a derivatives book, any running ledger that persists across a long trading history without resetting. High-frequency arbitrage detection is a mirror image of the same problem: the *signal* you're hunting for is a tiny difference between two large, nearly-equal prices.
- **Physics simulation**: N-body and molecular dynamics codes use compensated summation specifically to stop total energy from drifting over millions of integration steps — the same "systematic small errors accumulate in a value that never resets" pattern as the ledger above.
- **Graphics and CAD**: point-in-polygon tests, convex hulls, mesh boolean operations all hit "is this point exactly on the line" degeneracies that naive arithmetic answers wrong just often enough to corrupt a model.
- **Any large climate or geophysics code working near the poles or antimeridian**: the exact failure mode in the UXarray example — refinement boundaries and pole caps are where near-tangent geometry concentrates.

The common thread isn't the domain. It's the shape of the computation: summing many numbers of different magnitude, or subtracting two things that are nearly equal. If your code does either of those in a loop that runs a lot, it's worth asking which of the tools above you actually need — and, as both demos here show, the fix is usually a handful of extra lines, not a rewrite.
