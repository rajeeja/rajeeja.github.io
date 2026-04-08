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
excerpt: "A technical note on why the current Aurora path is plain DDP, how memory and I/O show up in practice, and where sharded training or chunk-aware storage would matter next for a climate emulator."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-hero">
  <p class="eyebrow">Research note · April 2, 2026</p>
  <h1 class="article-title">Porting a Climate Emulator to Aurora</h1>
  <p class="article-dek">A technical note on the current DDP-based Aurora path for a PlaSim and SFNO climate emulator, with attention to memory pressure, floating-point policy, launcher portability, and the next systems steps beyond one-node training.</p>
</div>

Climate emulators are easy to oversimplify. We usually describe them as neural surrogates for expensive physical models, trained once and then used for faster forecasts or long-rollout experiments. That description is true, but it hides the actual engineering burden. A useful emulator for climate science has to survive real data movement, real restart behavior, real distributed launchers, and real memory limits on the machines where the work will actually run.

That was the interesting part of the Aurora work for this codebase. The question was not only whether SFNO (Spherical Fourier Neural Operator) could run on Intel GPUs. The deeper question was: what parallel training path does the code really implement today, how portable is that path across CUDA (Nvidia GPU compute platform) and XPU (Intel GPU accelerator), and what should change next if we want to scale without breaking the scientific workflow?

The answer from the code is fairly clear. The current training path is plain Distributed Data Parallel (DDP). It is not using Fully Sharded Data Parallel (FSDP), ZeRO (Zero Redundancy Optimizer), or tensor parallelism. That is not a weakness. For where this project stands today, it is the right thing to stabilize first.

> The short version: this is currently a DDP-first climate-emulator codebase with AMP (Automatic Mixed Precision) hooks, activation-checkpointing hooks, and checkpoint-restore support, but no committed sharded-training path yet.

## Scientific basis: why this workload matters

The scientific basis of the workflow is PlaSim, an intermediate-complexity climate model that is much more useful for emulator research than synthetic toy data. PlaSim is complex enough to make the learning problem physically meaningful, but still tractable enough to support repeated experiments and systems work. In this codebase, the emulator learns multivariate atmospheric state with upper-air and surface fields, then rolls those states forward in time.

That makes this an emulator in the strong sense, not just a pattern recognizer. The model is trying to learn an evolution operator over a gridded atmospheric state. Once you view it that way, the systems questions become part of the science:

- rollout stability matters, not just one-step loss;
- calendar and climatology logic matter, not just generic tensor throughput;
- latitude-aware metrics matter, because the sphere is not an image plane;
- restart behavior matters, because long-running HPC (High-Performance Computing) jobs are part of the workflow.

The repository reflects that scientific basis directly. Validation is latitude-weighted rather than naively averaged:

```python
def latitude_weighting_factor_torch(latitudes):
    lat_weights_unweighted = torch.cos(3.1416 / 180. * latitudes)
    return latitudes.size()[0] * lat_weights_unweighted / torch.sum(lat_weights_unweighted)

def weighted_rmse_torch_channels(pred, target, latitudes):
    weight = torch.reshape(latitude_weighting_factor_torch(latitudes), (1, 1, -1, 1))
    result = torch.sqrt(torch.mean(weight * (pred - target)**2., dim=(-1, -2)))
    return result
```

The code also carries explicit climatology indexing and leap-year handling. That is a useful reminder that climate ML inherits domain logic all the way down. Portability work has to preserve those assumptions rather than treat them as incidental details.

## The parallelism the code actually uses today

The most important point for this article is simple: the committed training path is plain DDP.

In `train.py`, the distributed path is initialized with `torch.distributed`, the model is wrapped in `DistributedDataParallel`, the data loader uses `DistributedSampler`, and validation statistics are reconciled across ranks with `all_reduce`. That is the whole current parallel story.

