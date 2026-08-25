---
title: "Running Meta Muse Glimmer 30B Locally on M1 Max: Setup, the Metal Crash, and What Actually Limits Local Inference"
date: 2026-08-17
last_modified_at: 2026-08-25
permalink: /blog/muse-glimmer-30b-local-setup/
categories:
  - blog
tags:
  - local-llm
  - apple-silicon
  - llama-cpp
  - opencode
  - muse-glimmer
  - metal
  - agentic-ai
  - benchmarking
excerpt: "Running Meta's open-weights agentic model on a 64 GB M1 Max — quantization choice, the Gated Delta Net Metal crash and the upstream patch that fixes it, and then a controlled four-model benchmark that overturns the first version of this post's main conclusion."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">Engineering note &middot; Local LLM &middot; August 2026</p>
  <h1 class="article-title">Running Meta Muse Glimmer 30B Locally on M1 Max</h1>
  <p class="article-dek">Quantization fit on 64 GB, the Gated Delta Net Metal crash and the upstream patch that fixes it, and a controlled benchmark of what actually limits token generation on this hardware.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">local LLM</span>
  <span class="post-tag post-tag--teal">Apple Silicon</span>
  <span class="post-tag post-tag--amber">llama.cpp</span>
  <span class="post-tag post-tag--violet">opencode</span>
</div>

---

## Correction notice — 25 August 2026

The first version of this post, published 17 August, measured one model on one machine and drew a general conclusion from it: that llama.cpp's Metal backend was extracting only 26% of the memory-bandwidth roofline, and that this said something about the backend as a whole.

That was one uncontrolled datapoint. It could not distinguish three quite different explanations, and I picked the wrong one.

I have since run three control models on the same binary, the same machine and the same flags, measured the roofline denominator instead of reading it off a datasheet, and computed bytes-per-token from the actual tensor tables instead of using file size. The decision rule was written down and committed before any data was collected.

What changed:

| Claim in v1 | Status | What the data says |
|---|---|---|
| Muse Glimmer runs at 5.2 tok/s | **Revised** | 6.55 tok/s under controlled conditions. The original run was contended and possibly power-throttled |
| 26% of a 400 GB/s roofline | **Revised** | 36% of a *measured* 340 GB/s, or 31% of the 400 GB/s datasheet figure |
| Muse Glimmer's new GDN kernels are a plausible culprit | **Refuted** | A 16-month-old dense model gets 39.9%. Muse Glimmer gets 36.4%. A 3.5-point spread |
| "Most of the deficit is backend, not silicon" | **Survives, smaller** | ExecuTorch ~82% vs llama.cpp ~36%, so a 2.3× efficiency gap, not the 3.3× v1 implied |
| "No Apple Silicon laptop reaches 15 tok/s on a 30B model" | **Survives, narrowly** | An M5 Max would reach ~11.8 tok/s at llama.cpp's measured efficiency |

The one genuinely new finding is the flat one. Four models spanning a 6.8× range in bytes-per-token, three architecture families, 35 to 64 layers, and sixteen months of kernel age all land between 123 and 140 GB/s of achieved bandwidth. Whatever is costing the other ~60%, it is not specific to any architecture, and it is not a maturity curve.

I also made an error during this second round and caught it before publishing. It is described in full below, because a post about measurement error that hides its own is not worth much.

