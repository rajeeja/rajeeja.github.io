---
title: "I decided to write a basics book while setting up Meta Muse Glimmer 30B locally on my M1 Max"
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
  - benchmarking
excerpt: "A book-length introduction to running large language models on your own laptop, built around one machine and four models. Starts from what a model file even is, ends at a measured explanation of why a 30-billion-parameter model produces about six words per second on a 64 GB M1 Max — and why no setting you change will fix that."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">A basics book &middot; Local LLM &middot; One laptop, four models</p>
  <h1 class="article-title">I decided to write a basics book while setting up Meta Muse Glimmer 30B locally on my M1 Max</h1>
  <p class="article-dek">Everything you need to understand before downloading a 20 GB model file — what the numbers in its name mean, what your laptop can and cannot do with it, and then the measurements that show exactly where the speed goes.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">local LLM</span>
  <span class="post-tag post-tag--teal">Apple Silicon</span>
  <span class="post-tag post-tag--amber">llama.cpp</span>
  <span class="post-tag post-tag--violet">opencode</span>
</div>

---

I wanted to run a large model on my own laptop. Not through anyone's API, not in a browser tab — the actual weights, on my own disk, generating text with the network turned off.

It works. It is also much slower than the marketing around local AI would lead you to expect, and the reason it is slow turns out to be interesting, measurable, and almost entirely unrelated to the things people usually blame. It is not the model. It is not the software being badly written. It is a single number about the machine, and once you know that number you can predict the speed of any model on any laptop to within a few percent.

Getting to that point required understanding maybe fifteen concepts I did not have solid intuitions for. So this is both things at once: the setup log, and the book I wish I had read first.

**Who this is for.** You write code. You may have shipped things with AI assistants. You do not have a machine learning background, and you may not have thought hard about memory buses since school, or ever. That is exactly the right starting point. Nothing here assumes linear algebra, and every term is defined at the moment it first appears.

**What you'll be able to do at the end.** Look at any model on Hugging Face, read its name and its card, and say with confidence: this will run on my machine at roughly N tokens per second, or it will not run at all — and here is the specific reason.

---

## Contents

<nav markdown="1">

**Part I — What you are dealing with**

