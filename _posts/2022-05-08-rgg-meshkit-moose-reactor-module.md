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
excerpt: "A retrospective on my RGG and MeshKit work in DOE NEAMS, how it helped shape my thinking about open reactor meshing workflows, and why I see the same design goals reflected in the MOOSE Reactor Module."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">Research retrospective &middot; May 8, 2022</p>
  <h1 class="article-title">From RGG and MeshKit to the MOOSE Reactor Module</h1>
  <p class="article-dek">How early work on automated reactor geometry and mesh generation shaped my view of open, reusable meshing workflows for nuclear simulation.</p>
</div>

The 2023 paper ["MOOSE Reactor Module: An Open-Source Capability for Meshing Nuclear Reactor Geometries"](https://www.osti.gov/pages/biblio/2323542) caught my attention because it represents a direction I have cared about for a long time: making reactor geometry and mesh generation accessible, repeatable, and close to the physics workflow.

The paper describes an open-source MOOSE Reactor module for common reactor geometries: hexagonal pins, assemblies, and cores; Cartesian geometry support; control drums; core periphery triangulation; automatic tagging of physics regions; and Exodus II export for finite element workflows. The emphasis is not only on meshing as a geometry exercise. It is on lowering the barrier for reactor analysts and removing fragile handoffs between geometry construction, mesh generation, and multiphysics simulation.

That is exactly the problem space that motivated my work on RGG and MeshKit in the DOE NEAMS program from 2009 to 2016. I led the MeshKit project during that period and worked on RGG, the Reactor Geometry and Mesh Generator, to automate the construction of reactor core geometry and meshes for simulation teams. Looking back, I see a clear intellectual line between those efforts and newer MOOSE-native meshing tools: reactor analysts should not need to become meshing-tool specialists just to build a trustworthy model.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/rgg-meshkit-moose-lineage.svg" alt="Timeline connecting RGG, MeshKit, and the MOOSE Reactor Module." />
  <figcaption>RGG and MeshKit focused on making reactor geometry explicit and reusable. The MOOSE Reactor Module brings similar workflow goals directly into the MOOSE ecosystem.</figcaption>
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

RGG, the Reactor Geometry and Mesh Generator, was built around the idea that reactor core meshing should start from the structure of the reactor. The work that Tim Tautges and I published at the International Meshing Roundtable in 2010, later expanded in *Engineering with Computers*, described the lattice-hierarchy approach for creating geometry and mesh models for nuclear reactor core geometries.

That work won the 2010 International Meshing Roundtable Best Paper Award, but the more important contribution was practical: it showed that reactor-specific structure could be used to automate meshing workflows that would otherwise require substantial manual effort.

In practice, RGG helped with:

- building geometry from reactor concepts rather than raw CAD operations;
- preserving the relationship between pins, assemblies, cores, and material regions;
- producing meshes suitable for downstream reactor physics and multiphysics codes;
- making model generation repeatable when users changed design parameters;
- reducing the amount of solver-specific handwork required to get from design to analysis.

The current MOOSE Reactor Module paper cites our lattice-hierarchy work, which is a nice reminder that these design ideas stayed relevant. The details of the software ecosystem changed, but the underlying problem did not: reactor workflows need meshing tools that understand reactor structure.

## MeshKit as the broader framework

RGG was part of a larger effort: MeshKit, an open-source C++ toolkit for mesh generation and mesh-based workflows. I served as principal investigator and software lead for MeshKit within DOE NEAMS from 2009 to 2016.

MeshKit gave us a place to build reactor meshing tools as reusable software rather than one-off scripts. The project connected geometry, mesh generation, mesh operations, and file-format support in a way that reactor simulation teams could use across multiple analysis paths.

My work in MeshKit included:

- leading development of reactor geometry and mesh generation capabilities;
- building and maintaining RGG documentation and user workflows;
- developing parallel reactor core mesh generation;
- supporting boundary-layer mesh generation through PostBL;
- improving mesh copy, move, merge, and multi-format workflows;
- coordinating NEAMS deliverables and releases with collaborators at Argonne and other labs.

That experience shaped how I think about scientific software. The hard part is rarely just the algorithm. The hard part is turning the algorithm into a workflow that other scientists can trust, rerun, modify, and connect to their own codes.

## Publications and reports from the RGG / MeshKit arc

The work from 2009 to 2016 produced a set of papers, reports, manuals, and release artifacts. Together they show the progression from a lattice-hierarchy idea to a broader reactor meshing framework.

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
  <td>2012</td>
  <td>Jain and Tautges, "RGG: Reactor Geometry (and Mesh) Generator," ICAPP.</td>
  <td>Presented RGG as a practical reactor geometry and mesh generator for nuclear engineering workflows.</td>
</tr>
<tr>
  <td>2012</td>
  <td>Mohanty, Jain, Majumdar, Tautges, and Srinivasan, "Coupled Field Structural Analysis of HTGR Fuel Brick Using Abaqus," ICAPP.</td>
  <td>Applied reactor meshing and structural-analysis workflows to high-temperature gas reactor fuel-brick modeling.</td>
</tr>
<tr>
  <td>2013</td>
  <td>Jain and Tautges, "PostBL: Post-Mesh Boundary Layer Mesh Generation Tool," International Meshing Roundtable.</td>
  <td>Extended the workflow with boundary-layer mesh generation for cases where near-wall resolution mattered.</td>
</tr>
<tr>
  <td>2014</td>
  <td>Jain and Tautges, "Generating Unstructured Nuclear Reactor Core Meshes in Parallel," <em>Procedia Engineering</em>.</td>
  <td>Moved the reactor meshing workflow toward parallel generation for larger core-scale models.</td>
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

The MOOSE paper emphasizes several advantages: open-source availability, low barrier to entry, fast mesh generation, volume preservation for meshed fuel pins, automatic region tagging, and a simpler path from reactor geometry to MOOSE-based analysis. Those are the same kinds of goals that motivated RGG and MeshKit:

- represent reactor layouts using domain concepts, not only generic geometry entities;
- automate repeated lattice and core construction;
- keep material and physics-region information attached to the mesh;
- make meshing reproducible enough for design studies;
- reduce dependence on fragile external tool chains.

The newer module has an additional advantage: it lives inside the MOOSE ecosystem where many NEAMS physics applications already run. That matters. The closer meshing is to the solver workflow, the less friction analysts face when they want to run Griffin, Bison, Sockeye, Tensor Mechanics, or other MOOSE-based applications.

That is why I see my RGG and MeshKit work as part of the foundation for this direction. We were pushing reactor meshing away from manual geometry manipulation and toward open, scriptable, domain-aware workflows. The MOOSE Reactor Module reflects that same direction in a modern framework.

## What I learned from leading MeshKit

Leading MeshKit taught me lessons that still show up in my later scientific software work, including UXarray, FLASH-X, and HPC ML workflows.

First, domain structure matters. If the software understands the scientific object, the workflow becomes simpler. RGG understood reactors as lattices of pins and assemblies. UXarray understands unstructured climate grids as meshes with topology and geometry. In both cases, the software becomes useful because it models the scientist's object directly.

Second, open workflows matter as much as open code. Reactor analysts needed more than source code; they needed documentation, examples, releases, file-format support, and trust that the workflow could be repeated after design changes. That same lesson applies to every scientific software project I have worked on since.

Third, meshing is scientific infrastructure. A mesh is not just a preprocessing artifact. It controls what the solver can represent, how regions are tagged, how coupling happens, and how results are interpreted. Getting meshing closer to the physics workflow improves the whole simulation campaign.

## Closing thought

The MOOSE Reactor Module paper is exciting to me because it shows the reactor meshing community continuing to move toward open, domain-aware, workflow-integrated tools. My work on RGG and MeshKit was an earlier chapter in that story: encode the reactor hierarchy, automate the mesh, preserve the physics context, and make the workflow usable by real analysts.

That remains the right direction. Whether the tool is RGG, MeshKit, MOOSE, or a future system, the durable goal is the same: make complex reactor simulation workflows less manual, more reproducible, and more accessible to the scientists and engineers who need them.

## References

- Shemon, E., Miao, Y., Kumar, S., Mo, K., Jung, Y. S., Oaks, A., Richards, S., Giudicelli, G. L., Harbour, L. H., and Stogner, R. H. ["MOOSE Reactor Module: An Open-Source Capability for Meshing Nuclear Reactor Geometries."](https://www.osti.gov/pages/biblio/2323542) *Nuclear Science and Engineering*, 2023. DOI: [10.1080/00295639.2022.2149231](https://doi.org/10.1080/00295639.2022.2149231).
- Tautges, T. J. and Jain, R. ["Creating geometry and mesh models for nuclear reactor core geometries using a lattice hierarchy-based approach."](https://doi.org/10.1007/s00366-011-0236-8) *Engineering with Computers*, 2012.
