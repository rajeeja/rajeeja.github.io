---
title: "From RGG and MeshKit to the MOOSE Reactor Module"
date: 2022-05-08
permalink: /blog/rgg-meshkit-moose-reactor-module/
categories:
  - blog
tags:
  - reactor-meshing
  - meshkit
  - neams
  - nuclear-engineering
  - moose
  - scientific-computing
excerpt: "A retrospective on the RGG and MeshKit work in DOE NEAMS, including parallel CoreGen, the MONJU reactor mesh, and how those ideas connect to later MOOSE Reactor Module meshing work."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">Research retrospective &middot; May 8, 2022</p>
  <h1 class="article-title">From RGG and MeshKit to the MOOSE Reactor Module</h1>
  <p class="article-dek">How my RGG and MeshKit work on parallel reactor core meshing shaped my view of open, reusable meshing workflows for nuclear simulation.</p>
</div>

The 2023 paper ["MOOSE Reactor Module: An Open-Source Capability for Meshing Nuclear Reactor Geometries"](https://www.osti.gov/pages/biblio/2323542) caught my attention because it represents a direction I have cared about for a long time: making reactor geometry and mesh generation accessible, repeatable, and close to the physics workflow. The closer reference for the work described here is the RGG and MeshKit line from DOE NEAMS, especially ["RGG: Reactor Geometry (and Mesh) Generator"](https://www.mcs.anl.gov/papers/P2005-0612.pdf) and ["Generating Unstructured Nuclear Reactor Core Meshes in Parallel"](https://doi.org/10.1016/j.proeng.2014.10.396).

The paper describes an open-source MOOSE Reactor module for common reactor geometries: hexagonal pins, assemblies, and cores; Cartesian geometry support; control drums; core periphery triangulation; automatic tagging of physics regions; and Exodus II export for finite element workflows. The emphasis is not only on meshing as a geometry exercise. It is on lowering the barrier for reactor analysts and removing fragile handoffs between geometry construction, mesh generation, and multiphysics simulation.

That is exactly the problem space that motivated my work on RGG and MeshKit in the DOE NEAMS program from 2009 to 2016. I led the MeshKit project during that period and worked on RGG, the Reactor Geometry and Mesh Generator, to automate the construction of reactor core geometry and meshes for simulation teams. The important distinction is that RGG did not stop at convenient input generation. We pushed the reactor core assembly step into parallel execution so large full-core meshes could be generated on machines where serial meshing would fail or take far too long.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/rgg-meshkit-moose-lineage.svg" alt="Timeline connecting RGG, MeshKit, and the MOOSE Reactor Module." />
  <figcaption>RGG and MeshKit focused on making reactor geometry explicit, reusable, and scalable. The MOOSE Reactor Module brings related workflow goals directly into the MOOSE ecosystem.</figcaption>
</figure>

## The original problem

Nuclear reactor geometries have structure that is obvious to reactor engineers but awkward for general-purpose CAD and meshing tools. A reactor core is not just an arbitrary solid model. It is a hierarchy: pins inside assemblies, assemblies inside cores, repeated lattice patterns, material regions, boundary layers, and solver-specific region tags.

Before tools like RGG and MeshKit, a lot of this structure had to be reconstructed manually in external tools. That made the workflow slow and error-prone:

- a small change to a pin, duct, or assembly pattern could require rebuilding large parts of the model;
- material and boundary tags could be lost or rebuilt inconsistently;
- analysts had to move between geometry tools, meshing tools, and solver input formats;
- automation was difficult because the reactor hierarchy was implicit rather than represented as data.

The key idea behind RGG was to encode the reactor lattice hierarchy directly. Instead of treating the reactor as one large manually drawn geometry, we represented the design in terms of reusable reactor concepts: pins, assemblies, lattice layouts, axial regions, and core-level repetition. Once that hierarchy was explicit, geometry and mesh generation could become a repeatable workflow.

## What RGG contributed

RGG, the Reactor Geometry and Mesh Generator, was built around the idea that reactor core meshing should start from the structure of the reactor. The ICAPP paper ["RGG: Reactor Geometry (and Mesh) Generator"](https://www.mcs.anl.gov/papers/P2005-0612.pdf) presented the AssyGen and CoreGen workflow: generate assembly geometry, mesh the assembly models, then copy, move, merge, and tag assemblies into a full reactor core model.

The earlier lattice-hierarchy paper that led into RGG won the 2010 International Meshing Roundtable Best Paper Award, but the more important contribution was practical: it showed that reactor-specific structure could be used to automate meshing workflows that would otherwise require substantial manual effort.

In practice, RGG helped with:

- building geometry from reactor concepts rather than raw CAD operations;
- preserving the relationship between pins, assemblies, cores, and material regions;
- producing meshes suitable for downstream reactor physics and multiphysics codes;
- making model generation repeatable when users changed design parameters;
- reducing the amount of solver-specific handwork required to get from design to analysis.

That line of work was pushed further in ["Generating Unstructured Nuclear Reactor Core Meshes in Parallel"](https://doi.org/10.1016/j.proeng.2014.10.396). The parallel version of CoreGen exploited coarse-grained parallelism during reactor assembly and core mesh generation: processors were assigned copy/move work, shared interfaces were merged in parallel, metadata was propagated, and the final mesh was saved using MOAB's parallel I/O path.

The MONJU example is the one I like most because it shows why this mattered. In that paper, the full-core MONJU reactor model used 8 assembly types and 715 assemblies. CoreGen ran on 712 processors and produced a 101 million hexahedral element mesh from scratch in about 7 minutes, with the CoreGen stage itself taking about 90 seconds. The mesh file was about 14 GB, and the serial version could not run because the problem did not fit in memory. That is the practical value of parallel meshing: it changes what reactor models are feasible to build.

## MeshKit as the broader framework

RGG was part of a larger effort: MeshKit, an open-source C++ toolkit for mesh generation and mesh-based workflows. I served as principal investigator and software lead for MeshKit within DOE NEAMS from 2009 to 2016.

MeshKit gave us a place to build reactor meshing tools as reusable software rather than one-off scripts. The project connected geometry, mesh generation, mesh operations, and file-format support in a way that reactor simulation teams could use across multiple analysis paths.

My work in MeshKit included:

- leading development of reactor geometry and mesh generation capabilities;
- building and maintaining RGG documentation and user workflows;
- developing parallel reactor core mesh generation through CoreGen;
- supporting boundary-layer mesh generation through PostBL;
- improving mesh copy, move, merge, and multi-format workflows;
- coordinating NEAMS deliverables and releases with collaborators at Argonne and other labs.

That experience shaped how I think about scientific software. The hard part is rarely just the algorithm. The hard part is turning the algorithm into a workflow that other scientists can trust, rerun, modify, and connect to their own codes.

## Publications and reports from the RGG / MeshKit arc

The work from 2009 to 2016 produced a set of papers, reports, manuals, and release artifacts. The RGG papers are the primary references for the reactor geometry generator and the parallel core assembly algorithm.

<div class="table-scroll">
<table>
<thead>
<tr>
  <th>Year</th>
  <th>Work</th>
  <th>Contribution</th>
</tr>
</thead>
<tbody>
<tr>
  <td>2012</td>
  <td><a href="https://www.mcs.anl.gov/papers/P2005-0612.pdf">Jain and Tautges, "RGG: Reactor Geometry (and Mesh) Generator," ICAPP.</a></td>
  <td>Presented RGG as a practical reactor geometry and mesh generator built around AssyGen, CoreGen, and the reactor lattice hierarchy.</td>
</tr>
<tr>
  <td>2014</td>
  <td><a href="https://doi.org/10.1016/j.proeng.2014.10.396">Jain and Tautges, "Generating Unstructured Nuclear Reactor Core Meshes in Parallel," <em>Procedia Engineering</em>.</a></td>
  <td>Introduced the parallel CoreGen workflow, reported speedups, and demonstrated large full-core examples including MONJU.</td>
</tr>
<tr>
  <td>2010</td>
  <td>Tautges and Jain, "Creating Geometry and Mesh Models for Nuclear Reactor Core Geometries Using a Lattice Hierarchy-Based Approach," International Meshing Roundtable. Best Paper Award.</td>
  <td>Introduced the lattice-hierarchy approach for representing reactor pins, assemblies, and cores as structured meshing input.</td>
</tr>
<tr>
  <td>2011 / 2012</td>
  <td>Tautges and Jain, "Creating geometry and mesh models for nuclear reactor core geometries using a lattice hierarchy-based approach," <em>Engineering with Computers</em>.</td>
  <td>Journal version of the RGG foundation, later cited by the MOOSE Reactor Module paper.</td>
</tr>
<tr>
  <td>2013</td>
  <td>Jain and Tautges, "PostBL: Post-Mesh Boundary Layer Mesh Generation Tool," International Meshing Roundtable.</td>
  <td>Extended the workflow with boundary-layer mesh generation for cases where near-wall resolution mattered.</td>
</tr>
<tr>
  <td>2014</td>
  <td>Mahadevan, Merzari, Tautges, Jain, Obabko, Smith, and Fischer, "High-resolution coupled physics solvers for analysing fine-scale nuclear reactor design problems," <em>Philosophical Transactions of the Royal Society A</em>.</td>
  <td>Connected meshing work to coupled high-resolution reactor physics workflows.</td>
</tr>
<tr>
  <td>2015</td>
  <td>Jain and Tautges, "NEAMS MeshKit: Nuclear Reactor Mesh Generation Solutions," ICAPP.</td>
  <td>Summarized MeshKit reactor meshing capabilities for the NEAMS community.</td>
</tr>
<tr>
  <td>2015</td>
  <td>Jain, Mahadevan, and O'Bara, "Simplifying Workflow for Reactor Assembly and Full-Core Modeling," MC2015.</td>
  <td>Focused on reducing workflow complexity for assembly and full-core reactor modeling.</td>
</tr>
<tr>
  <td>2015</td>
  <td>Jain, Vanderzee, and Mahadevan, "Update on Development of Mesh Generation Algorithms in MeshKit," ANL/MCS-TM-355.</td>
  <td>Documented MeshKit algorithm development and release progress.</td>
</tr>
<tr>
  <td>2015</td>
  <td>Jain and Mahadevan, "Documentation for MeshKit-Reactor Geometry (&amp;mesh) Generator," ANL/MCS-TM-354.</td>
  <td>Produced user-facing documentation for RGG inside the MeshKit ecosystem.</td>
</tr>
<tr>
  <td>2016</td>
  <td>Jain, Vanderzee, Grindeanu, and Mahadevan, "Mesh Generation and Algorithm Development for NEAMS."</td>
  <td>Reported MeshKit v1.42-era capabilities and algorithm development to the NEAMS program.</td>
</tr>
</tbody>
</table>
</div>

## How this connects to the MOOSE Reactor Module

The MOOSE Reactor Module is not a direct continuation of MeshKit in the sense of sharing the same codebase. It is better understood as a continuation of a workflow philosophy.

The MOOSE paper emphasizes several advantages: open-source availability, low barrier to entry, fast mesh generation, volume preservation for meshed fuel pins, automatic region tagging, and a simpler path from reactor geometry to MOOSE-based analysis. MOOSE itself is a parallel finite element framework, but the Reactor Module meshing paper does not present the meshing step as a parallel CoreGen-style algorithm, nor does it report processor-scaling results for mesh generation. That is an important difference. RGG and MeshKit were already aimed at the scaling side of the problem: generating very large reactor meshes, including MONJU, by distributing the core assembly process across processors.

So the overlap is real, but it is not identical. MOOSE Reactor Module and its follow-on reactor meshing work bring reactor-aware meshing closer to MOOSE applications. RGG and MeshKit attacked the earlier problem of making reactor geometry generation open, repeatable, and parallel enough for large-core models. Both directions matter:

- represent reactor layouts using domain concepts, not only generic geometry entities;
- automate repeated lattice and core construction;
- keep material and physics-region information attached to the mesh;
- make meshing reproducible enough for design studies;
- scale the core assembly step when the full model is too large for a desktop workflow;
- reduce dependence on fragile external tool chains.

The newer module has an additional advantage: it lives inside the MOOSE ecosystem where many NEAMS physics applications already run. That matters. The closer meshing is to the solver workflow, the less friction analysts face when they want to run Griffin, Bison, Sockeye, Tensor Mechanics, or other MOOSE-based applications.

That is why I see my RGG and MeshKit work as part of the foundation for this direction. We were pushing reactor meshing away from manual geometry manipulation and toward open, scriptable, domain-aware workflows, with a parallel path for large reactor cores. The MOOSE Reactor Module reflects a related direction in a modern framework, and the next natural step is to keep closing the gap between convenient in-framework meshing and scalable full-core mesh generation.

## What I learned from leading MeshKit

Leading MeshKit taught me lessons that still show up in my later scientific software work, including UXarray, FLASH-X, and HPC ML workflows.

First, domain structure matters. If the software understands the scientific object, the workflow becomes simpler. RGG understood reactors as lattices of pins and assemblies. UXarray understands unstructured climate grids as meshes with topology and geometry. In both cases, the software becomes useful because it models the scientist's object directly.

Second, open workflows matter as much as open code. Reactor analysts needed more than source code; they needed documentation, examples, releases, file-format support, and trust that the workflow could be repeated after design changes. That same lesson applies to every scientific software project I have worked on since.

Third, meshing is scientific infrastructure. A mesh is not just a preprocessing artifact. It controls what the solver can represent, how regions are tagged, how coupling happens, and how results are interpreted. Getting meshing closer to the physics workflow improves the whole simulation campaign. Making meshing parallel changes the scale of the campaign itself.

## Closing thought

The MOOSE Reactor Module paper is exciting to me because it shows the reactor meshing community continuing to move toward open, domain-aware, workflow-integrated tools. My work on RGG and MeshKit was an earlier and more parallel chapter in that story: encode the reactor hierarchy, automate the mesh, preserve the physics context, and make very large reactor meshes possible.

That remains the right direction. Whether the tool is RGG, MeshKit, MOOSE, or a future system, the durable goal is the same: make complex reactor simulation workflows less manual, more reproducible, and more accessible to the scientists and engineers who need them.