```python
if params['world_size'] > 1:
    backend = get_default_ddp_backend()
    backend = os.environ.get('TORCH_DDP_BACKEND', backend)
    dist.init_process_group(backend=backend, init_method='env://')

...

if dist.is_initialized():
    self.model = DistributedDataParallel(
        self.model,
        device_ids=[params.local_rank],
        output_device=[params.local_rank],
        find_unused_parameters=True,
    )
```

The data path matches that design:

```python
sampler = DistributedSampler(dataset, shuffle=train) if distributed else None
```

and the validation path closes the loop explicitly:

```python
if dist.is_initialized():
    dist.all_reduce(valid_buff)
    dist.all_reduce(valid_surface_lwrmse)
    dist.all_reduce(valid_upper_air_lwrmse)
    for loss_tensor in multi_step_losses.values():
        dist.all_reduce(loss_tensor)
```

What is not present is just as important. There is no committed FSDP wrapper, no ZeRO-style optimizer sharding, and no tensor-parallel decomposition of the model. So relative to the usual menu of large-model strategies, this codebase sits squarely in the DDP bucket today.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/panguweather-ddp-overview.svg" alt="Diagram showing the current parallel training strategy: DistributedSampler shards batches across ranks, each rank holds a full model replica, and gradients are synchronized with all-reduce." />
  <figcaption>The current Aurora path is conventional DDP: each rank gets a shard of the batch, holds a full model replica, and synchronizes gradients. That keeps the semantics simple while the runtime path is still being hardened across CUDA and Intel XPU.</figcaption>
</figure>

## Why DDP is the right baseline for this Aurora work

When a codebase is being moved onto a new accelerator stack, it is usually a mistake to introduce too many new failure modes at once. DDP is not the most memory-efficient option, but it is the cleanest place to establish a supported path because:

- the training semantics are familiar and easier to debug;
- each rank still behaves like a normal full-model process;
- cross-rank synchronization is explicit;
- checkpoint and restore behavior stay conceptually simple;
- launcher, backend, and device-placement bugs stay separable from sharding bugs.

That matches the current Aurora handoff. The supported baseline is the Aurora smoke path plus one-node SFNO training, not universal support for every legacy config in the repository. That is the right scope. In porting work, a narrow supported path is much more valuable than broad but fragile claims.

The Aurora batch scripts make that visible. There is a focused two-rank DDP trainer smoke whose job is just to initialize `torch.distributed`, construct the trainer on each rank, and stop. Then there is a one-node SFNO training script for longer runs. That progression is exactly what you want on a new machine: initialize, smoke-test, restore, then train.

## Memory pressure shows up before exotic parallelism does

DDP is straightforward, but it pays for that simplicity by replicating model state on every device. Each rank owns its own copy of:

- model parameters,
- gradients,
- optimizer state,
- activations for the current step.

That is why memory pressure becomes central long before tensor parallelism makes sense.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/panguweather-memory-and-io.svg" alt="Diagram showing per-rank GPU memory with replicated model parameters, gradients, optimizer state, and activations, alongside a note that activations and optimizer state often dominate memory pressure in DDP." />
  <figcaption>Under DDP, every device carries the full training state. If memory becomes the limiter, the first question is not “should we jump to tensor parallelism?” but “which of parameters, gradients, optimizer state, or activations is actually dominating?”</figcaption>
</figure>

This repository already contains cheaper mitigation levers than sharded training. Both the Pangu model path and the SFNO path expose activation-checkpointing hooks, and the model code threads `checkpointing` and `use_reentrant` through the blocks:

```python
self.checkpointing = 0
self.use_reentrant = False
if hasattr(params, 'checkpointing'):
    self.checkpointing = params.checkpointing
if hasattr(params, 'use_reentrant'):
    self.use_reentrant = params.use_reentrant
```

and later:

```python
if self.checkpointing == 2 and train:
    x = checkpoint(self.layer1, x, use_reentrant=self.use_reentrant)
```

So the codebase does have a memory-relief path already. What is notable on Aurora is that the committed smoke configuration keeps it off by default:

```yaml
use_reentrant: False
checkpointing: 0
```

That choice makes sense. During bring-up, it is usually better to keep the baseline simple and deterministic, then turn on memory-saving mechanisms after the runtime path is stable.

