---
title: "The AI ROI Problem Is Real. The Fix Isn't Cutting Licenses."
date: 2026-05-28
permalink: /blog/ai-roi-mcp-discipline/
categories:
  - blog
excerpt: "Corporate leaders are questioning whether AI spending delivers returns. The problem isn't AI. It's that most enterprises handed out general-purpose chat access and called it a strategy. The projects delivering real value — including the UXarray MCP work I've been building — share an architecture that looks nothing like that."
tags:
  - mcp
  - ai-agents
  - scientific-computing
  - roi
  - enterprise-ai
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">AI in Production · May 2026</p>
  <h1 class="article-title">The AI ROI Problem Is Real. The Fix Isn't Cutting Licenses.</h1>
  <p class="article-dek">Companies spent billions, got chatbots that check the weather, and are now hitting the brakes. That's not an AI problem — it's an architecture problem. Here's what disciplined AI actually looks like.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--violet">AI agents</span>
  <span class="post-tag post-tag--blue">MCP</span>
  <span class="post-tag post-tag--teal">scientific computing</span>
  <span class="post-tag post-tag--amber">ROI</span>
  <span class="post-tag">enterprise AI</span>
</div>

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">$500M</span>
    <span class="stat-card__label">in a single month — one client who forgot to set AI usage limits</span>
  </div>
  <div class="stat-card stat-card--green">
    <span class="stat-card__value">10s</span>
    <span class="stat-card__label">to analyze a 1.1 GB facility mesh from a laptop — no SSH, no scripts</span>
  </div>
  <div class="stat-card stat-card--violet">
    <span class="stat-card__value">0</span>
    <span class="stat-card__label">weather queries in a scientific MCP server with a typed tool catalog</span>
  </div>
</div>

Corporate leaders are questioning whether soaring AI spending delivers meaningful returns. Major technology companies have pulled back on AI seat licenses. Operations chiefs at enterprise firms say costs are getting harder to justify. And a story making the rounds in consulting circles: one client spent half a billion dollars in a single month because nobody put usage limits on employee AI access.

One framing you hear from investors and founders lately is pointed: AI works reliably for coding. For everything else, the returns are murky.

That's wrong about the scope, but right about the underlying diagnosis. AI works reliably when it operates inside clear task boundaries with typed interfaces. Coding happens to be the domain where those boundaries exist by default — compilers, linters, tests, and version control all provide the feedback loops that keep an agent honest. The problem isn't that AI only works for coding. The problem is that most enterprises deployed AI in every other domain without building equivalent guardrails.

The right metric for AI ROI isn't tokens consumed — it's **intelligence per token**: useful, auditable work delivered per compute unit spent. That metric only improves when the agent is constrained to operations that matter. Unconstrained, it converges toward the path of least resistance: summarization, weather checks, email drafts. Constrained to a typed tool catalog, it converges toward the thing you actually needed done.

I have spent the past year building a system where AI works reliably for a hard scientific domain — production Earth-system mesh analysis on HPC clusters. The architecture that made it work is exactly the architecture that most enterprises are missing.

---

## The tokenmaxxing problem, diagnosed correctly

"Tokenmaxxing" — the push to burn as many AI tokens as possible — is a good name for a real phenomenon, but it describes a symptom. The disease is unrestricted general-purpose access.

When you give a thousand employees an all-you-can-eat chat interface and tell them to "use AI," here is what you get:

- **Checking the weather.** (Cited by multiple executives as a genuine discovery from their enterprise AI usage logs.)
- **Automating tasks they dislike** rather than tasks most valuable to the company — nearly every chief AI officer who has audited enterprise usage says the same thing.
- **Agents accessing proprietary data with no governance**, which makes organizations hesitant to give them access at all — which makes the agents less useful — which kills ROI.

The common thread: the interface between the human, the AI, and the organization's actual capabilities is undefined. There's no schema for what the AI can do. There's no validation of what it's doing. There's no record of what it did. The agent is a chatbot with a corporate credit card.

The fix is not to cut licenses. It's to define the interface.

---

## What a typed, governed AI interface looks like in practice

A concrete example from scientific computing: we built an MCP server for analyzing production Earth-system meshes on HPC clusters. It is not a chatbot. It is a typed tool catalog that an AI agent can call, with explicit schemas for every operation, structured return values, and a provenance record attached to every result.

The tool catalog covers a coherent workflow: discover data, inspect topology, compute area diagnostics, validate quality, subset by region, visualize, export. Every tool has an input schema the agent must satisfy. Every call returns structured data the agent can reason about. No tool is "send this question to a general-purpose model and see what it says."

The result: a scientist types "show me the mesh resolution near Florida." The agent converts that to a bounding box, runs the subset against a 1.1 GB mesh file on an HPC cluster, renders a wireframe plot on the cluster, and returns a PNG — in about ten seconds, from a laptop, with no SSH session and no handwritten code. The scientist gets a reproducible result with a full provenance record. The cluster does the computation on data that never leaves facility storage.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/regional-florida.png" alt="Florida coast mesh subset rendered on Improv via Globus Compute" />
  <figcaption>Florida coast subset of a high-resolution coastal mesh, rendered on Argonne Improv via Globus Compute and returned to a laptop in ~10 seconds. The agent extracted the bounding box from the phrase "Florida coast" — no coordinates entered by hand.</figcaption>
</figure>

That is AI delivering real value. The scientist who used to spend an hour on this problem now spends ten seconds. The result is documented. The computation ran where the data lives. The agent could not, even in principle, "check the weather" because the tool catalog contains no weather-checking tool.

