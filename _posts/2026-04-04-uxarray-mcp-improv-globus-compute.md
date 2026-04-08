---
title: "UXarray MCP as a Scientific Runtime: Discovery, Workflows, Plotting, and Improv"
date: 2026-04-04
permalink: /blog/uxarray-mcp-improv-globus-compute/
categories:
  - blog
excerpt: "A technical note on how the UXarray MCP server grew from a mesh-aware tool surface into a stateful scientific runtime with plotting, persisted workflows, exports, and a more disciplined Improv execution path."
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
  <p class="eyebrow">Research note · April 4, 2026</p>
  <h1 class="article-title">UXarray MCP as a Scientific Runtime</h1>
  <p class="article-dek">A technical note on how the UXarray MCP server evolved beyond basic inspection tools into a more complete scientific runtime: discovery, plotting, persisted workflows, exports, and remote execution on Improv through Globus Compute.</p>
</div>

The earlier version of this article described the UXarray MCP server as a promising bridge between mesh-aware scientific Python and AI clients. That was true, but it is no longer the most useful description. The repository has moved beyond a small set of inspection tools. It now looks much more like a scientific runtime with a natural-language interface.

That shift matters. A serious scientific MCP server should not stop at "tool wrappers for chat." It should help the user find datasets, understand which operations are valid, generate visual evidence, persist intermediate state, resume workflows, export results, and decide when remote infrastructure is healthy enough to trust. The current UXarray MCP server does all of those things in some form.

So this rewrite focuses on the server as it exists now, not as it existed a few weeks ago.

## What changed conceptually

The current server has grown along three axes at once:

- breadth of scientific operations;
- persistence and workflow state;
- operational discipline for HPC execution.

The registration surface in `server.py` makes that visible immediately:

```python
mcp.tool()(get_capabilities)
mcp.tool()(run_scientific_agent)
mcp.tool()(run_workflow)
mcp.tool()(resume_workflow)
mcp.tool()(create_session)
mcp.tool()(register_dataset)

mcp.tool()(inspect_mesh)
mcp.tool()(inspect_variable)
mcp.tool()(calculate_area)
mcp.tool()(calculate_zonal_mean)
mcp.tool()(validate_dataset)
mcp.tool()(list_datasets)

mcp.tool()(plot_mesh)
mcp.tool()(plot_variable)
mcp.tool()(plot_zonal_mean)

mcp.tool()(subset_bbox)
mcp.tool()(subset_polygon)
mcp.tool()(extract_cross_section)
mcp.tool()(compare_fields)
mcp.tool()(calculate_bias)
mcp.tool()(calculate_rmse)
mcp.tool()(calculate_pattern_correlation)
mcp.tool()(remap_variable)
mcp.tool()(regrid_dataset)
mcp.tool()(calculate_temporal_mean)
mcp.tool()(calculate_anomaly)
mcp.tool()(calculate_ensemble_mean)
mcp.tool()(calculate_ensemble_spread)
mcp.tool()(export_to_netcdf)
mcp.tool()(export_to_csv)
```

That is a very different statement from "here are four mesh tools and an HPC wrapper." The important thing is not only that there are more functions. It is that the tool surface now supports a coherent scientific session: discovery, inspection, analysis, visualization, persistence, export, and remote escalation.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-runtime-overview.svg" alt="Diagram showing the UXarray MCP flow from dataset discovery and capability filtering to sessions, workflows, plotting, exports, and local or Improv execution." />
  <figcaption>The current server behaves much more like a scientific runtime than a flat shelf of RPC-like calls. Discovery, workflow state, plotting, and export are now first-class pieces of the interface.</figcaption>
</figure>

## Why discovery matters more than people think

One of the most practical improvements is `list_datasets()`. Scientific users often do not start from a single clean pair of `grid.nc` and `data.nc`. They start from a directory tree full of files with mixed naming conventions and partial metadata. That is where most chat tooling falls apart. It assumes the user already knows what to pass in.

The catalog tool changes that starting point:

```python
list_datasets("/Users/mbook/uxarray/test/meshfiles/mpas/QU", recursive=True)
```

On a local MPAS test directory, it grouped files by subdirectory, labeled likely grid and data files, and returned suggested next tool calls such as:

```python
{
  "groups": [
    {
      "subdir": "480",
      "files": [
        {
          "name": "data.nc",
          "kind": "data",
          "suggested_tool": "inspect_variable(\"<grid_path>\", \"/Users/mbook/uxarray/test/meshfiles/mpas/QU/480/data.nc\")"
        },
        {
          "name": "grid.nc",
          "kind": "grid",
          "suggested_tool": "inspect_mesh(\"/Users/mbook/uxarray/test/meshfiles/mpas/QU/480/grid.nc\")"
        }
      ]
    }
  ],
  "recommendations": [
    "Grid and data files detected. Pair a grid file with a data file using inspect_variable, plot_variable, or run_scientific_agent."
  ]
}
```