## Floating-point policy is part of the systems story

One of the most practical changes in this work is that mixed precision is no longer treated as a single universal recipe. The AMP utilities are device-aware, and gradient scaling is only enabled on CUDA:

```python
def create_grad_scaler():
    if amp is None:
        return None
    device_type = get_device_name()
    if device_type == 'cuda':
        return amp.GradScaler()
    return None
```

That is exactly the right direction. CUDA and Intel XPU should not be forced through identical assumptions. The current code keeps the fp16 (16-bit floating point) scaler path for CUDA while allowing the XPU path to behave more naturally as a bf16 (bfloat16, brain floating point) oriented path. That is a much better foundation for reproducibility than pretending every accelerator stack wants the same numerical policy.

So if the model runs into memory or stability pressure, the sensible order of operations is:

1. keep the existing DDP path,
2. use AMP deliberately,
3. enable activation checkpointing where it helps,
4. profile the actual memory split,
5. only then consider sharded training.

That ordering matters because not every memory problem is really a parallelism problem.

## Aurora portability: launcher, backend, and queue discipline

The other reason to stabilize DDP first is that there was already substantial portability work to do without touching sharded training.

Aurora does not naturally look like a `torchrun` laptop workflow. The launch stack often comes through MPI (Message Passing Interface) or PMIx (Process Management Interface for Exascale), so the code now maps those launcher variables onto the environment names PyTorch expects:

```python
def populate_dist_env_from_mpi():
    env_map = {
        "RANK": ("PMIX_RANK", "PMI_RANK", "PALS_RANKID"),
        "WORLD_SIZE": ("PMIX_SIZE", "PMI_SIZE"),
        "LOCAL_RANK": ("PALS_LOCAL_RANKID", "PMI_LOCAL_RANK"),
    }
```

That is the kind of plumbing that determines whether DDP is actually portable across systems. The backend is also selected by active device rather than hard-coded for CUDA:

```python
def get_device():
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    ...
```

Operationally, the queue split on Aurora matters just as much:

- `debug` is the right queue for short smoke runs, setup validation, and trainer-init failure localization;
- `capacity` is the right queue for the longer one-node SFNO path;
- the committed two-rank smoke test is exactly the right bridge between single-rank bring-up and larger training.

That queue discipline is a real part of the engineering. Rapid turnaround is what makes portability work tractable.

## Where chunking and I/O really enter this codebase

The chunking question is worth handling carefully because it is relevant here, but not in exactly the same way as in xarray or Zarr benchmark talks.

The current training path is a multifile HDF5 (Hierarchical Data Format 5) workflow. The loader resolves a timestamp into a file such as `year_index.h5`, opens that file with `h5py`, and reads the variable subset needed for the current sample:

```python
def get_data_given_path(path, variables):
    with h5py.File(path, 'r') as f:
        data = {
            main_key: {
                sub_key: np.array(value)
                for sub_key, value in group.items()
                if sub_key in variables + ['time']
            }
            for main_key, group in f.items()
            if main_key in ['input']
        }
```

and the access path during training is driven from timestamps:

```python
data_file_path = get_out_path(self.data_dir, data_year, data_idx)
raw_data = get_data_given_path(data_file_path, self.variable_list_in)
```

So this is not a repo whose training loop is already centered on distributed Zarr rechunking. But chunking is still relevant, because DDP multiplies concurrent readers. Once several ranks are stepping through time-offset HDF5 files at once, storage layout becomes part of scaling behavior. If the on-disk layout does not match the access pattern, read amplification becomes a real bottleneck even when the model itself still fits in memory.

The place where chunk-aware thinking is already explicit is the inference output path. In `ensemble_inference.py`, the xarray dataset is chunked before being written:

```python
dataset = dataset.chunk({'ensemble_idx': 1, 'time': 1, self.params.lev: 1})
if self.params.use_sigma_levels and ('zg' in self.params.upper_air_variables or 'geopotential' in self.params.upper_air_variables):
    dataset = dataset.chunk({'plev': 1})
dataset.to_netcdf(os.path.join(savedir, filename))
```

