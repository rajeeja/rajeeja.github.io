---
title: "UXarray MCP on Argonne Improv: A Production Earth-System Mesh Campaign"
date: 2026-04-04
permalink: /blog/uxarray-mcp-improv-globus-compute/
categories:
  - blog
excerpt: "We present a Model Context Protocol server for UXarray that eliminates three concrete pain points in Earth-system mesh analysis: data gravity, reproducibility, and terminal-bound workflows. In a PBS-backed campaign over seven production meshes on Argonne Improv, and in an agentic regional explorer that converts plain-English descriptions into coastal mesh visualizations from a 1.1 GB facility file in ~10 seconds, from a laptop, without SSH."
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

<div class="article-hero">
  <p class="eyebrow">Research note · April 2026 · SciFM 2026 companion paper</p>
  <h1 class="article-title">UXarray MCP on Argonne Improv</h1>
  <p class="article-dek">A Model Context Protocol server for unstructured Earth-system meshes: production campaign results, agentic regional exploration, and provenance as scientific infrastructure.</p>
</div>

Analyzing a production Earth-system mesh today requires an SSH session on an HPC cluster, hand-written analysis scripts, and manual bookkeeping of what ran on which file. Getting a topology summary from a 10 GB coastal ocean grid means: (i) logging in; (ii) activating a conda environment; (iii) finding or rewriting analysis scripts; (iv) waiting for a batch job; and (v) downloading or re-deriving results. When a colleague asks "what is the resolution near Florida?" the answer is a project, not a question.

We built an MCP server for UXarray that addresses all three pain points. The server exposes mesh inspection, area diagnostics, bounding-box subsetting, and plotting as typed, provenance-producing tools. A Globus Compute backend routes computation to leadership-class hardware so multi-gigabyte mesh files never leave facility storage.

This post covers the companion paper we submitted to SciFM 2026: a validated PBS-backed campaign over seven production Earth-system meshes (28K to 24.9M faces, 0.06–10.82 GB) on Argonne Improv, and an agentic regional mesh explorer that converts natural-language region descriptions ("Florida coast", "San Francisco Bay coast") into precise mesh visualizations from a 1.12 GB facility file --- in 10 seconds, from a laptop, with no SSH session and no handwritten code.

## The server as a scientific runtime

The UXarray MCP server grew from a handful of inspection tools into a stateful scientific runtime. The tool surface now covers a coherent scientific session: discovery, inspection, analysis, visualization, persistence, export, and remote escalation.

```python
# tool registration excerpt from server.py
mcp.tool()(list_datasets)
mcp.tool()(get_capabilities)
mcp.tool()(inspect_mesh)
mcp.tool()(inspect_variable)
mcp.tool()(calculate_area)
mcp.tool()(calculate_zonal_mean)
mcp.tool()(validate_dataset)

mcp.tool()(plot_mesh)
mcp.tool()(plot_variable)
mcp.tool()(plot_zonal_mean)

mcp.tool()(subset_bbox)
mcp.tool()(subset_polygon)
mcp.tool()(compare_fields)
mcp.tool()(remap_variable)

mcp.tool()(create_session)
mcp.tool()(register_dataset)
mcp.tool()(run_workflow)
mcp.tool()(resume_workflow)
```

The key design property: HPC workers need only UXarray and its scientific dependencies, not the MCP server itself. Functions run on Improv in a plain virtual environment; the server attaches provenance on return. Raw mesh files **never leave facility storage** --- only a compact JSON summary or a PNG crosses the network.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-runtime-overview.svg" alt="UXarray MCP runtime overview diagram." />
  <figcaption>The server supports a complete scientific session: discovery, capability filtering, analysis, visualization, persistent sessions, and local-or-Improv execution routing.</figcaption>
</figure>

## Experiments on Argonne Improv