That is a small feature with a disproportionate effect on usability. It means the server can help the user orient before analysis begins. The same tool can also scan remote directories when an endpoint is configured, which is especially useful when the interesting data only exists on the cluster filesystem.

## Capability filtering is still the gatekeeper

The original post emphasized `get_capabilities()`, and that remains one of the most important design decisions in the repository. What has changed is that the capability surface is now much larger. It does not just gate mesh inspection or zonal means. It filters access to subsetting, comparison, remapping, exports, and workflow stages too.

That is crucial for scientific reliability. In this server, tool applicability is not left to the model's guesswork. The server itself knows that:

- a grid-only input should not trigger data-variable analysis;
- a node-centered variable should not be treated as face-centered;
- a variable without a time dimension should not go through temporal-anomaly logic;
- validation failures should gate downstream steps rather than produce attractive nonsense.

That last point is especially important because the newer feature sweep makes the guardrails visible. In the current comprehensive test run, two tools failed intentionally on the chosen sample dataset:

- `calculate_temporal_mean`
- `calculate_anomaly`

Both failed because the selected variable did not have a `time` dimension. That is a good failure. It is the server telling the client that the operation is scientifically inapplicable for this input, not that the code is broken.

## Plotting changes the human experience of the server

The plotting surface is the single most user-visible change in the newer server. Instead of returning only JSON dictionaries, the plotting tools return inline PNG plus a provenance-bearing metadata block. That is a better fit for exploratory science work because the user can inspect the result immediately, not just infer it from statistics.

The implementation is explicit:

```python
return [
    ImageContent(type="image", data=b64, mimeType="image/png"),
    TextContent(type="text", text=json.dumps(provenance, indent=2)),
]
```

That means plots are not an afterthought or a separate notebook-only layer. They are part of the MCP contract.

Here is a variable plot generated from the current local test dataset:

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-plot-variable.png" alt="UXarray MCP variable plot showing bottomDepth rendered on an MPAS mesh." />
  <figcaption>`plot_variable()` turns a face-centered field into something a scientist can inspect immediately. In the current test sweep, the local variable plot completed in about 2.9 seconds and returned an inline PNG plus provenance metadata.</figcaption>
</figure>

And here is the corresponding zonal-mean plot:

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/uxarray-mcp-plot-zonal-mean.png" alt="UXarray MCP zonal mean plot for bottomDepth by latitude." />
  <figcaption>`plot_zonal_mean()` matters because it moves the server from "fetch me a number" toward "help me reason about structure in the field." That is much closer to how scientists actually work.</figcaption>
</figure>

The remote plotting path matters just as much. The newer test matrix includes `remote_plot_mesh`, `remote_plot_variable`, and `remote_plot_zonal_mean`, all executed through the configured endpoint and returned as PNGs back to the client. That is a concrete proof point that the server can now support visual remote inspection, not just text summaries.

## The biggest architectural improvement: persisted sessions and workflows

The most meaningful evolution in the server is the stateful layer. The repository now includes:

- `create_session`
- `register_dataset`
- `run_workflow`
- `resume_workflow`
- `get_workflow_status`
- `get_result_handle`
- `get_operation_status`
- `list_operations`
- `reset_session_state`

This changes the interaction model completely. Instead of repeating the same file paths and tool arguments over and over, the user can register a dataset once and then work through handles. That is a much better abstraction for repeated scientific analysis.

The default persisted workflow is narrow on purpose, but already useful:

1. `validate_hpc_setup`
2. `probe_path_access`
3. `inspect_mesh`
4. `inspect_variable`
5. `validate_dataset`
6. `calculate_area`
7. `calculate_zonal_mean` when appropriate

The current local workflow run on the MPAS test dataset produced a session, a dataset handle, a workflow record, and a result handle:

```python
{
  "session": {
    "session_id": "session_a1fa9f6454fe",
    "name": "blog-demo"
  },
  "dataset": {
    "dataset_handle": "dataset_0b25c0221643",
    "dataset_count": 1
  },
  "workflow": {
    "workflow_id": "workflow_49901e8476ca",
    "status": "completed"
  },
  "steps": [
    {"name": "validate_hpc_setup", "status": "completed"},
    {"name": "probe_path_access", "status": "completed"},
    {"name": "inspect_mesh", "status": "completed"},
    {"name": "inspect_variable", "status": "completed"},
    {"name": "validate_dataset", "status": "completed"},
    {"name": "calculate_area", "status": "completed"},
    {"name": "calculate_zonal_mean", "status": "completed"}
  ],
  "result_handle": {
    "result_handle": "result_981eabbe969e",
    "kind": "workflow_summary"
  }
}
```