The full pre-registration, all six amendments, the raw JSON and the analysis scripts are listed under [reproducing this](#reproducing-this).

---

## Scope and provenance

The setup, crash and patch sections were run on one machine on 17 August 2026. The benchmark sections were run on the same machine on 24–25 August 2026. Numbers are what that machine produced; where a figure comes from a model card or from hardware I do not have, it is labelled as such. Upstream PR states were re-checked on 24 August 2026.

---

## Read This First — Should You Attempt It?

The setup works. The result is not usable interactively on this hardware, and the reason is predictable in advance.

| Your machine | Expect | Advice |
|---|---|---|
| M1/M2 Pro or Max, 32–64 GB | ~6.5 tok/s | Works after patching, but too slow for interactive use. Read the crash section, then run a smaller model instead |
| M1/M2, 16 GB | will not fit | 20 GB resident against 16 GB of shared memory. Don't |
| M4/M5 Max, 36 GB+ | 24–27 tok/s with Meta's ExecuTorch build; ~10–12 tok/s on llama.cpp | Worth it, but the backend matters more than the chip. No Metal crash on these |
| Discrete GPU, 24 GB+ VRAM | 40+ tok/s by roofline | The straightforward answer if you own one |
| Anything with <24 GB usable memory | won't fit at Q4 | Pick a smaller model, not a smaller quant |

The honest summary for older Apple Silicon: **this model is a poor fit, and no flag will fix it.** The limit is memory bandwidth combined with a backend that extracts about a third of it. You cannot configure your way past either.

---

## Machine Specifications

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">Apple M1 Max</span>
    <span class="stat-card__label">10-core CPU (8P+2E) &middot; Metal GPU</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">64 GB</span>
    <span class="stat-card__label">Unified Memory &mdash; shared CPU/GPU pool</span>
  </div>
  <div class="stat-card stat-card--violet">
    <span class="stat-card__value">340 GB/s</span>
    <span class="stat-card__label">Measured streaming read &mdash; 400 GB/s on the datasheet</span>
  </div>
</div>

| Property | Value |
|---|---|
| Chip | Apple M1 Max |
| CPU | 10 cores (8P + 2E) |
| GPU | Integrated, Metal, ~10.4 TFLOP/s fp32 |
| Unified memory | 64 GB |
| Memory bandwidth, datasheet | 400 GB/s (512-bit LPDDR5-6400) |
| Memory bandwidth, measured streaming read | ~340 GB/s |
| System-level cache | 48 MB |
| Storage free at test time | ~206 GB |
| OS | macOS 26.6.1 (build 25G76) |

The gap between 400 and 340 matters, and getting it right took two attempts. See [the denominator](#the-denominator-and-the-error-i-made-finding-it).

---

## Model

Released 9 August 2026 by Meta's Superintelligence Lab under Apache 2.0.

| Property | Value |
|---|---|
| Parameters | 29.6B, dense (not MoE) |
| Architecture | Dense causal transformer + 1.8B ViT-G/14 perception encoder |
| Novel layers | Gated Delta Net (GDN) + Lightning Indexer — hybrid SSM/attention |
| Context window | 131,072 tokens |
| Modalities | Text + image **input**, text **output** — no image generation |
| Reasoning | Always on; exposed in the `reasoning_content` field |
| Speculative decoding | DFlash block-diffusion drafter (16-token blocks), shipped alongside |
| Distilled from | Muse Spark |
| Knowledge cutoff | 4 January 2026 |
| License | Apache 2.0 |

Vision is understanding only. The `--mmproj` encoder lets the model read screenshots, charts, and figures; it cannot produce images. That needs a separate diffusion model.

### Reported benchmarks

From the model card, against same-size peers. Not independently reproduced here.

| Benchmark | Muse Glimmer 30B | Gemma4-31B | Qwen3.6-27B |
|---|:---:|:---:|:---:|
| MCP Atlas | **75.5** | 54.2 | 62.5 |
| SWE-Bench Pro | **51.2** | 36.9 | 50.2 |
| AIME 2026 | **94.7** | 89.2 | 94.1 |
| DeepSearch QA | **74.6** | 61.7 | 71.1 |
| Charxiv Reasoning | **78.8** | 77.7 | 78.4 |

The MCP Atlas and SWE-Bench Pro margins are the ones that matter for tool-driven agent work.

---

## Background: how a model like this is actually made

Skip this if you already know. Everything after it assumes these four ideas, and the performance analysis is impossible to follow without the third and fourth.

### 1. A model is a pile of matrices

"29.6 billion parameters" means 29.6 billion numbers. They are organised into a few hundred matrices, grouped into **layers** — Muse Glimmer has 52, Qwen3-32B has 64. Each layer holds roughly the same set of matrices:

- **Attention projections** (`Q`, `K`, `V`, `O`) — let each position in the text look at earlier positions.
- **Feed-forward / MLP** (`gate`, `up`, `down`) — the bulk of the parameters, typically 60–70%. A per-position nonlinear transform.
- **Norms** — small vectors, negligible in size.

Plus two matrices outside the layer stack: `token_embd`, which maps a token ID to a vector, and the output head, which maps the final vector back to a score per vocabulary entry. These are `vocab_size × d_model`, so for a 200,000-token vocabulary they are not small.

Running the model is: turn text into token IDs, look up a vector per token, push the vectors through all 52 layers of matrix multiplies, and read off which token is most likely next. Append it, repeat.

There is nothing else in there. No database, no lookup of training text. The knowledge is in the numbers.

### 2. Training sets the numbers; you are not doing that

Two phases, both far out of reach of a laptop.

**Pretraining** runs next-token prediction over trillions of tokens of text. The loss is "how surprised was the model by the token that actually came next", and gradient descent nudges all 29.6 billion numbers to reduce it. This is the part that costs millions of dollars and weeks on thousands of accelerators.

**Post-training** takes the pretrained model and shapes its behaviour: supervised fine-tuning on demonstrations, then some preference-optimisation method to make it prefer helpful answers over unhelpful ones. Muse Glimmer additionally is *distilled* from a larger model (Muse Spark) — the big model's output distribution is used as the training target, which transfers some of its behaviour into a smaller parameter count.

Everything in this post is about **inference**: the weights are frozen, and we are only asking how fast the machine can push data through them.

### 3. Quantization: making the numbers smaller

Training produces 16-bit floats. 29.6B parameters at 2 bytes each is 59 GB, which does not fit comfortably in 64 GB of shared memory alongside everything else.

Quantization stores each weight in fewer bits. The `Q4_K_M` scheme used here is roughly 4.5 bits per weight, achieved by splitting weights into small blocks (256 at a time), storing a 4-bit integer per weight, and storing a couple of higher-precision scale factors per block to reconstruct the approximate original value. 4.5 bits works out to **0.5625 bytes per weight**, so 29.6B parameters become about 17 GB — and the "K-quant" family spends extra bits on the layers that are most sensitive, which is why the file is 19.7 GB rather than 16.7 GB.

The quality cost for this model is −0.2% averaged over 15 benchmarks, per Meta's card. That is a good trade and it is why nobody runs fp16 locally.

The critical consequence for everything below: **quantization changes how many bytes you have to read, and reading bytes is the bottleneck.** It is not primarily a memory-capacity trick, it is a bandwidth trick.

### 4. GGUF: the file format

`.gguf` is llama.cpp's container. It holds a key-value header (architecture name, layer count, vocabulary, RoPE settings, chat template) followed by a **tensor table** — one entry per matrix, giving its name, shape, quantization type and byte offset — followed by the tensor data.

The tensor table is what makes the analysis below possible. You can ask a GGUF file exactly how many bytes each matrix occupies without loading it, which is how bytes-per-token gets computed properly instead of guessed from the file size.

---

## Quantization Choice on 64 GB

`meta-models/Muse-Glimmer-30B-GGUF` is ungated and ships two text builds plus two companions.

| File | Disk | Resident (weights + KV) | Quality vs full precision |
|---|---|---|---|
| `KQuant-17GB-Q4_K_M.gguf` | 16.8 GB | ~17 GB | −1.0% |
| **`KQuant-Dynamic-Q4_K_XL.gguf`** | **19.7 GB** | **~20 GB** | **−0.2%** |
| `mmproj-...Q4_K_M.gguf` (vision) | 1.4 GB | +1.4 GB | — |
| `dflash-...Q4_K_M.gguf` (drafter) | 1.6 GB | +1.6 GB | — |

Dynamic + vision + DFlash is ~23 GB resident: 36% of 64 GB, leaving ~41 GB. The degradation figures are Meta's, measured across 15 benchmarks. On a 64 GB machine there is no reason to take the 17 GB build.

Note in advance that dropping to the 17 GB build would save 14% of the per-token traffic and buy you roughly 14% more speed. That is not the lever you are looking for.

---

## Setup

### 1. Install llama.cpp

```bash
brew install llama.cpp
llama-server --version
# version: 0.1.0-dev (build 10450, commit ece963f41)
```

`muse-glimmer` architecture support merged in [PR #26841](https://github.com/ggml-org/llama.cpp/pull/26841) on 10 August 2026, so the minimum build is b10353. Homebrew delivers b10450.

The Homebrew binary is not sufficient on M1 Max — it loads the model and then dies on inference. See the Metal crash section before launching anything.

### 2. Download weights

```bash
pip install huggingface_hub hf_xet   # hf_xet enables the fast xet transfer protocol
mkdir -p ~/Models/Muse-Glimmer-30B-GGUF

python3 << 'EOF'
import hf_xet  # noqa: F401  — importing activates the xet protocol
from huggingface_hub import hf_hub_download
import os

dest = os.path.expanduser("~/Models/Muse-Glimmer-30B-GGUF")
for fname in [
    "Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf",   # 19.7 GB
    "mmproj-Muse-Glimmer-30B-Q4_K_M.gguf",            #  1.4 GB
    "dflash-Muse-Glimmer-30B-Q4_K_M.gguf",            #  1.6 GB
]:
    print(f"Downloading {fname}...")
    hf_hub_download(repo_id="meta-models/Muse-Glimmer-30B-GGUF",
                    filename=fname, local_dir=dest)
print("Done.")
EOF
```

Observed throughput with `hf_xet`: ~150 MB/s, so the 19.7 GB file landed in about two minutes.

---

## The Metal Crash

### Symptom

`llama-server` starts, loads the model, accepts a request, and the process exits before returning a response. No crash report, no Crash Reporter entry. It reproduces on every inference, not intermittently.

```
0.17.667.784  I slot print_timing: eval time = 12501.11 ms / 50 tokens (3.92 t/s)
0.17.667.829  I slot release: id 0 | task 0 | stop processing: n_tokens = 106
# process exits here
```

### Cause

Muse Glimmer introduces two layer types with no precedent in earlier models — Gated Delta Net (a linear-attention recurrent state layer) and Lightning Indexer (sparse retrieval). Both register at startup:

```
I resolve_fused_ops: fused Gated Delta Net (autoregressive) enabled
I resolve_fused_ops: fused Gated Delta Net (chunked) enabled
I resolve_fused_ops: Lightning Indexer enabled
```

Their Metal kernels were still in flight when the model shipped. When a fused GDN op writes output directly into the KV cache it elides an intermediate destination, but the unpatched encode loop still registers that destination's memory range with the concurrency tracker. The spurious barrier that follows aborts on M1 Max's older Metal GPU architecture.

The fix is [ggml-org/llama.cpp #25788](https://github.com/ggml-org/llama.cpp/pull/25788), *"metal: gated_delta_net cache fusion"* by @angt — opened 16 July 2026, **still open as of 24 August 2026**.

Meta's macOS benchmarks were run on M4 Max and M5 Max, which do not exhibit this, which is a plausible reason it was not caught pre-release.

### Workarounds that do not help

| Attempt | Result |
|---|---|
| `-fa off` (disable flash attention) | still crashes |
| `--no-op-offload` | one inference succeeds, then crash |
| `-ngl 0` (CPU only) | still crashes — GDN is in the compute graph either way |
| `-ngl 26` (partial offload) | still crashes |
| `METAL_DEBUG_ERROR_MODE=0` | still crashes |
| `GGML_METAL_N_CB=1` | still crashes |
| drop `-md` (no drafter) | still crashes |

### Applying the patch

PR #25788 adds a `state_out_stride` field to the GDN kernel args struct, adds a `fuse_elide_dst` method that marks consumed nodes elided so the concurrency tracker skips their ranges, and corrects the Metal shader to use the stride.

Build somewhere persistent. My original build lived in `/tmp` and was gone the next time the machine cleared it; `~/src` costs nothing and survives.

```bash
# 1. Full clone — a 3-way merge needs the pre-image blobs
git clone https://github.com/ggml-org/llama.cpp ~/src/llamacpp-head
cd ~/src/llamacpp-head

# 2. Apply PR #25788 as a proper 3-way merge, not a flat patch
git remote add angt https://github.com/angt/llama.cpp
git fetch angt 85a466332d636f88ba5e6a5608f09c92ef00bb27
git fetch origin 86a9c79f8667          # the patch base
git tag pr25788-aug17 85a466332d63     # freeze it locally
git checkout -b bench-pinned 087f94d82e59
git cherry-pick pr25788-aug17

# 3. Build — Metal is on by default on macOS
cmake -B build -DGGML_METAL=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF .
cmake --build build --config Release -j8 --target llama-server

# 4. Confirm
~/src/llamacpp-head/build/bin/llama-server --version
# version: 0.1.1-dev (build 1, commit 087f94d+)
```

Build time on M1 Max: about 90 seconds. After this, inference is stable across repeated requests.

That recipe builds only `llama-server`, which is all you need to *run* the model. The benchmarks below additionally need `llama-bench` and `test-backend-ops`, which live under `tools/` and `tests/`, so they came from a second configure of the same tree with `-DLLAMA_BUILD_TOOLS=ON -DLLAMA_BUILD_TESTS=ON` and `--target llama-bench test-backend-ops`. Also turn `-DLLAMA_BUILD_UI=OFF`: it defaults on at this commit and drags in a full node/npm build.

Two practical notes learned the hard way. The v1 of this post used `git apply` on a `.diff` from the PR page; use `cherry-pick` instead, because all four touched files changed between the patch base and the pin, and a flat apply either fails or silently mis-applies. And **fetch the patch by commit SHA, not by PR URL** — this PR was force-pushed twice on 24 August, and its current head patches a file that does not exist at the pinned commit. The state that existed on 17 August is only reachable through the fork's push-event log, which GitHub expires after about 90 days.

---

## Launching the Server

This is the configuration that was actually used for the v1 timings — text only, all layers on the GPU:

```bash
~/src/llamacpp-head/build/bin/llama-server \
    -m     ~/Models/Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf \
    -a     muse-glimmer-30B \
    -ngl   99 \
    -c     8192 -np 1 \
    --host 127.0.0.1 --port 8080 \
    --jinja --temp 1.0 --top-p 0.95 --top-k 64 \
    --no-warmup
```

Vision and speculative decoding are opt-in additions. Neither was active during any benchmark, so treat their cost and benefit on M1 Max as unmeasured:

```bash
    --mmproj ~/Models/Muse-Glimmer-30B-GGUF/mmproj-Muse-Glimmer-30B-Q4_K_M.gguf \
    -md      ~/Models/Muse-Glimmer-30B-GGUF/dflash-Muse-Glimmer-30B-Q4_K_M.gguf \
    -ngld 99
```

Verify:

```bash
curl -s http://127.0.0.1:8080/health
# {"status":"ok"}

curl -s http://127.0.0.1:8080/v1/models | python3 -c "
import json,sys; m=json.load(sys.stdin)['data'][0]
print(m['id'], '|', m['meta']['ftype'], '|', 'ctx:', m['meta']['n_ctx'])
"
# muse-glimmer-30B | Q4_K - Medium | ctx: 8192
```

### Flags that matter

| Flag | Value | Effect |
|---|---|---|
| `-m` | path | main text model |
| `-ngl` | 99 | offload all layers to the Metal GPU |
| `-c` | 8192–32768 | context, divided across `-np` slots |
| `-np` | 1 | parallel request slots |
| `--jinja` | flag | **mandatory** — activates the embedded chat template; without it the server aborts immediately |
| `--no-warmup` | flag | skips the startup inference. Mandatory on an *unpatched* binary, where the warmup pass is itself the crash. On the patched build it is probably unnecessary — I kept it for continuity with the v1 config and never went back to test removing it |
| `--temp` / `--top-p` / `--top-k` | 1.0 / 0.95 / 64 | Meta's recommended sampling |
| `--mmproj` | path | perception encoder for image input, +1.4 GB |
| `-md` / `-ngld` | path / 99 | DFlash drafter, +1.6 GB — Meta reports a speedup on M4/M5 Max; unmeasured here |

### Context per slot

`-c` is divided across `-np`. With `-c 8192 -np 4` each slot gets 2048 tokens, which is not enough for a model that reasons before answering. Either keep `-np 1` or scale `-c` to match:

```bash
-c 32768 -np 4   # four slots, 8K each
```

### Reasoning depth

Reasoning cannot be disabled, only tuned.

```bash
# server-wide: low / medium / high / xhigh (default high)
--chat-template-kwargs '{"reasoning_strength":"low"}'

# hard cap on thinking tokens
--reasoning-budget 512
```

Per request, put `{"role":"system","content":"Reasoning strength: low"}` in the messages.

Reasoning goes to `reasoning_content`, the answer to `content`. An empty `content` with `finish_reason: "length"` means reasoning consumed the whole budget — raise `max_tokens`.

### Stop tokens

Stop only on `<|end_of_text|>` (200001) and `<|eot|>` (200008). Do not stop on `<|eom|>` — it marks end of message, not end of turn, and stopping there collapses parallel tool calls.

---

## What inference actually does, and why it has two speeds

This is the section that makes the rest of the post readable. Every local-LLM benchmark reports two numbers, they differ by more than an order of magnitude, and the reason is a property of matrix multiplication rather than anything to do with language.

### Prefill and decode

Generating a response happens in two phases.

**Prefill** processes your prompt. If you send 512 tokens, all 512 are pushed through the model *at once*. Every layer's weight matrix is multiplied against a matrix of 512 column vectors, one per token position.

**Decode** generates the answer, one token at a time. It has to be sequential: token 200 depends on token 199, which the model has not produced yet. So each step pushes exactly *one* vector through all 52 layers.

Measured here on Muse Glimmer: prefill 87 tok/s, decode 6.55 tok/s. A 13× difference, on the same weights, the same GPU, the same instant.

### Why: mat×mat versus mat×vec

Take one weight matrix `W` of shape `[4096 × 14336]`, which is a realistic MLP projection. At Q4_K that matrix occupies 33 MB.

**Prefill** computes `W × X` where `X` is `[14336 × 512]` — 512 tokens side by side. You read `W` once, 33 MB, and do `2 × 4096 × 14336 × 512 ≈ 60 GFLOP` of arithmetic. Every byte of `W` that you loaded gets used 512 times.

**Decode** computes `W × x` where `x` is `[14336 × 1]` — a single token. You read the same 33 MB and do `2 × 4096 × 14336 ≈ 117 MFLOP`. Every byte gets used *once*.

The ratio of arithmetic to bytes moved is called **arithmetic intensity**, and it is the whole story:

| Operation | Bytes read | FLOP | Arithmetic intensity |
|---|---:|---:|---:|
| Prefill, 512 tokens (`mat×mat`) | 33 MB | 60 GFLOP | **1820 FLOP/byte** |
| Decode, 1 token (`mat×vec`) | 33 MB | 117 MFLOP | **3.6 FLOP/byte** |

The M1 Max can do about 10.4 TFLOP/s and move about 340 GB/s. Divide them and you get the **ridge point**: 30.6 FLOP/byte. Below that intensity, the GPU finishes its arithmetic and sits waiting for memory. Above it, memory keeps up and the arithmetic units are the limit.

Prefill at 1820 is 60× above the ridge — solidly compute-bound. Decode at 3.6 is 8.5× below it — solidly memory-bound. This is not a llama.cpp property or an Apple property. It is arithmetic, and it is why every "tokens per second" claim needs to say which phase it means.

These are measured numbers, not a derivation. See [the microbenchmarks](#test-3-per-operation-microbenchmarks) below.

### Consequences you can feel

- **Decode speed does not depend on what you asked.** The same weights are read whatever the token is. A poem and a Rust refactor generate at the same rate. (This stops being true for mixture-of-experts models, which route different tokens to different weights. None of the models here are MoE.)
- **Batching is free performance, and you are not getting it.** Serving 32 users at once reads `W` once for all 32 — arithmetic intensity 32× higher, and decode moves toward compute-bound. This is why an API endpoint generates faster per user than your laptop does for one user. At `-np 1` you pay full price for every token.
- **A bigger GPU will not help decode.** The GPU is already idle most of the time.

---

## Measured Throughput, v1: the original real-prompt run

Kept for continuity, and because it is what a real session looks like.

The prompt, in full, was a request for an explanation of gradient descent covering intuition, the math, learning rate, momentum, and practical guidance. It produced 781 tokens of output through `llama-server` with the configuration above. Numbers come from the `timings` block of the API response:

| Metric | Value |
|---|---|
| Prompt ingestion | 48.4 tok/s |
| Token generation | 5.2 tok/s |
| Time to first token | ~0.58 s |
| Total generation | ~150 s for 781 tokens |

**Remote comparison — Claude Sonnet 5 via Argo proxy on `localhost:44445`.** Wall-clock only; the proxy does not expose per-token timings, so this is an effective rate over the whole response and is not directly comparable to a `timings`-derived figure.

| | Local Muse Glimmer 30B | Remote Claude Sonnet 5 |
|---|---|---|
| Generation | 5.2 tok/s | ~104 tok/s |
| Ratio | 1× | ~20× |
| TTFT | ~0.6 s | <0.5 s |
| Data location | on device | leaves the machine |
| Marginal cost | none | metered |
| Context | 8K as configured (131K model max) | 200K |
| Works offline | yes | no |

The controlled re-measurement below gets **6.55 tok/s** for the same model — 26% faster. I cannot fully attribute the gap, and it is worth being explicit about the candidates rather than picking a flattering one:

- **Power state was not recorded.** The machine may have been on battery with Low Power Mode active, which caps GPU clocks. This is my leading suspect and it is entirely my fault for not checking.
- **Background load was not controlled.** The v2 runs record it continuously; see below for how much it matters.
- **Cold page cache.** `--no-warmup` was set, so the first tokens included paging 19.7 GB off SSD.
- **Different harness.** `llama-server` carries HTTP, tokenizer, sampler and template overhead per token that `llama-bench` does not.
- **KV cache growth.** By token 781 there was ~900 tokens of KV to read per step. Small — under 1% of the weight traffic — but not zero.

The direction is consistent: v1 measured a machine that was doing worse than it can. Treat 5.2 as a floor for a real session on a contended laptop and 6.55 as the ceiling for a quiet one. Both are too slow.

---

## The control experiment

### Why one datapoint was not enough

v1 observed one model at one speed and concluded something about llama.cpp's Metal backend in general. But that observation is consistent with at least three different worlds:

- **(A)** llama.cpp Metal is inefficient on this machine for *every* model.
- **(B)** llama.cpp's brand-new Gated Delta Net and Lightning Indexer kernels are slow, while mature dense-transformer kernels are fine.
- **(C)** llama.cpp gives *any* recently-added architecture immature Metal kernels — recency, not exoticism, predicts efficiency.

(B) was the most plausible when I wrote v1 — the GDN kernels were two weeks old and had a live correctness bug, which is not the profile of well-optimised code. (B) and (C) each require a different rewrite, and (A) means the post stands.

You cannot tell these apart with one model. You can tell them apart with three.

### The three controls

| Role | Model | arch | arch age | file GB | B_tok GB |
|---|---|---|---|---:|---:|
| Reference | `Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL` | `muse-glimmer` | ~2 weeks | 19.654 | 18.884 |
| Mature control | `Qwen3-32B-Q4_K_M` | `qwen3` | ~16 months | 19.762 | 19.319 |
| Recency control | `google_gemma-4-31B-it-Q4_K_M` | `gemma4` | ~5 months | 19.598 | 19.583 |
| Phone comparison | `gemma-3n-E4B-it-Q4_K_M` | `gemma3n` | ~14 months | 4.539 | 2.771 |

The first three are within ±0.6% of each other by file size and all in the Q4_K family, so neither the byte count nor the dequantization kernel differs meaningfully between them. The only variable left is the architecture and how long its Metal kernels have been getting attention.

- **Qwen3-32B** is a plain dense transformer — grouped-query attention, RoPE, SwiGLU — in llama.cpp since April 2025. The mature baseline.
- **Gemma 4 31B** is dense but not vanilla: 512-wide keys, per-layer KV head counts, a 5:1 sliding-window interleave, logit softcapping. Shipped March 2026. Recent *without* being exotic, which is exactly what separates (B) from (C).
- **Gemma 3n E4B** is a different question entirely and is discussed [in its own section](#gemma-3n-what-small-actually-buys-and-costs). It is not part of the A/B/C decision.

### Pre-registration

The decision rule, the byte-count table and the exact benchmark invocation were written into `PREREGISTRATION.md` and committed **before any data was collected**. The rule:

| Condition | Verdict |
|---|---|
| Qwen ≤ 35% of roofline and all three within 8 points | **(A)** — backend-wide inefficiency |
| Qwen ≥ 55%, Gemma ≥ 55%, Muse ≤ 35% | **(B)** — GDN kernels specifically |
| Qwen ≥ 55%, Gemma ≤ 40%, Muse ≤ 35% | **(C)** — recency curve |
| 35% < Qwen < 55% | **Indeterminate** — do not force it; escalate to per-op measurement |

The point of writing this down first is that once you see the numbers, every result looks like it supports whatever you already believed. A rule committed in advance cannot be bent to fit.

It did not survive entirely intact, and the honest version of that story is in the amendments: six of them, the fifth of which relaxed a background-load rejection criterion **after** I had seen preliminary numbers. The criterion was genuinely mis-specified — it gated on the *maximum* observed load, which grows mechanically with the number of samples, so it was rejecting windows whose median load was *below* the quiet-machine baseline. But I noticed it because it rejected a run, which means the amendment is not blind, and the pre-registration is weaker than if I had caught it beforehand. The change was applied identically to all four models, and the defect is arguable from the sample counts alone. I think the direction of the verdict is trustworthy. I do not think I get to claim a clean pre-registration.

---

## How performance was measured

Four separate measurements feed the analysis. Each is described with the exact command, because "we benchmarked it" is not a method.

### Test 1: throughput — `llama-bench`

```bash
llama-bench -m "$MODEL" -ngl 99 -p 512 -n 128 -d 0 -fa on,off -t 8 \
            -b 2048 -ub 512 -ctk f16 -ctv f16 -lm auto \
            -r 5 --delay 8 --progress -o json
```

**There is no text prompt.** This surprises people, so it is worth stating plainly: `-p 512` does not send 512 tokens of English. It synthesises 512 dummy token IDs and measures how fast the model ingests them. `-n 128` then generates 128 tokens starting from an essentially empty context.

That is legitimate here, and it is the reason to prefer it over timing a real chat. As established above, for a dense model the decode cost is identical regardless of which token you are processing — the same 18.884 GB of weights gets read either way. Using synthetic tokens removes tokenizer differences, chat-template differences, and any chance that one model happened to write a longer answer. It would *not* be legitimate for a mixture-of-experts model, where token content selects which experts are read.

Flag by flag:

| Flag | Why |
|---|---|
| `-ngl 99` | every layer on the GPU — matches how anyone would actually run this |
| `-p 512` | prefill measurement, 512 synthetic tokens |
| `-n 128` | decode measurement, 128 generated tokens |
| `-d 0` | **start from zero context.** This keeps KV-cache traffic under 0.25% of bytes read for all four models, which is what makes a weights-only roofline exact rather than hand-waved |
| `-fa on,off` | sweep flash attention. The default `auto` resolves *per architecture*, so leaving it would let a hidden per-model decision drive the result |
| `-r 5` | five repetitions per cell |
| `--delay 8` | eight seconds between repetitions |
| `-o json` | the only output format carrying per-repetition samples |

`-d 0` deserves a note because it is the flag that could most easily have produced a flattering answer. At `-d 8192` the KV term would range from +1.0% for Muse Glimmer (2 KV heads, plus a 2048-token sliding window over three quarters of its layers) to +16.0% for Gemma 4 (512-wide keys on its global layers). That 15-point spread would have made Muse Glimmer look better against exactly the models it was being compared to — biasing the measurement toward the hypothesis under test. Depth zero removes the term instead of modelling it.

Two full passes were run, the second in reverse model order and starting deliberately hot, so any thermal drift shows up as an order-dependent gradient rather than hiding inside a single ordering.

### Test 2: background load — a sampler running alongside

Every benchmark window had a sampler recording, every three seconds:

```
foreign% = (100 - system_idle%) - bench_cpu% / n_cpu
```

That is: total CPU busy, minus the benchmark's own legitimate CPU use, normalised across ten cores. It answers "how much of this machine is something other than the thing I am measuring".

Originally this was a *rejection* criterion — windows above a threshold were discarded. That turned out to be both statistically wrong and unrealistic: nobody runs a model on a machine with nothing else on it. It is now recorded as a covariate and reported. Median foreign load across the eight windows ranged from 10.0% to 16.6%.

### Test 3: per-operation microbenchmarks

```bash
test-backend-ops perf -b Metal -o MUL_MAT --output csv
test-backend-ops perf -b Metal -o CPY --output csv
```

This is llama.cpp's own per-kernel harness. It runs a single operation in isolation, thousands of times, and reports time and throughput. It is what produced the arithmetic-intensity table above:

```
MUL_MAT(q4_K, m=4096, n=1,   k=14336):   157.22 us/run -> 747 GFLOPS,  3.6 FLOP/byte
MUL_MAT(q4_K, m=4096, n=8,   k=14336):   867.75 us/run -> 1.08 TFLOPS, 28.4 FLOP/byte
MUL_MAT(q4_K, m=4096, n=512, k=14336): 12741.96 us/run -> 4.72 TFLOPS, 1820 FLOP/byte
```

`n` is the batch: `n=1` is decode, `n=512` is prefill. Same matrix, same kernel, 6.3× the FLOP rate purely because the bytes get reused.

Converting the `n=1` row to bandwidth: 33.0 MB of weights in 157.22 µs is **210 GB/s**. Hold onto that number.

### Test 4: streaming bandwidth — the denominator

Described in its own section below, because getting it right took two attempts and the first one was wrong.

---

## B_tok: the bytes that actually move

The roofline is `bandwidth ÷ bytes-read-per-token`. v1 used the file size, 19.65 GB, for the second term. That is wrong, and it is wrong in a direction that mattered.

**`token_embd` is not streamed.** It is a lookup table of shape `vocab_size × d_model`. Generating a token reads exactly *one row* of it — the row for the token you just produced. A few kilobytes, not the whole matrix. Counting all of it as per-token traffic overstates the denominator.

Except when the model has **tied embeddings**, where the same matrix serves as both the input lookup and the output head. Then it *is* fully read every token, because computing the score for every possible next token requires multiplying against every row.

So the correction is per model, and its size tracks vocabulary size:

| Model | file GB | `token_embd` | tied? | gathered, not streamed | **B_tok** | file-size error |
|---|---:|---:|:--:|---:|---:|---:|
| Muse Glimmer Q4_K_XL | 19.654 | 0.756 | no | 0.770 | **18.884** | +4.1% |
| Qwen3-32B Q4_K_M | 19.762 | 0.438 | no | 0.443 | **19.319** | +2.3% |
| Gemma 4 31B Q4_K_M | 19.598 | 1.156 | **yes** | 0.015 | **19.583** | +0.1% |
| Gemma 3n E4B Q4_K_M | 4.539 | 0.302 | **yes** | 1.762 | **2.771** | +63.8% |

Note the direction. The correction is largest for Muse Glimmer (+4.1%) and essentially zero for Gemma 4 — because Muse Glimmer has a 202,048-token vocabulary and untied embeddings, while Gemma 4 ties its embeddings and therefore streams the whole thing. Using file size would have inflated Muse Glimmer's apparent bandwidth relative to its controls, flattering exactly the model under suspicion.

Gemma 3n is the extreme case at +63.8%, and for a different reason: its embeddings *are* tied, so `token_embd` is fully streamed and not subtracted at all. What comes out instead is a 1.762 GB `per_layer_token_embd` tensor, part of its per-layer-embeddings design, which is another per-token gather. Using the file size would have made it look nearly twice as bandwidth-efficient as it is.

These come from parsing the GGUF tensor tables, not from estimation. Recomputing v1's headline number with the corrected value: `5.2 × 18.884 = 98.2 GB/s`, which is 24.6% of 400 GB/s — so v1's "26%" was itself inflated by the file-size error.

---

## The denominator, and the error I made finding it

v1 divided by 400 GB/s, the datasheet figure. That is a pin rate: width times clock, `64 bytes × 6.4 G/s = 410 GB/s`. No real workload reaches it, so dividing by it makes every piece of software look worse than it is.

The first attempt at a real number came from `test-backend-ops`:

```
CPY(q4_0->f32, ne_src=[8192,512,2,1])
  8980 runs - 121.34 us/run - 37376 kB/run - 293.79 GB/s
```

37,376 kB is 36.5 MB, re-read 8,980 times, on a machine with a 48 MB system-level cache. Whatever that measures, it is not the rate at which you can stream 19 GB. So I wrote a direct measurement: allocate fp16 buffers from 16 MB up to 2 GB, run a read-only reduction over each, and time it.

**And I misread the result.** The raw curve looked like this:

| Working set | Measured read |
|---:|---:|
| 16 MB | 33.7 GB/s |
| 48 MB | 73.5 GB/s |
| 128 MB | 126.6 GB/s |
| 512 MB | 291.9 GB/s |
| 2048 MB | 336.3 GB/s |

Bandwidth rising steeply and then flattening, with the steep part below 48 MB. I wrote that up as a cache knee: small working sets sit in the SLC, large ones go to DRAM, ratio 0.22×.

That reading is backwards, and it should have been obvious. A working set that *fits* in cache should be **faster**, not slower. Cache cannot make you slower than DRAM.

The real cause was my instrument. The machine had torch 1.13.1, which predates `torch.mps.synchronize()`, so the script waited for the GPU by pulling one element back to the host — a fixed cost of roughly 0.3–0.8 ms per timed iteration. Fitting `time = overhead + bytes/bandwidth` over the large sizes recovers it: that fixed cost is **69% of the 16 MB measurement and 5% of the 2 GB one**. Subtract it and the curve is flat from 256 MB upward. There is no knee. There never was.

I could not resolve a cache effect with this tool, and I am not claiming one.

The overhead-corrected extrapolation is also not reportable: it is a two-parameter fit over a short lever arm, and it moved from 354 GB/s to 400 GB/s between two consecutive runs. The second figure is the datasheet pin rate exactly, which is a good sign the fit is fitting noise.

**So: `R_stream = 340 GB/s`,** the mean of the raw largest-working-set reads across two runs (336.3 and 343.3). This is a *measured lower bound* — instrument overhead can only push it down — which means efficiency percentages computed against it are *upper* bounds. Percentages against the 400 GB/s datasheet figure are also given throughout, about 3 points lower.

The load-bearing result below is a comparison *between* models, which is unaffected by this choice entirely.

---

## Results

Two passes, reverse order, five repetitions per cell, flash attention swept. Decode figures are medians of repetitions 2–5 (dropping the first, which absorbs page-cache warmup), averaged across passes.

### Decode — flash attention on

| Model | arch | arch age | B_tok | tok/s | achieved GB/s | % of 340 | % of 400 |
|---|---|---|---:|---:|---:|---:|---:|
| Muse Glimmer 30B | `muse-glimmer` | ~2 weeks | 18.884 | 6.55 | 123.6 | **36.4%** | 30.9% |
| Gemma 4 31B | `gemma4` | ~5 months | 19.583 | 6.36 | 124.5 | **36.6%** | 31.1% |
| Qwen3-32B | `qwen3` | ~16 months | 19.319 | 7.02 | 135.7 | **39.9%** | 33.9% |
| Gemma 3n E4B | `gemma3n` | ~14 months | 2.771 | 50.45 | 139.8 | **41.1%** | 34.9% |

Flash attention off moves everything by less than a point and changes no ordering.

**The spread across the three size-matched models is 3.5 percentage points.** A two-week-old architecture with a live correctness bug in its Metal kernels, a five-month-old one, and a sixteen-month-old one all extract essentially the same fraction of memory bandwidth.

Hypotheses (B) and (C) are refuted. There is no GDN penalty and there is no maturity curve. The pre-registered rule returns **indeterminate** on the letter of it — Qwen3 lands at 39.9%, inside the 35–55% dead band that says "do not force a verdict" — but the *shape* is unambiguously (A)'s: everything clusters. The honest summary is that (A) is right about the pattern and v1 was wrong about the magnitude. The backend is uniformly inefficient, and it is less inefficient than v1 claimed.

### Prefill — the ordering inverts

| Model | pass 1 | pass 2 | mean |
|---|---:|---:|---:|
| Muse Glimmer 30B | 83.4 | 90.8 | **87.1** |
| Qwen3-32B | 77.3 | 72.1 | 74.7 |
| Gemma 4 31B | 74.8 | 73.3 | 74.1 |
| Gemma 3n E4B | 689.3 | 684.9 | 687.1 |

The newest and most exotic architecture is the **fastest** of the three at prompt ingestion, by 17%. When the GPU is actually saturated — the compute-bound regime — Muse Glimmer's kernels are not merely adequate, they win.

This is the single cleanest refutation of the "immature kernels" story. Immature kernels would be slow in both regimes. These are fast where compute matters and average where bandwidth matters, which is the signature of a bandwidth problem that has nothing to do with the kernels.

### Where the missing bandwidth is

Three measurements of the same machine, in increasing order of realism:

| What | Achieved read bandwidth |
|---|---:|
| Streaming read, 2 GB working set | 340 GB/s |
| Isolated `q4_K` batch-1 mat-vec, 33 MB re-read 6,816 times | 210 GB/s |
| Full decode, four real models | 124–140 GB/s |

The isolated kernel — under conditions far friendlier than reality, with a working set that fits in cache and is read thousands of times — already reaches only 62% of streaming bandwidth. Real decode then reaches only about 60% of *that*.

So the deficit is in two places, and neither of them is a specific architecture's kernels. Roughly a third is lost inside the mat-vec kernel itself even in the best case, and roughly another third to everything the full graph does that an isolated kernel does not: dispatching hundreds of small operations per token, synchronising between them, and touching the KV cache and norms and residuals between the large multiplies.

### A dead end worth reporting

My first explanation for the residual was fixed per-layer dispatch overhead — Metal command-buffer cost paid once per layer regardless of layer size. It predicts that microseconds-per-layer should be roughly constant across models. It is not:

| Model | layers | MB/layer | µs/layer |
|---|---:|---:|---:|
| Muse Glimmer | 52 | 363.2 | 2936 |
| Gemma 4 31B | 60 | 326.4 | 2621 |
| Qwen3-32B | 64 | 301.9 | 2226 |
| Gemma 3n E4B | 35 | 79.2 | 566 |

Per-layer cost varies 5.2× and is monotonic in bytes-per-layer, which itself varies 4.6×. The cost is proportional to data moved, not to the number of dispatches — the model with the *most* layers is not the slowest per layer, the one with the fattest layers is. Fixed-overhead-per-layer is refuted, by my own data, and I am recording it because the negative result is what rules out the most intuitive explanation.

### Reproducibility, and one failure

Pass-to-pass agreement was within 3% for every model except Gemma 4, which differed by 11.7% at flash-attention-on and 6.6% at flash-attention-off.

It is not thermal and not ordering — the reverse-order second pass rules both out, and the other three models agree across it. The recorded background load points at contention:

| Window | median | 90th pct | peak | tok/s |
|---|---:|---:|---:|---:|
| Gemma 4, pass 1 | 12.8% | 18.6% | 32.8% | 6.73 |
| **Gemma 4, pass 2** | **16.6%** | **24.4%** | **42.3%** | **5.98** |
| Gemma 3n, pass 2 | 16.3% | 20.5% | 23.8% | 50.06 |
| other five windows | 10.0–14.2% | 18.6–22.4% | 26.5–36.3% | — |

Gemma 4's second pass is the only window whose 90th-percentile load exceeded 24% and whose peak exceeded 40%, and it is the slowest cell in the matrix. But note the third row: Gemma 3n's second pass had almost the same *median* load with much lower peaks, and lost only 1.5%. So sustained peaks look like the thing that hurts rather than average load — which is plausible, and which eight windows are nowhere near enough to establish. I am reporting the association, not claiming a dose-response curve.

This is also the reason the load criterion was changed from a rejection filter to a recorded covariate partway through. Under the original design that window would have been discarded and the sensitivity never observed. The practical takeaway is unchanged either way: close things before benchmarking, and remember that the number you actually live with on a working machine is the contended one.

Pageouts grew from 2,019 to 2,473 across the full matrix, about 7 MB, confirming RAM was never exceeded.

---

## Gemma 3n: what "small" actually buys, and costs

Gemma 3n E4B was included to answer a different question — how a laptop compares to a phone — and it turned into the most interesting result in the set.

**50.45 tok/s on the same machine, same binary, same flags.** Against Muse Glimmer's 6.55. That is 7.7× faster, and it comes almost entirely from reading 6.8× fewer bytes per token: 2.771 GB versus 18.884 GB. Its achieved bandwidth, 139.8 GB/s, is barely different from anyone else's.

That is the whole lesson in one line. **Nothing about the software got better. It just had less to read.**

### How it gets small

"E4B" means *effective* 4B — the model has more parameters than that on disk but activates about 4B worth per token, through two mechanisms:

- **MatFormer nesting.** The model is trained so that a smaller model is embedded inside the larger one, sharing weights, like nested Russian dolls. You can extract and run the smaller nesting without retraining.
- **Per-layer embeddings (PLE).** A large chunk of the parameters — the 1.762 GB `per_layer_token_embd` tensor — is a lookup table indexed by token, not a matrix you multiply against. It is *gathered*, a row at a time, not streamed. This is why its file size is 4.539 GB but its B_tok is 2.771 GB.

PLE is a genuinely clever bandwidth trick: it moves capacity into a structure that costs a lookup instead of a full read. It is also why file-size-based roofline math is off by 64% for this model.

### What you give up

Quality was **not measured here** — this benchmark measured speed, and I will not invent numbers for the other axis. But the structural trade-offs are not mysterious:

- **Knowledge.** Fewer active parameters means less memorised world knowledge. A 4B model has read the same internet and retained much less of it.
- **Reasoning depth.** 35 layers versus 52. Multi-step problems that need to hold several intermediate results have less machinery to hold them in.
- **Long-context coherence.** Small models drift over long outputs and lose track of constraints stated early in a prompt.
- **Code and agentic work.** This is where the gap is widest. Muse Glimmer's whole reason to exist is the MCP Atlas and SWE-Bench Pro margins in the table at the top. A 4B model is not doing multi-step tool use with a large tool schema.

The right way to hold both facts: Gemma 3n at 50 tok/s is genuinely interactive and Muse Glimmer at 6.5 tok/s genuinely is not, and Muse Glimmer would do things Gemma 3n cannot attempt. On this hardware you do not get to have both.

### Laptop versus phone

| | tok/s | TTFT |
|---|---:|---:|
| M1 Max, 2021 laptop | 50.45 | — |
| Pixel 10 Pro XL, 2025 phone | 9.74 | 557 ms |
| ratio | **5.2×** | — |

Two caveats before reading anything into that ratio, both mine. The laptop figure is Gemma 3n E4B Q4_K_M under `llama-bench`, measured here. **The phone figure is second-hand**, reported to me for a Gemma-3n-class model on the device's own runtime — I did not run it, I did not verify the exact checkpoint or quantization, and the on-device runtime is not llama.cpp. So this is a rough same-family comparison, not the controlled same-binary comparison the rest of this post is built on.

And I did not measure the phone's memory bandwidth, so **no roofline percentage is quoted for it.** The ratio is a throughput comparison, not an efficiency comparison.

With those attached: a four-year-old laptop is roughly five times a current flagship phone in the same weight class. Less than the spec-sheet gap would suggest, and the phone number is entirely usable — 9.74 tok/s is about reading speed.

---

## Small, domain-specific models are probably the interesting direction

This is opinion, flagged as such, but it is opinion the measurements above push me toward.

The bottleneck for local inference is bytes-per-token, and bytes-per-token is set by parameter count and quantization. Everything else — a faster GPU, a better backend, more RAM — is a smaller lever than simply having fewer parameters to read. Gemma 3n gets 7.7× on this machine by being small. No amount of backend work is going to get llama.cpp 7.7×.

And most of a general-purpose 30B model is capacity you are not using. If your local model exists to write Python, summarise papers in one field, or drive a specific set of tools, the parameters holding sixteenth-century poetry and Portuguese football statistics are pure bandwidth cost on every token you generate.

The pieces to make small-and-specific work are largely in place: distillation from a strong teacher, which is how Muse Glimmer itself was made; LoRA and QLoRA fine-tuning that fits on a single consumer machine; MatFormer-style nesting that lets one training run yield several sizes; retrieval, which moves factual recall out of the weights and into a database where updating a fact costs a write instead of a training run.

The plausible shape is a small model that is *actually good* at one domain, with retrieval for facts and tool calls for anything requiring precision — running at 40+ tok/s on hardware people already own, rather than a 30B generalist at 6.5 tok/s.

The honest counterargument, which I take seriously: the agentic benchmarks at the top of this post are exactly where small models are weakest, and Muse Glimmer's lead on MCP Atlas is large. Multi-step tool use seems to need general capability in a way that summarisation does not. Nobody has yet shown a 4B model doing competent agentic work in a narrow domain. If that turns out to be impossible, the argument above is wrong.

---

## Revised hardware guidance

### Comparison with Meta's published figures

Meta's numbers come from their ExecuTorch PTE artifact, not this GGUF, so the per-token byte count may differ and these percentages are approximate. M5 Max bandwidth is corrected here from v1's "~600 GB/s" — it is 614 GB/s for the 40-core part and 460 GB/s for the 32-core.

| Hardware | Backend | tok/s | Bandwidth | Achieved GB/s | % of bandwidth |
|---|---|---:|---:|---:|---:|
| M1 Max (measured here) | llama.cpp | 6.55 | 340 measured / 400 spec | 123.6 | **36% / 31%** |
| M4 Max (Meta) | ExecuTorch | 23.7 | 546 spec | 447.6 | **~82%** |
| M5 Max, 40-core (Meta) | ExecuTorch | 26.6 | 614 spec | 502.3 | **~82%** |

The two ExecuTorch datapoints land on the same efficiency from different chips and different reported speeds, which is a mild consistency check on the whole framework — the model of "bytes per token divided by bandwidth" reproduces both.

The v1 conclusion survives with a smaller magnitude. M4/M5 Max carry 1.4–1.5× the bandwidth of M1 Max, which is real but nowhere near the ~4× observed gap. The larger factor is that ExecuTorch extracts about 82% of available bandwidth while llama.cpp extracts about 36% — a 2.3× efficiency gap, not the 3.3× v1 implied. ExecuTorch runs a pre-compiled graph with MLX-native Metal kernels; llama.cpp dispatches through a runtime-interpreted path.

Most of the deficit is still backend, not silicon. It is just not *as* much of it, and — the correction that matters — it is not specific to Muse Glimmer's architecture.

### What it would take to be bearable

Around 10 tok/s a response arrives roughly as fast as you read it. Around 25 it stops feeling like waiting.

Required bandwidth is `target × 18.884 GB ÷ efficiency`:

| Target | With a compiled backend (82%) | With llama.cpp today (36%) |
|---|---|---|
| 10 tok/s | ~230 GB/s | ~525 GB/s |
| 15 tok/s | ~345 GB/s | ~790 GB/s |
| 25 tok/s | ~575 GB/s | ~1310 GB/s |

At llama.cpp's measured efficiency, an M5 Max 40-core — 614 GB/s, the fastest Apple laptop available — would reach about **11.8 tok/s** on this model. Better than this machine's 6.55, and still short of comfortable. The v1 claim that no Apple Silicon laptop reaches 15 tok/s on a 30B model through llama.cpp survives, more narrowly than it was stated.

Four levers, cheapest first:

1. **Run a smaller model.** By far the strongest lever, and the measurement above quantifies it: Gemma 3n E4B gets 7.7× on this exact machine with no changes to anything else. Bytes-per-token scale with parameter count, and nothing else in this analysis moves by more than about 2×. Note this is a *model* change, not a *quant* change — dropping to the 17 GB build saves 14% of the traffic and buys 14% of speed.
2. **Close your other applications.** Small, free, and measurable: the one benchmark window that ran under heavy background load was 11.7% slower than its twin.
3. **Wait for a compiled backend.** ExecuTorch reaches ~82% of roofline on M4/M5. The same efficiency on this machine would be ~14.8 tok/s — usable, no hardware purchase. Extrapolated, not measured, and the number I would most like to see someone produce.
4. **Buy bandwidth, or buy a discrete GPU.** M5 Max gets to 26.6 tok/s with Meta's backend. A 24 GB card in the RTX 3090/4090 class carries roughly 940–1010 GB/s and CUDA backends run close to roofline, which puts a 30B Q4 in the 40+ tok/s range. Derived from spec sheets, not tested here.

Where this machine was specifically inferior: not RAM (41 GB spare), not GPU compute (idle most of every token), not storage or CPU. Memory bandwidth, and a backend that extracts about a third of it.

### Where local still wins

- Code or data that must not leave the machine.
- Genuinely offline work — travel, air-gapped sites.
- Batch jobs. Fifty file summaries queued overnight do not care about 6.5 tok/s.
- Very high sustained volume, where marginal token cost dominates hardware cost.
- Anything a small model can do well. This is the growing category.

For interactive 30B sessions on M1 Max, a remote frontier model remains the right call.

### Paths to usable local speed

- **Short term.** [PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788) merges and reaches Homebrew. Stability, not speed — still ~6.5 tok/s, but no patched build to maintain, and `--no-warmup` becomes unnecessary.
- **Medium term.** ExecuTorch Metal. `meta-models/Muse-Glimmer-30B-ExecuTorch-PTE` is a pre-exported artifact with Metal and MLX kernels compiled from PyTorch via `torch.export`. At the ~82% these figures imply, M1 Max would land near 14.8 tok/s — a 2.3× gain with no hardware change.
- **Also medium term, and now better supported.** Given that the deficit is uniform across architectures rather than specific to new ones, generic llama.cpp graph-level work — fusing more operations, cutting per-token dispatch count — would lift every model at once. The measurements above suggest that is where the headroom is, not in per-architecture kernel tuning.
- **Long term.** Newer hardware, or smaller models. The second one is available today.

---

## opencode Integration

opencode's `@ai-sdk/openai-compatible` provider talks to `llama-server`'s OpenAI-compatible endpoint directly. In `~/.config/opencode/opencode.json`:

```json
{
  "provider": {
    "local-llamacpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local llama.cpp (Muse Glimmer)",
      "options": {
        "baseURL": "http://127.0.0.1:8080/v1",
        "apiKey": "none"
      },
      "models": {
        "muse-glimmer-30B": {
          "name": "Muse Glimmer 30B (local, M1 Max)",
          "contextLength": 8192,
          "attachments": true
        }
      }
    }
  }
}
```

Switch per session with `/model`, or set the default with `{ "model": "local-llamacpp/muse-glimmer-30B" }`.

One tuning note: send `max_tokens` of 800 or more. The model reasons before answering, and a budget that runs out mid-reasoning returns an empty `content`. For interactive use, pair that with a `Reasoning strength: low` system message.

---

## Optional: UXarray MCP Alongside It

Not required to run Muse Glimmer — the two are independent. It is worth pairing only if you do climate mesh work, and the reason is cost structure.

`uxarray-mcp-server` exposes 31 tools for mesh analysis (`inspect_mesh`, `calculate_area`, `calculate_zonal_mean`, `run_analysis` for vorticity/divergence/gradient/remap, `plot_dataset`, and others). Enabling it injects roughly 10,600 tokens of tool schema into every request, whether or not the turn touches a mesh. On a metered remote model that is a standing per-turn cost, which is why it stays off:

```json
"mcp": {
  "uxarray": {
    "type": "local",
    "command": ["uv", "--directory", "/Users/mbook/uxarray-mcp-server",
                "run", "uxarray-mcp", "serve"],
    "enabled": false
  }
}
```

`"enabled": false` means opencode neither starts the subprocess nor includes the schema. `true` starts it at launch and injects all 31 schemas into every request. There is no per-tool granularity — it is all or nothing per server, so the convention is to flip it on for mesh sessions and back off afterwards.

Running locally the schema is free in dollar terms, so the flag can stay on. It is not free in latency: 10,600 tokens of added prompt costs about two extra minutes of ingestion per turn at the measured 87 tok/s prefill rate. That is the prefill number doing real work — it is the one that governs how much prompt you can afford.

---

## Reproducing this

Everything is scripted and the raw outputs are kept.

| File | What |
|---|---|
| `PREREGISTRATION.md` | the decision rule, committed before data collection, plus all six amendments including the two errors described above |
| `run_pass.sh` | the benchmark runner — power gate, load sampler, both passes |
| `gguf_btok.py` | parses GGUF tensor tables to compute B_tok |
| `stream_bw.py` | the streaming-bandwidth measurement, with the overhead artifact documented in the source |
| `analyze.py` | applies the pre-registered rule mechanically to the raw JSON |
| `*_pass{1,2}.json` | raw `llama-bench` output, per-repetition |
| `*_pass{1,2}.load.json` | background-load statistics per window |

The analysis is one command:

```bash
python3 analyze.py --rgpu 340
```

`analyze.py` implements the decision rule as code specifically so that reading the result cannot influence how it is scored.

---

## Summary

| | |
|---|---|
| Model | Meta Muse Glimmer 30B, Apache 2.0, August 2026 |
| Quant on 64 GB M1 Max | KQuant-Dynamic Q4_K_XL — 19.7 GB on disk, 18.884 GB read per token |
| Blocking bug | GDN Metal kernel crash, every inference, M1 Max |
| Fix | cherry-pick [PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788), rebuild (~90 s); still open upstream as of 24 Aug 2026 |
| Required flags | `--jinja` and `-ngl 99`; plus `--no-warmup` on an unpatched binary |
| Measured decode | 6.55 tok/s controlled (5.2 tok/s in a contended real session) |
| Measured prefill | 87 tok/s — the fastest of the three 30B-class models tested |
| Memory bandwidth | 340 GB/s measured streaming read, 400 GB/s datasheet |
| Achieved | 123.6 GB/s — 36% of measured, 31% of datasheet |
| Control result | Qwen3-32B 39.9%, Gemma 4 31B 36.6%, Muse Glimmer 36.4%. A 3.5-point spread across 16 months of kernel age |
| Binding constraint | memory bandwidth plus a uniformly inefficient backend — **not** the new GDN kernels, which win at prefill |
| Fastest lever | a smaller model. Gemma 3n E4B: 50.45 tok/s on the same machine, 7.7× |
| Phone comparison | Gemma 3n E4B — M1 Max 50.45 tok/s measured, vs a reported 9.74 tok/s on a Pixel 10 Pro XL, 5.2× |
| Image output | none — image input understanding only |
| opencode | `@ai-sdk/openai-compatible` against `http://127.0.0.1:8080/v1` |
| Verdict | correct and stable after the patch; too slow for interactive use on M1 Max, and the reason is not the model |
