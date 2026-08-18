---
title: "Running Meta Muse Glimmer 30B Locally on M1 Max: Setup, Bug Hunt, and the Fix"
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
excerpt: "A complete guide to running Meta's newest open-weights agentic model locally on an M1 Max MacBook Pro — hardware fit analysis, the Apple Silicon Metal crash, applying an upstream patch to fix it, real timing benchmarks vs. Argo Claude Sonnet 5, and opencode + UXarray MCP integration."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">Engineering note &middot; Local LLM &middot; August 2026</p>
  <h1 class="article-title">Running Meta Muse Glimmer 30B Locally on M1 Max</h1>
  <p class="article-dek">Hardware fit, the Metal crash, applying the upstream fix, benchmarks against Argo Claude Sonnet&nbsp;5, and wiring it into opencode and the UXarray MCP server — everything documented as it actually happened.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">local LLM</span>
  <span class="post-tag post-tag--teal">Apple Silicon</span>
  <span class="post-tag post-tag--amber">llama.cpp</span>
  <span class="post-tag post-tag--violet">opencode</span>
</div>

---

## Machine Specifications

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">Apple M1 Max</span>
    <span class="stat-card__label">10-core CPU (8P+2E) &middot; Metal 4 GPU</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">64 GB</span>
    <span class="stat-card__label">Unified Memory &mdash; shared CPU/GPU pool</span>
  </div>
  <div class="stat-card stat-card--violet">
    <span class="stat-card__value">400 GB/s</span>
    <span class="stat-card__label">Memory bandwidth &mdash; the real LLM bottleneck</span>
  </div>
</div>

| Property | Value |
|---|---|
| **Chip** | Apple M1 Max |
| **CPU** | 10 cores (8P + 2E) |
| **GPU** | Apple Metal 4 (integrated) |
| **Unified Memory** | 64 GB |
| **Memory bandwidth** | ~400 GB/s |
| **Storage free** | ~206 GB |
| **OS** | macOS 26.6.1 (Tahoe, build 25G76) |

---

## What is Muse Glimmer?

Released **August 9, 2026** by Meta's Superintelligence Lab under **Apache 2.0** — fully open, commercial use allowed.