That output is more important than it looks. It means the server now speaks in durable references, not just one-turn answers. A client can inspect what happened, fetch the final artifact later, and resume or branch from known state. That is exactly the direction scientific agent tooling should move.

## A realistic way to use it: local first, then Improv

One reason the newer server feels more mature is that there is now a sensible order of operations. A user does not need to begin on the cluster. They can start locally, get confidence in the data and the workflow, and only then move outward.

A reasonable sequence now looks like this:

```python
list_datasets("/Users/mbook/uxarray/test/meshfiles/mpas/QU", recursive=True)
create_session(name="blog-demo")
register_dataset(
    session_id="session_a1fa9f6454fe",
    grid_path="/Users/mbook/uxarray/test/meshfiles/mpas/QU/480/grid.nc",
    data_path="/Users/mbook/uxarray/test/meshfiles/mpas/QU/480/data.nc",
)
run_workflow(
    session_id="session_a1fa9f6454fe",
    dataset_handle="dataset_0b25c0221643",
    workflow_name="full_analysis",
)
plot_variable(
    grid_path="/Users/mbook/uxarray/test/meshfiles/mpas/QU/480/grid.nc",
    data_path="/Users/mbook/uxarray/test/meshfiles/mpas/QU/480/data.nc",
    variable_name="bottomDepth",
)
```

Only after that local path is trustworthy does it make sense to ask harder operational questions:

- should execution mode stay on `auto`, or be forced to `hpc`?
- is the endpoint healthy enough for a remote run?
- is the exact remote dataset path readable?
- is plotting or inspection the right first remote test?

That progression is what makes the current server feel usable. It is no longer "all remote" or "all local." It supports a staged scientific workflow in which local runs establish correctness and remote runs extend scale or data locality.

## The workflow layer is intentionally conservative

One thing I like about the current implementation is that it does not pretend to be more general than it is. The workflow runtime is deliberately narrow:

- one canonical workflow template;
- JSON-backed local state;
- explicit resume support;
- stage-based events rather than fake progress percentages.

That conservatism is good engineering. Scientific orchestration gets fragile quickly if it tries to be too clever too early. Here, the point is not to build a universal planner first. The point is to make one important workflow predictable and inspectable.

That same mindset shows up in the implementation details. Each workflow stage updates persistent state, appends events, and writes artifacts only after concrete steps complete. The result is a workflow model that is inspectable by both humans and clients.

## Advanced tools make the server useful beyond first inspection

The new advanced tool layer is what turns the server from a demo into a workbench. The current repository now includes:

- spatial queries like `subset_bbox`, `subset_polygon`, and `extract_cross_section`;
- field comparison metrics such as `compare_fields`, `calculate_bias`, `calculate_rmse`, and `calculate_pattern_correlation`;
- remapping tools like `remap_variable` and `regrid_dataset`;
- temporal and ensemble summaries;
- export tools for NetCDF, CSV, and persisted result writing.

This matters because scientific users rarely stop at inspection. They subset, compare, regrid, export, and revisit. Those are not peripheral tasks. They are the workflow.

The test matrix makes the current scope concrete. The repo now records a 42-call feature sweep across 10 tiers:

| Tier | What it covers |
| --- | --- |
| 1 | discovery and config |
| 2 | HPC health checks |
| 3 | core local inspection |
| 4 | local plotting |
| 5 | subsetting and extraction |
| 6 | statistical analysis |
| 7 | sessions and workflows |
| 8 | exports |
| 9 | remote inspection on Improv |
| 10 | remote plotting |

In the current saved results:

- 42 tool invocations ran;
- 40 passed;
- 2 failed for scientifically appropriate reasons tied to missing time coordinates;
- remote plotting and remote inspection both succeeded.

That is a much stronger maturity signal than a handful of ad hoc examples.

## Improv now feels more like a playbook than an experiment

The older version of the article treated Improv mostly as a debugging story. The newer repo has moved that knowledge into a reusable operational pattern.

There is now:

- `validate_hpc_setup()` for deep readiness checks;
- `probe_path_access()` for proving the exact remote path is readable;
- `scripts/hpc_doctor.py` as a CLI entry point for those checks;
- `scripts/improv_endpoint.sh` to generate single-host or PBS-backed endpoint templates;
- stronger local fallback behavior in the remote wrappers;
- explicit documentation of the failure modes that actually happened.

The CLI doctor is a good example of the current mindset:

```bash
uv run python scripts/hpc_doctor.py \
  --timeout-seconds 180 \
  --sample-path /gpfs/fs1/home/<username>/path/to/file.nc
```

