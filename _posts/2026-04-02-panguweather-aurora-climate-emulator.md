---
title: "Porting a Climate Emulator to Aurora: PanguWeather, SFNO, and the Real Work of Runtime Portability"
date: 2026-04-02
permalink: /blog/panguweather-aurora-climate-emulator/
categories:
  - blog
tags:
  - climate
  - hpc
  - aurora
  - pytorch
  - sfno
  - machine-learning
excerpt: "A technical note on making a PlaSim-driven atmospheric emulator run reproducibly on Aurora, with attention to floating-point policy, distributed launch, checkpoint restore, and queue-aware operations."
author_profile: false
toc: true
toc_sticky: true
---

Climate emulators are often presented as a pure machine-learning success story: train a neural model on atmospheric data, obtain fast forecasts, and then compare accuracy curves. In practice, that picture is incomplete. A useful emulator for climate science must also be portable across hardware stacks, reproducible under distributed launchers, and operationally debuggable on real systems. This was the technical problem I worked on for the PanguWeather codebase on Aurora.

This article expands the Aurora portability project in a form that emphasizes the systems and climate-science details rather than presentation shorthand.

The starting point was not a toy benchmark. The repository couples physically meaningful PlaSim climate data, nontrivial model implementations, iterative forecast logic, checkpointing, and distributed training. That matters. If the goal is to understand how an atmospheric emulator behaves on emerging GPU platforms, then the benchmark has to include the parts of the workflow that climate scientists actually depend on: data movement, mixed precision, restart behavior, and evaluation against climatology-aware metrics.

## Why this work is needed

For climate and weather workflows, "it runs on my GPU" is not a serious endpoint. Scientific users need a path from development to repeated execution on shared supercomputers. That path has several failure modes:

- the code assumes CUDA-specific APIs and fails on Intel XPU;
- the launcher exports MPI or PMIx variables that PyTorch does not automatically interpret;
- mixed-precision settings that are reasonable on one vendor stack are unsafe or irrelevant on another;
- checkpoint restore works only for the original device type;
- debugging is too expensive because every iteration requires a long production job.

Those are not peripheral engineering concerns. They determine whether an emulator can be studied, validated, and eventually trusted in production research workflows.

## Scientific setting: PlaSim and emulator design

The scientific basis of this work is the PlaSim dataset. PlaSim is an intermediate-complexity climate model, which makes it especially valuable for emulator research. It is more realistic than synthetic or heavily simplified benchmarks, but still tractable enough to support repeated machine-learning experiments.

In this repository, the emulator learns from multivariate atmospheric state data including upper-air variables such as temperature, zonal and meridional winds, humidity, and geopotential height, along with surface pressure and surface temperature. That places the workload squarely in the regime of global geophysical learning rather than image-style pattern matching.

One representative Aurora smoke configuration makes that explicit:

```yaml
SFNO:
  name: "SFNO-PLASIM-Aurora-Smoke"
  upper_air_variables: ["ta", "ua", "va", "hus", "zg"]
  surface_variables: ["pl", "tas"]
  diagnostic_variables: ["pr_6h"]
  climatology_file: mean_daymean_climatology_sigma.nc
  num_levels: 10
  use_sigma_levels: True
```

This is where the term *emulator* is important. The model is not merely fitting isolated samples; it is learning a surrogate evolution operator for atmospheric state. That means the scientific stakes extend beyond per-step loss. Errors compound over lead time, and evaluation has to respect the geometry and seasonality of the climate system.

The repository already reflects that scientific reality. For example, error metrics are latitude-weighted rather than naively averaged over the grid:

```python
def latitude_weighting_factor_torch(latitudes):
    lat_weights_unweighted = torch.cos(3.1416 / 180. * latitudes)
    return latitudes.size()[0] * lat_weights_unweighted / torch.sum(lat_weights_unweighted)

def weighted_rmse_torch_channels(pred, target, latitudes):
    weight = torch.reshape(latitude_weighting_factor_torch(latitudes), (1, 1, -1, 1))
    result = torch.sqrt(torch.mean(weight * (pred - target)**2., dim=(-1, -2)))
    return result
```

That detail matters because equal-area thinking matters on the sphere. A climate emulator that ignores latitude weighting can report misleading aggregate skill.

The code also carries climatology-aware logic for day-of-year indexing, including leap-year handling:

```python
def get_climatology_index(date):
    if hasattr(date, 'dayofyr'):
        day_of_year = date.dayofyr
    elif hasattr(date, 'dayofyear'):
        day_of_year = date.dayofyear
    else:
        day_of_year = date.timetuple().tm_yday

    if hasattr(date, 'is_leap_year'):
        is_leap_year = date.is_leap_year
    else:
        year = date.year
        is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    if not is_leap_year and day_of_year > 59:
        clim_index = day_of_year
    else:
        clim_index = day_of_year - 1

    return clim_index
```

This is a useful reminder that scientific ML pipelines inherit calendar logic, physical weighting, and diagnostic conventions from the domain itself. Portability work has to preserve those assumptions, not flatten them away.

## Why SFNO is a good systems target

The Spherical Fourier Neural Operator (SFNO) is a strong fit for this repository because it is scientifically motivated and computationally demanding at the same time. Spectral operators are natural candidates for global atmospheric fields on spherical domains, and they create a workload that is richer than a narrowly optimized tensor microbenchmark.

That is precisely why I focused on SFNO as a portability target. It exercises:

- global-field input pipelines rather than tiny synthetic batches;
- iterative forecast and validation behavior rather than a single forward pass;
- distributed execution and rank-local device setup;
- checkpoint save and restore;
- precision policy choices that affect stability and throughput.

If a code path survives that full workload, it is far more informative than a benchmark that measures only a hand-picked kernel.

## What I changed for Aurora

The main engineering goal was to convert a largely CUDA-oriented runtime into a shared runtime path that works on Intel XPU as well. The point was not to create a one-off Aurora branch. The point was to make the repository itself understand multiple GPU ecosystems.

### 1. Device selection and distributed backend resolution

The first step was to normalize device discovery and backend selection. The runtime now chooses XPU first, then CUDA, then CPU, and it exposes backend selection explicitly:

```python
def get_device():
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

def get_default_ddp_backend():
    if torch.cuda.is_available() and dist.is_nccl_available():
        return "nccl"
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        is_xccl_available = getattr(dist, "is_xccl_available", None)
        if callable(is_xccl_available) and is_xccl_available():
            return "xccl"
        if hasattr(dist, "is_backend_available") and dist.is_backend_available("xccl"):
            return "xccl"
    return "gloo"
```

That sounds straightforward, but it removes a large class of implicit CUDA assumptions. Once the active device becomes a resolved runtime choice rather than a hard-coded expectation, the rest of the training path becomes much easier to regularize.

### 2. Translating MPI and PMIx launch state into PyTorch's expected environment

Aurora launch patterns are not identical to the `torchrun` assumptions many PyTorch projects encode. The repository now maps MPI and PMIx variables onto the names used by `torch.distributed`:

```python
def populate_dist_env_from_mpi():
    env_map = {
        "RANK": ("PMIX_RANK", "PMI_RANK", "PALS_RANKID"),
        "WORLD_SIZE": ("PMIX_SIZE", "PMI_SIZE"),
        "LOCAL_RANK": ("PALS_LOCAL_RANKID", "PMI_LOCAL_RANK"),
    }

    for target, candidates in env_map.items():
        for source in candidates:
            value = os.environ.get(source)
            if value:
                os.environ[target] = value
                break
```

This is the kind of change that often gets dismissed as plumbing. In reality, it is central to portability. Distributed training is not portable if rank identity, world size, and local device placement depend on one launcher ecosystem.

### 3. Separating floating-point policy by vendor stack

One of the most important technical points in this project is floating-point precision. It is tempting to force all accelerators through one universal "mixed precision" recipe. That approach is usually wrong.

In this repository, the AMP path is now device-aware:

```python
def create_grad_scaler():
    if amp is None:
        return None
    device_type = get_device_name()
    if device_type == 'cuda':
        return amp.GradScaler()
    return None
```

The training entry point also gates TF32 behavior under CUDA instead of applying it globally:

```python
if torch.cuda.is_available():
    try:
        torch.backends.cuda.matmul.fp32_precision = 'tf32'
        torch.backends.cudnn.conv.fp32_precision = 'tf32'
    except Exception:
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

torch.set_float32_matmul_precision('high')
```