1. [Open weights, closed weights](#ch1) — What you can actually download and own, what the licence lets you do with it, and why "open source" is usually the wrong phrase for a model.
2. [Tokens, and tokens per second](#ch2) — The only two units in this book. What a token is, how fast is fast enough, and why a speed quoted without saying *which* speed is meaningless.
3. [Why run one locally at all](#ch3) — The honest case for and against, including the part where a remote model is twenty times faster and better.

**Part II — What a model is**

4. [A pile of matrices](#ch4) — What is actually inside the file. Layers, attention, the feed-forward block, and what "running" a model means mechanically.
5. [How one gets made](#ch5) — Pretraining, post-training, distillation. Enough to make clear that you are doing none of it.
6. [Reading a model card](#ch6) — Parameters, layers, hidden size, vocabulary, context window, dense versus mixture-of-experts. What each number costs you.
7. [Quantization](#ch7) — Squeezing 16 bits into 4.5. Why this is a *speed* trick that happens to save space, and not the other way round.
8. [GGUF, the file format](#ch8) — Header, tensor table, tensor data. The tensor table is why the byte accounting later in this book is exact rather than guessed.

**Part III — The four models**

9. [The four models in this book](#ch9) — Muse Glimmer 30B, Qwen3-32B, Gemma 4 31B, Gemma 3n E4B: who made each, what it is good at, how it is built, and what its makers do not tell you. Includes short explainers on grouped-query attention, sliding-window attention, linear attention, and MatFormer.

**Part IV — The machine**

10. [What a laptop is made of](#ch10) — CPU, GPU, memory, and the bus between them. Where "GB per second" comes from. Unified memory versus a graphics card.
11. [The two speeds](#ch11) — Reading your prompt is a completely different kind of work from writing the answer. One is limited by arithmetic, the other by memory. This distinction explains everything that follows.
12. [This machine](#ch12) — The M1 Max in detail, and the measured — not datasheet — bandwidth number that the rest of the book divides by.
13. [Will it run on yours?](#ch13) — A table: memory floor and bandwidth needed per model, per machine class. Plus a plain list of what will not work and why no flag rescues it.

**Part V — Doing it**

14. [Setup](#ch14) — Install the runtime, pick a quantization, download 20 GB, verify it loads.
15. [Reading a llama.cpp startup log](#ch15) — The log tells you a great deal, and two of its most alarming-looking lines mean the opposite of what they appear to say.
16. [Launching the server](#ch16) — The flags that matter, context budgeting, and how to wire it to an editor.

**Part VI — Measuring**

17. [How performance was measured](#ch17) — Four experiments, the exact commands, and why the benchmark deliberately uses fake text.
18. [Bytes per token](#ch18) — Why the file size is the wrong number, and how to get the right one out of the file itself.
19. [The denominator](#ch19) — Why not to use the number on the spec sheet, and how to measure the real one in twenty lines of Python.

**Part VII — What came out**

20. [Results](#ch20) — Three 30-billion-parameter models with different architectures land within 3.5 percentage points of each other. Why that is the whole story.
21. [Gemma 3n: what small buys and costs](#ch21) — Eight times the speed. What you give up for it.
22. [Small and specific is probably the direction](#ch22) — Opinion, clearly labelled as such.
23. [Hardware guidance](#ch23) — What it would actually take to make this pleasant, and the four levers available to you.
24. [Using it day to day](#ch24) — Editor integration, and the surprising cost of giving a model tools.

**Appendix**

- [A — Reproducing this](#appendix-a) — Every script, and the one command that regenerates every number in Part VII.

</nav>

---

# Part I — What you are dealing with

## Chapter 1 — Open weights, closed weights {#ch1}

*This chapter establishes what you can and cannot download, and what you are permitted to do with it.*

A language model, as a thing on a disk, is a large file full of numbers. Those numbers are called **weights**. They are the entire model — there is no additional secret sauce held back on a server. If you have the weights and a program that knows how to feed numbers through them, you have the model, permanently, offline, yours.

The industry splits roughly three ways.

**Closed.** You cannot have the weights. Claude, GPT, Gemini. You send text to a server, you get text back, you pay per token. The company can change the model under you, rate-limit you, or read your inputs subject to whatever their policy says. In exchange you get the strongest models that exist and you need no hardware.

**Open weights.** You can download the file. Llama, Qwen, Gemma, Mistral, DeepSeek, and the model this book is built around. This is the category that makes local inference possible at all.

**Open source, in the strict sense.** Almost nobody. Genuine open source would mean the training data, the training code, the data-cleaning pipeline, and a licence with no use restrictions — enough that you could rebuild the model from scratch. Models like OLMo do this. The big ones do not.

That middle category is where nearly all the interesting local models live, and it is why "open source model" is a phrase to be a little careful with. You are getting the compiled binary, not the source.

### Licences, in the twenty seconds they deserve

Three of the four models in this book are **Apache 2.0**. That is a genuine, boring, permissive open source licence. Use it commercially, modify it, ship it inside a product, do not ask anyone. The only real obligation is attribution.

The fourth, Gemma 3n, is under the **Gemma Terms of Use**. That is a custom licence, not an OSI-approved one. It is generous — commercial use is fine — but Google retains a use policy you must pass through to anyone you redistribute to, and they reserve the right to restrict uses they consider harmful. For a personal setup this is irrelevant. For a product it is a lawyer conversation.

Worth internalising: **licences are attached to weights, not to capabilities**. A model being downloadable tells you nothing about whether you are allowed to use its outputs to train another model, which is the restriction that most often bites.

<div class="callout callout--amber" markdown="1">
**A note on how I treat capability claims in this book.** When I say a model is good at something, I am reporting what its own model card claims, and I say so. I did not run capability benchmarks. Everything in Part VI and Part VII, by contrast, is measured on this machine and reproducible from the linked repository. Keep the two categories separate as you read — I try hard to.
</div>

---

## Chapter 2 — Tokens, and tokens per second {#ch2}

*This chapter establishes the only two units used in the rest of the book.*

### What a token is

Models do not read characters and they do not read words. They read **tokens**, which are chunks of text somewhere in between — usually a common word, a word fragment, or a piece of punctuation.

"The quick brown fox" is four tokens, one per word. "unbelievability" is probably four tokens too — something like `un`, `bel`, `iev`, `ability` — because it is a rare word and the tokenizer never learned it whole. Code tokenizes badly: indentation, braces, and identifiers like `getUserById` shatter into pieces.

A workable rule of thumb for English prose: **one token is about four characters, or about 0.75 words.** A thousand words is roughly 1,300 tokens. A dense page of code is more.

The model has a fixed **vocabulary** — a numbered list of every token it knows. Muse Glimmer's has 202,048 entries. Every piece of text you send is converted to a list of numbers indexing into that table, and every piece of text it generates comes back as such a list. Text never enters the model as text.

Why this matters practically: your bill, your context limit, and your speed are all denominated in tokens, and tokens are not words. When a model says "128K context", that is 128,000 tokens, which is roughly 96,000 words, which is roughly a 380-page book.

### Tokens per second

Generation is sequential. The model produces token 1, then reads its own token 1 in order to produce token 2, and so on. It cannot produce token 5 before token 4 exists. This is the single most important structural fact about how these things run, and Chapter 11 is entirely about its consequences.

So speed is **tokens per second (tok/s)**, and here is the scale:

| tok/s | What it feels like |
|---|---|
| 3–5 | Painful. You watch each word appear. Fine for a batch job you walk away from. |
| 6–10 | Slightly slower than reading aloud. Usable for chat, frustrating for long answers. |
| 15–20 | Comfortable reading speed. This is the threshold where it stops being annoying. |
| 40+ | Faster than you read. Feels instant. |
| 100+ | What a hosted frontier model gives you. |

Human reading speed is roughly 250 words per minute, which is about **5.5 tokens per second**. That is a useful anchor: a model running at 6 tok/s is producing text at almost exactly the rate you can read it, and it still feels slow, because you also want time to think.

### The trap: one number, two meanings

Here is where quoted benchmarks mislead, and it is worth being irritated about.

Running a model has two phases, and they run at wildly different speeds:

- **Prefill** (also called prompt processing) — the model reads your prompt. It can process all of your prompt's tokens *simultaneously*, because they all already exist. Fast.
- **Decode** (also called generation) — the model writes the answer, one token at a time, each depending on the last. Slow.

On the machine in this book, the same model does prefill at **87 tokens per second** and decode at **6.55 tokens per second**. Thirteen times apart. Both are honestly "tokens per second for Muse Glimmer on an M1 Max."

So when someone posts "I'm getting 90 tok/s on my laptop!", the first question is always: *which phase?* Nine times out of ten it is prefill, which is the number that does not determine how long you wait.

**In this book, an unqualified tok/s figure always means decode**, because decode is what you experience. Prefill numbers are labelled as prefill every time.

---

## Chapter 3 — Why run one locally at all {#ch3}

*This chapter establishes the honest case in both directions, so you can decide before spending an afternoon on it.*

### The case for

**Privacy that is structural, not promised.** Nothing leaves the machine. Not a policy commitment — a network-level fact. For source code under NDA, medical notes, unpublished research, legal documents, this is not a preference; it is the only option that clears review.

**It works with no network.** Planes, trains, bad conference wifi, air-gapped environments.

**Fixed cost.** You already own the laptop. Marginal cost per token is electricity. If you are running something in a loop over ten thousand documents, this can matter enormously.

**Nothing changes underneath you.** The weights on your disk in August behave identically in December. Hosted models get silently updated, deprecated, and retired. If you have built an evaluation suite against specific behaviour, that stability is worth real money.

**You can look inside.** Attention patterns, logits, per-layer activations. Impossible through an API.

### The case against

I will be blunt, because a lot of writing about local models is not.

**It is much slower.** Claude Sonnet 5 delivers about 104 tok/s wall clock to my terminal. Muse Glimmer on this laptop delivers 6.55. That is a factor of **twenty**. An answer that streams in five seconds from a hosted model takes a minute and a half locally.

**It is meaningfully less capable.** A 30-billion-parameter model quantized to about 4.5 bits is not a frontier model. It is good. It is not the same thing, and any post telling you a 30B local model "matches GPT-4" is comparing on a benchmark that has leaked into training data.

**It costs 20 GB of disk and most of your RAM.** While the model is loaded, roughly 23 GB of my 64 GB is gone. On a 16 GB machine, a model this size is simply not an option — Chapter 13 covers what is.

**The setup is not one command.** It is closer to an afternoon, and this book is largely a record of that afternoon.

### The honest summary

Local inference is worth it when **privacy, offline operation, or cost-at-volume** genuinely matter to you. It is not, today, worth it for raw capability or speed. Anyone selling you otherwise has something to sell.

What surprised me is how much I learned by doing it anyway. The performance analysis in Part VII taught me more about how these systems actually work than a year of using hosted APIs did — because on a laptop, the physical limits are close enough to touch.

---

# Part II — What a model is

## Chapter 4 — A pile of matrices {#ch4}

*This chapter establishes what is physically inside the file and what "running" it means.*

Forget neurons and brains. Here is the mechanical truth.

A transformer language model is a **stack of identical-looking layers**. Each layer is a handful of large rectangular grids of numbers — **matrices** — plus a few small ones. Running the model means: turn your token into a list of numbers, push that list through layer 1, take the output, push it through layer 2, and so on to the end. At the end you get a score for every token in the vocabulary. Pick a high-scoring one. That is the next token. Repeat.

That is genuinely it. Everything else is detail about the shape of the grids.

### The vector that flows through

The list of numbers being pushed through is called the **hidden state** or **residual stream**. Its length is a fixed property of the model called **d_model**, or hidden size, or embedding length — three names for one number. For Muse Glimmer it is 6,656.

So: one token in, one vector of 6,656 numbers created, that vector transformed 52 times (once per layer), and at the end converted into 202,048 scores.

### What a matrix multiply is, if you need it

If a matrix is new to you: it is a grid of numbers. Multiplying a vector by a matrix means producing a new vector where each output entry is the sum of (every input entry × its corresponding weight in one column of the grid).

The important consequence, and honestly the only one this book needs: **to multiply a vector by a matrix, you must read every single number in the matrix.** All of them. There is no shortcut, no partial read, no caching your way out of it. A matrix with 44 million entries requires reading 44 million numbers to use it once.

Hold onto that. It is the whole book.

### Inside one layer

Each layer does two things in sequence.

**1. Attention** — the mechanism that lets a token look at earlier tokens. Mechanically it builds three vectors from the hidden state, called **query**, **key**, and **value** (Q, K, V), via three matrices. The query of the current token is compared against the keys of all earlier tokens to produce weights; those weights are used to average the values. The result goes through a fourth matrix, the **output projection**.

The intuition: "which earlier words are relevant to what I'm doing right now, and what should I pull from them?" In "the cat sat on the mat because *it* was warm", attention is how *it* gets connected to *mat*.

**2. The feed-forward network (FFN or MLP)** — two or three much bigger matrices that expand the vector to several times its width, apply a nonlinear function, and squeeze it back. Muse Glimmer expands 6,656 → 19,968 → 6,656. No token talks to any other token here; this is pure per-token processing.

The FFN is where **most of the weights live** — typically two-thirds of the model. When you read later that decode is bandwidth-bound, the FFN is the main thing being read.

Sprinkled between these are **normalization layers** (tiny, cheap, they keep numbers from exploding) and **residual connections** (the layer's output is added to its input rather than replacing it, which is what lets you stack 52 of them without the signal degrading).

### The two ends

**Embedding** (`token_embd`) — a lookup table with one row per vocabulary entry. Token 4,127 means "read row 4,127". This is a *gather*, not a multiply: you read one row, not the whole table. This distinction becomes financially important in Chapter 18.

**Output head** (`output`) — converts the final 6,656-vector into 202,048 scores. This *is* a full multiply, and it is one of the largest single matrices in the model.

Some models **tie** these two — literally reuse the same matrix for both, transposed — which saves a lot of file size. Gemma 4 and Gemma 3n do. Muse Glimmer and Qwen3 do not. Again: Chapter 18.

### The KV cache

One optimisation you need to know because it eats your RAM.

When generating token 500, attention needs the keys and values of tokens 1–499. Recomputing them every step would be quadratic and absurd. So they are computed once and kept. That store is the **KV cache**.

It grows linearly with conversation length and is, unlike the weights, *unbounded* — a long conversation can consume gigabytes. It is the reason a local model that was fine at the start of a session gets slower and eventually falls over. Chapter 16 covers budgeting it.

---

## Chapter 5 — How one gets made {#ch5}

*This chapter establishes what training is, mainly so it is clear you are not doing any of it.*

You are doing **inference** — using a finished model. Training is a separate universe with a separate cost structure, and understanding the boundary keeps you from misreading model cards.

### Pretraining

Take an enormous pile of text — Qwen3 used roughly **36 trillion tokens**, Gemma 3n roughly 11 trillion — and repeatedly ask the model to predict the next token, adjusting the weights slightly each time it is wrong.

That is the whole objective. Everything the model appears to know — grammar, facts, code idioms, the shape of an argument — falls out of doing next-token prediction at that scale.

Cost: thousands of GPUs for weeks or months. Tens of millions of dollars for a model this size. This is what "foundation model" means and why only about a dozen organisations produce them.

Note what pretraining produces: something that continues text. Ask it a question and it might reply with more questions, because that is a plausible continuation. It is not yet an assistant.

### Post-training

Turning a text-continuer into something useful.

**Supervised fine-tuning (SFT)** — train further on curated examples of instruction and good response. This is where "act like a helpful assistant" is installed.

**Reinforcement learning from feedback (RLHF / RLAIF)** — generate multiple answers, have humans or another model rank them, push the weights toward the winners. This shapes tone, refusal behaviour, and formatting.

**Reasoning training** — more recent. Reward the model for producing correct answers *after* generating a chain of intermediate steps. This is what produces models that "think" before answering. Muse Glimmer has this always on, which is relevant to speed: reasoning tokens are tokens, and you pay for them at the same tokens-per-second.

Post-training is orders of magnitude cheaper than pretraining and is where most of the differentiation between similarly-sized models now comes from.

### Distillation

Train a small model to imitate a big one — not on human text, but on the big model's own output distributions. The small model learns not just the answer but the shape of the big model's uncertainty, which turns out to transfer a surprising amount of capability.

This is directly relevant here: **Muse Glimmer 30B is distilled from Muse Spark**, Meta's closed flagship. That is why a 30B model punches above what 30B used to mean. It is also why "parameter count" has become a much weaker predictor of quality than it was two years ago.

### What this means for you

Nothing you do at inference time changes the weights. Not the system prompt, not the temperature, not the context you paste in. The model is frozen. All you control is what goes in and how the output is sampled.

Fine-tuning — cheaply adapting a model on your own data with a technique like LoRA — is real and doable on a laptop for small models. It is out of scope here. This book is about inference.

---

## Chapter 6 — Reading a model card {#ch6}

*This chapter establishes what each number on a model's page implies for the machine that has to run it.*

A Hugging Face model card is dense with numbers. Here is what each one costs you.

### Parameter count

The headline number. "30B" means roughly 30 billion individual weights.

Its direct consequence is **file size**, via the bits-per-weight of the quantization (Chapter 7). At about 4.5 bits per weight, 30 billion parameters is about 17 GB. At 16 bits — the format the model was trained in — it would be 60 GB.

Its indirect consequence is **speed**, and this is the one people miss: because decode must read every weight for every token (Chapter 4), parameter count is very nearly a direct divisor on tokens per second. Doubling the model halves your speed. Not approximately — nearly exactly, on a bandwidth-limited machine.

Beware the label. Muse Glimmer's file says `size_label: 28B`, its card says 30B, and it actually has 29.6 billion text parameters plus a 1.8 billion parameter vision encoder. These are marketing-rounded. Use the file size.

### Layers, hidden size, heads

| Term | Also called | What it is | Muse Glimmer |
|---|---|---|---|
| Layers | blocks, `n_layer` | How many times the stack repeats | 52 |
| Hidden size | `d_model`, embedding length | Width of the vector flowing through | 6,656 |
| FFN size | intermediate size | Width the FFN expands to | 19,968 |
| Attention heads | `n_head` | Parallel attention computations per layer | 32 |
| KV heads | `n_head_kv` | How many of those share key/value data | 2 |

Roughly, parameters ≈ layers × (attention matrices + FFN matrices), and the FFN dominates. Deep-and-narrow versus shallow-and-wide is a real design choice with real performance consequences — Chapter 20 measures it.

That **32 heads / 2 KV heads** line is worth flagging now. It means grouped-query attention, explained in Chapter 9, and it is the single biggest factor in how much RAM your conversation consumes.

### Context window

The maximum number of tokens the model can attend to at once: prompt plus generated output plus everything earlier in the conversation.

Muse Glimmer: 131,072. Gemma 4: 262,144. Qwen3-32B: 40,960 natively.

**The catch that catches everyone**: the advertised context is what the model *architecturally supports*, not what you can afford. Filling 131K tokens of context requires enough RAM for a 131K-token KV cache, which for many models is more memory than the weights themselves. You will typically run at a fraction of the maximum. Chapter 16 does the arithmetic.

### Dense versus mixture-of-experts

**Dense** — every weight is used for every token. All four models here are dense.

**Mixture of experts (MoE)** — the FFN is split into many "experts" and a router picks a few per token. A model might have 100B total parameters but only activate 10B for any given token.

For local inference the distinction is sharp and important:

- **RAM** is set by *total* parameters. You must hold all the experts, since any token might need any of them.
- **Speed** is set by *active* parameters, because only those get read per token.

So MoE is the good trade if you have lots of RAM and limited bandwidth — which is precisely the situation on a big unified-memory Mac. A 100B MoE with 10B active can be *faster* than a 30B dense model while being far more capable. This is not hypothetical; it is why MoE has taken over the open-weights space.

### Modality

Text-only, or does it also take images or audio? Multimodal models ship extra encoder weights — Muse Glimmer's vision encoder is a separate 1.4 GB file. You can skip loading it if you only want text, and save the RAM.

### The things not on the card

Usually absent, and their absence is informative: training data composition, exact token count, energy cost, and evaluation results on anything the model does badly. Model cards are marketing documents with a technical vocabulary.

---

## Chapter 7 — Quantization {#ch7}

*This chapter establishes why the model file is a third of the size it "should" be, and why that is mainly a speed decision.*

Models are trained with 16 bits per weight. A 30B model in its native format is 60 GB. **Quantization** stores each weight in fewer bits — commonly 4 to 5 — bringing that to 17–20 GB.

### Why it works at all

Neural network weights are extraordinarily redundant. A given weight's exact value barely matters; what matters is the aggregate behaviour of millions of them. Rounding each one to a coarse grid loses much less than intuition suggests.

### How it works: blocks and scales

The naive version — clamp everything to one global scale — destroys the model, because weight magnitudes vary enormously across the network.

The real version divides each tensor into small **blocks** (typically 32 weights), and stores per block:

- A **scale** — the largest magnitude in this block, at higher precision.
- **32 small integers**, each 4 bits, indexing a position on that block's local grid.

Reconstruction is `weight ≈ integer × scale`. Because the scale is local, a block of tiny weights and a block of huge weights each get the full resolution of their 4 bits.

The per-block overhead is why "4-bit" quantization is actually about 4.5 bits per weight in practice. That extra half-bit is the scales.

**K-quants**, the family used throughout this book, refine this further: the scales themselves are quantized against a super-block, and — importantly — different tensors get different precision. Attention matrices, which are more sensitive, get more bits than the bulk FFN matrices.

### The naming scheme

`Q4_K_M` decodes as:

- `Q4` — about 4 bits per weight
- `K` — K-quant family
- `M` — medium; `S` is small, `L` is large, indicating how generous the mixed-precision policy is

`Q4_K_XL` and the various "dynamic" variants push further, assigning higher precision to the tensors that empirically matter most.

### The quality curve

Roughly, in perplexity terms (a standard measure of prediction quality — lower is better):

| Quantization | Size, 30B model | Quality loss |
|---|---|---|
| fp16 | 60 GB | baseline |
| Q8_0 | 32 GB | negligible |
| Q6_K | 25 GB | ~0.1% |
| Q5_K_M | 21 GB | ~0.3% |
| **Q4_K_M** | **17 GB** | **~1%** |
| Q3_K_M | 14 GB | ~3%, noticeable |
| Q2_K | 11 GB | badly degraded |

The knee is at Q4. Above it you pay a lot of gigabytes for very little quality. Below it, quality falls off a cliff.

The community rule of thumb is well supported and worth stating plainly: **a larger model at Q4 beats a smaller model at Q8 at the same file size.** If you have 20 GB to spend, spend it on a 30B at Q4, not a 13B at Q8.

### Why this is a speed decision

Here is the reframe that took me longest to internalise, and it is the hinge of this book.

Everyone describes quantization as a way to fit big models in small memory. That is true, and it is the *lesser* benefit.

Decode reads every weight, every token. Time per token is therefore (bytes of weights) ÷ (bandwidth). Quantizing from 16 bits to 4.5 bits cuts the bytes by 3.5×, which cuts the time per token by **3.5×**.

Quantization is the single largest speed lever available on a laptop, and it is a speed lever that happens to also save disk. If your machine had unlimited RAM you would still quantize, for exactly this reason.

The cost — dequantizing those blocks back to floats on the GPU — is real, and Chapter 20 measures it. It is nowhere near 3.5×.

---

## Chapter 8 — GGUF, the file format {#ch8}

*This chapter establishes the file layout, because reading it directly is what makes Part VI exact instead of estimated.*

**GGUF** — GGML Universal Format — is the file format used by llama.cpp and therefore by most consumer local-inference tooling. One file, self-describing, memory-mappable.

Three sections:

**1. Header.** Magic bytes `GGUF`, version, tensor count, metadata count.

**2. Metadata.** Arbitrary key-value pairs. This is where everything you need to know lives:

```
general.architecture           = muse-glimmer
general.size_label             = 28B
general.license                = apache-2.0
muse-glimmer.block_count       = 52
muse-glimmer.embedding_length  = 6656
muse-glimmer.feed_forward_length = 19968
muse-glimmer.attention.head_count = 32
muse-glimmer.attention.head_count_kv = 2
muse-glimmer.context_length    = 131072
muse-glimmer.rope.freq_base    = 500000
tokenizer.ggml.tokens          = [202048 entries]
```

The `general.architecture` string is load-bearing: it tells llama.cpp which C++ graph-building function to call. A model whose architecture string the runtime does not recognise will not load at all, however valid the file. This is why new models need a llama.cpp release before they work.

**3. Tensor table, then tensor data.** For every tensor: its name, its dimensions, its quantization type, and its byte offset into the data section.

That table is the thing that makes Part VI honest. Because every tensor's exact size and type is listed, you can compute precisely how many bytes must be read to produce one token — as opposed to using the file size, which includes the vocabulary strings, the metadata, and tensors that are *not* read per token. On one of the models in this book, the difference is **64%**. Chapter 18 goes through it.

### Memory mapping

llama.cpp `mmap`s the file rather than reading it. The OS maps the file into the address space and pages it in on demand.

Consequences worth knowing:

- Load appears near-instant; the real cost is deferred to the first inference.
- The pages are file-backed, so under memory pressure the OS can evict them without writing to swap. Cheaper than anonymous memory.
- Activity Monitor will report alarming numbers. It is counting mapped pages, not committed RAM. Do not panic.

### Getting the metadata out

```bash
python3 -c "
from gguf import GGUFReader
r = GGUFReader('model.gguf')
for f in r.fields.values():
    print(f.name)
"
```

Or just start the server: llama.cpp prints most of it during load, which is the subject of Chapter 15.

---
# Part III — The four models

## Chapter 9 — The four models in this book {#ch9}

*This chapter establishes what each model is, who built it, what it is claimed to be good at, and how it is built — the last of which comes from the files on my disk rather than from anyone's marketing.*

I benchmarked four models. Three are 30-billion-parameter class; one is deliberately tiny, as a control. Every architecture number below was read out of the GGUF metadata on this machine, so you can check it yourself against your own copy.

### The comparison, up front

| | **Muse Glimmer 30B** | **Qwen3-32B** | **Gemma 4 31B** | **Gemma 3n E4B** |
|---|---|---|---|---|
| Maker | Meta Superintelligence Labs | Alibaba | Google DeepMind | Google DeepMind |
| Released | Aug 2026 | Apr 2025 | Mar 2026 | Jun 2025 |
| Licence | Apache 2.0 | Apache 2.0 | Apache 2.0 | Gemma Terms |
| Architecture string | `muse-glimmer` | `qwen3` | `gemma4` | `gemma3n` |
| Layers | 52 | 64 | 60 | 35 |
| Hidden size | 6,656 | 5,120 | 5,376 | 2,048 |
| FFN size | 19,968 | 25,600 | 21,504 | 16,384 |
| Heads / KV heads | 32 / 2 | 64 / 8 | 32 / per-layer | 8 / 2 |
| Head dimension | 128 | 128 | 512 global, 256 sliding | 256 |
| Context | 131,072 | 40,960 | 262,144 | 32,768 |
| Sliding window | 2,048, 3:1 | none | 1,024, 5:1 | 512, 4:1 |
| Vocabulary | 202,048 | 151,936 | 262,144 | 262,144 |
| Tied embeddings | no | no | yes | yes |
| Tensors in file | 731 | 707 | 833 | 847 |
| File on disk | 19.65 GB | 19.76 GB | 19.60 GB | 4.54 GB |

Three of these are nearly the same size on disk and were chosen for exactly that reason: it makes the comparison in Part VII a controlled experiment rather than a list.

---

### Muse Glimmer 30B

Meta released this on 9 August 2026 under Apache 2.0, from Meta Superintelligence Labs. At the time of writing it has around half a million downloads. It is **distilled from Muse Spark**, Meta's closed flagship, which is the interesting part: it is a small model carrying a large model's fingerprints.

**What it is.** 29.6 billion text parameters, plus a separate 1.8 billion parameter vision encoder (a ViT-G/14 from Meta's Perception Encoder line, [arXiv:2504.13181](https://arxiv.org/abs/2504.13181)). Text and images in, text out. Knowledge cutoff 4 January 2026.

**Reasoning is always on.** There is no toggle. Every response begins with an internal reasoning pass emitted in a `reasoning_content` field before the visible answer. This is a real cost in a local setting — those are tokens, generated at the same tokens per second as everything else. A short answer might spend 300 tokens thinking. At 6.55 tok/s that is 45 seconds before you see the first visible word.

**What it is claimed to be good at.** Agentic work — tool calling, multi-step tasks, search loops. The model card's numbers, which I did not verify:

| Benchmark | Muse Glimmer | Gemma 4 31B | Qwen3.6 27B |
|---|---|---|---|
| MCP Atlas (tool use) | **75.5** | 54.2 | 62.5 |
| SWE-Bench Pro | **51.2** | 36.9 | 50.2 |
| AIME 2026 (maths) | **94.7** | 89.2 | 94.1 |
| DeepSearch QA | **74.6** | 61.7 | 71.1 |
| Charxiv Reasoning | **78.8** | 77.7 | 78.4 |

The gap on MCP Atlas is the notable one — a 21-point lead on tool use over the nearest comparison. If that holds up, it is the most interesting thing about this model for anyone wiring it into an editor.

**What is not published.** Pretraining token count, data composition, the distillation recipe. Post-training is described only as "Safety SFT" and "Safety RL". Standard for a 2026 frontier-adjacent release.

**Architecture, read off my disk.** This is a plain grouped-query-attention transformer. No state-space layers, no linear attention, nothing exotic. What it does have:

- **Sliding-window attention** with a 2,048-token window, in a 3:1 pattern — three sliding layers then one full-attention layer, repeating.
- **QK-norm** — normalization applied to queries and keys before the attention dot product. A training-stability trick that stuck.
- **An attention output gate** — a sigmoid-gated multiply applied to the attention result before the output projection. The model learns to attenuate attention's contribution per-channel.
- **Final logit softcapping** at 20.0 — the output scores are squashed through a `tanh` so no single token can dominate. Borrowed from Gemma.
- **RoPE base 500,000** — the positional encoding is stretched for long context.

**Shipped extras.** A multimodal projector (`mmproj`, 1.4 GB) for images, and a **DFlash draft model** (1.6 GB). DFlash ([arXiv:2602.06036](https://arxiv.org/abs/2602.06036)) is a 5-layer block-diffusion draft head that proposes 16 tokens at a time for speculative decoding — explained in Chapter 23, and measured in Chapter 20.

llama.cpp support merged 10 August 2026 in PR #26841; you need build b10353 or later.

---

### Qwen3-32B

Alibaba, April 2025, Apache 2.0, [arXiv:2505.09388](https://arxiv.org/abs/2505.09388). The oldest architecture here by a wide margin — about sixteen months, which in this field is a generation and a half.

**What it is.** 32.8 billion parameters, dense, text-only. 64 layers — the deepest and narrowest of the four. Trained on roughly **36 trillion tokens** across 119 languages, which is among the largest disclosed pretraining runs of any open-weights model.

**What it is claimed to be good at.** Multilingual work, where it is genuinely exceptional, and general reasoning. Its distinguishing feature is **hybrid thinking**: `/think` and `/no_think` in the prompt switch reasoning on and off, letting you pay for deliberation only when you want it. Muse Glimmer, by comparison, gives you no choice.

**What is published.** Unusually much. A 3-stage pretraining curriculum (general → knowledge-intensive → long-context) and a 4-stage post-training pipeline (long chain-of-thought SFT → reasoning RL → thinking-mode fusion → general RL) are all described in the paper. If you want to understand how a modern model is actually assembled, this is the most transparent of the four by some distance.

**Architecture.** Plain GQA transformer, no sliding window at all — every layer attends to the full context. Native 32K context, extendable to 131K with YaRN (a rescaling trick applied at inference). 64 heads to 8 KV heads.

Its inclusion here is as an **architectural control**: it is the oldest, plainest, most conventional design in the set, at essentially the same file size as the other two. If architecture were driving performance, this is the one that should look different.

---

### Gemma 4 31B

Google DeepMind, released 31 March 2026, [arXiv:2607.02770](https://arxiv.org/abs/2607.02770). Notable as the **first Gemma released under plain Apache 2.0** — earlier Gemmas carried Google's custom terms, and this was a deliberate and welcome change.

**What it is.** 30.7 billion parameters, dense, text and images in. Part of a family that includes E2B and E4B (small, on-device), a 26B mixture-of-experts with 3.8B active, this 31B dense, and a 12B "Unified" variant.

**What it is claimed to be good at.** General-purpose assistant work with a very long context — 262,144 tokens, the longest here by 2×. Strong multimodal document understanding.

**Architecture, and this one is unusual.** Gemma 4 has the most aggressive attention design of the four:

- **Sliding-window attention with a 5:1 ratio** — five layers with a mere 1,024-token window, then one full-attention layer. Only ten of its sixty layers see the whole context.
- **Asymmetric head dimensions** — 512 for the global-attention layers, 256 for the sliding ones. I have not seen this elsewhere.
- **Per-layer KV head counts** — the metadata carries an array, `[16,16,16,16,16,4,...]`, rather than a single number. Different layers have genuinely different attention shapes.
- **Tied embeddings** and **logit softcapping** at 30.0.

That 5:1 sliding pattern is what makes a 262K context affordable: full attention over 262K tokens in every layer would need an unusable KV cache. This is the clearest example in the set of an architecture designed around a memory constraint rather than around accuracy.

---

### Gemma 3n E4B

Google DeepMind. Preview May 2025, full release June 2025. Under the **Gemma Terms of Use**, not Apache — the only non-OSI licence here.

**What it is.** Explicitly built for phones. About 8 billion raw parameters but roughly **4 billion "effective"** — the `E` in the name — because of a mechanism explained below. Trained on ~11 trillion tokens, cutoff June 2024. Text, images, and **audio** in, via a 12-layer conformer audio encoder and a MobileNet-V5 vision tower.

**Why it is in this book.** As a control at the other end of the scale. It is 4.5 GB against the others' ~19.6 GB. If the performance story in Part VII were about model architecture, this model — which is architecturally the strangest of the four — should behave completely differently. It does, in tokens per second. It does not, in the number that turns out to matter.

**Architecture, and it is genuinely novel.** Three ideas worth knowing because they represent where on-device models are going:

**MatFormer** ([arXiv:2310.07707](https://arxiv.org/abs/2310.07707)) — "Matryoshka Transformer". The model is trained such that smaller models are *nested inside* the big one. You can slice out a 2B model from the 4B weights and it works, without retraining. One download, a family of models, chosen at load time by how much RAM you have.

**Per-Layer Embeddings (PLE)** — instead of one embedding table at the input, each layer gets its own small learned per-token embedding, added as the token passes through. The clever part for deployment: these tables are large but *sparsely accessed* — you read one row per layer per token, not the whole table. They can therefore live on slower storage while the actual weights sit in fast memory. This is the trick that makes an 8B model behave like a 4B one on a phone. It has a dramatic and measurable consequence in Chapter 18.

**AltUp (Alternating Updates)** — the hidden state is split into four parallel sub-streams, only one of which is fully processed per layer while the others are cheaply predicted and corrected. Effective width without the full cost.

Also: activation sparsity (a learned threshold that zeroes most FFN activations) and 15 shared-KV layers, where several layers reuse one layer's keys and values instead of computing their own.

---

### Four concepts these models depend on

Four things appeared in the tables above without explanation. They matter for the rest of the book.

#### Grouped-query attention (GQA)

All four models use it. It is the reason your conversation fits in RAM.

In the original transformer, every attention head had its own key and value projections. 32 heads meant 32 sets of keys and values cached per token. The KV cache was enormous.

GQA makes several query heads **share** one key/value pair. Muse Glimmer has 32 query heads and 2 KV heads: sixteen query heads share each KV head. The KV cache shrinks by 16×, at very little measured quality cost.

You can read this straight off any model card. `n_head / n_head_kv` is your KV cache compression ratio. High ratio, small cache, long conversations affordable.

#### Sliding-window attention

Full attention means every token can see every earlier token. Cost grows with the square of the sequence, and the KV cache grows linearly and never stops.

Sliding-window attention limits most layers to the last N tokens — 2,048 for Muse Glimmer, 1,024 for Gemma 4. Those layers only need to keep N tokens of cache, ever, regardless of conversation length.

But then nothing could see far back, so a minority of layers are left with full attention. Muse Glimmer: three sliding to one full. Gemma 4: five to one. The full-attention layers carry long-range information; the sliding ones do local work cheaply.

Practical consequence: **KV cache does not grow linearly with context on these models.** It grows on the full-attention layers only. Gemma 4's 262K context is affordable precisely because only ten of sixty layers pay for it.

#### Linear attention, and why I am mentioning it

Some 2026 architectures replace attention with recurrent, constant-memory mechanisms — **Gated Delta Net**, Mamba-style state-space layers, **Lightning Indexer** sparse attention. These have a fixed-size state instead of a cache that grows, which changes the memory story completely.

**None of the four models here use any of them.** I am defining the terms anyway for one specific reason: llama.cpp prints startup lines that read as though your model does use them, and it prints those lines for every model. Chapter 15 shows the log and explains why. It is a genuinely useful thing to be able to read correctly, and I would have saved myself several hours if I could.

#### Speculative decoding

Since decode is limited by memory rather than arithmetic (Chapter 11), the GPU spends most of its time waiting. Speculative decoding uses that idle arithmetic.

A small, fast **draft model** proposes the next several tokens. The big model then verifies all of them **in one pass** — which costs barely more than generating one token, because the expensive part was reading the weights, and you read them once for the whole batch. Accepted drafts are free. Rejected ones cost nothing but the draft model's time.

Muse Glimmer ships DFlash for this: a 5-layer draft head proposing 16-token blocks. Its reported speedups are 3.1× on an RTX 5090 and 1.5–1.8× on M4/M5 Max. Chapter 20 has what it did here.

---

# Part IV — The machine

## Chapter 10 — What a laptop is made of {#ch10}

*This chapter establishes the four pieces of hardware that matter and, most importantly, the one number that will determine everything.*

If you have never had reason to think about computer architecture, this is the chapter that makes the rest of the book work. Four components.

### CPU

A handful of powerful, general-purpose cores. Good at branchy, sequential, unpredictable work. Bad at doing the same simple arithmetic ten billion times. Mine has ten cores — eight performance, two efficiency.

For LLM inference the CPU mostly organises work and hands it to the GPU.

### GPU

Thousands of simple cores, all doing the same operation on different data simultaneously. This is exactly the shape of a matrix multiply, which is why GPUs run neural networks and CPUs mostly do not.

Measured in **FLOP/s** — floating-point operations per second. Mine does about **10.4 trillion** per second, written 10.4 TFLOP/s.

That is a big number. Remember it, because in a few pages it becomes irrelevant, and the fact that it becomes irrelevant is the point of the book.

### Memory

RAM. The model must be here to be used — reading weights off an SSD per token would be a hundred times slower.

Two numbers describe memory, and confusing them is the most common mistake in this whole area:

- **Capacity** (GB) — how much fits. Determines *whether* a model runs.
- **Bandwidth** (GB/s) — how fast you can read it. Determines *how fast* it runs.

Capacity is a threshold: you have enough or you do not. Bandwidth is a rate, and it sets your tokens per second almost single-handedly.

### The bus

The wires between memory and processor. This is the thing nobody thinks about and the thing that decides your experience.

Bandwidth comes from two factors multiplied:

```
bandwidth = bus width (bytes) × transfer rate (per second)
```

My M1 Max has a **512-bit** bus — 64 bytes wide — running LPDDR5 at **6.4 billion transfers per second**:

```
64 bytes × 6.4 × 10⁹ /s = 409.6 GB/s   (marketed as 400 GB/s)
```

For contrast, a typical Intel or AMD laptop has a 128-bit bus at similar rates: about 100 GB/s. That 4× difference in a spec nobody reads is why Apple Silicon became the default for local LLMs.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/muse-bus.jpg" alt="Diagram: 64 GB of unified memory holding 18.9 GB of model weights on the left, a 512-bit-wide memory bus drawn as many parallel arrows in the middle, and the M1 Max GPU on the right. A single thin arrow returns one token." />
  <figcaption><strong>The memory bus, and why it is the whole story.</strong> <em>Reading the diagram:</em> on the left is <strong>unified memory</strong> — the pool of RAM that both CPU and GPU read directly, 64 GB on this machine. Inside it sit the model's <strong>weights</strong>: 18.884 GB of numbers that <em>are</em> the model. The wide blue channel is the <strong>memory bus</strong>, the physical wires between memory and processor. Its speed is just two numbers multiplied: it is 512 bits (64 bytes) wide and moves data 6.4 billion times a second, giving 400 GB/s on paper. Measured, this machine sustains <strong>340 GB/s</strong>. The small white box is the <strong>cache</strong>, 48 MB of very fast memory next to the GPU — about 1/400th of what the weights need, so it cannot help here. <em>Why it matters:</em> to produce one <strong>token</strong> (roughly one word), the GPU must read every weight once. There is no way to read fewer. At 340 GB/s, 18.884 GB takes <strong>55.5 milliseconds</strong> — a hard floor of about 18 tokens per second no matter how fast the GPU is. Actual measured speed is 6.55 tokens per second, or <strong>152.7 ms per token</strong>; Chapter 20 accounts for the gap. Note the asymmetry: gigabytes flow right, and about <strong>two bytes</strong> — the token itself — flow back. A single 781-token answer moves <strong>14.7 terabytes</strong> across this bus.</figcaption>
</figure>

### Unified memory versus a graphics card

On a PC with a discrete GPU, there are two separate memories: system RAM (large, slow-ish, 100 GB/s) and the graphics card's VRAM (small, very fast, 500–1000 GB/s), connected by a comparatively narrow PCIe link.

For LLMs this is brutal and binary. If the model fits in VRAM, it is very fast. If it does not — even by one gigabyte — layers must stream across PCIe every token, and throughput collapses by an order of magnitude. A 24 GB RTX 4090 runs a 20 GB model beautifully and a 26 GB model appallingly.

Apple Silicon has **one** memory pool, shared, with the GPU reading it directly. No copying, no VRAM ceiling. A 64 GB Mac can run models that no consumer graphics card can hold.

The trade is bandwidth: 340 GB/s measured here against 1,000 GB/s on a high-end discrete card. So the shape of the trade-off is:

- **Discrete GPU** — much faster, if it fits. Falls off a cliff if it does not.
- **Unified memory** — slower, but the ceiling is your whole RAM, and degradation is graceful.

For a 30B model on a laptop, unified memory usually wins, because 20 GB of VRAM is rare and 64 GB of unified memory is purchasable.

### Cache

A small amount of very fast memory next to the processor. My M1 Max has a 48 MB system-level cache.

For most software, caches are transformative. For LLM decode they are useless, and the arithmetic is worth doing once: the weights are 18.884 GB, the cache is 0.048 GB. The working set is roughly **400 times** too large. Every weight is read from main memory, every token, and evicted before it could ever be reused.

This is why Chapter 19 spends effort on measuring bandwidth with a working set that deliberately exceeds the cache. Measure it with a small buffer and you measure the cache, get a number that looks great, and draw a wrong conclusion. I made sure not to.

---

## Chapter 11 — The two speeds {#ch11}

*This chapter establishes why reading your prompt and writing the answer are limited by completely different parts of the hardware. It is the most important chapter in the book.*

### Two phases, two shapes of work

**Prefill** — the model reads your prompt. All those tokens already exist, so they can be pushed through the network together, as a batch. Mechanically this is **matrix × matrix**: 512 token-vectors multiplied by a weight matrix at once.

**Decode** — the model writes, one token at a time. Token N+1 requires token N. Nothing can be batched. Mechanically this is **matrix × vector**: one lonely token-vector against the same weight matrix.

Same weights. Same arithmetic per token. Radically different economics.

### Arithmetic intensity

The concept that explains everything: for a given piece of work, how much arithmetic do you do per byte you read?

```
arithmetic intensity = FLOPs performed ÷ bytes read
```

Take a weight matrix of 4,096 × 14,336 in 4-bit quantization — about 29 million bytes.

**Decode**, one token: about 117 million FLOPs. Intensity = **4 FLOP per byte**.

**Prefill**, 512 tokens: about 60 billion FLOPs, reading *the same 29 million bytes*. Intensity = **2,048 FLOP per byte**.

Five hundred times the intensity, from the same weights. Batching does not reduce the reading; it amortises it.

### The ridge point

Every processor has a break-even intensity where it flips from being limited by memory to being limited by arithmetic:

```
ridge point = peak FLOP/s ÷ peak bandwidth
            = 10.4 × 10¹² ÷ 340 × 10⁹
            = 30.6 FLOP per byte
```

Below 30.6, you are **memory-bound**: the GPU sits idle waiting for data, and adding compute changes nothing. Above it, you are **compute-bound**: the memory system keeps up, and faster arithmetic helps.

Now place the two phases:

| Phase | Intensity | Ridge point | Verdict |
|---|---|---|---|
| Decode | ~4 | 30.6 | Memory-bound, by 8× |
| Prefill | ~2,048 | 30.6 | Compute-bound, by 67× |

**Decode is not close to the line. It is nowhere near it.** The M1 Max's 10.4 TFLOP/s is, for the purpose of generating text, almost entirely wasted. You could triple the GPU and decode would not move.

### Measuring it, rather than asserting it

That is theory. Here is the same matrix multiplied at three batch sizes on this machine, from llama.cpp's own operation benchmark:

| Batch | Time | Achieved | Intensity | Effective bandwidth |
|---|---|---|---|---|
| 1 token (decode) | 157 µs | 0.75 TFLOP/s | 3.6 FLOP/byte | **210 GB/s** |
| 8 tokens | 868 µs | 1.08 TFLOP/s | 28.4 FLOP/byte | 190 GB/s |
| 512 tokens (prefill) | 12,742 µs | **4.72 TFLOP/s** | 1,820 FLOP/byte | 11 GB/s |

Read that table twice. At batch 1, the GPU achieves 7% of its arithmetic peak and 62% of its bandwidth peak — it is a memory system with a GPU attached. At batch 512 it achieves 45% of its arithmetic peak and uses almost no bandwidth — a completely different machine, made of the same silicon.

Notice too that batch 8 sits right at the ridge point (28.4 against 30.6) and is the worst of both worlds — neither limit is saturated. The theory predicts the crossover and the measurement finds it there.

### The consequences, which are not intuitive

**Your GPU's TFLOP/s number does not predict your tokens per second.** Bandwidth does. When comparing machines for local inference, look up GB/s and ignore everything else.

**A bigger model is proportionally slower.** Twice the weights, twice the bytes, twice the time. This is nearly exact, not approximate.

**Quantization is the biggest available speed lever**, for the reason given in Chapter 7 and now visible in the arithmetic.

**Batching is free capacity.** Serving four users at once costs barely more than one, because you read the weights once for all four. This is why hosted inference is cheap and local inference is not — you are a batch of one.

**Speculative decoding works** for precisely this reason: it converts a memory-bound problem into a slightly-less-memory-bound one by giving the idle arithmetic something to verify.

---

## Chapter 12 — This machine {#ch12}

*This chapter establishes the exact hardware and the measured bandwidth number that Part VII divides by.*

<div class="stat-row">
  <div class="stat-card"><strong>M1 Max</strong><br>10 CPU cores (8P + 2E)</div>
  <div class="stat-card stat-card--violet"><strong>~10.4 TFLOP/s</strong><br>32-core GPU, fp32</div>
  <div class="stat-card stat-card--amber"><strong>64 GB</strong><br>unified memory</div>
  <div class="stat-card stat-card--green"><strong>340 GB/s</strong><br>measured streaming read</div>
</div>

| Component | Specification |
|---|---|
| Chip | Apple M1 Max, 5 nm, 2021 |
| CPU | 10 cores: 8 performance, 2 efficiency |
| GPU | 32 cores, ~10.4 TFLOP/s fp32 |
| Memory | 64 GB LPDDR5-6400, unified |
| Bus | 512-bit |
| Bandwidth, datasheet | 400 GB/s |
| Bandwidth, measured streaming read | **340 GB/s** |
| System-level cache | 48 MB |
| Free disk | ~206 GB |
| OS | macOS 26.6.1 (25G76) |

### Why 340 and not 400

400 GB/s is the **pin rate** — what the memory interface is clocked at. Real transfers include refresh cycles, bank conflicts, controller scheduling, and page misses. No workload achieves the pin rate.

So I measured it, with a working set of 2 GB — over forty times the cache, so nothing could be served from it. Chapter 19 gives the method and the script. Two independent runs returned 336.3 and 343.3 GB/s, and I use **340** throughout.

This matters more than it sounds. Dividing achieved bandwidth by 400 instead of 340 understates efficiency by 15%, and 15% is the difference between "this runtime is doing badly" and "this runtime is doing about as well as anything could." Using a datasheet number as a denominator is the easiest way to reach a wrong conclusion in this whole area.

### The ridge point, restated for this machine

```
10.4 TFLOP/s ÷ 340 GB/s = 30.6 FLOP per byte
```

Decode operates at about 4. This machine is, for text generation, a memory system with a very good GPU bolted on that has nothing to do.

---

## Chapter 13 — Will it run on yours? {#ch13}

*This chapter establishes the two thresholds any machine must clear, and gives you the arithmetic to check your own.*

Two independent questions, in order.

### Question 1: does it fit?

```
RAM needed ≈ model file + KV cache + 2–3 GB overhead
```

The KV cache scales with context length, layer count, and KV head count. For a 30B model at a modest 8K context, budget 1–2 GB. At 32K, more like 4–8 GB.

Working numbers for the models here:

| Model | File | Minimum RAM | Comfortable RAM |
|---|---|---|---|
| Muse Glimmer 30B Q4_K_XL | 19.65 GB | 24 GB | 32 GB |
| Muse Glimmer 30B Q4_K_M | 16.8 GB | 21 GB | 24 GB |
| Qwen3-32B Q4_K_M | 19.76 GB | 24 GB | 32 GB |
| Gemma 4 31B Q4_K_M | 19.60 GB | 24 GB | 32 GB |
| Gemma 3n E4B Q4_K_M | 4.54 GB | 8 GB | 16 GB |

"Minimum" means it will load and run. "Comfortable" means you can also have a browser open.

There is no partial credit here. Exceed your RAM and the OS starts swapping to SSD, and since decode reads every weight every token, you are now reading gigabytes off flash storage per token. Throughput does not degrade — it falls off a cliff, by roughly 50×. If it does not fit, it does not run.

### Question 2: will it be fast enough?

Rearranging the roofline:

```
tokens per second = achieved bandwidth ÷ bytes per token
```

And from Part VII, **achieved bandwidth is about 36% of your machine's peak streaming bandwidth** when running llama.cpp on Metal. That fraction turns out to be remarkably stable across very different models, which is what makes this predictive.

So:

```
tok/s ≈ (peak GB/s × 0.36) ÷ model GB
```

Try it on this machine: (340 × 0.36) ÷ 18.884 = 6.5 tok/s. Measured: 6.55.

### The table

Bandwidth required to hit 10 tok/s, at the 36% efficiency llama.cpp actually delivers:

| Model | Bytes per token | Bandwidth for 10 tok/s |
|---|---|---|
| 30B class at Q4 | ~19 GB | **525 GB/s** |
| 13B at Q4 | ~8 GB | 220 GB/s |
| 7B at Q4 | ~4.5 GB | 125 GB/s |
| Gemma 3n E4B | 2.77 GB | 77 GB/s |

And what real machines have:

| Machine | Memory | Bandwidth | 30B at Q4 | 7B at Q4 |
|---|---|---|---|---|
| MacBook Air M2, 16 GB | 16 GB | 100 GB/s | Will not fit | ~8 tok/s |
| MacBook Pro M1 Max, 64 GB | 64 GB | 400 GB/s | **6.5 tok/s** | ~28 tok/s |
| MacBook Pro M4 Max, 64 GB | 64 GB | 546 GB/s | ~10 tok/s | ~38 tok/s |
| MacBook Pro M5 Max, 128 GB | 128 GB | 614 GB/s | ~12 tok/s | ~43 tok/s |
| Typical Intel/AMD laptop | 32 GB | 90 GB/s | Will not fit usefully | ~7 tok/s |
| Desktop + RTX 4090 | 24 GB VRAM | 1,000 GB/s | ~19 tok/s, barely fits | ~70 tok/s |
| Desktop + RTX 5090 | 32 GB VRAM | 1,790 GB/s | ~34 tok/s | ~125 tok/s |

### What will not work, and why no setting fixes it

**A 30B model on 16 GB of RAM.** Not slowly — not at all. The weights alone exceed the machine. Offloading layers to CPU means those layers stream from SSD per token. You will see 0.2 tok/s. No flag changes this. Run a 7B model.

**Getting a 30B model to 20 tok/s on any current laptop.** You would need 1,050 GB/s. The fastest laptop memory available is 614 GB/s. This is not a software problem and it will not be fixed by a better runtime; Chapter 23 goes through what the actual ceiling is.

**Expecting a better GPU to help decode.** It will not. You are at 4 FLOP/byte against a ridge point of 30.6. The arithmetic units are already idle. Chapter 11 measured this.

**Q2 quantization to make a big model fit.** It fits and it is worse than the Q4 of a smaller model. Below Q3 the degradation is not subtle.

**Long contexts on a machine that barely fits the weights.** The KV cache is additional, and it grows as you talk. Fitting at 4K context tells you nothing about 32K.

<div class="callout callout--green" markdown="1">
**The one-line version.** Take your machine's memory bandwidth in GB/s, multiply by 0.36, divide by your model's size in GB. That is your tokens per second, and in this book it was accurate to within 1%.
</div>

---
# Part V — Doing it

## Chapter 14 — Setup {#ch14}

*This chapter establishes the actual commands, from nothing installed to a model answering questions.*

### The runtime

**llama.cpp** is the C++ inference engine that most consumer local-LLM tooling is built on. Ollama, LM Studio, and Jan all wrap it. Using it directly means more flags and much more visibility, and visibility is the point of this book.

```bash
brew install llama.cpp
```

That is sufficient. I want to state that plainly because a lot of writing on this topic reflexively tells you to build from source. I ran the same model through the Homebrew binary and through two builds from source at different commits, and they all work. Build from source when you want a specific unreleased commit, or when you need the benchmark tools — not because the packaged binary is somehow lesser.

You do need a recent enough version. Muse Glimmer support landed in llama.cpp build **b10353** (PR #26841, 10 August 2026). Check with:

```bash
llama-server --version
```

If your architecture is newer than your binary, the model will refuse to load with an unknown-architecture error. That is the failure mode, and it is unambiguous.

### Building from source, if you want to

You want this if you need `llama-bench` and `test-backend-ops`, which is what Part VI runs on.

```bash
git clone https://github.com/ggml-org/llama.cpp ~/src/llamacpp
cd ~/src/llamacpp
cmake -B build -DGGML_METAL=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build build -j8
```

One thing that cost me time: the default configure does **not** build the benchmark targets. If you want them, configure a second build directory with tests and tools enabled, and build the specific targets:

```bash
cmake -B build-bench -DGGML_METAL=ON -DLLAMA_BUILD_TESTS=ON -DLLAMA_BUILD_TOOLS=ON \
      -DCMAKE_BUILD_TYPE=Release
cmake --build build-bench -j8 --target llama-bench test-backend-ops
```

`-DGGML_METAL=ON` is what enables the Apple GPU backend. Without it everything runs on CPU at roughly a fifth of the speed.

### Choosing a quantization

For Muse Glimmer on 64 GB, the realistic options:

| Build | File | Total resident | Quality cost |
|---|---|---|---|
| `Q4_K_M` | 16.8 GB | ~17 GB | ~1.0% |
| **`Q4_K_XL` (dynamic)** | **19.7 GB** | **~20 GB** | **~0.2%** |
| `Q5_K_M` | 21.5 GB | ~22 GB | ~0.1% |
| `Q6_K` | 25 GB | ~26 GB | negligible |

I took `Q4_K_XL`. The reasoning: 64 GB is enough that the extra 3 GB over `Q4_K_M` is free in practice, and the dynamic variant's mixed precision recovers most of the quality gap for that cost.

Be aware of the trade you are making, though, and it is the one this book is about. That extra 3 GB is 3 GB you read *per token*. Choosing `Q4_K_XL` over `Q4_K_M` costs you roughly 15% of your generation speed in exchange for about 0.8% of quality. On a machine with less headroom, or if speed matters more to you than the last fraction of quality, `Q4_K_M` is the better pick and I would not argue.

Adding the optional pieces:

| Component | Size |
|---|---|
| Main weights, `Q4_K_XL` | 19.7 GB |
| Vision projector (`mmproj`) | 1.4 GB |
| DFlash draft model | 1.6 GB |
| **Total resident** | **~23 GB** |

23 GB of 64 GB, or 36%. Comfortable, with room for the KV cache and everything else you have open.

### Downloading

```bash
pip install -U "huggingface_hub[cli]"

hf download meta-models/Muse-Glimmer-30B-GGUF \
   --include "*Q4_K_XL*" --local-dir ~/Models/Muse-Glimmer-30B-GGUF
```

20 GB. Expect a while. The download resumes if interrupted, which you will need.

### Verifying

```bash
llama-cli -m ~/Models/Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf \
          -ngl 99 -p "Explain what a memory bus is in two sentences." -n 64
```

`-ngl 99` means "put 99 layers on the GPU", which in practice means all of them. If you omit it, llama.cpp runs on CPU and you will conclude, wrongly, that your machine is far too slow.

Words appearing is success. Now the interesting part: the log it printed while doing it.

---

## Chapter 15 — Reading a llama.cpp startup log {#ch15}

*This chapter establishes how to read the wall of text that scrolls past on load — including two lines that mean the precise opposite of what they appear to mean.*

llama.cpp prints a great deal at startup, and almost all of it is useful. Learning to read it is the difference between debugging by guesswork and debugging by evidence.

### The parts worth reading

**Architecture and geometry.** Everything from Chapter 6, confirmed from the file rather than from a web page:

```
llama_model_loader: - kv 2: general.architecture str = muse-glimmer
llama_model_loader: - kv 8: muse-glimmer.block_count u32 = 52
llama_model_loader: - kv 9: muse-glimmer.embedding_length u32 = 6656
print_info: n_head = 32
print_info: n_head_kv = 2
print_info: n_swa = 2048
```

If any of these disagree with what you expected, you have downloaded a different model than you think.

**Quantization mix.** llama.cpp lists the type of every tensor. This is where you confirm a "Q4" file is genuinely mixed-precision rather than uniformly Q4.

**Backend and offload.**

```
ggml_metal_init: found device: Apple M1 Max
load_tensors: offloaded 53/53 layers to GPU
load_tensors: Metal_Mapped model buffer size = 18884.38 MiB
```

`53/53` is what you want. Anything less means some layers are on CPU and you will be slow. The buffer size line is your ground truth for how much memory the weights actually occupy — and note that it matches the bytes-per-token figure in Chapter 18, because it is the same quantity.

**KV cache size.**

```
llama_kv_cache: Metal KV buffer size = 416.00 MiB
```

Check this against your RAM budget before you increase the context.

### The two lines that mislead

Now the part I want to spend real time on, because it is a lovely example of a log telling you something true that reads as something false.

Run any model with verbose logging on and you will see this:

```
resolve_fused_ops: Flash Attention enabled
resolve_fused_ops: resolving fused Gated Delta Net support:
resolve_fused_ops:   fused Gated Delta Net (autoregressive) enabled
resolve_fused_ops:   fused Gated Delta Net (chunked) enabled
resolve_fused_ops: resolving fused Lightning Indexer support:
resolve_fused_ops:   Lightning Indexer enabled
resolve_fused_ops: resolving fused DeepSeek V4 HC support:
resolve_fused_ops:   fused DeepSeek V4 HC pre enabled
resolve_fused_ops:   fused DeepSeek V4 HC comb enabled
resolve_fused_ops:   fused DeepSeek V4 HC post enabled
```

Read naively, that says your model uses Gated Delta Net, Lightning Indexer, and DeepSeek V4 hierarchical compression. It is very easy to read it that way — the lines are indented under the model's own load sequence and use the word "enabled".

The last group gives the game away. **This is Muse Glimmer's log.** Muse Glimmer is not DeepSeek V4. It shares no architecture with DeepSeek V4. Yet three DeepSeek V4 features report as enabled.

**What these lines actually report is backend capability, not model architecture.** The function walks a list of fused-operation probes, and for each one asks: is there any device in this setup that would *fail* to run this operation? It scans the reserved compute graph for nodes matching the probe's operation type. If it finds none — which is exactly what happens when the model does not use that operation at all — nothing mismatches, and it prints "enabled".

So "enabled" means *"nothing here prevents this"*, not *"this is in use"*. The line prints for every model. It is a report about Metal, not about your weights.

You can confirm this from the model's own definition. Muse Glimmer is implemented in `src/models/muse-glimmer.cpp`, 208 lines, and it builds a plain grouped-query-attention transformer: pre- and post-attention norms, QK-norm, a sigmoid gate on the attention output, a gated feed-forward network, and a `tanh` logit softcap. Search it for `GATED_DELTA_NET` and you get zero hits. Gated Delta Net lives in `delta-net-base.cpp`; Lightning Indexer lives in the DeepSeek and MiniMax files. Muse Glimmer is in neither.

<div class="callout callout--amber" markdown="1">
**The general lesson, which is worth more than the specific one.** When a log line is emitted from a loop over a capability table rather than from the code path that does the work, it will happily report on things that never happen. Before building a theory on a log line, find the line in the source and see what condition actually produces it. Here, `grep` for the message text takes about thirty seconds and settles it completely.
</div>

### On stability

I did hit an instability during my first evening of setup — the server loading fine and then dying during inference. I pinned a build and moved on.

When I came back to establish the cause properly, I could not reproduce it on any binary I tried: not the Homebrew build, not a source build at the pinned commit, not a source build at the commit *before* the patch I had assumed was responsible. Four inference runs on each, all clean.

So I have no causal story to offer, and I would rather say that than invent one. What I can tell you is what currently works, which is: everything I tested. If you hit something similar, the useful move is to pin a known-good build and check whether it reproduces before theorising — which is the step I skipped the first time.

Everything measured in Part VII ran on a source build at commit `8cb03844d`.

---

## Chapter 16 — Launching the server {#ch16}

*This chapter establishes the flags that matter and how to budget context.*

```bash
llama-server \
  -m ~/Models/Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf \
  --mmproj ~/Models/Muse-Glimmer-30B-GGUF/mmproj-Muse-Glimmer-30B-F16.gguf \
  -md ~/Models/Muse-Glimmer-30B-GGUF/DFlash-Muse-Glimmer-30B-Q8_0.gguf \
  -ngl 99 -ngld 99 \
  -c 32768 --parallel 1 \
  -fa on \
  --host 127.0.0.1 --port 8080 \
  --jinja
```

### What each flag does

| Flag | Meaning |
|---|---|
| `-m` | The weights |
| `--mmproj` | Vision projector. Omit for text-only and save 1.4 GB |
| `-md` | Draft model for speculative decoding |
| `-ngl 99` | Put all layers on the GPU. Non-negotiable |
| `-ngld 99` | Same, for the draft model |
| `-c 32768` | Total context in tokens |
| `--parallel 1` | One slot. Context is *divided* between slots |
| `-fa on` | Flash attention. Faster, less memory. Leave on |
| `--jinja` | Use the model's own chat template from the GGUF. Required for tool calling |

### Context budgeting, the part that surprises people

`-c` is the **total** context, split across `--parallel` slots. `-c 32768 --parallel 4` gives each slot 8,192 tokens, not 32,768. Every "why does it forget after a few messages" report I have seen traces to this.

For agentic use — where a single conversation carries a long file, a tool schema, and a growing history — you want **one slot with all the context**.

Sizing it: a reasoning model emitting 500 thinking tokens plus a 700-token answer needs 1,200 tokens per turn on top of your input. Add a 40 KB source file at roughly 12,000 tokens, and 32K context gives you maybe eight or nine substantial turns before eviction. That is the real number, and it is smaller than the 131,072 on the model card.

### Sampling

Defaults are reasonable. If you touch anything:

- `--temp 0.7` for general use, `--temp 0.2` for code
- `--top-p 0.9`
- `--repeat-penalty 1.1` if it loops

Reasoning models are more sensitive to high temperature than instruct models — the chain of thought compounds early randomness. Keep it low.

### Confirming it works

```bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Say hi."}],"max_tokens":32}' | jq -r '.choices[0].message.content'
```

The endpoint is OpenAI-compatible, so anything that speaks to OpenAI speaks to this by changing a base URL.

---

# Part VI — Measuring

## Chapter 17 — How performance was measured {#ch17}

*This chapter establishes the experiments, the exact commands, and the choices that make the results trustworthy.*

Everything in Part VII comes from four measurements. All scripts are in the [companion repository](https://github.com/rajeeja/local-llm-bench-m1max).

### Experiment 1 — throughput, four models

```bash
llama-bench -m "$MODEL" -ngl 99 -p 512 -n 128 -d 0 -fa on,off \
            -t 8 -b 2048 -ub 512 -ctk f16 -ctv f16 -lm auto \
            -r 5 --delay 8 --progress -o json
```

`-p 512` measures prefill on a 512-token prompt. `-n 128` measures decode over 128 generated tokens. `-r 5` repeats each five times. `--delay 8` idles between repetitions so thermals settle.

**Two full passes, with the model order reversed in the second.** Pass 1 runs Muse Glimmer, Qwen3, Gemma 4, Gemma 3n; pass 2 runs the same four backwards. Any drift from the machine warming up across a pass shows as a systematic difference between the passes, and reporting the mean of the two cancels it. Every number in Part VII is such a mean.

Before each model, a pre-gate checks the machine is on AC power with Low Power Mode off. Those two conditions genuinely invalidate a measurement — Low Power Mode caps GPU clocks outright. Background CPU load is *recorded* rather than gated on: a sampler writes foreign CPU usage every three seconds to a sidecar file, so throughput can be reported against the load it ran under. The alternative — rejecting any window with a load spike — measures a quiet machine that no actual user ever has.

### Why the benchmark uses fake text

`llama-bench` feeds synthetic tokens, not real prose. This looks like a flaw and is the opposite.

Decode speed is set by how many bytes must be read per token, and that is fixed by the architecture — identical for every token regardless of content. What *would* vary with real text is early stopping, tokenizer behaviour, and prompt-cache hits, none of which are properties of the hardware. Synthetic tokens remove those confounds and measure the thing being measured.

The honest caveat: this measures raw generation. It does not measure your experience with a reasoning model that emits 400 thinking tokens before answering. That is a real cost, and it is a property of the model's behaviour, not its speed.

### Experiment 2 — bytes per token

A script that opens the GGUF, walks the tensor table, and classifies every tensor by whether it is read on every token. Chapter 18 is this experiment.

### Experiment 3 — memory bandwidth

A working set far larger than cache, streamed on the GPU. Chapter 19.

### Experiment 4 — kernel-level arithmetic intensity

```bash
test-backend-ops perf -o MUL_MAT
```

llama.cpp's own operation benchmark, run on one matrix shape at batch 1, 8, and 512. This produced the table in Chapter 11 and is what pins the ridge-point crossover to a measurement rather than a calculation.

---

## Chapter 18 — Bytes per token {#ch18}

*This chapter establishes why the file size is the wrong number, and how to get the right one.*

The roofline model needs bytes read per token. The obvious source is the file size. The obvious source is wrong, and on one model here it is wrong by 64%.

### What the file contains that decode does not read

A GGUF holds:

- **Weight tensors that decode reads every token.** Attention matrices, FFN matrices, norms, output head. These are the number we want.
- **Tensors that are *gathered*, not streamed.** The embedding table has one row per vocabulary entry, and a token reads exactly one row. Reading 6,656 numbers out of a 202,048 × 6,656 table costs the one row, not the table.
- **Metadata and tokenizer.** 202,048 vocabulary strings and their scores. Tens of megabytes. Read at load, never during inference.

So: walk the tensor table, and for each tensor decide whether it is streamed or gathered.

```python
GATHERED = {"token_embd.weight", "per_layer_token_embd.weight"}

streamed = 0
for t in reader.tensors:
    if t.name in GATHERED:
        continue
    streamed += t.n_bytes
```

Plus one adjustment: if the model has **tied embeddings** — no separate `output` tensor, the embedding matrix reused transposed for the output head — then that matrix *is* fully read for the output projection, and must be counted after all.

### The results

| Model | Streamed per token (B_tok) | File size | File overstates by |
|---|---|---|---|
| Muse Glimmer | **18.884 GB** | 19.654 GB | +4.1% |
| Qwen3-32B | **19.319 GB** | 19.762 GB | +2.3% |
| Gemma 4 31B | **19.583 GB** | 19.598 GB | +0.1% |
| Gemma 3n E4B | **2.771 GB** | 4.539 GB | **+63.8%** |

The three 30B models are close enough that file size would have been a tolerable approximation. Gemma 3n is not close at all, and its gap is the most instructive result in this chapter.

### Where the differences come from

| Model | `token_embd` | Tied? | Gathered, not streamed |
|---|---|---|---|
| Muse Glimmer | 0.756 GB | no | 0.770 GB |
| Qwen3-32B | 0.438 GB | no | 0.443 GB |
| Gemma 4 31B | 1.156 GB | **yes** | 0.015 GB |
| Gemma 3n E4B | 0.302 GB | **yes** | **1.762 GB** |

**Untied models** (Muse Glimmer, Qwen3) have a separate output head, so the input embedding table is pure gather and comes off the total.

**Gemma 4 is tied.** Its 1.156 GB embedding matrix is read in full every token for the output projection, so almost nothing is excluded. Its file size and its bytes-per-token are within 0.1%.

**Gemma 3n has Per-Layer Embeddings** — the mechanism from Chapter 9. `per_layer_token_embd` is a **1.762 GB** tensor, and it is gathered: one small row per layer per token. It is 39% of the file and it contributes almost nothing to per-token bandwidth.

This is the design paying off exactly as intended. Google built a model where a large fraction of the file is deliberately not on the bandwidth-critical path, because on a phone bandwidth is the binding constraint and storage is not. Using the file size for this model would have made it look 64% more expensive per token than it is — and would have made the roofline analysis in Chapter 20 look like Gemma 3n was an outlier, when in fact it lands right on the line with everything else.

<div class="callout callout--green" markdown="1">
**Worth generalising.** Anyone comparing local models on a bytes-per-token basis using file sizes will systematically mis-rank models that use sparse or gathered structures. Parse the tensor table. It is about forty lines of Python and it is the difference between an estimate and a measurement.
</div>

---

## Chapter 19 — The denominator {#ch19}

*This chapter establishes the bandwidth figure that Part VII divides by, and why it is measured rather than quoted.*

Efficiency is achieved bandwidth over peak bandwidth. Choosing "peak" badly is the easiest way to reach a confident wrong answer, and there are two distinct traps.

### Trap one: the datasheet

400 GB/s is the pin rate. Refresh cycles, bank conflicts, controller scheduling, and page misses all take a cut. No workload sees it. Dividing by 400 understates efficiency by about 15% against reality.

### Trap two: measuring the cache

The subtler trap, and the one I nearly fell into. llama.cpp's own operation benchmark reports a copy kernel at 294 GB/s — a tempting number, already measured, right there.

Look at the working set: 37,376 kB, or 36.5 MB. The M1 Max system-level cache is 48 MB. **The entire buffer fit in cache and was re-read nine thousand times.** That measures cache bandwidth, not memory bandwidth.

Decode streams 18.884 GB per token, roughly 400× the cache. Nothing is ever reused. The two situations have nothing to do with each other.

### Measuring it properly

Sweep the working set from below cache to far above it, using two kernels whose traffic is unambiguous: a sum (reads N bytes, writes ~0) and an in-place add (reads N, writes N). Read bandwidth is the relevant one, since decode reads weights and writes almost nothing.

```
   MB    read GB/s   note
   16         33.7   fits in 48 MB cache
   48         73.5   fits in 48 MB cache
  128        126.6
  512        291.9
 2048        336.3
```

Two independent runs of the largest size gave 336.3 and 343.3 GB/s. I use **340 GB/s**.

### Reading that curve honestly

The curve rises with size, which looks like a cache effect and is not one. Fitting `time = overhead + bytes/bandwidth` over the large sizes recovers a fixed per-iteration cost of about 0.3 ms — the synchronisation this script uses to make sure it times GPU work rather than enqueue time. That overhead dominates the small sizes and is what produces the rise. Subtract it and the curve is flat from 256 MB up, so no cache knee is resolvable here, and I do not claim one.

Which is why the reported number is the **raw** measurement at the largest working set, not the overhead-corrected extrapolation. The extrapolation is a two-parameter fit over a short lever arm and it moved by 46 GB/s between two runs. The raw number is a measured lower bound: instrument overhead can only depress it, never inflate it. A lower bound on the denominator makes the efficiency figures in Part VII conservative, which is the direction to err.

### The ladder

Three honest bandwidth numbers for the same chip, each measuring something different:

| Measurement | GB/s | What it is |
|---|---|---|
| Datasheet pin rate | 400 | The interface clock |
| Streaming read, 2 GB working set | **340** | What memory sustains |
| One isolated q4_K mat×vec kernel | 210 | Best case for the operation decode does |
| Full decode, all four models | 124–140 | What actually happens |

340 is the denominator for the roofline. 210 is interesting because it bounds how much of the remaining gap is attributable to the operation itself rather than to everything around it — and Chapter 20 uses that to split the loss into parts.

---
# Part VII — What came out

## Chapter 20 — Results {#ch20}

*This chapter establishes what four very different models actually did on one machine, and what the pattern in those numbers means.*

### Decode

Mean of two passes, flash attention on. Achieved bandwidth is tokens per second × bytes per token from Chapter 18.

| Model | tok/s | Bytes/token | Achieved GB/s | % of 340 measured | % of 400 datasheet |
|---|---|---|---|---|---|
| Muse Glimmer 30B | 6.55 | 18.884 GB | 123.6 | **36.4%** | 30.9% |
| Gemma 4 31B | 6.36 | 19.583 GB | 124.5 | **36.6%** | 31.1% |
| Qwen3-32B | 7.02 | 19.319 GB | 135.7 | **39.9%** | 33.9% |
| Gemma 3n E4B | 50.45 | 2.771 GB | 139.8 | **41.1%** | 34.9% |

One caveat before the interpretation. Three of the four models agreed between the two passes to within 1.5%. Gemma 4 did not — its two passes differ by 11.7%, and the load sidecars show its second window ran under heavier background load. I report the mean with that spread visible in the [raw data](https://github.com/rajeeja/local-llm-bench-m1max) rather than dropping the window, because a machine with background load is the machine people actually have. It does not change any conclusion below; Gemma 4's two passes bracket 36.6% efficiency from both sides.

Sit with that last column for a moment.

Four models. Different makers, different countries, different years. Architectures that disagree about nearly everything — 35 to 64 layers, hidden sizes from 2,048 to 6,656, sliding-window ratios of none to 5:1, tied and untied embeddings, one of them using MatFormer and per-layer embeddings and alternating updates. Sizes spanning **7×**. Speeds spanning **8×**.

They all extract between 36.4% and 41.1% of this machine's memory bandwidth.

The three 30B-class models are within **3.5 percentage points** of each other. Gemma 3n, which is architecturally the strangest model here and eight times faster, is only 4.7 points above Muse Glimmer.

**The 8× difference in tokens per second is entirely explained by the 6.8× difference in bytes per token.** Once you divide it out, the models are indistinguishable. Architecture is not what makes one of these faster than another on this hardware. Size is.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/muse-bandwidth-waterfall.jpg" alt="Four descending bars: 400 GB/s datasheet pin rate, 340 measured streaming read, 210 for one isolated q4_K matrix-vector kernel, and 124 to 140 GB/s for real decode across all four models." />
  <figcaption><strong>Four honest answers to "how fast is memory on this chip", each smaller than the last.</strong> <em>Reading the chart:</em> <strong>GB/s</strong> is gigabytes per second — how much data can be pulled out of memory in one second. Bar 1 is the <strong>datasheet pin rate</strong>, the speed the memory interface is clocked at; no real workload reaches it. Bar 2 is what this machine <strong>actually sustains</strong> when reading a large block of memory end to end, which is the honest ceiling and the number this book divides by. Bar 3 is one <strong>q4_K mat×vec</strong> in isolation — a single 4-bit-quantized weight matrix multiplied by one token's vector, the exact operation generating text performs. It loses 130 GB/s to unpacking those 4-bit numbers back into floats and to the fixed cost of launching a GPU operation. Bar 4 is a <strong>real model decoding</strong>, which loses another 80 GB/s to doing that operation 52 to 64 times over (once per layer), plus normalization and attention between each. <em>Why it matters:</em> the four tokens-per-second figures on the right differ by 8× — and all four land inside the same narrow bandwidth band. Divide out how many bytes each model must read per token and the models become indistinguishable. Speed here is not a property of the model. It is a property of how much of the bus the runtime manages to keep busy, and that figure is about <strong>36%</strong> for everything.</figcaption>
</figure>

### Where the missing 64% goes

Three honest measurements bracket the loss:

```
340 GB/s   streaming read, 2 GB working set        ← the ceiling
210 GB/s   one q4_K mat×vec kernel, in isolation   ← 62% of ceiling
124 GB/s   full decode, whole model                ← 36% of ceiling
```

The first drop, 340 → 210, is **38% lost inside a single operation**. That is dequantization — unpacking 4-bit blocks and their scales back into floats — plus per-kernel launch overhead, plus the fact that a matrix-vector product has poor reuse of anything the GPU has loaded into registers.

The second drop, 210 → 124, is **41% lost to everything around the operations**. Fifty-two to sixty-four sequential layers per token, each with its own dispatch. Normalization, attention, softmax, residual adds. Synchronisation between dependent kernels. None of it individually large; collectively larger than the dequantization cost.

That second gap is where a runtime could plausibly improve. But note that it is a *dispatch and orchestration* problem, not a kernel problem, and Metal's command submission model puts a floor under it. Nobody is getting this to 80% on this stack.

### The per-layer hypothesis, and why the data kills it

A tempting story: if the loss is fixed dispatch overhead per layer, models with more layers should be less efficient. Qwen3 has 64 layers to Muse Glimmer's 52 — it should be worse.

It is better. So let me put actual numbers on it:

| Model | Layers | Bytes per layer | Time per layer |
|---|---|---|---|
| Muse Glimmer | 52 | 363.2 MB | 2,936 µs |
| Gemma 4 31B | 60 | 326.4 MB | 2,621 µs |
| Qwen3-32B | 64 | 301.9 MB | 2,226 µs |
| Gemma 3n E4B | 35 | 79.2 MB | 566 µs |

If dispatch overhead dominated, time-per-layer would be roughly constant. It varies by **5.2×**, and it varies monotonically with bytes per layer. Fixed per-layer cost is not the story; per-layer *bytes* is.

The residual trend is real though. Ranking by bytes per layer gives exactly the reverse of ranking by efficiency: Muse Glimmer has the fattest layers and the lowest efficiency, Qwen3 has thinner layers and does better, Gemma 3n has the thinnest and does best. Deeper-and-narrower extracts slightly more bandwidth than shallower-and-wider. It is a second-order effect worth a few percent, sitting on top of a first-order effect worth everything.

### Prefill, and an inversion

Mean of two passes, 512-token prompt:

| Model | Prefill tok/s | Decode tok/s | Ratio |
|---|---|---|---|
| Muse Glimmer 30B | **87.1** | 6.55 | 13.3× |
| Qwen3-32B | 74.7 | 7.02 | 10.6× |
| Gemma 4 31B | 74.1 | 6.36 | 11.7× |
| Gemma 3n E4B | 687.1 | 50.45 | 13.6× |

Muse Glimmer is **slowest at decode among the 30B models and fastest at prefill**. That inversion is Chapter 11 made visible.

Prefill is compute-bound. What helps is doing your arithmetic in a small number of large, GPU-friendly matrix multiplies. Muse Glimmer's 52 fat layers (6,656 wide) do exactly that. Qwen3's 64 thin layers (5,120 wide) mean more, smaller multiplies — better for the memory-bound phase, worse for the compute-bound one.

The same architectural choice that costs Muse Glimmer 7% of decode buys it 17% of prefill. There is no free lunch; there is a dial, and the two phases want it turned opposite ways.

Practically: if your workload is long prompts and short answers — summarisation, classification, extraction — Muse Glimmer's shape is the right one. If it is short prompts and long answers, it is the wrong one.

### Flash attention

Enabling flash attention changed decode throughput by under 1% on every model, at a 512-token prompt. That is expected and not a disappointment: flash attention optimises the attention computation, which at short context is a small fraction of the work. Its benefit grows with context length, and at 32K it is substantial. Leave it on; do not expect it to rescue you here.

### Speculative decoding

Running the server with the DFlash draft model attached, the first generation came in at **9.14 tok/s** against roughly 6.4 without it — about a **1.4× speedup**, and in the same range as the 1.5–1.8× reported for M4 and M5 Max. A subsequent generation gave 7.42 tok/s, which is the expected behaviour: the acceptance rate depends on how predictable the text is, so the speedup varies by content.

This is measured at the server, not through the benchmark harness, so treat it as an indication rather than a controlled result. But it is the largest single speed win available here, and it is free — the draft model costs 1.6 GB and idle arithmetic that was going to waste anyway.

### The one-sentence version

**On a bandwidth-limited machine, tokens per second is bytes per token divided by about 36% of your memory bandwidth, and nothing about the model's design moves that 36% by more than a few points.**

---

## Chapter 21 — Gemma 3n: what small buys and costs {#ch21}

*This chapter establishes what the 8× speed difference actually feels like, and what it costs you.*

Gemma 3n E4B ran at **50.45 tok/s**. Muse Glimmer ran at 6.55. Same machine, same session, same afternoon.

50 tok/s is faster than you read. Answers appear essentially complete. There is no watching, no waiting, no tabbing away and coming back. It is, subjectively, a completely different product — and this is worth saying plainly, because a table of numbers does not convey it. The gap between 6.5 and 50 tok/s is not a quantitative difference in the same experience. It is the difference between a tool you use and a tool you avoid.

It is also, on the bandwidth measure, the *same machine doing the same thing at the same efficiency*: 41.1% against 36.4%. It reads 2.771 GB per token instead of 18.884.

### What you give up

Real things, and I would not pretend otherwise:

**Reasoning depth.** Multi-step problems, subtle instructions, long chains of inference. This is where parameter count still buys you something no architecture trick replaces.

**Breadth of knowledge.** ~11 trillion training tokens against Qwen3's ~36 trillion, in a model a seventh the size. It knows less. The cutoff is June 2024, which is old.

**Code generation.** Usable for small, well-specified functions. Not for anything architectural.

**Long context.** 32K against Gemma 4's 262K.

### What you keep

More than I expected. Conversation, summarisation, extraction, classification, rewriting, simple tool calls, and answering questions about text you give it. For a large fraction of what people actually use a local model for, the 4B model at 50 tok/s is the better product than the 30B model at 6.5.

### Laptop versus phone

Google reports Gemma 3n E4B at **9.74 tok/s on a Pixel 10 Pro XL**, with 557 ms to the first token. That is a reported figure from a different runtime, not something I measured, and I flag it as such.

Taken at face value it is a 5.2× gap to this laptop, which is roughly the ratio of the two memory bandwidths. The same physics governs both. A phone runs a small model at usable speed for the same reason a laptop runs a large one at unusable speed — the ratio of bytes-per-token to bandwidth. The hardware differs by a factor of five; the model differs by a factor of seven; the arithmetic is identical.

---

## Chapter 22 — Small and specific is probably the direction {#ch22}

<div class="callout callout--amber" markdown="1">
**This chapter is opinion.** Everything before it is measurement. I am flagging the switch explicitly because the two should not be read the same way.
</div>

The Gemma 3n result reframed how I think about this.

A 30B general-purpose model on a laptop is, right now, a slightly unhappy compromise: not as capable as a hosted frontier model, not fast enough to be pleasant, and consuming a third of your RAM to be neither. It is the worst point on the curve, and it is the point almost everyone starts at because it is the one with the impressive number in its name.

The interesting direction is the other one. A **4B model fine-tuned for one job**, running at 50 tok/s, using 5 GB, is a genuinely good product for that job. And most jobs are narrow: extract fields from these invoices, classify these tickets, rewrite this in house style, answer questions about this codebase, transcribe and summarise these meetings.

The economics favour this strongly, and the favour compounds:

- **Speed** is the whole difference between a tool you reach for and one you avoid. 8× is not a tuning improvement; it is a category change.
- **Fine-tuning a 4B model** on your own data is achievable on hardware you already own. Fine-tuning a 30B model is not.
- **Bandwidth is the constraint**, and it improves at maybe 15% a year. Model quality at a given size improves much faster than that. The gap between "what a 4B model can do" and "what you need" closes from the model side, not the hardware side.
- **You can run several at once.** Five specialised 4B models fit where one 30B does, and they fit in memory simultaneously.

The counter-argument is real: for genuinely open-ended agentic work — the kind where the model has to decide what to do, use tools, recover from failure, and keep a long context straight — capability is not decomposable and the big model wins. That is also, notably, the use case Muse Glimmer is built for and where its tool-use benchmark lead sits.

So I would put it this way. Big general models on laptops are a transitional artefact of a moment when small models were not good enough. That moment is ending faster than laptop memory buses are getting wider, and the bus is the thing that is not going to save us.

---

## Chapter 23 — Hardware guidance {#ch23}

*This chapter establishes what it would actually take to make a 30B model pleasant locally, and the four things you can change.*

### A useful comparison point

Meta published ExecuTorch numbers for Muse Glimmer on newer Apple hardware. Their runtime is not llama.cpp, and the difference is the most informative part.

| Runtime | Machine | Peak GB/s | tok/s | Achieved GB/s | Efficiency |
|---|---|---|---|---|---|
| llama.cpp Metal | M1 Max | 340 measured | 6.55 | 123.6 | **36%** |
| ExecuTorch | M4 Max | 546 | 23.7 | 447.6 | **~82%** |
| ExecuTorch | M5 Max, 40-core | 614 | 26.6 | 502.3 | **~82%** |

That 82% is remarkable, and it separates two things that are easy to conflate.

**How much is the hardware?** M5 Max has 1.8× the bandwidth of this machine. Running llama.cpp at its 36% on an M5 Max would give roughly **11.8 tok/s** — better, not transformative.

**How much is the software?** ExecuTorch's efficiency on this M1 Max, if it were available here, would give roughly **14.8 tok/s** at 340 GB/s. On the same silicon I already own.

**The software gap is larger than the hardware gap.** A 2026 laptop running llama.cpp is slower than a 2021 laptop running a runtime that keeps the bus busy. That is worth knowing before spending four thousand dollars.

Two caveats I will not skip. ExecuTorch is Meta's runtime measured by Meta on Meta's model, which is the best possible case for it. And llama.cpp is doing something much harder — supporting dozens of architectures and quantization formats across five backends. Generality has a cost and this is what it looks like.

### What each speed target requires

| Target | Bandwidth needed at 82% | Bandwidth needed at 36% |
|---|---|---|
| 10 tok/s | 230 GB/s | 525 GB/s |
| 15 tok/s | 345 GB/s | 790 GB/s |
| 25 tok/s | 575 GB/s | 1,310 GB/s |

At llama.cpp's current efficiency, **comfortable reading speed for a 30B model on a laptop is not purchasable**. 790 GB/s does not exist in a portable machine. At ExecuTorch's efficiency it is already here — a current M4 Max would do it.

### The four levers, ranked by what they actually return

**1. Run a smaller model.** 8× from a 7× size reduction, immediately, free. This is not a consolation prize; per Chapter 22 it is probably the right answer.

**2. Speculative decoding.** 1.4× measured here, up to 1.8× reported on newer chips. Costs 1.6 GB and nothing else. If your model ships a draft model, use it.

**3. A better runtime.** 2.3× available in principle, based on the ExecuTorch comparison. Not available to you today for arbitrary models on this stack, but it is the largest single number on this list and the one most likely to move.

**4. Better hardware.** 1.8× for the price of a new laptop, and it does not change the shape of the problem. Buy it for the RAM, which lets you run models you cannot run at all — not for the speed.

Notice what is absent: nothing about your GPU, your CPU cores, your thread count, or any flag in `llama-server`. Those are not the constraint and adjusting them is how people spend an evening learning that.

### Where local still wins outright

**Batch work overnight.** 6.55 tok/s is 23,000 tokens an hour. Run it over a thousand documents while you sleep and speed stops mattering. Cost per token is electricity.

**Anything that cannot leave the building.** No speed comparison applies, because the alternative is not available.

**Small models for narrow jobs.** Covered at length in Chapter 22, and the strongest case here.

**Prefill-heavy work.** 87 tok/s of prefill against 6.55 of decode. Summarising a long document is 90% prefill, and prefill on this machine is respectable.

---

## Chapter 24 — Using it day to day {#ch24}

*This chapter establishes how to wire a local model into an editor, and one cost nobody warns you about.*

### Editor integration

[opencode](https://opencode.ai) is a terminal coding agent that accepts any OpenAI-compatible endpoint. In `~/.config/opencode/opencode.json`:

```json
{
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local llama.cpp",
      "options": { "baseURL": "http://127.0.0.1:8080/v1" },
      "models": {
        "muse-glimmer-30b": {
          "name": "Muse Glimmer 30B (local)",
          "tools": true,
          "reasoning": true,
          "limit": { "context": 32768, "output": 8192 }
        }
      }
    }
  }
}
```

`"tools": true` enables function calling — required for anything agentic, and it depends on `--jinja` being set on the server so the model's own chat template is used. `"reasoning": true` tells opencode to expect and render the `reasoning_content` field rather than showing it as body text.

Set `"limit".context` to match your server's `-c`, or the client will happily send more than the server can hold.

### The honest experience

At 6.55 tok/s, a single-file edit takes a minute or two. Anything spanning several files is a coffee break. It works; the model follows instructions and uses tools competently. It is not a replacement for a hosted model in an interactive loop, and I do not use it as one.

Where it is genuinely good: work you can fire and forget. Refactors with a clear spec. Batch edits across a repository. Anything where you would have context-switched away anyway.

### The tool schema cost, which is not obvious

If you connect an MCP server — the protocol for exposing tools to a model — every tool's JSON schema is sent with **every single request**.

I connect a mesh-analysis server exposing 31 tools. Its schemas total roughly **10,600 tokens**. Every request.

Against a 32K context that is a third of your budget consumed before you have said anything. At 87 tok/s of prefill, that is 2 minutes of prefill per request just to re-read the tool definitions.

Consequences worth acting on:

- **Enable MCP servers per-session, not globally.** Turn them on for work that needs them.
- **Prefer few, broad tools over many narrow ones.** A dozen focused tools beat thirty granular ones on a local model, and the difference is measured in minutes.
- **Watch the prefill time in the server log.** It tells you immediately when schema bloat has crept in.

This is a cost that is essentially invisible on a hosted model, where prefill is fast and context is large. Locally it is one of the biggest levers you have.

---

# Appendix A — Reproducing this {#appendix-a}

Every number in Part VII comes from these scripts, and they are all in **[github.com/rajeeja/local-llm-bench-m1max](https://github.com/rajeeja/local-llm-bench-m1max)** along with the raw output of both passes.

| Script | What it does |
|---|---|
| `run_pass.sh` | Runs one full benchmark pass over all four models, with power pre-gate and background-load sampling |
| `analyze.py` | Reads both passes' JSON, computes achieved bandwidth, roofline efficiency, per-layer figures |
| `gguf_btok.py` | Parses a GGUF tensor table and computes bytes streamed per token |
| `stream_bw.py` | Sweeps GPU working-set size to measure streaming read bandwidth |

Full reproduction:

```bash
./run_pass.sh pass1
./run_pass.sh pass2          # reverse order, thermal control
python3 stream_bw.py         # gives the denominator
python3 gguf_btok.py <model.gguf>
python3 analyze.py --rgpu 340
```

`analyze.py` regenerates every table in Chapter 20.

**Environment.** All measurements on macOS 26.6.1 (25G76), M1 Max 64 GB, on AC power with Low Power Mode off. Benchmark binary built from llama.cpp source at commit `8cb03844d`. Models as listed in Chapter 9, all Q4_K quantizations.

---

## Where this leaves me

I set out to run a large model on my laptop and ended up writing down everything I had to learn to understand why it was slow.

The answer is one number. Generating a token requires reading the entire model, and the memory bus reads about 340 GB per second, and llama.cpp keeps roughly 36% of that busy. Everything else — the architecture, the layer count, the attention scheme, the quantization family, the flags — is second-order or noise. Four models designed by four teams across five years land within five percentage points of each other on the only measure that decides how long you wait.

That is a satisfying kind of answer. It means you can predict this. Take the bandwidth of any machine, multiply by 0.36, divide by the model's size in gigabytes, and you have its speed to within a percent or two. No benchmarking required.

It also means the interesting work is not in tuning. It is in the two places where the constant actually moves: **smaller models**, which change the numerator by an order of magnitude, and **better runtimes**, which have already been shown to more than double the 36%. The hardware will improve at 15% a year and will not rescue anyone.

If you take one thing from this book: **look up your machine's memory bandwidth before you download anything.** It is the number that decides, and it is the number nobody puts in the model card.