This is not glamorous, but it is exactly the right kind of infrastructure. HPC users need a way to prove that:

- local Globus auth is good,
- the endpoint manager is visible,
- remote code can actually execute,
- the worker can read the exact file path,
- and scientific dependencies exist on the remote side.

The newer Improv documentation is stronger because it treats these as separate layers. That distinction was learned the hard way. An endpoint manager showing `online` is not enough. A remote worker being able to run a no-op is not enough. An interactive `/home/...` path being readable on a login node is not enough. The server now encodes those lessons.

## The remote wrappers are better because they fail gracefully

One of the better design decisions in the newer code is that remote wrappers no longer behave like brittle pass-through calls. They run a real pre-flight check and fall back locally if the endpoint is not ready:

```python
ready, reason = _endpoint_is_ready(agent)
if not ready:
    result = local_call()
    result["_provenance"]["warnings"].append(
        f"HPC endpoint not ready ({reason}); ran locally."
    )
    return result
```

That is a subtle but important improvement. Scientific users often want a result plus a caveat, not a hard stop at the first infrastructure wobble. The warning becomes part of the provenance record, which means the model and the user can both see what happened.

The current timing snapshot from the saved feature sweep helps illustrate the operational shape of the system:

| Operation | Example elapsed time |
| --- | --- |
| `run_workflow` on local test data | 1.83 s |
| `validate_hpc_setup` | 31.13 s |
| `probe_path_access(use_remote=True)` | 10.15 s |
| `inspect_mesh_hpc` | 20.62 s |
| `calculate_zonal_mean_hpc` | 6.01 s |
| `remote_plot_variable` | 10.49 s |

These are not universal performance claims. They are one concrete snapshot from this environment. But they make an important point: the remote path is now a usable operational surface, not just an aspirational architecture.

## What still feels early, and why that is fine

The current server is much stronger than the version I first wrote about, but it is still early in exactly the right places.

- the persisted workflow layer is intentionally narrow rather than prematurely generic;
- the plotting surface is useful, but still closer to "scientific inspection" than publication-grade figure composition;
- the remote path is operationally credible, but cluster-specific knowledge still matters;
- some advanced tools depend heavily on variable structure, so capability filtering and validation remain essential.

That is a healthy state for the project. The hard part is not adding a hundred loosely connected functions. The hard part is making discovery, applicability, state, provenance, and remote execution line up in a way that scientists can actually trust.

## Why the newer server is more compelling

The value of the server is no longer only that it exposes UXarray to a chat client. The more interesting value is that it is starting to express a scientific style of interaction:

- first orient to the dataset;
- then filter to valid operations;
- then inspect or plot;
- then persist the analysis state;
- then export or hand off the result;
- and only escalate to HPC when the runtime path is actually ready.

That is a much better fit for scientific computing than generic file chat. It respects the structure of the data, the importance of validation, and the operational reality of shared systems.

## What I think the project demonstrates now

At this point, the UXarray MCP server is best understood as an early scientific runtime for AI clients, not as a thin wrapper around a numerical library.

The new pieces are what make that claim believable:

- discovery through `list_datasets`;
- applicability filtering through `get_capabilities`;
- inline visual outputs through the plotting tools;
- persistent state through sessions, handles, and workflows;
- result artifacts that can be revisited later;
- and a more disciplined remote-execution playbook on Improv.

That combination is what makes the project feel substantive now. The server is not finished, and it should not pretend to be. But it has moved from "interesting prototype" to "credible foundation" much faster than most scientific chat interfaces do.

## Where I think this can go next

The next step is not merely "more tools." The more important direction is deeper composition.

- richer workflow templates for common scientific tasks, not just one canonical path;
- stronger artifact browsing so result handles become easier to inspect and compare;
- more explicit provenance around remote execution venue, endpoint identity, and fallback decisions;
- broader dataset-catalog intelligence for messy real project directories;
- and tighter links between analysis tools and plots so the visual layer becomes a first-class part of agent reasoning.

That is where the project starts to become especially interesting. Once a scientific MCP server can combine discovery, workflow state, validation, plots, and remote execution in a disciplined way, it stops being a novelty interface and starts to look like real research infrastructure.

## Closing thought

The most useful scientific AI systems will not be the ones that speak most fluently about data. They will be the ones that help users move through a disciplined workflow: discover, validate, inspect, visualize, persist, export, and only then scale out.

That is why this newer version of the UXarray MCP server matters more than the earlier one. It now captures more of the actual structure of scientific work. The natural-language interface is still there, but it is no longer the whole story. The stronger story is that the runtime underneath it is getting good enough to deserve serious use.