The practical point is simple: CUDA and Intel XPU should not be treated as if they share identical precision semantics. CUDA often benefits from a GradScaler-centered fp16 path, whereas the Aurora XPU path is more naturally aligned with bf16-oriented execution and does not need a forced CUDA-style scaling policy. Making those distinctions explicit improves correctness and makes later performance analysis more interpretable.

### 4. Checkpoint and restore behavior as a first-class requirement

Training portability is incomplete if checkpoint restore only works for the original hardware target. Part of the Aurora work was therefore operational: smoke-test the full path, including restart behavior, rather than declaring success after a single forward or backward pass.

That is why the Aurora tooling includes setup checks, trainer-initialization smoke tests, single-rank train smoke runs, and checkpoint-restore verification. In scientific computing, restart is not a convenience feature. It is part of the contract, especially when jobs run under walltime constraints.

## Queue-aware engineering on Aurora

Aurora operations are not just about code correctness. They are also about using the machine in a way that supports rapid debugging and reproducible long runs.

For fast iteration, I added debug-queue smoke scripts with aggressive diagnostics:

```bash
#PBS -q debug
#PBS -l select=1:ncpus=16:ngpus=2
#PBS -l walltime=00:20:00

export PYTHONFAULTHANDLER=1
export TORCH_DISTRIBUTED_DEBUG=${TORCH_DISTRIBUTED_DEBUG:-DETAIL}
```

This matters because porting is usually bottlenecked by turnaround time. If every test requires a long production submission, small runtime mistakes become expensive. The debug queue turns setup validation, trainer initialization, and restore checks into short-cycle engineering tasks.

For longer SFNO training, the repository now includes a one-node production-oriented script aimed at the `capacity` queue:

```bash
#PBS -q capacity
#PBS -l select=1:ncpus=32:ngpus=6
#PBS -l walltime=04:00:00

export WORLD_SIZE=${NPROC_PER_NODE:-12}
RUNCMD=("${MPIEXEC_BIN}" --pmi=pmix -n "${NPROC_PER_NODE}" -ppn "${NPROC_PER_NODE}" "${PYTHON_BIN}")
```

Two details are worth noting.

First, the queue choice is part of the technical design. The shorter `debug` queue is appropriate for smoke paths and failure localization, while the longer `capacity` queue is the right place for sustained one-node training. Putting those roles into committed scripts makes the workflow teachable and repeatable for other users.

Second, Aurora exposes 12 XPU devices per node to PyTorch while PBS accounts for 6 physical GPUs. That distinction has to be reflected in the launch logic. Encoding it in the batch script avoids a great deal of user confusion and reduces the chance of silently incorrect rank topology.

## Why this is more valuable than a microbenchmark

The resulting Aurora path is useful not only because it runs, but because it creates a realistic scientific benchmark across GPU ecosystems. The workload includes:

- atmospheric data loading from PlaSim-derived products;
- an SFNO model with real global-field structure;
- distributed launch and backend setup;
- mixed-precision choices that differ by hardware vendor;
- checkpoint and restore validation;
- queue-aware operational scripts for both debugging and longer jobs.

That combination is more informative than a synthetic throughput test. It tells us how a climate-emulator workflow behaves as a workflow.

This is especially important for earth-system ML, where the hard problems are often end-to-end: getting the science right, keeping the training stable, preserving restart behavior, and making the code usable on the actual machines available to the project.

## What I see as the contribution

My contribution here was not just "making Aurora work." It was establishing a supported execution path for a scientifically meaningful emulator codebase. Concretely, that meant:

- turning device selection, AMP, and distributed backend choices into shared runtime logic;
- translating Aurora launcher state into PyTorch-compatible distributed state;
- preserving scientific evaluation conventions such as latitude weighting and climatology-aware indexing;
- adding smoke-test and checkpoint-restore infrastructure so debugging does not depend on long production jobs;
- encoding Aurora queue usage and batch-launch details in committed scripts so others can rerun the workflow.

For climate-science software, that kind of work is often what separates a promising repository from a usable research instrument.

## Closing thought

Climate-emulator research needs more than faster models. It needs durable execution paths on the systems where those models will actually be trained and studied. Aurora portability for PanguWeather is one example of that broader lesson: scientific ML becomes much more credible when runtime engineering, floating-point policy, scheduler behavior, and domain-specific evaluation are treated as part of the science rather than as afterthoughts.