All experiments run against production Earth-system meshes staged on Improv's GPFS filesystem at `/gpfs/fs1/home/jain/uxarray/mcp-demo-big-meshes`, accessed through a PBS-backed Globus Compute endpoint on `ilogin1.lcrc.anl.gov`. The scientist never opens an SSH session or downloads a file.

### Mesh families

The campaign covers the complete MPAS-Ocean production resolution hierarchy, one MPAS-Atmosphere regional mesh, and two interoperability formats (SCRIP, ESMF), plus three deliberate failure cases.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-mesh-context.png" alt="MPAS-Ocean resolution hierarchy context panel." />
  <figcaption>The MPAS-O resolution hierarchy from oQU120 (28K faces, 120 km) through oRRS18to6 (3.7M faces, 6–18 km). The four ocean meshes span four orders of magnitude in face count while maintaining consistent sphere coverage (~0.707, the ocean fraction of Earth's surface).</figcaption>
</figure>

| Label | Format | Size | Scientific role |
|---|---|---|---|
| **oQU120** | MPAS-O | 0.10 GB | Quasi-uniform 120 km global ocean baseline. Standard low-resolution reference in E3SM ocean campaigns. |
| **oEC60to30** | MPAS-O | 0.62 GB | Variable-resolution 60–30 km mesh for eddy-closure studies. Refines eddy-active open-ocean regions to 30 km. |
| **WC14to60** | MPAS-O | 1.12 GB | Western-Atlantic/coastal refinement mesh, 14–60 km. Designed for storm surge, coastal sea-level, and river-plume studies. |
| **oRRS18to6** | MPAS-O | 10.82 GB | Fine-scale 18–6 km coastal-refined mesh; the largest MPAS-O file in the campaign. |
| **CONUS-MPAS-A** | MPAS-A | 5.61 GB | Regional MPAS atmosphere mesh over the continental United States (637K faces). |
| **PAMIP-ne30x8** | SCRIP | 0.06 GB | Global atmosphere grid from the Polar Amplification Model Intercomparison Project. |
| **ESMF-mesh** | ESMF | 1.03 GB | ESMF-format mesh with 24.9M faces --- the largest by face count. |
| *STOFS-2D-glo* | --- | 11.43 GB | *Deliberate failure: CF violation on dim nvel.* |
| *ne512np4-latlon* | --- | 0.54 GB | *Deliberate failure: unrecognized latlon-hybrid layout.* |
| *E3SM-CAM-h1 + ne256np4* | --- | --- | *Deliberate failure: grid/data topology mismatch.* |

### Experiment 1: Data estate discovery

**Question:** Can the agent discover and classify files staged on Improv, from a laptop, without SSH?

The agent submits `probe_path_access` for each file in the manifest. All nine files are readable through the endpoint. Analysis-layer failures (CF violation, format mismatch, topology error) are detected only at analysis time, not at the I/O layer --- which means the triage machinery has something real to work with.

| Label | Size (GB) | Readable | Notes |
|---|---|---|---|
| oQU120 | 0.10 | yes | MPAS topology intact |
| oEC60to30 | 0.62 | yes | variable-resolution faces |
| WC14to60 | 1.12 | yes | coastal refinement |
| oRRS18to6 | 10.82 | yes | largest; requires PBS-backed endpoint |
| PAMIP-ne30x8 | 0.06 | yes | SCRIP format, global atmosphere |
| STOFS-2D-glo | 12.28 | yes | readable but CF collision on dim `nvel` |
| ne512np4-latlon | 0.57 | yes | readable but latlon-hybrid layout |
| E3SM-CAM-h1 | 0.58 | yes | ncol=325,190; mismatched |
| ne256np4-grid | 0.40 | yes | grid_size=3,538,946; wrong grid |

### Experiment 2: Multi-mesh topology diagnostics

**Question:** Does UXarray expose scientifically meaningful topology diagnostics across the full resolution hierarchy and across formats, executed remotely without moving files?

For each of the seven production meshes, the agent calls `inspect_mesh` and `calculate_area` through the MCP server.

| Label | Size (GB) | Faces | Mean area (sr) | Coverage | Inspect (s) | Area (s) |
|---|---|---|---|---|---|---|
| oQU120 | 0.10 | 28,571 | 3.07×10⁻⁴ | 0.699 | 20.4 | 20.5 |
| oEC60to30 | 0.62 | 235,160 | 3.77×10⁻⁵ | 0.706 | 20.0 | 20.0 |
| WC14to60 | 1.12 | 407,420 | 2.18×10⁻⁵ | 0.707 | 20.0 | 20.0 |
| oRRS18to6 | 10.82 | 3,693,225 | 2.41×10⁻⁶ | 0.707 | 20.0 | 20.0 |
| CONUS-MPAS-A | 5.61 | 637,604 | 7.39×10⁻⁷ | 0.037 | 20.0 | 20.0 |
| PAMIP-ne30x8 | 0.06 | 325,190 | 3.87×10⁻⁵ | 1.001 | 20.0 | 20.0 |
| ESMF-mesh | 1.03 | 24,875,336 | 3.59×10⁻⁷ | 0.711 | 120.0 | 60.0 |

**Resolution hierarchy.** The four MPAS-O ocean meshes form a coherent hierarchy across four orders of magnitude in face count: oQU120 (28K faces, 120 km) through oRRS18to6 (3.7M faces, 6–18 km), with mean face area decreasing by a factor of ~128. Coverage holds within 0.001 of 0.707 across all four ocean meshes, confirming topological consistency of UXarray's area integration across the full resolution hierarchy.

**Cross-format.** CONUS-MPAS-A returns coverage ~0.037, matching the fraction of Earth's surface occupied by the continental United States. PAMIP-ne30x8 returns ~1.001 (global atmosphere). All three formats --- MPAS, SCRIP, ESMF --- produce scientifically interpretable geometry with the same tool call.

**Timing.** For six of the seven meshes (0.06–10.82 GB, 28K to 3.7M faces), both `inspect_mesh` and `calculate_area` cost ~20 s each --- the PBS compute-node dispatch floor. UXarray computation is sub-second at these scales; the observable cost is Globus scheduling overhead, not science. For ESMF-mesh (24.9M faces), computation dominates: 120 s for inspection and 60 s for area. The crossover from scheduling-dominated to compute-dominated cost lies between 3.7M and 24.9M faces for this PBS configuration.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-convergence-panel.png" alt="Convergence panel showing MPAS-O resolution hierarchy diagnostics." />
  <figcaption>Resolution hierarchy diagnostics from the local convergence-aware agent demo: mean face area, sphere coverage, and timing across the MPAS-O hierarchy. Coverage ~0.699–0.707 across all four ocean meshes is physically expected (the ocean fraction of Earth's surface).</figcaption>
</figure>

### Experiment 3: Structured failure recovery

**Question:** Can the agent classify realistic failure modes in ways that reduce wasted facility cycles by surfacing actionable error records before reruns?

Rather than surfacing a raw Python traceback, the server applies a rule-based classifier to each exception, producing a structured triage record with an error class, a severity tier (SKIP, PATCH, QUARANTINE, BLOCK), an optional automatic remediation, and a suggested human action.

| Case | Operation | Error class | Severity | Suggested action |
|---|---|---|---|---|
| **STOFS-2D-glo** | `inspect_mesh` | `cf-violation` | PATCH | Rename scalar `nvel` to avoid the dimension collision, then retry. |
| **ne512np4-latlon** | `inspect_mesh` | `unrecognized-format` | QUARANTINE | Confirm grid vs. data; locate matching grid by `ncol`. |
| **E3SM-CAM-h1 + ne256np4** | `validate_dataset` | `topology-mismatch` | QUARANTINE | Locate the matching grid (ncol=325,190 does not match grid_n_face=3,538,946). |

All three failures are representative of real workflows. CF-convention violations are common in operational forecast output. Topology mismatches occur whenever a scientist pairs a data file with a grid from a different resolution or campaign. Unrecognized formats surface when model output changes conventions between versions. In each case the triage record gives the scientist a precise next action, not a stack trace.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-failure-recovery.png" alt="Failure recovery panel showing triage classification results." />
  <figcaption>The failure recovery panel from the convergence-aware agent demo. Three distinct UXarray failure classes, each triaged to a one-line classification and suggested action: cf-violation (patchable), unrecognized-format (quarantine), topology-mismatch (quarantine before rerun).</figcaption>
</figure>

### Experiment 4: Artifact economics

**Question:** What does the scientist pay in time, and what do they receive?

| Mesh | File size | Inspect (s) | Area (s) | Artifact | Data ratio |
|---|---|---|---|---|---|
| oQU120 | 0.10 GB | 20.4 | 20.5 | <1 KB JSON | ~10⁵:1 |
| WC14to60 | 1.12 GB | 20.0 | 20.0 | <1 KB JSON + 40 KB PNG | ~10⁶:1 |
| oRRS18to6 | 10.82 GB | 20.0 | 20.0 | <1 KB JSON | ~10⁷:1 |

The 20 s overhead is real and should not be minimized. What it buys is: no data movement, no SSH, no code authorship, no manual bookkeeping, and a machine-readable provenance record. On a 10 Mbps VPN connection, downloading WC14to60 takes ~15 minutes; the MCP endpoint call returns targeted scientific content in 20 s. For oRRS18to6 at 10.82 GB, download is not a realistic option; the endpoint is the most practical path available in this deployment.

## Agentic regional mesh explorer

**Setup.** A two-stage agentic pipeline: (1) Claude API converts a free-text region description into a lat/lon bounding box; (2) a self-contained Globus Compute function is submitted directly to the Improv endpoint, subsets the WC14to60 mesh, renders a wireframe PNG on the worker, and returns mesh statistics plus the image. The scientist provides no coordinates, no SSH credentials, and no analysis code.

**The pipeline in one sentence.** The user types "Florida coast". Claude API returns `{"lon_bounds": [-88.0, -79.0], "lat_bounds": [24.0, 31.5]}`. The bounding box is forwarded to Improv via Globus Compute. Three thousand hexagonal mesh cells are subsetted from the 407K-face WC14to60 file. A wireframe PNG is rendered on the worker. The image arrives on the laptop in 10 s. No data left Improv GPFS.

### Results

| Region (natural language) | LLM bounding box | Faces | Res. ratio | Time (s) |
|---|---|---|---|---|
| Continental United States | lon[−125, −66], lat[24, 49.5] | 23,331 | 4.36× | 52.6 |
| Florida coast | lon[−88, −79], lat[24, 31.5] | 3,081 | 5.24× | 10.0 |
| New York City coast | lon[−75, −72.5], lat[39.5, 42] | 104 | 5.18× | 10.0 |
| San Francisco Bay coast | lon[−123.5, −121], lat[36.5, 38.7] | 104 | 5.20× | 10.0 |

The first call (Continental US, 52.6 s) reflects PBS cold-start overhead; the three subsequent calls on the warm worker each cost ~10 s. The resolution ratio ~5.2× across all three coastal sites (Florida, NYC, SFO) confirms that WC14to60 achieves its design goal: cells in these regions are ~5× smaller than the global mean, corresponding to ~14 km vs. the ~60 km open-ocean average. The consistent ratio across three independently queried regions --- extracted by the LLM from natural language with no scientist-provided coordinates --- is consistent with the mesh's coastal-refinement design goal.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/regional-conus.png" alt="WC14to60 mesh subset: Continental United States." />
  <figcaption>Continental United States subset of WC14to60: 23,331 faces, resolution ratio 4.36×. First call in the cold-start sequence; PBS dispatch took 52.6 s. Visible coastal refinement concentrated along the East Coast and Gulf of Mexico.</figcaption>
</figure>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 2rem 0;">
  <figure class="article-figure" style="margin: 0;">
    <img src="/images/blog/regional-florida.png" alt="WC14to60 mesh subset: Florida coast." style="width: 100%;" />
    <figcaption><strong>Florida coast.</strong> 3,081 faces · res. ratio 5.24× · 10.0 s. Bounding box extracted by Claude API from "Florida coast".</figcaption>
  </figure>
  <figure class="article-figure" style="margin: 0;">
    <img src="/images/blog/regional-nyc.png" alt="WC14to60 mesh subset: New York City coast." style="width: 100%;" />
    <figcaption><strong>New York City coast.</strong> 104 faces · res. ratio 5.18× · 10.0 s. LLM-derived bbox; warm worker call.</figcaption>
  </figure>
  <figure class="article-figure" style="margin: 0;">
    <img src="/images/blog/regional-sfbay.png" alt="WC14to60 mesh subset: San Francisco Bay coast." style="width: 100%;" />
    <figcaption><strong>San Francisco Bay coast.</strong> 104 faces · res. ratio 5.20× · 10.0 s. Sub-second UXarray computation; cost is dispatch floor.</figcaption>
  </figure>
  <figure class="article-figure" style="margin: 0;">
    <img src="/images/blog/uxarray-mcp-convergence-panel.png" alt="MPAS-O convergence diagnostics panel." style="width: 100%;" />
    <figcaption><strong>MPAS-O hierarchy convergence.</strong> Consistent coverage and area scaling across four orders of magnitude in face count.</figcaption>
  </figure>
</div>

The pipeline combines three capabilities that each exist independently (LLM API, typed tool calls, Globus Compute) but have not previously been composed in this way for unstructured mesh analysis. A scientist at a laptop can describe a geographic region in plain English and receive a topologically correct mesh visualization from a multi-gigabyte file on a leadership-class cluster --- without an SSH session, without code, in the time it takes to make coffee.

A 12-region survey would cost approximately 52 + 11 × 10 = 162 s if the warm-worker pattern holds, dominated by the single cold start.

## Provenance as scientific infrastructure

Every call to `remote_subset_bbox_plot` returns a structured record containing all information required to reproduce or modify the result:

```json
{
  "tool": "remote_subset_bbox_plot",
  "timestamp": "2026-05-04T19:29:58Z",
  "grid_path": "/gpfs/.../WC14to60E2r5.230313.nc",
  "region_name_input": "Florida coast",
  "bbox_from_llm": {
    "lon_bounds": [-88.0, -79.0],
    "lat_bounds": [24.0, 31.5]
  },
  "plot_params": {
    "edgecolor": "steelblue",
    "facecolor": "lightcyan",
    "linewidth": 0.3,
    "width_px": 900,
    "height_px": 500,
    "dpi": 100
  },
  "n_face_total": 407420,
  "n_face_subset": 3081,
  "fraction_of_mesh": 0.0076,
  "resolution_ratio": 5.24,
  "wall_time_s": 10.01,
  "endpoint_id": "caf37dc0-759f-4e48-9e0a-04f2cdbd23d2",
  "uxarray_version": "2024.12.0"
}
```

This record is a complete specification of the computation: every field corresponds to a parameter of the analysis, and every field can be changed to produce a modified result. Six months after the initial analysis, the scientist loads the JSON record and resubmits with the same parameters. The scientist wants to change the colormap for a publication? Change `"edgecolor": "steelblue"` to `"edgecolor": "darkred"` and resubmit --- the analysis does not re-run, only the rendering changes.

Without the MCP layer, a scientist analyzing the same data would: (1) SSH into Improv; (2) find or reconstruct the Python analysis script; (3) remember or re-derive the bounding box coordinates; (4) hardcode plot parameters in the script; (5) submit the job; (6) download the output. The plot parameters live in the script, not in any durable record. Six months later, the scientist cannot determine what parameters produced a specific figure without git-blaming every commit that touched the script. MCP turns this implicit knowledge into a first-class result field.

## The three-tier model

The experiments in this paper instantiate a specific three-tier composition that we think is a general pattern for tiered automation of scientific workflows.

**Tier 1 --- Natural Language (LLM).** The agent converts unstructured human intent into structured tool calls. Its strength is understanding; its weakness is hallucination and lack of execution authority. In our system, Claude API extracts bounding boxes from prose --- a task where hallucination is immediately detectable and where no computation occurs.

**Tier 2 --- Typed Tool Surface (MCP Server).** The MCP server is the trust boundary. It validates every tool call against a Pydantic schema, rejects ill-formed inputs before they reach any compute resource, attaches provenance, and presents a stable interface that does not change when the backend changes. This tier substantially reduces the hallucinated-API failure mode: the agent cannot call a function absent from the catalog, and schema-invalid arguments are rejected before any computation occurs.

**Tier 3 --- Execution Backend (HPC / Globus Compute).** The backend runs the actual computation on data-local hardware --- a PBS-backed Globus Compute endpoint on Improv with direct access to GPFS. The backend has no knowledge of MCP, no LLM dependency, and no network access to the client: it receives a serialized Python callable, executes it, and returns a result. Raw mesh files never leave facility storage.

This decomposition has a clean information-theoretic reading: each tier compresses its input. Tier 1 compresses natural language to a structured call; Tier 2 validates and routes; Tier 3 compresses a multi-gigabyte file to a kilobyte artifact. The ~20 s overhead is the cost of Tier 3's scheduling barrier --- not of the MCP or LLM tiers, which together add less than 2 s.

Zhou et al. benchmark six contemporary LLMs on E3SM land-surface hydrology diagnostics and find that unconstrained code generation succeeds in only ~5% of attempts, and that self-debugging *increases* the silent-failure rate from ~16% to ~40%. Their module-grounded ESFlow framework --- which restricts the LLM to composing validated tools executed by a deterministic engine --- achieves >80% success. This is independent corroboration of the typed-tool principle: constraining the LLM to compose from a vetted catalog, whether via YAML or MCP schema, markedly improves reliability over free-form code generation.

## What this demonstrates

The UXarray MCP server is best understood as an early scientific runtime for AI clients, not as a thin wrapper around a numerical library.

In the PBS-backed campaign on Argonne Improv, the server discovers and classifies all files on facility GPFS without SSH, completes topology diagnostics for every mesh, triages three realistic failure modes into actionable records, and returns compact artifacts from files up to 10.82 GB --- all in ~20 s per call, dominated by Globus scheduling overhead rather than UXarray computation across four orders of magnitude in mesh size.

In the agentic extension, Claude API converts natural-language region descriptions into lat/lon bounding boxes, and the same MCP server returns precise coastal mesh visualizations from a 1.1 GB facility file in ~10 s per region with no code authorship and no data movement.

The result is a practical template for adding agent control surfaces to unstructured-mesh or simulation-output libraries without re-architecting the underlying scientific code. The hard part is not adding a hundred loosely connected functions. The hard part is making discovery, applicability, state, provenance, and remote execution line up in a way that scientists can actually trust. That is what this server is starting to do.

**Reproducibility.** The MCP server source, tool definitions, and Globus Compute functions are available at [github.com/UXARRAY/uxarray-mcp-server](https://github.com/UXARRAY/uxarray-mcp-server). Campaign scripts and raw outputs (PNGs, provenance JSON) are in the `outputs/` directory of the repository.

*Supported by the U.S. National Science Foundation under Grant No. 2126458 (EarthCube) and the U.S. Department of Energy Office of Science SEATS project.*