This is not a scientific curiosity. It is a template. The same pattern — typed tool surface, schema validation, provenance record, compute-to-data — applies to any domain where the cost of getting it wrong is real.

**That's the point.** The interface defines what's possible. If you define the interface well, the agent is useful and auditable. If you don't define the interface, you get tokenmaxxing.

---

## The four ROI problems — and what actually fixes them

The enterprise AI reckoning keeps surfacing the same four blockers. Each one has a structural fix, not a budget cut.

### 1. Use cases: automating the wrong things

*Most people default to automating tasks they dislike rather than tasks most valuable to the company.*

The fix is not telling people to automate better things. The fix is giving them access only to tools that touch high-value workflows. In a well-designed MCP deployment, the tool catalog is the strategy document made executable. The tools cover the operations that take expert time and block real work. An employee cannot accidentally spend tokens on low-value work because low-value work is not in the catalog.

Designing the tool catalog is the hard, domain-specific work that AI deployment actually requires. Most enterprises skip it.

### 2. Costs: the weather query problem

*Employees were using AI models to check the weather.*

General-purpose chat is general-purpose. A bounded tool catalog is bounded. The cost profile of an MCP server with 20 typed tools is predictable because the tool surface is finite. Input schemas validate before computation runs. A query that doesn't match any tool schema is rejected before a single token is burned on the model.

This is not a novel idea. APIs have had rate limits and input validation for decades. The mistake was treating AI like something different — as an oracle rather than a system with inputs, outputs, and costs that need to be governed.

### 3. Humans as the bottleneck

*The thousand-flowers-bloom approach isn't leading to tangible returns.*

The bottleneck is not human capability. It's the absence of a feedback loop. When an agent has no schema contract, no validation, and no provenance, there's no signal for what's working. You can't improve what you can't observe.

In a governed MCP deployment, every tool call produces a structured provenance record: inputs, parameters, endpoint, library version, wall time. That record is machine-readable and human-auditable. Six months later, when a scientist wants to regenerate a figure or an analyst wants to replay a decision, the provenance record is the full specification. No reconstruction needed.

Provenance is not a nice-to-have for scientific reproducibility. It's the observability layer that makes an AI system improvable over time. Enterprises that want ROI from AI need to build this into every agent deployment, not treat outputs as ephemeral chat.

### 4. Data: the governance deadlock

*When enterprises are hesitant to give AI agents unfettered access to proprietary data, those agents become less effective.*

This is the right diagnosis with the wrong conclusion. Most enterprise AI rollbacks imply organizations need to loosen access controls. The actual fix is a better access model — one where the agent can use data without the data leaving a governed perimeter.

In the scientific computing system described above, production mesh files — some over 10 GB — live on facility filesystems and never move. Computation runs on the cluster where the data lives; only compact results (a JSON summary, a PNG) cross the network back to the agent. The agent gets what it needs without the data being exposed.

The enterprise equivalent is running agent computation in a governed compute environment rather than sending proprietary documents to an external API. The technical infrastructure for this — Globus Compute for HPC, VPCs for enterprise, trusted execution environments for regulated industries — exists. The issue is that most enterprises haven't built the access model; they've oscillated between "full access" (governance concern) and "no access" (ROI concern), missing the middle path.

**Trust is the real bottleneck.** Not trust in the AI model itself — trust in the system around it. An organization will hand an agent its proprietary data only when it can see exactly what the agent is allowed to do, verify that it did only that, and reproduce the result later. A typed tool catalog with provenance records is a trust architecture as much as it is a technical one. The schema defines the contract. The provenance record is the audit trail. Without both, you're asking the organization to trust a black box — and rational organizations don't do that with sensitive data.

---

## The piece that the AI ROI debate keeps missing

The "AI only works for coding" framing captures a real insight even if it overstates the case. What coding environments have that most other enterprise workflows lack is a **typed interface between the human, the AI, and the system being changed.**

Code has types. Function signatures. Test suites. Compilers that reject invalid outputs. Version control that records what changed and why. When an AI agent writes code, every output is validated by layers of automated feedback before it touches production.

The MCP protocol is an attempt to bring that same interface discipline to other domains. A typed tool catalog with explicit schemas, structured returns, and provenance records is the non-coding equivalent of a type system and test suite for AI behavior.

The five SEPs that merged in the past three months — multi-round-trip requests (SEP-2322), state handles (SEP-2567), OTel trace propagation (SEP-414), audit context (SEP-2704), stateless mode (SEP-2575) — are the protocol community making that interface discipline progressively more complete. You can [read the full breakdown here](https://rajeeja.github.io/blog/mcp-landscape-seps-community-2026/).

The enterprise AI ROI problem will not be solved by cutting licenses or by vague injunctions to "use AI for high-value work." It will be solved by organizations that build — or buy — the interface layer that makes AI behavior typed, governed, auditable, and connected to data where it lives. The measure of success is not seat count or token spend — it's intelligence per token: useful, verifiable work produced per dollar of compute.

The scientific computing example above is one proof point. Every result is auditable. Every tool call is schema-validated. The data never moves. Scientists trust it because the system earns that trust at every layer — not because they were told to trust an AI.

The correction the enterprise is going through is healthy. The question is whether it produces discipline or just retrenchment. The organizations that come out ahead will be the ones that use the correction to build the trust architecture they skipped the first time: typed interfaces, governed data access, and a provenance record that makes every AI action legible to the humans who have to stake their reputation on the results.

