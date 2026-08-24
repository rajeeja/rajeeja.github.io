---
title: "Running Meta Muse Glimmer 30B Locally on M1 Max: Setup, the Metal Crash, and the Fix"
date: 2026-08-17
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
excerpt: "Running Meta's open-weights agentic model on a 64 GB M1 Max — quantization choice, the Gated Delta Net Metal crash and the upstream patch that fixes it, measured throughput against a remote frontier model, and opencode wiring."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">Engineering note &middot; Local LLM &middot; August 2026</p>
  <h1 class="article-title">Running Meta Muse Glimmer 30B Locally on M1 Max</h1>
  <p class="article-dek">Quantization fit on 64 GB, the Gated Delta Net Metal crash and the upstream patch that fixes it, measured throughput, and opencode integration.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">local LLM</span>
  <span class="post-tag post-tag--teal">Apple Silicon</span>
  <span class="post-tag post-tag--amber">llama.cpp</span>
  <span class="post-tag post-tag--violet">opencode</span>
</div>

---

## Scope and provenance

Everything below was run on one machine on 17 August 2026. Numbers are what that machine produced; where a figure comes from Meta's model card or from hardware I do not have, it is labelled as such. Upstream PR states were re-checked on 24 August 2026.

---

## Read This First — Should You Attempt It?

The setup works. The result is not usable interactively on this hardware, and the reason is predictable in advance. Check your machine against this before spending an afternoon:

| Your machine | Expect | Advice |
|---|---|---|
| M1/M2 Pro or Max, 32–64 GB | ~5 tok/s | Works after patching, but too slow for interactive use. Read the crash section, then run a smaller model instead |
| M1/M2, 16 GB | will not fit | 20 GB resident against 16 GB of shared memory. Don't |
| M3/M4/M5 Max, 36 GB+ | 20–27 tok/s (Meta's figures) | Worth it. No Metal crash on these |
| Discrete GPU, 24 GB+ VRAM | 40+ tok/s by roofline | The straightforward answer if you own one |
| Anything with <24 GB usable memory | won't fit at Q4 | Pick a smaller model, not a smaller quant |

The honest summary for older Apple Silicon: **this model is a poor fit, and no flag will fix it.** The limit is memory bandwidth, and you cannot configure your way past it. What follows is still worth reading if you want the crash fix — it is the same GDN bug on any M1/M2 machine — or if you want the arithmetic for deciding what hardware would actually work.

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
    <span class="stat-card__value">400 GB/s</span>
    <span class="stat-card__label">Memory bandwidth &mdash; the binding constraint</span>
  </div>
</div>

| Property | Value |
|---|---|
| Chip | Apple M1 Max |
| CPU | 10 cores (8P + 2E) |
| GPU | Integrated, Metal |
| Unified memory | 64 GB |
| Memory bandwidth | ~400 GB/s |
| Storage free at test time | ~206 GB |
| OS | macOS 26.6.1 (build 25G76) |

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

## Quantization Choice on 64 GB

`meta-models/Muse-Glimmer-30B-GGUF` is ungated and ships two text builds plus two companions.

| File | Disk | Resident (weights + KV) | Quality vs full precision |
|---|---|---|---|
| `KQuant-17GB-Q4_K_M.gguf` | 16.8 GB | ~17 GB | −1.0% |
| **`KQuant-Dynamic-Q4_K_XL.gguf`** | **19.7 GB** | **~20 GB** | **−0.2%** |
| `mmproj-...Q4_K_M.gguf` (vision) | 1.4 GB | +1.4 GB | — |
| `dflash-...Q4_K_M.gguf` (drafter) | 1.6 GB | +1.6 GB | — |

Dynamic + vision + DFlash is ~23 GB resident: 36% of 64 GB, leaving ~41 GB. The degradation figures are Meta's, measured across 15 benchmarks. On a 64 GB machine there is no reason to take the 17 GB build.

---

## Setup

### 1. Install llama.cpp

```bash
brew install llama.cpp
llama-server --version
# version: 0.1.0-dev (build 10450, commit ece963f41)
```

`muse_glimmer` architecture support merged in [PR #26841](https://github.com/ggml-org/llama.cpp/pull/26841) on 10 August 2026, so the minimum build is b10353. Homebrew delivers b10450.

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
# 1. Shallow clone, deep enough to carry the recent Metal work
git clone --depth 200 https://github.com/ggml-org/llama.cpp ~/src/llamacpp-head

# 2. Apply PR #25788
curl -sL https://github.com/ggml-org/llama.cpp/pull/25788.diff -o /tmp/pr25788.diff
cd ~/src/llamacpp-head
git apply /tmp/pr25788.diff

# 3. Build — Metal is on by default on macOS
cmake -B build -DGGML_METAL=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF .
cmake --build build --config Release -j8 --target llama-server

# 4. Confirm
~/src/llamacpp-head/build/bin/llama-server --version
# version: 0.1.1-dev (build 1, commit 087f94d+)
```

Build time on M1 Max: about 90 seconds. After this, inference is stable across repeated requests.

---

## Launching the Server

This is the configuration that was actually used for the timings below — text only, all layers on the GPU:

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

Vision and speculative decoding are opt-in additions. Neither was active during the benchmark, so treat their cost and benefit on M1 Max as unmeasured:

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
| `--no-warmup` | flag | skips the startup inference; needed on M1 Max, since on an unpatched binary that warmup is itself a crash |
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

## Measured Throughput

Same prompt in both cases: an explanation of gradient descent covering intuition, the math, learning rate, momentum, and practical guidance.

**Local — Muse Glimmer 30B, patched build, Metal, Q4_K_XL, text only.** From the `timings` block in the API response:

| Metric | Value |
|---|---|
| Prompt ingestion | 48.4 tok/s |
| Token generation | 5.2 tok/s |
| Time to first token | ~0.58 s |
| Total generation | ~150 s for 781 tokens |

**Remote — Claude Sonnet 5 via Argo proxy on `localhost:44445`.** Wall-clock only; the proxy does not expose per-token timings, so this is an effective rate over the whole response and is not directly comparable to a `timings`-derived figure.

| Metric | Value |
|---|---|
| Output tokens | 1,200 |
| Wall time | 11.5 s |
| Effective output rate | ~104 tok/s |

| | Local Muse Glimmer 30B | Remote Claude Sonnet 5 |
|---|---|---|
| Generation | 5 tok/s | ~104 tok/s |
| Ratio | 1× | ~20× |
| TTFT | ~0.6 s | <0.5 s |
| Data location | on device | leaves the machine |
| Marginal cost | none | metered |
| Context | 8K as configured (131K model max) | 200K |
| Works offline | yes | no |

---

## 5 tok/s Is Not Interactive

At 5 tok/s a 500-word answer takes roughly two and a half minutes. A twenty-exchange coding session is thirty to sixty minutes of pure generation wait. That is not a tuning problem; it rules out interactive use on this hardware.

### The GPU was not the bottleneck

Worth being precise about what is slow, because the obvious reading is wrong. This ran with `-ngl 99` — every layer resident on the Metal GPU. The GPU was fully engaged and almost entirely idle.

Generating one token from a dense 30B model reads **every weight exactly once**. That is the whole 19.65 GB file, per token, again for the next token. The arithmetic attached to that traffic is small: roughly `2 × 29.6e9 ≈ 59 GFLOP` per token.

Put those against the machine:

| Quantity | Value |
|---|---|
| Weights read per token | 19.65 GB |
| Memory bandwidth | ~400 GB/s |
| Bandwidth ceiling | 400 / 19.65 ≈ **20 tok/s** |
| Measured | **5.2 tok/s** — 26% of ceiling |
| Compute demanded at 5.2 tok/s | ~0.3 TFLOP/s |
| GPU capability | ~10 TFLOP/s |
| GPU utilization | **~3%** |

The GPU spends the overwhelming majority of each token waiting for weights to arrive. It is starved, not slow. This is also why 64 GB of RAM bought nothing — 23 GB resident, 41 GB idle. Capacity was never the constraint; the rate at which memory can be streamed was.

### How the memory bus sets that ceiling

Bandwidth is a width-times-rate product. M1 Max drives a 512-bit LPDDR5 interface at 6400 MT/s: 64 bytes × 6.4 G/s ≈ 410 GB/s. M4 Max keeps the 512-bit width and raises the rate to 8533 MT/s, giving 546 GB/s. The generational gain is a faster bus, not a fundamentally different memory system.

Apple's unified memory removes the discrete-GPU copy — CPU and GPU address one pool, so weights never cross PCIe. The tradeoff is that DRAM speed becomes the hard ceiling. A discrete card pays a one-time PCIe transfer and then reads from dedicated VRAM at rates well above what LPDDR5 delivers; there is no equivalent fast local tier here to hide in.

One more reason servers do not see this: batching. Read a weight once, apply it across many concurrent sequences, and the read amortizes. At `-np 1` every token pays the full traversal.

### Why this machine is far off Meta's numbers

| Hardware | Baseline tok/s | With DFlash | Bandwidth | Roofline | % of roofline |
|---|---|---|---|---|---|
| M1 Max (measured here) | 5.2 | not measured | 400 GB/s | ~20 tok/s | **26%** |
| M4 Max (Meta) | 23.7 | 37.8 | ~546 GB/s | ~28 tok/s | **85%** |
| M5 Max (Meta) | 26.6 | 50.2 | ~600 GB/s | ~31 tok/s | **87%** |

This separates the two effects cleanly. M4/M5 Max carry 1.4–1.5× the bandwidth, which is real but nowhere near the observed ~5× gap. The larger factor is that ExecuTorch extracts roughly 85% of the available bandwidth while llama.cpp extracts about a quarter of it. ExecuTorch runs a pre-compiled graph with MLX-native Metal kernels; llama.cpp dispatches through a runtime-interpreted path. Most of the deficit is backend, not silicon.

Caveat on the comparison: Meta's figures come from the ExecuTorch PTE artifact, not this GGUF, so the per-token byte count may differ somewhat and the roofline percentages should be read as approximate. KV-cache traffic is also excluded, though at 8K context it is small next to 19.65 GB of weights.

### What it would take to be bearable

Define the target first. Around 10 tok/s a response arrives roughly as fast as you read it. Around 25 tok/s it stops feeling like waiting. Below 10 you are watching a progress bar.

Required bandwidth follows directly from `target × 19.65 GB ÷ efficiency`:

| Target | With a compiled backend (85%) | With llama.cpp today (26%) |
|---|---|---|
| 10 tok/s | ~230 GB/s | ~760 GB/s |
| 15 tok/s | ~350 GB/s | ~1130 GB/s |
| 25 tok/s | ~580 GB/s | ~1890 GB/s |

Read the right-hand column carefully: on llama.cpp's current efficiency, **no Apple Silicon laptop reaches 15 tok/s on a 30B model.** Not the M5 Max. The backend has to improve, or the hardware has to be something else.

That leaves four levers, cheapest first.

1. **Run a smaller model.** The strongest lever available today and the one most people skip. Bytes-per-token scale with model size, so an 8B at Q4 is roughly 5 GB and would run near 20 tok/s on this same M1 Max, unchanged. Trading 30B quality for 4× speed is usually the right call on constrained hardware. Note this is a *model* change, not a *quant* change — dropping to the 17 GB build saves 14% of the traffic and buys almost nothing.
2. **Wait for a compiled backend.** ExecuTorch reaches ~85% of roofline on M4/M5. The same efficiency here would be ~17 tok/s — genuinely usable, no hardware purchase. Extrapolated, not measured.
3. **Buy bandwidth.** M4 Max at 546 GB/s gets 23.7 tok/s measured by Meta; M5 Max 26.6. Both need the compiled backend to hit those numbers.
4. **Use a discrete GPU.** A 24 GB card in the RTX 3090/4090 class carries roughly 940–1010 GB/s of spec bandwidth — a 2.4× on M1 Max — and CUDA backends run close to roofline. That puts a 30B Q4 in the 40+ tok/s range. Derived from spec sheets, not tested here.

Where this machine was specifically inferior: not RAM (41 GB spare), not GPU compute (~3% used), not storage or CPU. One number — 400 GB/s — and one immature backend. Everything else was adequate.

### Where local still wins

- Code or data that must not leave the machine.
- Genuinely offline work — travel, air-gapped sites.
- Batch jobs. Fifty file summaries queued overnight do not care about 5 tok/s.
- Very high sustained volume, where marginal token cost dominates hardware cost.

For interactive sessions on M1 Max, a remote frontier model remains the right call.

### Paths to usable local speed

- **Short term.** [PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788) merges and reaches Homebrew. Stability, not speed — still ~5 tok/s, but no patched build to maintain, and `--no-warmup` becomes unnecessary.
- **Medium term.** ExecuTorch Metal. `meta-models/Muse-Glimmer-30B-ExecuTorch-PTE` is a pre-exported artifact with Metal and MLX kernels compiled from PyTorch via `torch.export`. If it hit the same ~85% of roofline here that it reaches on M4/M5 Max, M1 Max would land near 17 tok/s — a 3× gain with no hardware change. That is an extrapolation, not a measurement: no M1 Max ExecuTorch figure has been published, and this is the number I would most like to see someone produce.
- **Long term.** Newer hardware. 37.8–50 tok/s with DFlash on M4/M5 Max is interactive.

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

Running locally the schema is free in dollar terms, so the flag can stay on. It is not free in latency: at 5 tok/s, 10.6k tokens of added prompt costs a few extra seconds of ingestion per turn at the measured 48 tok/s.

---

## Summary

| | |
|---|---|
| Model | Meta Muse Glimmer 30B, Apache 2.0, August 2026 |
| Quant on 64 GB M1 Max | KQuant-Dynamic Q4_K_XL — 19.7 GB, −0.2% |
| Blocking bug | GDN Metal kernel crash, every inference, M1 Max |
| Fix | apply [PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788), rebuild (~90 s); still open upstream as of 24 Aug 2026 |
| Required flags | `--jinja`, `--no-warmup`, `-ngl 99` |
| Measured local | 5.2 tok/s generation, 48.4 tok/s ingestion, text only |
| Remote comparison | ~104 tok/s effective, Claude Sonnet 5 via Argo |
| Binding constraint | memory bandwidth, not RAM or GPU — 26% of a 20 tok/s roofline, GPU ~3% utilized |
| Image output | none — image input understanding only |
| opencode | `@ai-sdk/openai-compatible` against `http://127.0.0.1:8080/v1` |
| Verdict | correct and stable after the patch; too slow for interactive use on M1 Max |
