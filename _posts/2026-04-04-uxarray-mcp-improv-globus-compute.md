---
title: "Bringing UXarray MCP to HPC: Globus Compute, Improv, and the Hidden Work of Remote Scientific Tooling"
date: 2026-04-04
permalink: /blog/uxarray-mcp-improv-globus-compute/
categories:
  - blog
excerpt: "A technical note on getting UXarray MCP to run cleanly across local and remote environments, debugging Globus Compute on Argonne Improv, and turning that work into reusable tooling and documentation."
tags:
  - hpc
  - climate
  - uxarray
  - globus-compute
  - mcp
author_profile: false
toc: true
toc_sticky: true
---

Scientific tooling often looks deceptively simple from the outside. A user sees a tool like `inspect_mesh`, points it at a file, and expects a result. But once that same tool is supposed to run on a remote cluster, the problem becomes much less about a single function call and much more about the operational stack around it: authentication, environment bootstrapping, scheduler access, file-system conventions, worker packages, and observability.

That is the work I just finished for the UXarray MCP server on Argonne Improv.

The goal was straightforward: make the [UXarray MCP server](https://github.com/UXARRAY/uxarray-mcp-server) usable with remote execution so a local MCP client can trigger mesh-aware analysis on HPC resources. In practice, the real task was to make that path understandable, testable, and recoverable when it fails.

## What the system is trying to do

At a high level, the architecture is:

1. A local MCP client such as Claude calls a UXarray tool.
2. The local MCP server decides whether to run it locally or remotely.
3. If remote execution is selected, the server submits a self-contained Python function through Globus Compute.
4. A configured endpoint on the cluster receives that function.
5. A worker process on the cluster executes it and sends the result back.

That sounds manageable, but there are several distinct layers hidden inside it:

- the local machine running the MCP server
- the Globus Compute client state on that local machine
- the endpoint manager on the cluster
- the child endpoint and scheduler-launch path
- the remote worker environment that must actually import `uxarray`

The key lesson is that those layers fail independently.

## What failed first on Improv

The first round of debugging exposed the usual HPC trap: a status check that was technically true but operationally misleading. The endpoint looked `online`, but real remote tasks still did not complete.

That mismatch turned out to matter more than any single bug. It meant the repo needed to distinguish:

- endpoint manager health
- child endpoint startup
- scheduler submission health
- real path readability
- remote scientific package availability

Once we started checking those layers one by one, the actual failures became much more concrete:

- local Globus authentication was missing
- the endpoint child process could not find `qsub`
- the remote worker did not have `uxarray` installed
- `/home/...` paths that looked fine interactively were not the canonical paths the worker needed
- stale PID files and multi-login-node behavior caused false starts

None of those are UXarray bugs. They are bring-up bugs. But if the tooling does not surface them clearly, they feel like UXarray bugs to the end user.

## The most useful debugging insight

The most important operational decision was to stop debugging PBS and UXarray at the same time.

Instead, the workflow that finally worked was:

1. start with a single-host endpoint
2. prove a tiny remote no-op task runs
3. prove one exact remote file path is readable
4. only then run UXarray-specific remote tools
5. only after that switch back to PBS-backed execution

That change alone made the system debuggable.

For example, one of the early path checks looked like a file problem:

```text
/home/jain/2case2_wrf_eplus/met_em.d01.2017-03-16_00:00:00.nc
```

But the real issue was path resolution on the remote side. The worker needed the canonical GPFS path:

```text
/gpfs/fs1/home/jain/WPSV39/20170316_2days/met_em.d01.2017-03-16_00:00:00.nc
```

That is exactly the kind of thing users should not have to discover by trial and error.

## What we added to the repo

The debugging session turned into concrete improvements to the repository.

First, we added HPC bring-up diagnostics:

- `validate_hpc_setup()`
- `probe_path_access()`
- `scripts/hpc_doctor.py`

These are designed to answer simpler questions before users jump into full UXarray analysis:

- is local Globus auth working?
- is the endpoint manager reachable?
- can a real remote task run?
- can the remote worker read the exact file path?
- can the worker do a generic NetCDF open?

Second, we added reusable HPC bring-up guidance:

- a first-time-user Globus Compute guide
- a generic HPC bring-up playbook
- an Improv-specific troubleshooting and worked-example page

Third, we added a sequential remote workflow example:

- `scripts/agentic_hpc_loop.py`

That script proves the system can already do something like:

1. submit a remote task
2. poll until it finishes
3. inspect the result
4. decide the next task
5. submit the next task

That is not yet a full workflow engine, but it is a real foundation for one.

## The first real remote UXarray success

The clean success case on Improv used MPAS sample files under the canonical shared filesystem:

```text
/gpfs/fs1/home/jain/uxarray/test/meshfiles/mpas/dyamond-30km/gradient_grid_subset.nc
/gpfs/fs1/home/jain/uxarray/test/meshfiles/mpas/dyamond-30km/gradient_data_subset.nc
```

With those paths, remote UXarray inspection successfully returned:

- `n_face = 195`
- `n_node = 442`
- `n_edge = 636`

and identified the face variables:

- `face_lat`
- `face_lon`
- `gaussian`
- `inverse_gaussian`

That result mattered because it proved the whole path end to end:

- local client auth
- endpoint health
- remote task execution
- remote file access
- remote UXarray import
- remote scientific result return

## Why this matters beyond one cluster

Although this work was done on Improv, the real value is broader. The design now makes it much easier to bring up the same stack on other HPC systems, especially those with similar scheduler models. The repo is still not “one click” across clusters, but it is no longer opaque.

That difference is huge. If a scientific software stack cannot explain why it failed, it is hard to adopt anywhere outside the machine where it was first developed.

The work here was not just getting one endpoint to function. It was making the path to first success shorter and making the failure modes legible enough that another cluster can be tackled with confidence instead of guesswork.

## Where this goes next

The current tool surface is still synchronous, but the remote pieces are now good enough to support a more agentic workflow model:

- submit a job
- wait for completion
- inspect the result
- choose the next computation
- keep state across steps

That is exactly the direction I think this should go next, especially for scientific workflows that need validation gates, retries, and path-aware decision making.

For now, the key result is simpler: the UXarray MCP server now works cleanly enough on a real HPC machine that the repo can teach others how to do the same.