That is a small but important clue about where this codebase can go next. The current training work is mostly about runtime portability. The next layer of systems work, especially if multi-node scale becomes important, is to make data layout match the access pattern more deliberately.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/panguweather-chunking-path.svg" alt="Diagram showing ranks reading time-step HDF5 files and a comparison between poorly aligned versus access-aligned chunk layouts for climate data." />
  <figcaption>Chunking is not the main training abstraction in this repo today, but it still matters. DDP increases concurrent readers, so storage layout and access pattern start to matter well before a model demands tensor parallelism.</figcaption>
</figure>

For this codebase, that means the right chunking discussion is not "we already solved this with rechunked Zarr." It is "the training path already has a concrete per-rank access pattern, so if I/O starts to dominate, chunk-aligned storage is one of the highest-leverage next optimizations."

Compression belongs in the same conversation. Smaller files can help storage pressure, but compression only helps training throughput when the chunk geometry still matches the way ranks read data. Otherwise, the workflow just trades one bottleneck for another: less data on disk, but more decompression and more unnecessary reads.

## What still needs work before scaling further

The Aurora documentation is explicit that the current path is not yet "every historical config on every machine." The main remaining issues are mundane but important:

- sigma-level metadata still needs to match the Aurora dataset exactly;
- some inherited year ranges still reflect non-Aurora copies of the data;
- old filename assumptions still show up in copied configs;
- launcher scripts across systems are not yet fully standardized on `torch.distributed.run` or `torchrun`.

That last point is worth calling out because the codebase currently mixes both worlds. Some paths already use the newer launcher, while others still rely on `torch.distributed.launch`. Standardizing that layer would remove one more source of avoidable variation across machines.

That matters because these are exactly the kinds of issues that can be mistaken for parallel-scaling failures when they are really dataset or launcher mismatches.

The practical roadmap I would use for this codebase is:

| Area | Current state | Best next step |
| --- | --- | --- |
| Training parallelism | Plain DDP | Keep DDP as the supported Aurora baseline |
| Memory relief | AMP hooks and activation checkpointing exist | Turn those knobs on deliberately before changing the parallel algorithm |
| Launcher portability | Mixed launcher state across systems | Standardize around `torch.distributed.run` where possible |
| Aurora configs | Smoke path is supported, legacy configs vary | Fix sigma-level, year-range, and filename mismatches first |
| Data path | Multifile HDF5 reads per rank | Profile I/O and make layout or chunking match real access patterns |
| Next major parallel upgrade | Not yet present | Prototype FSDP only if per-device memory becomes the true blocker |

The key point is that FSDP is the next likely parallelism upgrade if the model stops fitting comfortably per device. Tensor parallelism is not where I would go first here. That is usually the answer only when a single layer is too large for one device, and this codebase is not there yet.

## What I see as the contribution

The contribution of this Aurora work is not that it introduced every modern scaling technique at once. The contribution is that it established a defensible, scientifically meaningful, portable baseline:

- the model now has a supported DDP path on Aurora;
- the runtime understands CUDA and Intel XPU rather than assuming one vendor;
- checkpoint and restore were treated as part of the contract, not an afterthought;
- smoke tests and queue-aware scripts make debugging feasible;
- the code now has a clearer separation between "what is supported now" and "what should come next."

That is often the right kind of progress in research software. Before we chase the most sophisticated sharding scheme, we need a workflow that the science team can rerun, debug, and trust.

## Closing thought

Climate-emulator work on supercomputers is rarely blocked by model architecture alone. More often, it is blocked by the less glamorous details: how ranks are launched, how memory is consumed, how files are laid out, how checkpoints are restored, and how quickly failures can be diagnosed.

This Aurora effort moved the codebase forward by tightening exactly those pieces. Today the code is a DDP-first emulator workflow with portable device logic and a supported one-node path. The next steps are clear: harden the data and launcher assumptions, turn on the existing memory-saving knobs where needed, and only then decide whether sharded training is worth the added complexity.
