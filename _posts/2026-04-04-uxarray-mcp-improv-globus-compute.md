---
title: "UXarray MCP: Agentic Analysis of Earth-System Meshes at Facility Scale"
date: 2026-04-04
permalink: /blog/uxarray-mcp-improv-globus-compute/
categories:
  - blog
excerpt: "A teaser for our SciFM 2026 companion paper: an MCP server for UXarray that lets AI agents inspect, visualize, and reason about production Earth-system meshes on HPC clusters — from a laptop, without SSH, without writing code."
tags:
  - hpc
  - climate
  - uxarray
  - globus-compute
  - mcp
  - ai-agents
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">Teaser &middot; SciFM 2026 companion paper</p>
  <h1 class="article-title">UXarray MCP on Argonne Improv</h1>
  <p class="article-dek">Agentic analysis of production Earth-system meshes at facility scale — typed tools, Globus Compute, provenance, and a natural-language regional explorer. Full results in our SciFM 2026 paper.</p>
</div>

Getting a topology summary from a production Earth-system mesh today requires an SSH session, a conda environment, hand-written analysis scripts, a batch job, and a download step. When a colleague asks "what is the resolution near Florida?" the answer is a project, not a question.

We have been building toward a better answer: an MCP server for [UXarray](https://uxarray.readthedocs.io/) that exposes mesh inspection, area diagnostics, subsetting, and plotting as typed, provenance-producing tools. A Globus Compute backend routes computation to leadership-class hardware so multi-gigabyte files never leave facility storage.

This is a teaser. The full campaign results are in our companion paper submitted to SciFM 2026. We will link it here when it is publicly available.

## The problem

Production Earth-system meshes are large, opaque, and live on HPC clusters. A coastal ocean mesh can weigh ten gigabytes or more. Getting scientifically meaningful information from it — face counts, area distributions, resolution near a coastline — normally requires direct cluster access and the right scripts in the right environment.

That friction adds up. It blocks scientists from exploring datasets quickly. It produces results with no durable record of how they were generated. And it makes it hard for an AI agent to act on scientific data in a controlled, reproducible way.

The Model Context Protocol (MCP) addresses the interface problem: it gives an agent a typed tool catalog with explicit input schemas, structured return values, and a clear server-side execution boundary. But MCP by itself does not make scientific software agent-ready. The contribution of this work is an MCP server that makes UXarray usable as a controlled, provenance-producing action surface for agents working with unstructured Earth-system meshes at facility scale.

## What the server does

The server exposes mesh analysis as a set of typed tools that any MCP-compatible client — including Claude — can call directly. The tool surface covers a coherent scientific workflow:

- **Discovery** — scan a directory tree on a local or remote filesystem, classify files as grid or data, and return suggested next tool calls
- **Inspection** — load a mesh file (MPAS, UGRID, SCRIP, ESMF, HEALPix) and return topology metadata: face count, node count, edge count, mesh format
- **Area diagnostics** — compute face area statistics with automatic unit detection (steradians vs. m²)
- **Validation** — check for NaN, Inf, fill values, and topology mismatches before any analysis runs
- **Subsetting** — select faces by bounding box or polygon; extract cross-sections
- **Visualization** — render inline PNG plots of mesh wireframes, face-centered variables, and zonal means
- **Session and workflow state** — register datasets by handle, run multi-step workflows, resume from saved state, export results

Every tool call produces a structured provenance record containing the inputs, parameters, and execution context. That record is a complete specification: any result can be reproduced or modified months later without reconstructing what was done.

The HPC path is handled by Globus Compute. The MCP tool interface does not change when the backend moves from a laptop to an HPC cluster. Raw mesh files never transit the network — only compact JSON summaries or PNG images cross back to the client.

## The campaign

We ran a PBS-backed validation campaign on Argonne Improv, using production Earth-system meshes staged on the facility GPFS filesystem. The meshes span a wide range of formats, resolutions, and file sizes — from a compact global atmosphere grid to a large coastal-refined ocean mesh.

The campaign tested four things:

1. **Data estate discovery** — can the agent find and classify files on facility storage without SSH?
2. **Multi-mesh topology diagnostics** — does UXarray produce scientifically consistent geometry across mesh families and formats?
3. **Structured failure recovery** — can the server classify realistic failure modes (CF violations, format mismatches, topology errors) into actionable triage records rather than raw tracebacks?
4. **Artifact economics** — what does the scientist receive in exchange for the overhead of a remote call?

Full results — tables, timing, coverage values, and discussion — are in the companion paper.

## The regional mesh explorer

The most visually direct piece of the work is an agentic pipeline we built on top of the server. A scientist types a region name in plain English. The Claude API converts it to a lat/lon bounding box. That bounding box is forwarded to Improv via Globus Compute, which subsets the mesh, renders a wireframe plot on the worker, and returns the image to the laptop.

No coordinates entered by hand. No SSH. No code written.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/regional-florida.png" alt="WC14to60 mesh subset: Florida coast, rendered on Improv." />
  <figcaption>Florida coast subset of a Western-Atlantic coastal refinement mesh, rendered on an Argonne Improv worker via Globus Compute and returned to the laptop as a PNG. The agent extracted this bounding box from the phrase "Florida coast" with no scientist-provided coordinates.</figcaption>
</figure>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.2rem;margin:1.5rem 0;">
  <figure class="article-figure" style="margin:0;">
    <img src="/images/blog/regional-conus.png" alt="Continental US mesh subset." style="width:100%;" />
    <figcaption><strong>Continental United States.</strong> Full CONUS bounding box. Coastal refinement visible along the East Coast and Gulf of Mexico.</figcaption>
  </figure>
  <figure class="article-figure" style="margin:0;">
    <img src="/images/blog/regional-nyc.png" alt="New York City coast mesh subset." style="width:100%;" />
    <figcaption><strong>New York City coast.</strong> Tight coastal region. LLM-extracted bounding box; warm Globus Compute worker.</figcaption>
  </figure>
  <figure class="article-figure" style="margin:0;">
    <img src="/images/blog/regional-sfbay.png" alt="San Francisco Bay coast mesh subset." style="width:100%;" />
    <figcaption><strong>San Francisco Bay coast.</strong> West-coast fine cells. Same pipeline, different region description.</figcaption>
  </figure>
</div>

The resolution ratio between the subsetted region and the full-mesh mean tells you whether the mesh actually achieves its stated coastal refinement goal — confirmed numerically in the paper.

## Provenance as infrastructure

Every tool call in this server returns a structured provenance record alongside the result. That record captures the grid path, variable name, bounding box, plot parameters, endpoint ID, library version, and wall time — everything needed to reproduce or modify the result without reconstruction.

This matters most six months later, when a scientist wants to regenerate a figure for a revised manuscript, compare results across mesh versions, or zoom in on a different subregion. With MCP provenance, that is a matter of editing one JSON field and resubmitting. Without it, it is a matter of finding the script, guessing the parameters, and hoping the environment still matches.

## The three-tier model

The system composes three layers:

**Natural language (LLM)** converts unstructured intent into structured tool calls — bounding boxes from region names, variable selections from prose descriptions. This is the tier where hallucination risk is highest, and where the schema contract of the MCP layer provides the most protection.

**Typed tool surface (MCP server)** is the trust boundary. It validates every tool call against a schema, rejects ill-formed inputs before they reach any compute resource, routes to local or HPC execution, and attaches provenance. The agent cannot call a function absent from the catalog.

**Execution backend (HPC / Globus Compute)** runs actual computation on data-local hardware. Raw mesh files never leave facility storage. Only compact artifacts cross the network. The backend has no knowledge of MCP or the LLM; it receives a serialized Python callable and returns a result.

## What is coming

Full campaign results, timing tables, failure triage details, and discussion of the artifact economics and the path toward fully autonomous scientific campaigns are in our companion paper submitted to SciFM 2026. We will post the link here when it is publicly available.

*Supported by the U.S. National Science Foundation under Grant No. 2126458 (EarthCube) and the U.S. Department of Energy Office of Science SEATS project.*
