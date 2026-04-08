---
title: "Bringing UXarray MCP to HPC: Local Examples, Improv, and the Start of AI-Native Scientific Tooling"
date: 2026-04-04
permalink: /blog/uxarray-mcp-improv-globus-compute/
categories:
  - blog
excerpt: "A technical note on building a mesh-aware MCP server that works locally today, reaches Improv through Globus Compute, and points toward richer AI-agent workflows for scientific data."
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
  <h1 class="article-title">Bringing UXarray MCP to HPC</h1>
  <p class="article-dek">Local worked examples, remote execution on Improv, and why mesh-aware MCP tooling is more than a thin wrapper around scientific Python.</p>
</div>

Scientific tooling often looks deceptively simple from the outside. A user sees a tool like `inspect_mesh`, points it at a file, and expects a result. But once the same tool is supposed to work through an MCP client, reason about dataset structure, expose only relevant operations, and optionally run on a remote cluster, the problem changes shape. It is no longer just a function call. It becomes a systems problem: tool design, provenance, execution routing, endpoint health, path conventions, and recoverability when remote infrastructure fails.

That is the work I just finished for the UXarray MCP server and the [Improv](https://www.lcrc.anl.gov/systems/improv) execution path.

The immediate goal was practical: make a mesh-aware MCP (Model Context Protocol) server useful for natural-language dataset exploration, first on a laptop and then on an HPC (High-Performance Computing) system through Globus Compute. The broader point is more interesting. This is an early example of what AI-native scientific tooling can look like when the interface is not just "chat over a file," but a structured tool surface that understands topology, variable locations, execution venue, and scientific failure modes.

## Why this is more than a flat tool shelf

The UXarray MCP server is not just a collection of callable functions exposed to a chat client. It has several pieces that make it genuinely useful for scientific workflows:

- `get_capabilities()` filters the tool surface to what actually applies to the dataset in front of the agent.
- `run_scientific_agent()` performs an Analyze → Plan → Execute → Verify loop instead of blindly calling one function.
- every tool attaches `_provenance` metadata so results carry execution venue, versions, inputs, and artifacts.
- HPC tools register only when a real endpoint is configured.
- execution mode can be switched between `local`, `hpc`, and `auto` without editing source or config files by hand in the middle of a session.

The server registration code makes that design visible:

```python
mcp = FastMCP("uxarray-mcp-server")

mcp.tool()(get_capabilities)
mcp.tool()(run_scientific_agent)

mcp.tool()(inspect_mesh)
mcp.tool()(inspect_variable)
mcp.tool()(calculate_area)
mcp.tool()(calculate_zonal_mean)
mcp.tool()(validate_dataset)

mcp.tool()(get_execution_mode)
mcp.tool()(set_execution_mode)

if load_config().has_endpoint:
    mcp.tool()(inspect_mesh_hpc)
    mcp.tool()(calculate_area_hpc)
    mcp.tool()(inspect_variable_hpc)
    mcp.tool()(calculate_zonal_mean_hpc)
```

That last block matters. The tool list itself adapts to the available infrastructure. Local-only users do not get cluttered with dead HPC controls, while cluster users do not need a separate server.

## Worked example 1: local, from zero, with no external dataset

One of the strongest design choices in this project is that it can be exercised immediately with built-in `healpix` meshes. That means the first encounter with the MCP server does not require downloading a climate dataset, wiring an endpoint, or even launching a client. You can run the same logic from Python first.

For example, local mesh inspection on the built-in demo mesh:

```bash
uv run python -c "from uxarray_mcp.tools.inspection import inspect_mesh; print(inspect_mesh('healpix:4'))"
```

produced:

```python
{
  'format': 'HEALPix',
  'n_face': 3072,
  'n_node': 3074,
  'n_edge': 6144,
  'n_max_face_nodes': 4,
  'file_size_mb': 0.0,
  '_provenance': {
    'tool': 'inspect_mesh',
    'execution_venue': 'local'
  }
}
```

The corresponding area calculation:

```bash
uv run python -c "from uxarray_mcp.tools.inspection import calculate_area; print(calculate_area('healpix:4'))"
```

returned:

```python
{
  'total_area': 12.566370614359174,
  'mean_area': 0.00409061543436171,
  'min_area': 0.0040906154343617095,
  'max_area': 0.0040906154343617095,
  'area_units': 'm^2',
  'n_face': 3072,
  '_provenance': {
    'tool': 'calculate_area',
    'execution_venue': 'local'
  }
}
```

That is already useful, but the more interesting example is the scientific agent:

```bash
uv run python -c "from uxarray_mcp.tools.scientific_agent import run_scientific_agent; import pprint; pprint.pp(run_scientific_agent('healpix:3'))"
```

which returned a structured reasoning trace:

```python
{
  'execution_venue': 'local',
  'reasoning_trace': [
    {'stage': 'analyze', 'action': "inspect_mesh('healpix:3')"},
    {'stage': 'analyze', 'observation': 'mesh has 768 faces'},
    {'stage': 'plan', 'decision': "execution_venue='local'"},
    {'stage': 'plan', 'operations': ['calculate_area']},
    {'stage': 'execute', 'venue': 'local'},
    {'stage': 'verify', 'check': 'total_area > 0', 'result': 'pass'}
  ],
  'mesh_summary': {'format': 'HEALPix', 'n_face': 768, 'n_node': 770},
  'area_results': {'total_area': 12.566370614359174, 'n_face': 768},
  'verification': {'passed': True, 'warnings': []}
}
```

This is where the MCP approach starts to matter. The agent is not just calling `calculate_area()` because the user asked. It is inspecting the problem, choosing the operation, recording why it chose that operation, and verifying the result.

## Worked example 2: capability discovery instead of tool guessing

One of the common weaknesses of LLM (Large Language Model) tool use is that the model has to guess what tools are relevant before it has enough structural context. For scientific datasets, that is a recipe for bad calls. A grid without a data file should not invite zonal-mean analysis. A dataset with node-centered variables should not be treated like face-centered data.

That is why `get_capabilities()` is one of the most important pieces of the UXarray MCP design:

```bash
uv run python -c "from uxarray_mcp.tools.capabilities import get_capabilities; import pprint; pprint.pp(get_capabilities('healpix:2'))"
```

On a pure grid input, it returned:

```python
{
  'grid_summary': {'n_face': 192, 'n_node': 194, 'n_edge': 384, 'format': 'HEALPix'},
  'mcp_server_tools': [
    {'name': 'inspect_mesh', 'applicable': True},
    {'name': 'inspect_variable', 'applicable': False, 'reason': 'Requires a data file'},
    {'name': 'calculate_area', 'applicable': True},
    {'name': 'calculate_zonal_mean', 'applicable': False, 'reason': 'Requires face-centered data'},
    {'name': 'validate_dataset', 'applicable': False, 'reason': 'Requires a data file'}
  ],
  'recommendations': [
    'Provide a data_path to unlock variable-level filtering and tools like inspect_variable, calculate_zonal_mean, and validate_dataset.'
  ]
}
```

This is the difference between a tool list and an assistant. Instead of forcing the model to hallucinate which scientific operation might work, the server describes the valid action surface for the specific dataset.

## Worked example 3: execution mode as part of the interface

Another subtle but important feature is that execution venue is itself queryable state, not hidden configuration. Locally, the server reported:

```bash
uv run python -c "from uxarray_mcp.tools.execution_control import get_execution_mode; import pprint; pprint.pp(get_execution_mode())"
```

```python
{
  'mode': 'local',
  'endpoint_id': None,
  'endpoint_status': 'no_endpoint',
  'description': 'Local mode: all computations run on this machine regardless of HPC availability.'
}
```

That may sound mundane, but it is exactly the kind of state exposure that makes a tool usable in an interactive client. The user and the agent can both ask, "Where will this run?" before a heavy computation starts. That is much better than burying the answer in a YAML (configuration file format) file.

## Why provenance matters for scientific AI workflows

Every tool result carries a `_provenance` block. That is not just bookkeeping. It is how the system stays scientifically accountable when an LLM (Large Language Model) is part of the loop.

The provenance attachment is explicit in the code:

```python
provenance = {
    "tool": tool,
    "inputs": inputs,
    "execution_venue": venue,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "uxarray_version": _get_uxarray_version(),
    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    "warnings": warnings if warnings is not None else [],
    "artifacts": artifacts if artifacts is not None else [],
}
```

That means a downstream consumer can see not just the answer, but what tool ran, where it ran, what version of UXarray was used, and whether warnings were raised. In scientific work, that is the difference between a useful result and an unverifiable anecdote.

## The [Improv](https://www.lcrc.anl.gov/systems/improv) path: where remote execution became real

The local UXarray MCP story is already useful, but the more ambitious goal was remote execution on [Improv](https://www.lcrc.anl.gov/systems/improv) — Argonne's 825-node AMD EPYC cluster managed by LCRC — through Globus Compute. At a high level, the path is:

1. a local MCP client calls a tool,
2. the local server decides whether to run locally or remotely,
3. Globus Compute submits the serialized computation,
4. an endpoint on [Improv](https://www.lcrc.anl.gov/systems/improv) receives it,
5. a remote worker executes the scientific function and returns the result.

The configuration surface is intentionally small:

```yaml
hpc:
  globus_compute:
    endpoint_id: "your-endpoint-uuid"
  execution_mode: "auto"
  timeout_seconds: 300
```

But the debugging work underneath that small interface was not trivial. On [Improv](https://www.lcrc.anl.gov/systems/improv), the first important lesson was that an endpoint can look `online` while real scientific work still fails. Once the remote path was decomposed into smaller checks, the real failure modes became visible:

- missing local Globus authentication
- endpoint child processes without `qsub` (the PBS job-submission command) in path
- remote workers missing `uxarray`
- path mismatches between interactive `/home/...` habits and canonical GPFS (General Parallel File System) paths
- stale PID files and login-node drift

The most useful operational change was to stop debugging PBS (Portable Batch System scheduler) and UXarray at the same time. The successful bring-up path became:

1. prove a tiny remote no-op runs,
2. prove the remote worker can open the exact file path,
3. prove a generic NetCDF (Network Common Data Form) read succeeds,
4. only then run UXarray-specific tools,
5. only after that move back to the scheduler-backed endpoint path.

That turned remote execution from a black box into a layered system that could actually be diagnosed.

One representative [Improv](https://www.lcrc.anl.gov/systems/improv) issue looked like a data problem at first:

```text
/home/jain/2case2_wrf_eplus/met_em.d01.2017-03-16_00:00:00.nc
```

but the real fix was to use the canonical GPFS path the worker could actually resolve:

```text
/gpfs/fs1/home/jain/WPSV39/20170316_2days/met_em.d01.2017-03-16_00:00:00.nc
```

That distinction is precisely why HPC-aware tooling needs better diagnostics than "task failed."

## Why the remote wrappers are powerful

The remote wrappers in `remote_tools.py` do more than pass a `use_remote=True` flag through to an endpoint. They perform pre-flight checks and fail back to local execution when appropriate:

```python
ready, reason = _endpoint_is_ready(agent)
if not ready:
    result = inspect_mesh(file_path)
    result["_provenance"]["warnings"].append(
        f"HPC endpoint not ready ({reason}); ran locally."
    )
    return result
```

That pattern is important for AI-agent workflows. It gives the model a structured warning and a scientifically valid fallback instead of a hard infrastructure failure. The user still gets a result, but also gets the execution caveat in a form the agent can reason about.

## Why this is only the start

The current UXarray MCP server already demonstrates something meaningful:

- a local user can do real mesh-aware analysis through natural language,
- the system can explain which tools apply before a bad call is made,
- scientific outputs carry provenance by default,
- the same interface can extend to HPC execution,
- and the scientific agent can already perform a small reasoning loop instead of one-shot tool firing.

But this is still early-stage work. The next steps are the interesting ones:

- richer asynchronous workflows that submit work, wait, inspect, and continue,
- hosted sample environments so people can try the system without local setup,
- broader dataset-aware planning, not just mesh-aware planning,
- and more cross-domain use cases where the same agentic pattern applies outside climate analysis.

That is the larger point of this project. The value is not only that UXarray now has an MCP server, or that the server can reach [Improv](https://www.lcrc.anl.gov/systems/improv). The value is that scientific software can be exposed in a way that is both AI-friendly and scientifically disciplined. This work shows one path toward that, and it feels much more like a beginning than an endpoint.
