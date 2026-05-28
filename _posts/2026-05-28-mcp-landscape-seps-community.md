---
title: "MCP in 2026: From Anthropic Side Project to Industry Infrastructure"
date: 2026-05-28
permalink: /blog/mcp-landscape-seps-community-2026/
categories:
  - blog
excerpt: "Eighteen months after launch, MCP has moved to the Linux Foundation, acquired a community governance process driven by SEPs and Discord working groups, and shipped five major spec changes that reshape what agents can do. Here is the full picture — timeline, governance, the five recently merged SEPs, and the active proposals that landed this week."
tags:
  - mcp
  - ai-agents
  - standards
  - hpc
  - scientific-computing
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">MCP Landscape · May 2026</p>
  <h1 class="article-title">MCP in 2026: From Anthropic Side Project to Industry Infrastructure</h1>
  <p class="article-dek">Eighteen months after launch, MCP has a foundation, a governance process, five major spec changes, and a community that ships working groups on Discord every week. Here is where it stands.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--violet">MCP</span>
  <span class="post-tag post-tag--blue">AI agents</span>
  <span class="post-tag post-tag--teal">standards</span>
  <span class="post-tag post-tag--amber">HPC</span>
  <span class="post-tag">scientific computing</span>
</div>

I have been building with MCP since early 2026 — an [MCP server for UXarray](https://rajeeja.github.io/blog/uxarray-mcp-improv-globus-compute/) that lets AI agents analyze production Earth-system meshes on HPC clusters without SSH or handwritten scripts. I presented that work this week at [SciFoundationModels 2026 (SciFM26)](https://scifm.ai) in Chicago. Spending the past few months deep inside the protocol's edges — authentication, long-running jobs, HPC dispatch, structured provenance — has given me a particular vantage point on how fast the ecosystem is moving and where it still has gaps.

This post is the landscape view I wish I had had when I started: the timeline from launch to today, what a SEP is and how they actually get merged, how the community governs itself on Discord, the five major SEPs that shipped in the last three months, and the active proposals that hit the GitHub discussions board this week.

---

## The agentic loop — and why MCP is the right substrate for it

Before the timeline, the frame. The pattern that makes MCP useful for serious scientific work is not just "tool calling." It is a closed reasoning loop:

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/mcp-agentic-loop.svg" alt="The MCP Agentic Loop: Ask · Retrieve · Analyze · Plan · Measure · Update · Verify" style="width:100%;max-width:900px;" />
  <figcaption>The seven-step agentic loop and its MCP substrate. Each step maps to one or more typed MCP tools; the protocol layer — governed by five recently merged SEPs — enforces schemas, carries state, propagates traces, and attaches audit context across the entire loop.</figcaption>
</figure>

**Ask** — the scientist states intent in natural language. The LLM converts it to a structured tool call. This is where hallucination risk is highest; the MCP schema contract at the next layer is what contains it.

**Retrieve** — `list_datasets`, `inspect_mesh`, `inspect_variable`. The agent discovers what data exists and where. On HPC, this step goes through Globus Compute; files never leave facility storage.

**Analyze** — `calculate_zonal_mean`, `calculate_area`, `validate_dataset`, `plot_variable`. The agent runs the diagnostic and gets structured results back, not raw text.

**Plan** — the agent reads `recommended_next_steps` from the tool response and decides what to do next. This is where SEP-2322 (multi round-trip) changes the game: the server can report partial results and continue rather than forcing the agent to poll.

**Measure** — `calculate_bias`, `calculate_rmse`, `calculate_pattern_correlation`. The agent evaluates quality against a reference.

**Update** — `create_session`, `register_dataset`, `export_to_netcdf`. State is persisted. SEP-2567 (state handles) means the server does not have to maintain session storage — the client holds the handle.

**Verify** — `validate_dataset`, scientist review. If the result does not pass, the loop iterates. SEP-414 (OTel) means the entire trace from Ask through HPC execution is observable as a single distributed span.

This loop is why MCP matters more for science than for simple chat plugins. The protocol now has the primitives to support it properly — which is what the SEP story below is about.

---

## The timeline: November 2024 to now

**November 2024 — public launch.** Anthropic publicly released the Model Context Protocol and its specification. At the time it was positioned as a way to give Claude access to local tools — filesystem, databases, APIs. The key design decision was already in place: the protocol is transport-agnostic (stdio, HTTP) and server-agnostic (any language, any runtime), and the tool schema is typed and validated. Those properties turned out to matter enormously once other runtimes and companies got involved.

**Early 2025 — first wave of community servers.** The weeks after launch produced a fast-growing catalog of community MCP servers: GitHub, Slack, Google Drive, Postgres, browser automation, and dozens of domain-specific integrations. The protocol worked well for read-heavy, short-latency, local tools. Long-running operations, authentication delegation, and stateful workflows were already visible pain points.

**March–April 2025 — Google confirms.** Sundar Pichai signaled Google's alignment publicly:

<figure class="article-figure">
  <img src="/images/blog/mcp-google-sundar.png" alt="Sundar Pichai confirms Google will support MCP, April 2025" style="max-width:520px;" />
  <figcaption>Sundar Pichai publicly committing Google to MCP on April 9, 2025 — a signal that the protocol would not remain an Anthropic-only standard.</figcaption>
</figure>

That public endorsement, combined with OpenAI adopting the protocol for its own agent tooling, effectively settled the question of whether MCP would be a single-vendor format. It would not.

**December 9, 2025 — Linux Foundation handoff.** Anthropic donated MCP to the Linux Foundation and simultaneously announced the Agentic AI Foundation — a directed fund with OpenAI, AWS, Blocks, Bloomberg, Cloudflare, Google, and Microsoft as co-founding members.

<figure class="article-figure">
  <img src="/images/blog/mcp-linux-foundation-announcement.png" alt="Mike Krieger announcement of MCP donation to Linux Foundation, December 2025" style="max-width:520px;" />
  <figcaption>Mike Krieger's announcement, December 9, 2025. MCP moved from internal Anthropic project to Linux Foundation stewardship in one year.</figcaption>
</figure>

The move to the Linux Foundation matters because it changes the governance model. Anthropic can no longer unilaterally change the spec. Changes now go through a community process — which brings us to SEPs.

**February–May 2026 — the SEP era begins.** Five major specification changes shipped in three months. Working groups formed on Discord. The pace of community proposals accelerated. At the time of this writing (SciFM26 week, May 28), there are dozens of active SEP discussions open on GitHub, with several landing specifically this week.

---

## What is a SEP?

A **SEP** is a **Specification Enhancement Proposal** — the mechanism by which the MCP community proposes, debates, and merges changes to the protocol. The process is modeled loosely on Python's PEPs and Rust's RFCs, but lives on GitHub Discussions rather than a separate repository.

A SEP typically:

1. **Opens as a GitHub Discussion** in the `modelcontextprotocol/modelcontextprotocol` repository, usually in the "SEPs" or "Ideas" category
2. **Collects community feedback** over days to weeks — the discussion thread is the primary venue for technical objections, alternative approaches, and implementation notes
3. **Gets picked up by a working group** if it touches a specific area (authentication, transport, observability, etc.)
4. **Is merged or closed** by the maintainers once there is rough consensus — "merged" meaning the spec document is updated and the change becomes normative

The SEP number is simply the GitHub Discussion number. There is no separate numbering scheme. SEP-2575 is GitHub Discussion #2575. SEP-414 is Discussion #414 from early in the repo's history. This is intentional — it keeps the proposal pipeline flat and searchable.

---

## How the community governs itself

The MCP community governance runs through three interlocking channels:

**GitHub Discussions** is where proposals live and die. Every SEP starts and ends here. The discussion thread is the authoritative record of why a change was made or rejected. Anyone with a GitHub account can participate.

**Discord** is where the working groups meet. There are several active interest groups, each with a recurring meeting cadence and meeting notes posted back to GitHub Discussions:

- **Inspector V2 Working Group** — tooling for testing and debugging MCP servers (meeting notes from May 20 and May 27 both posted this week)
- **Interceptors Working Group** — middleware and hook patterns for pre/post tool call processing (meeting notes from May 28)
- **Primitive Grouping Interest Group** — how tools, resources, and prompts should be organized and composed (notes from May 25)
- **Skills Over MCP Working Group** — higher-level skill abstractions on top of primitive tools (notes from May 22)
- **Enterprise Interest Group** — deployment patterns, auth, and policy for enterprise environments (pain points catalog posted May 21)

The Discord channel is also where informal alignment happens before a proposal is formally written up. If you are building something that will eventually need a SEP, the Discord is where you figure out if the idea has legs.

**GitHub Issues** handles bug reports, clarification requests, and tooling issues in the reference implementations. The reference TypeScript and Python SDKs are the de facto ground truth for spec ambiguities.

The governance is lightweight by design. There are no voting committees or formal ballots. Rough consensus — as judged by the maintainers — is sufficient to merge a SEP. This has allowed rapid iteration but will likely formalize as the protocol is used in higher-stakes enterprise and government contexts.

---

## The five major SEPs that shipped in the last three months

These are the five specification changes that matter most for anyone building non-trivial MCP servers, particularly for scientific or HPC contexts.

### SEP-414 — OpenTelemetry trace propagation (February 2026)

OTel trace context propagation was added to the MCP transport layer. Every tool call can now carry a W3C `traceparent` header, allowing distributed traces to span from the MCP client through the server into backend systems — including HPC schedulers, database queries, or downstream API calls.

For scientific computing, this is significant. A multi-step mesh analysis workflow that runs a PBS job on Improv, waits, retrieves results, and renders a plot now produces a single distributed trace from the initial agent tool call through to the final PNG. That trace is the provenance record. You do not need a custom logging scheme — the observability infrastructure is baked into the transport.

### SEP-2243 — HTTP transport standardization (April 2026)

The HTTP transport was clarified and tightened: endpoints are now expected to behave predictably behind reverse proxies, load balancers, and API gateways. Specific requirements around path handling, connection upgrades, and header forwarding were added to the spec.

In practice, this makes it feasible to deploy MCP servers in standard cloud infrastructure without custom proxy configuration. Before this SEP, HTTP MCP deployments that sat behind nginx or an AWS ALB would sometimes break in subtle ways depending on how the proxy handled SSE or connection keep-alives.

### SEP-2322 — Multi round-trip requests (May 2026)

This one changes what an agent can do. Before SEP-2322, a tool call was a single request/response exchange. The server could not send back an intermediate result and then continue processing. This forced workarounds: polling endpoints, callback registrations, or chunking long operations into separate tool calls.

SEP-2322 allows a tool invocation to involve multiple round trips — the server can send partial results, request clarification, or report progress before the final response. This is native support for agentic loops where the agent and server need to negotiate rather than just transact.

For long-running scientific operations — a mesh subset that takes 30 seconds, a model evaluation that runs a batch job — this is the right primitive. The agent does not have to poll a status endpoint; the server sends progress events naturally.

### SEP-2567 — Explicit state handles (May 2026)

Stateful sessions in MCP previously required the server to maintain server-side state identified by a session ID. This created scaling and deployment complexity: you needed sticky sessions, session storage, and session cleanup.

SEP-2567 introduces explicit state handles — opaque tokens that the client holds and passes back on subsequent calls. The server can reconstruct the necessary context from the handle without maintaining persistent server-side state. This makes it possible to build composable, sessionless tool workflows where each call is self-contained but can still reference prior computation through the handle.

For scientific sessions — "open this dataset, then run these diagnostics, then plot this variable" — state handles let the server be stateless while the workflow remains coherent from the client's perspective.

### SEP-2575 — Stateless mode (May 2026)

The companion to SEP-2567. Stateless mode is an explicit server-declared capability indicating that the server does not require session management. Clients that see this capability can simplify their connection management: no session negotiation, no keep-alive, no reconnection on session expiry.

This is important for serverless deployments and for tool composition across multiple MCP servers. If every server in a chain is stateless, the client can call them independently, mix results, and compose without coordinating session state across servers.

Together, SEP-2567 and SEP-2575 move MCP meaningfully toward a model where individual tool calls compose cleanly, even in workflows that span multiple servers or multiple invocations over time.

---

## What landed this week (May 22, 2026)

The SciFM26 week coincided with a notable cluster of new proposals on GitHub. These are not yet merged — they are at the discussion stage — but they give a clear picture of where the community's attention is.

**SEP-2774 — RFC 8628 OAuth Device Authorization Grant.** Adds support for the OAuth 2.0 device authorization flow, which allows MCP clients on constrained devices (or headless servers) to authenticate without a browser redirect. Relevant for HPC use cases where the MCP client may be running on a login node without a display.

**SEP-2767 — Cross-Ecosystem Trust Evidence Framework (CTEF).** A proposal for a behavioral trust scoring system for MCP servers — essentially a way for clients to know whether a server has been audited, what claims it makes about its behavior, and whether those claims can be verified. This is the enterprise governance story: before an agent is allowed to call a tool, there should be machine-readable evidence about what that tool does and who is responsible for it.

**SEP-2766 — Skills Over MCP.** The Skills working group posted meeting notes this week covering a design discussion on higher-level skill abstractions — named, composable workflows built from primitive MCP tools. The science angle here is direct: an "analyze mesh" skill is more useful to a domain scientist than a catalog of fifteen individual tools.

**SEP-2704 — Standard audit context for AI-initiated tool invocations.** Proposed on May 9 but actively discussed this week: a standard way to attach audit metadata (initiating model, session ID, user identity, policy context) to every MCP tool call. For regulated or shared HPC environments, this is a compliance requirement, not a nice-to-have.

**SEP-2797 — Cryptographic proof-of-possession for MCP clients.** Revives a previously closed proposal: clients should be able to prove they hold a key corresponding to a registered identity, preventing token theft and replay attacks. The discussion is active because the Agentic AI Foundation's enterprise members have flagged this as a blocker for production deployments.

---

## Why this matters for scientific computing

I have spent the past year building an MCP server for a specific scientific domain — unstructured Earth-system mesh analysis. That experience makes the SEP trajectory legible in a way that general AI agent discussions often are not.

The core observation is that scientific workflows stress the parts of MCP that are easy to defer in consumer-facing demos:

- **Authentication** — facility data is not public. Access is governed by project allocations and credential delegation. SEP-2774 and SEP-2797 are not abstract; they are blockers for production HPC deployments.
- **Long-running operations** — a mesh analysis job that PBS queues for 20 minutes and then runs for 5 minutes cannot look like a synchronous function call. SEP-2322 (multi round-trip) is the right primitive.
- **Provenance and auditability** — a plot produced by an AI agent needs the same provenance as a plot produced by a human. SEP-2704 (audit context) and SEP-414 (OTel) together make this tractable.
- **Composability at scale** — a scientist who wants to run the same analysis on 50 mesh files should not have to manage session state across 50 server interactions. SEP-2567 and SEP-2575 (state handles and stateless mode) reduce that friction substantially.

The UXarray MCP server I have been building anticipated several of these with custom mechanisms. The structured provenance record we attach to every tool call is essentially what SEP-2704 is trying to standardize. The state handles we use for session-aware HPC workflows are a precursor to SEP-2567.

As these SEPs merge, the custom scaffolding gets replaced by protocol primitives. That is exactly how a standards process should work.

---

## Looking ahead

The MCP spec is moving fast in the right directions. The five SEPs that shipped in three months address real gaps — not theoretical ones. The community governance is functional: working groups meet, post notes, and proposals get discussed seriously.

The remaining gaps from a scientific computing perspective are:

- **Artifact handling** — plots, derived datasets, and structured results need first-class metadata and lifecycle management in the spec, not just conventions. There is an active SEP discussion thread on this (referenced in active discussions).
- **Pre-execution policy hooks** — before an agent launches an HPC job or reads a restricted path, there should be a protocol-level checkpoint. The Interceptors working group is the right venue for this.
- **Long-running task management** — SEP-2322 adds multi round-trips, but a full task management model (cancel, retry, resume, progress events with structured payloads) is still largely left to implementers.

I am tracking all of these through the MCP Discord and GitHub Discussions. If you are building scientific MCP servers and want to compare notes, find me at the UXarray GitHub or reach out directly.

---

*The UXarray MCP server is open source at [github.com/UXARRAY/uxarray-mcp-server](https://github.com/UXARRAY/uxarray-mcp-server). The companion poster was presented at SciFM26, May 27–29, 2026, Chicago. Supported by NSF EarthCube Grant No. 2126458 and the U.S. DOE Office of Science SEATS project.*