| Property | Value |
|---|---|
| **Parameters** | 29.6B (dense — not MoE) |
| **Architecture** | Dense Causal Transformer + 1.8B ViT-G/14 Perception Encoder |
| **Novel layers** | Gated Delta Net (GDN) + Lightning Indexer — hybrid SSM/attention |
| **Context window** | 131,072 tokens |
| **Modalities** | Text + Image **input** → Text **output** |
| **Image generation?** | ❌ No — vision understanding only |
| **Reasoning** | Built-in chain-of-thought (exposed in `reasoning_content` field) |
| **Speculative decoding** | DFlash block-diffusion drafter (16-token blocks), ships alongside |
| **Distilled from** | Muse Spark (Meta's larger flagship) |
| **Knowledge cutoff** | January 4, 2026 |
| **License** | Apache 2.0 ✅ |

### Why it matters for agentic work

Benchmarked against same-size peers:

| Benchmark | **Muse Glimmer 30B** | Gemma4-31B | Qwen3.6-27B |
|---|:---:|:---:|:---:|
| MCP Atlas | **75.5** | 54.2 | 62.5 |
| SWE-Bench Pro | **51.2** | 36.9 | 50.2 |
| AIME 2026 | **94.7** | 89.2 | 94.1 |
| DeepSearch QA | **74.6** | 61.7 | 71.1 |
| Charxiv Reasoning | **78.8** | 77.7 | 78.4 |

The MCP Atlas and SWE-Bench Pro leads are the interesting ones for opencode users.

---

## Hardware Fit Analysis — 64 GB M1 Max

The official GGUF repo (`meta-models/Muse-Glimmer-30B-GGUF`) ships two text builds plus two companion files:

| File | Disk | Weights + KV in RAM | Quality vs full precision |
|---|---|---|---|
| `KQuant-17GB-Q4_K_M.gguf` | 16.8 GB | ~17 GB | −1.0% |
| **`KQuant-Dynamic-Q4_K_XL.gguf`** | **19.7 GB** | **~20 GB** | **−0.2%** |
| `mmproj-...Q4_K_M.gguf` (vision) | 1.4 GB | +1.4 GB | — |
| `dflash-...Q4_K_M.gguf` (speculative) | 1.6 GB | +1.6 GB | — |

**All-in — Dynamic + vision + DFlash: ~23 GB.** Your 64 GB machine uses 36% of its RAM and has 41 GB free for everything else.

Meta validated the −0.2% degradation across 15 benchmarks. The Dynamic build is the right choice here — there is no reason to use the 17GB variant on a 64 GB machine.

---

## Step-by-Step Setup

### Step 1 — Install llama.cpp

```bash
brew install llama.cpp
llama-server --version
# version: 0.1.0-dev (build 10450, commit ece963f41)
```

The minimum required build is **b10353**, when `muse_glimmer` architecture support merged via [PR #26841](https://github.com/ggml-org/llama.cpp/pull/26841) on 10 Aug 2026. Homebrew delivers b10450. ✅

> **Stop here and read the Metal crash section before launching anything.** The Homebrew binary will crash on M1 Max without the patch described below.

### Step 2 — Download weights

The official GGUF repo is ungated — no HuggingFace account required.

```bash
pip install huggingface_hub hf_xet   # hf_xet activates the fast xet download protocol
mkdir -p ~/Models/Muse-Glimmer-30B-GGUF

python3 << 'EOF'
import hf_xet  # activates fast xet protocol
from huggingface_hub import hf_hub_download
import os

dest = os.path.expanduser("~/Models/Muse-Glimmer-30B-GGUF")
for fname in [
    "Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf",   # 19.7 GB
    "mmproj-Muse-Glimmer-30B-Q4_K_M.gguf",             #  1.4 GB
    "dflash-Muse-Glimmer-30B-Q4_K_M.gguf",             #  1.6 GB
]:
    print(f"Downloading {fname}...")
    hf_hub_download(repo_id="meta-models/Muse-Glimmer-30B-GGUF",
                    filename=fname, local_dir=dest)
print("Done.")
EOF
```

Real-world speed with hf_xet: **~150 MB/s** — the 19.7 GB model took about 2 minutes.

---

## The Apple Silicon Metal Crash — Root Cause and Fix

This is the most important section. **Every M1/M2 user will hit this.** Skip it and you will spend hours debugging.

### What happens

You start `llama-server`, the model loads, you fire a request — and the server process silently dies before returning a response. No crash report. No macOS Crash Reporter entry. The process just disappears.

```
0.17.667.784  I slot print_timing: eval time = 12501.11 ms / 50 tokens (3.92 t/s)
0.17.667.829  I slot release: id 0 | task 0 | stop processing: n_tokens = 106
# <process exits silently here>
```

It happens on **every single inference** — not intermittently.

### Root cause — the GDN Metal kernel

Muse Glimmer introduces two novel layer types not present in any previous model:

- **Gated Delta Net (GDN)** — a linear-attention recurrent state layer
- **Lightning Indexer** — a sparse retrieval layer

You can see them being registered at server startup:

```
I resolve_fused_ops: fused Gated Delta Net (autoregressive) enabled
I resolve_fused_ops: fused Gated Delta Net (chunked) enabled
I resolve_fused_ops: Lightning Indexer enabled
```

The Metal kernels for these layers were still being developed when the model shipped. The relevant open pull request is [**ggml-org/llama.cpp #25788**](https://github.com/ggml-org/llama.cpp/pull/25788): *"metal: gated_delta_net cache fusion"* — open as of August 2026.

The crash occurs because the GDN Metal kernel incorrectly handles the concurrency tracker during command buffer cleanup. Specifically, when a fused op writes its output directly to the KV cache, it elides an intermediate destination — but without the fix, the encode loop still adds that destination's memory range to the concurrency tracker, causing a spurious barrier and an abort on M1 Max's older Metal GPU architecture.

> The bug does not affect M3/M4/M5 Max. Meta's own macOS benchmarks were done on M4 Max and M5 Max — which is why the issue was not caught before release.

### Things that do NOT fix it

We systematically tested every obvious workaround. None solved the core problem:

| Workaround | Result |
|---|---|
| `-fa off` (disable Flash Attention) | Still crashes |
| `--no-op-offload` | Allowed one inference, then crash |
| `-ngl 0` (CPU only) | Still crashes (GDN is in the compute graph) |
| `-ngl 26` (partial GPU) | Still crashes |
| `METAL_DEBUG_ERROR_MODE=0` | Still crashes |
| `GGML_METAL_N_CB=1` | Still crashes |
| Removing `-md` (no DFlash drafter) | Still crashes |

### The actual fix — apply PR #25788 and rebuild

The PR adds three things: a `state_out_stride` field to the GDN kernel args struct, a `fuse_elide_dst` method that marks consumed nodes as elided so the concurrency tracker skips their memory ranges, and corrects the Metal shader to use this stride. Once applied, the crash is gone.

```bash
# 1. Clone with enough depth to have all the Metal fixes
git clone --depth 200 https://github.com/ggml-org/llama.cpp /tmp/llamacpp-head

# 2. Download and apply PR #25788
curl -sL https://github.com/ggml-org/llama.cpp/pull/25788.diff -o /tmp/pr25788.diff
cd /tmp/llamacpp-head
git apply /tmp/pr25788.diff

# 3. Build (Metal enabled by default on macOS)
cmake -B build -DGGML_METAL=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF .
cmake --build build --config Release -j8 --target llama-server

# 4. Confirm
/tmp/llamacpp-head/build/bin/llama-server --version
# version: 0.1.1-dev (build 1, commit 087f94d+)
```

Build time on M1 Max: **~90 seconds**.

### Launch the server

```bash
/tmp/llamacpp-head/build/bin/llama-server \
    -m       ~/Models/Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf \
    --mmproj ~/Models/Muse-Glimmer-30B-GGUF/mmproj-Muse-Glimmer-30B-Q4_K_M.gguf \
    -md      ~/Models/Muse-Glimmer-30B-GGUF/dflash-Muse-Glimmer-30B-Q4_K_M.gguf \
    -a muse-glimmer-30B \
    -ngl 99 -ngld 99 \
    -c 8192 -np 1 \
    --host 127.0.0.1 --port 8080 \
    --jinja --temp 1.0 --top-p 0.95 --top-k 64 \
    --no-warmup
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

---

## Key Launch Flags Explained

| Flag | Recommended value | What it does |
|---|---|---|
| `-m` | path to `.gguf` | Main text model |
| `--mmproj` | path | Perception encoder — needed for image input, +1.4 GB |
| `-md` | path | DFlash speculative drafter — +1.6 GB, boosts speed ~1.5× |
| `-ngl 99` | 99 | Offload all layers to Metal GPU |
| `-ngld 99` | 99 | Offload all draft model layers to Metal |
| `-c 8192` | 8192–32768 | Context window. Divided across `-np` slots |
| `-np 1` | 1 | Parallel request slots. Each slot gets `-c / -np` tokens |
| `--jinja` | (flag) | **Mandatory.** Activates the embedded chat template. Without it: immediate abort |
| `--no-warmup` | (flag) | **Required on M1 Max** with patched build — skip startup inference |
| `--temp 1.0` | 1.0 | Meta's recommended sampling temperature |
| `--top-p 0.95` | 0.95 | Meta's recommended nucleus sampling |
| `--top-k 64` | 64 | Meta's recommended top-k filter |

### Controlling reasoning depth

Muse Glimmer always reasons — you cannot disable it, only tune the depth:

```bash
# Server-wide: low/medium/high/xhigh (default: high)
--chat-template-kwargs '{"reasoning_strength":"low"}'

# Per-request: in the system prompt
{"role":"system","content":"Reasoning strength: low"}

# Hard token cap on thinking
--reasoning-budget 512
```

Reasoning tokens appear in `reasoning_content`. Your answer appears in `content`. If `content` is empty and `finish_reason` is `"length"`, you need more `max_tokens` — the reasoning consumed all of them.

### Stop tokens

Only stop on `<|end_of_text|>` (200001) and `<|eot|>` (200008). **Never stop on `<|eom|>`** — it marks end-of-message, not end-of-turn. Stopping on it collapses parallel tool calls.

### Context per slot

`-c` is divided across `-np` slots. With `-c 8192 -np 4`, each slot gets 2048 tokens — not enough for a reasoning model. Either use `-np 1`, or scale `-c`:

```bash
# Four slots, 8K each:
-c 32768 -np 4
```

---

## Timing Benchmarks: Local vs. Remote

Both tests used the same prompt: a detailed explanation of gradient descent — intuition, math, learning rate, momentum, and practical tips.

### Local — Muse Glimmer 30B on M1 Max (patched build, Metal GPU, Q4_K_XL)

From `timings` in the API response:

| Metric | Value |
|---|---|
| **Prompt ingestion** | **48.4 tok/s** |
| **Token generation** | **5.2 tok/s** |
| **Time-to-first-token** | ~0.58 s |
| **Total generation time** | ~150 s for 781 tokens |
| **Quantization degradation** | 0.2% vs. full precision |

### Remote — Argo Claude Sonnet 5 (via Argo proxy at localhost:44445)

Measured via wall time (Argo proxy does not expose per-token timings):

| Metric | Value |
|---|---|
| **Output tokens** | 1,200 |
| **Total wall time** | 11.5 s |
| **Effective output speed** | **~104 tok/s** |

### Side by side

| | Local Muse Glimmer 30B | Remote Claude Sonnet 5 |
|---|---|---|
| **Generation speed** | 5 tok/s | ~104 tok/s |
| **Speed ratio** | 1× | ~20× faster |
| **Latency (TTFT)** | ~0.6 s | <0.5 s |
| **Privacy** | ✅ 100% on-device | ☁️ data leaves machine |
| **Cost** | $0/token after hardware | Metered API |
| **Context** | 8K (server limit) | 200K |
| **Offline** | ✅ Yes | ❌ No |
| **Image input** | ✅ Yes (mmproj) | ✅ Yes |
| **Reasoning** | ✅ Built-in | ✅ Extended thinking |

The speed gap is real. Remote frontier models are ~20× faster at generation. Local wins on privacy, offline availability, zero marginal cost, and data sovereignty. For long agentic sessions processing sensitive code or scientific data, local is the right choice. For interactive chat, remote wins.

---

## opencode Integration

opencode uses the `@ai-sdk/openai-compatible` provider, which speaks directly to `llama-server`'s OpenAI-compatible API. Add this to `~/.config/opencode/opencode.json`:

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

Switch models in-session with `/model` → `Local llama.cpp (Muse Glimmer)` → `Muse Glimmer 30B (local, M1 Max)`, or set as the default:

```json
{ "model": "local-llamacpp/muse-glimmer-30B" }
```

**One important tuning:** always send `max_tokens` of 800 or more. The model reasons internally before answering, and if the token budget runs out during the reasoning phase, `content` will be empty. Add a low-reasoning system prompt for faster interactive sessions:

```json
{"role":"system","content":"Reasoning strength: low"}
```

---

## UXarray MCP Server Integration

The `uxarray-mcp-server` at `~/uxarray-mcp-server` is an MCP server that exposes **31 tools** for climate mesh analysis — `inspect_mesh`, `calculate_area`, `calculate_zonal_mean`, `run_analysis` (vorticity, divergence, gradient, remap), `analyze_dataset` (full pipeline in one call), `plot_dataset`, and more.

### Why it is disabled by default in opencode

```json
// ~/.config/opencode/opencode.json
"mcp": {
  "uxarray": {
    "enabled": false,   // <-- off by default
    "_comment": "31 tools = ~10.6k tokens of schema on EVERY request"
  }
}
```

31 tools adds ~10,600 tokens of schema to every request context. On a remote metered model, that is real money on every turn, even when you are not doing mesh work.

### Enabling for a local-model session

When using Muse Glimmer locally, there is no per-token cost, so enabling the full schema is essentially free:

```json
"mcp": {
  "uxarray": {
    "type": "local",
    "command": [
      "uv", "--directory", "/Users/mbook/uxarray-mcp-server",
      "run", "uxarray-mcp", "serve"
    ],
    "enabled": true    // change false -> true
  }
}
```

### What you can do with both enabled together

Muse Glimmer scores 75.5 on MCP Atlas — it is genuinely good at multi-step tool orchestration. Combined with uxarray-mcp, you can do things like:

```
"Analyze this MPAS mesh, compute vorticity from the u and v fields,
 plot a choropleth of the result, and tell me where the strongest
 cyclonic anomalies are."
```

The model will chain `get_capabilities` → `run_analysis(operation="curl")` → `plot_dataset` autonomously.

### The `--enabled` flag in plain English

`"enabled": false` means opencode does not start the MCP subprocess and does not include its tool schema in any request. The server binary still exists; it just does not run. `"enabled": true` starts the subprocess on opencode launch and injects all 31 tool schemas into every request context. There is no per-tool granularity — it is all-or-nothing at the server level, which is why the convention is to flip it only for sessions doing actual mesh analysis, then flip it back.

---

## Does Muse Glimmer Generate Images?

**No.** The model card is explicit:

> *"Supported modalities: Input: text + image, Output: text"*

It can *understand* images passed to it via the `--mmproj` vision encoder — interpreting screenshots, charts, and scientific figures — but it cannot produce images. For image generation you need a separate diffusion model.

---

## When Will This Be Properly Fixed Upstream?

Watch [llama.cpp PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788). Once it merges and appears in a Homebrew release:

```bash
brew upgrade llama.cpp
```

You can then use the Homebrew binary directly without maintaining a patched local build. Drop `--no-warmup` as well — that flag was only needed to prevent the warmup inference from crashing on the unpatched binary.

For those who want even better performance once the kernel bugs are resolved: Meta also ships `meta-models/Muse-Glimmer-30B-ExecuTorch-PTE`, a pre-exported ExecuTorch artifact with Metal-native and MLX kernels compiled directly from PyTorch via `torch.export`. This is what Meta's own M4/M5 Max benchmarks used (23.7 tok/s baseline → 37.8 tok/s with DFlash). Once the ExecuTorch build toolchain is more accessible, this path will replace llama.cpp for Apple Silicon.

---


---

## Honest Assessment: 5 tok/s Is Unbearable

Let's not sugarcoat it. **At 5 tokens per second, Muse Glimmer is not usable for interactive work on M1 Max today.**

To put that in perspective: a 500-word response takes roughly **2–3 minutes** to arrive. A typical opencode coding session — where you iterate back and forth, ask follow-ups, review diffs — involves maybe 20 exchanges. At 5 tok/s average, you are waiting **30–60 minutes of raw generation time** per session. Every. Single. Interaction. Is. Painful.

For comparison:
- **Claude Sonnet 5 via Argo:** 104 tok/s → 500 words in ~12 seconds
- **Muse Glimmer local:** 5 tok/s → 500 words in ~2.5 minutes
- **Speed ratio:** ~20× slower

This is not a minor inconvenience. It is the difference between a tool that augments your thinking and a tool that breaks your flow entirely.

### Why is M1 Max so much slower than Meta's numbers?

Meta benchmarked on **M4 Max (23.7 tok/s baseline) and M5 Max (26.6 tok/s)**. These are not small differences:

| Hardware | Baseline tok/s | With DFlash | Memory bandwidth |
|---|---|---|---|
| M1 Max (this machine) | ~5 | — (crashes without patch) | 400 GB/s |
| M4 Max (Meta benchmark) | 23.7 | 37.8 | ~546 GB/s |
| M5 Max (Meta benchmark) | 26.6 | 50.2 | ~600 GB/s |

Two factors compound here. First, M4/M5 Max have significantly higher memory bandwidth — LLM inference on Apple Silicon is purely bandwidth-limited, so the newer chips are proportionally faster. Second, Meta's benchmarks used the **ExecuTorch Metal backend**, not llama.cpp. ExecuTorch exports a pre-compiled, backend-optimized compute graph with MLX-native kernels, while llama.cpp interprets the model in real time with more overhead.

### When does local actually make sense?

Despite the speed penalty, there are legitimate use cases for running locally on M1 Max *today*:

- **Privacy-sensitive code** — You are not comfortable sending proprietary code to any external API
- **Truly offline work** — No internet connection (travel, air-gapped environments)  
- **Long batch jobs** — If you queue a set of 50 file summaries overnight, 5 tok/s is fine; you are not watching
- **Cost at extreme scale** — If you are doing millions of tokens/day, local wins economically

For interactive opencode sessions, though? Use Argo Claude Sonnet 5 until either (a) the ExecuTorch path is accessible on M1 Max, or (b) you upgrade hardware.

### The path to actually usable local speed

**Short term (months):** Track [llama.cpp PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788). Once the GDN Metal kernel fix merges and `brew upgrade llama.cpp` brings it in, the server stabilizes. Still ~5 tok/s, but at least no crash workarounds.

**Medium term (6–12 months):** The ExecuTorch Metal path. Once `muse-glimmer-mlx` cmake preset is properly documented and the build is reliable, M1 Max users should see 15–20 tok/s — a 3–4× improvement from the llama.cpp path, because ExecuTorch uses properly compiled Metal kernels rather than the interpreted path.

**Long term:** M4/M5 Max hardware. 37.8–50 tok/s with DFlash is genuinely interactive. It is not Claude Sonnet 5 speed, but it is usable.

---

## UXarray MCP: Not Required Here

To be direct about the UXarray MCP integration mentioned earlier: **you do not need it to run Muse Glimmer**. The two are independent.

The UXarray MCP server (`~/uxarray-mcp-server`) is a specialized tool for climate mesh analysis — inspecting MPAS/UGRID/SCRIP grids, computing vorticity, divergence, zonal means, remapping, and so on. It is relevant only if you are doing that kind of scientific computing work.

What the two have in common is that **local Muse Glimmer makes the UXarray MCP cheaper to use**. The server exposes 31 tools, which inject ~10,600 tokens of schema into every request. On a remote metered API, that is real money on every turn. Running locally, the token cost is zero — so you can enable the full schema without thinking about it.

But if you are just setting up Muse Glimmer as a local coding assistant, skip the UXarray MCP entirely.

---

## How to Promote This Post

The article connects to several active communities and upstream projects. Here is how to amplify it effectively.

### Link back to llama.cpp PR #25788

The crash fix is a concrete, reproducible contribution to the upstream project. Leave a comment on [PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788) pointing to this post as real-world evidence from an M1 Max machine — the PR author (@angt) and the llama.cpp maintainers (@ggerganov) can confirm M1 Max behavior from this writeup.

**Draft comment for PR #25788** (keep short per public-comment rules):

> Confirmed: this patch resolves the Metal crash on M1 Max (macOS 26.6.1, build 10450+). After applying and rebuilding, llama-server survives multiple inferences. Full writeup with M1 Max timing vs. remote Claude Sonnet 5: [rajeeja.github.io/blog/muse-glimmer-30b-local-setup](https://rajeeja.github.io/blog/muse-glimmer-30b-local-setup/)

### Reply to the Meta / PyTorch announcement

The PyTorch Foundation published the official announcement on August 10, 2026:
[**pytorch.org/blog/fast-ondevice-agentic-ai-with-executorch/**](https://pytorch.org/blog/fast-ondevice-agentic-ai-with-executorch/)

And the Meta AI blog has coverage at:
[**ai.meta.com/blog/**](https://ai.meta.com/blog/)

### Draft LinkedIn post

```
Just published: a full technical writeup on running Meta's Muse Glimmer 30B
locally on M1 Max — including the Metal crash that hits every M1/M2 user,
the upstream llama.cpp patch that fixes it, real timing benchmarks vs.
Claude Sonnet 5, and honest thoughts on whether 5 tok/s is actually usable
(spoiler: it is not, for interactive work).

→ https://rajeeja.github.io/blog/muse-glimmer-30b-local-setup/

Key findings:
• Applying PR #25788 from @ggml-org/llama.cpp fixes the GDN Metal kernel crash
• Local speed: ~5 tok/s (M1 Max) vs. ~104 tok/s remote — a 20× gap
• ExecuTorch Metal path (M4/M5 Max target) is the right long-term answer
• opencode integration works cleanly via @ai-sdk/openai-compatible

#LocalLLM #AppleSilicon #OpenSource #MetaAI #llama #AIEngineering
```

### Draft X/Twitter post

```
Ran Meta Muse Glimmer 30B locally on M1 Max:

✅ Works — after applying llama.cpp PR #25788 (Metal GDN kernel patch)  
❌ Slow — 5 tok/s vs ~104 tok/s for remote Claude Sonnet 5  
❌ Not interactive — 2-3 min per response is unbearable in a coding session

Full writeup with the patch, benchmarks, and opencode setup:
→ rajeeja.github.io/blog/muse-glimmer-30b-local-setup/

cc @aiatmeta @pytorch
```

### Suggested X reply to Meta AI announcement

Find the Meta AI / PyTorch X post announcing Muse Glimmer and reply:

```
Tested on M1 Max — hits a Metal GDN kernel crash on every inference 
(llama.cpp b10450). Fix: apply PR #25788 + rebuild. After patch: stable 
but 5 tok/s — too slow for interactive use. M4 Max is the real target. 
Full breakdown: rajeeja.github.io/blog/muse-glimmer-30b-local-setup/
```

## Summary

| | |
|---|---|
| **Model** | Meta Muse Glimmer 30B (Apache 2.0, Aug 2026) |
| **Best quant on 64 GB M1 Max** | KQuant-Dynamic Q4_K_XL — 19.7 GB, 0.2% degradation |
| **Critical bug** | Metal GDN kernel crash on M1 Max after every inference |
| **Fix** | Apply [PR #25788](https://github.com/ggml-org/llama.cpp/pull/25788) and rebuild (~90s) |
| **Critical flags** | `--jinja` (mandatory), `--no-warmup` (M1 Max), `-ngl 99` |
| **Local speed** | 5 tok/s generation, 48 tok/s prompt ingestion |
| **Remote Sonnet 5** | ~104 tok/s — ~20× faster |
| **Image generation** | ❌ No — image input understanding only |
| **opencode** | `@ai-sdk/openai-compatible` on `http://127.0.0.1:8080/v1` |
| **UXarray MCP** | Enable locally (free tokens), keep disabled on remote (10.6k schema cost/request) |
| **Restart server** | `~/Models/Muse-Glimmer-30B-GGUF/start-server.sh` |
