---
title: "Urban Microclimate at Scale: Array of Things, EnergyPlus, and CFD for Chicago"
date: 2020-07-01
permalink: /blog/urban-ecp-array-of-things/
categories:
  - blog
tags:
  - urban-computing
  - hpc
  - cfd
  - scientific-computing
  - argonne
  - array-of-things
excerpt: "How a seed-funded urban exascale project with Charlie Catlett connected Chicago's IoT sensor network, mesoscale weather models, building energy simulation, and high-fidelity CFD into one coherent research program."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner article-banner--warm">
  <p class="eyebrow">Urban computing &middot; 2020</p>
  <h1 class="article-title">Urban Microclimate at Scale: Array of Things, EnergyPlus, and CFD for Chicago</h1>
  <p class="article-dek">How a seed-funded urban exascale project connected Chicago's IoT sensor network, mesoscale weather models, building energy simulation, and high-fidelity CFD into one coherent research program.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--amber">urban computing</span>
  <span class="post-tag post-tag--blue">CFD</span>
  <span class="post-tag post-tag--green">IoT / sensors</span>
  <span class="post-tag post-tag--violet">HPC</span>
  <span class="post-tag post-tag--teal">climate</span>
</div>

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">3</span>
    <span class="stat-card__label">coupled simulation scales: WRF → EnergyPlus → Nek5000</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">2–5°C</span>
    <span class="stat-card__label">urban heat island effect in dense city cores</span>
  </div>
  <div class="stat-card stat-card--green">
    <span class="stat-card__value">100s</span>
    <span class="stat-card__label">Array of Things sensor nodes across Chicago</span>
  </div>
</div>

From 2016 to 2019 I led a seed-funded urban computing effort at Argonne in collaboration with Charlie Catlett, who at the time was directing the Array of Things project and Argonne's urban science program. The goal was to bring exascale-level computation to city-scale environmental science: couple real sensor observations with mesoscale weather models and high-fidelity computational fluid dynamics to understand how urban geometry, buildings, and local climate interact at the street level.

The work produced a peer-reviewed journal paper, several AGU and International Conference on Urban Climate presentations, and a multi-code computational workflow connecting tools that operate at very different spatial and temporal scales.

## Why urban microclimate is hard to model

When you watch a weather forecast, the model behind it divides the atmosphere into grid cells that are typically 1 to 13 kilometers across. At that resolution a cell covers dozens of city blocks. Temperature, wind speed, humidity — these are averaged over an entire neighborhood. That is useful for knowing whether to bring an umbrella, but it tells you almost nothing about conditions at street level in a dense city.

Urban environments break the assumptions that work fine over open terrain. Buildings create wind tunnels and sheltered zones. Dark pavements and rooftops absorb more solar radiation than vegetation. Air conditioners dump heat from buildings into the street. Heat emitted by one building changes the microclimate of the buildings around it. These effects are real, measurable, and important — they drive the *urban heat island* effect, where dense city cores can be 2–5 °C hotter than surrounding suburbs on summer nights.

Understanding and predicting urban microclimate requires physics-based simulation at scales much finer than a standard weather model — but weather models provide the only practical source of large-scale atmospheric boundary conditions. The research problem is how to connect the two scales: take the output of a regional weather model and use it to drive fine-resolution building and street-level simulation, while feeding back what happens at street level to improve the larger-scale picture.

## The Array of Things: treating a city as a scientific instrument

The Array of Things (AoT) project, led by Charlie Catlett at Argonne and the University of Chicago, took a direct approach to the observational gap. Instead of relying on a handful of airport weather stations — the traditional source of urban ground-truth data — AoT deployed a network of sensor nodes across Chicago neighborhoods.

Each node, mounted on streetlight poles throughout the city, continuously measured temperature, humidity, pressure, air quality (ozone, particulates, SO₂, NO₂), light intensity, pedestrian and vehicle counts, and sound levels. With hundreds of nodes active across Chicago, the network turned the city itself into a distributed environmental measurement instrument — capturing spatial variability in temperature and air quality that a sparse station network simply cannot see.

For modeling purposes, this matters in two ways. First, AoT data provides validation ground truth: if your simulation predicts a temperature gradient between the Loop and Lincoln Park, you can check it against actual sensor readings. Second, spatially dense observations support data-driven analysis directly — mapping heat vulnerability, identifying neighborhoods where mitigation interventions would have the largest effect, and detecting anomalies that models might miss.

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/urban-ecp-workflow.svg" alt="Three-layer urban simulation workflow: WRF/HRRR → EnergyPlus → Nek5000 LES" />
  <figcaption>The three nested simulation scales. Each layer provides boundary conditions for the one below it — and AoT sensor data provides ground-truth validation at street level.</figcaption>
</figure>

## Three modeling layers: from regional weather to building walls

The simulation workflow we built operated at three nested spatial scales.

### Layer 1: Mesoscale weather — WRF and HRRR

The Weather Research and Forecasting model (WRF) is an open-source numerical weather prediction system developed jointly by NCAR, NOAA, and other institutions. It simulates the atmosphere by dividing a domain into a 3D grid and solving equations for fluid dynamics, thermodynamics, moisture, and radiation at each grid point forward in time. WRF can be configured at horizontal resolutions from tens of kilometers down to a few hundred meters.

HRRR (High-Resolution Rapid Refresh) is a NOAA operational analysis product that runs WRF over the continental United States at 3 km horizontal resolution, updated every hour with real observations assimilated in. We used HRRR output as our outer boundary condition — the large-scale atmospheric state (wind, temperature, humidity profiles) that drives everything at smaller scales.

WRF and HRRR give us a physically consistent three-dimensional picture of the atmosphere above Chicago. But at 3 km resolution, they cannot resolve the street canyons, building facades, or block-scale heat sources that define microclimate at the human scale.

### Layer 2: Building energy — EnergyPlus

EnergyPlus is the DOE building energy simulation tool, developed by LBNL and NREL. It simulates the thermal behavior of a building: how heat moves through walls, roofs, and windows; how HVAC systems respond; how much energy the building consumes; and how much heat the building releases back to the surrounding environment.

Standard EnergyPlus practice uses weather data from a *typical meteorological year* — a statistical average of conditions at a weather station, usually an airport. For urban buildings, airport weather is a poor proxy. Wind speeds, temperatures, and humidity can differ significantly between an airport 20 miles away and a street in the Loop, especially during heat waves when the urban heat island effect is strongest.

Our paper ["Representation and evolution of urban weather boundary conditions in downtown Chicago"](https://doi.org/10.1080/19401493.2018.1534275) (Jain, Luo, Sever, Hong, Catlett, *Journal of Building Performance Simulation*, 2020) developed the method for replacing the static airport weather file with time-varying, spatially specific boundary conditions derived from WRF and HRRR. We mapped the mesoscale model output onto each building's exterior surfaces as a time series — giving EnergyPlus access to the actual atmospheric state at the building's location rather than a regional average from an airport.

The paper demonstrated this on a test area in downtown Chicago and showed that high-resolution weather inputs change the simulated energy load, particularly during periods when the urban environment departs most from airport conditions. Buildings also emit heat — waste heat from HVAC condensers, for example — which feeds back into the local temperature field. Capturing that feedback loop is part of what motivated the coupling work.

### Layer 3: Street-level fluid dynamics — Nek5000 and LES

For the highest-resolution layer, we used Nek5000, the spectral-element computational fluid dynamics code developed at Argonne by Paul Fischer's group. Nek5000 solves the Navier-Stokes equations for incompressible flow using high-order polynomial basis functions on unstructured hexahedral meshes, with exceptional parallel scaling on large supercomputers.

The specific technique we applied was *large-eddy simulation* (LES) — in particular, wall-resolved LES. LES resolves the large turbulent eddies in the flow directly and models only the small-scale eddies below the grid resolution. Wall-resolved means the mesh is fine enough near building surfaces to directly capture the velocity gradient in the boundary layer, rather than using a wall model. This is computationally expensive but produces accurate predictions of drag, heat transfer, and flow separation at building corners and street intersections.

**I built the entire downtown Chicago urban geometry model** that served as the computational domain for this work. The model, documented on the [SIGMA urban modeling page](https://sigma.mcs.anl.gov/meshes/urban-modeling/), captures the realistic 3D geometry of downtown Chicago buildings — including architecturally complex structures like Lake Point Tower, whose distinctive trefoil (three-lobed clover) plan creates unusual wake patterns and recirculation zones that simpler box-building approximations miss entirely. Getting buildings like Lake Point Tower into a CFD mesh at sufficient resolution to resolve boundary layers and street-canyon flow is a non-trivial geometry and meshing problem, drawing directly on the mesh generation experience from the MeshKit and reactor work.

WRF-urban output provided the inlet boundary conditions for the Nek5000 domain. The resulting simulations, presented at the 2018 International Conference on Urban Climate ([Obabko, Jain et al.](https://ui.adsabs.harvard.edu/)) and the 2019 AGU Fall Meeting ([Jacob, Sever, Obabko, Jain, Catlett](https://ui.adsabs.harvard.edu/abs/2019AGUFM.A11M2784J/abstract)), showed street-canyon flow patterns — recirculation zones, channeling of wind through building gaps, regions of stagnant air — that the coarser WRF model cannot represent.

## Heat mitigation and neighborhood-scale analysis

A parallel track used AoT sensor data more directly. The 2018 AGU abstract ([Silva, Sharma, Budhathoki, Jain, Catlett](https://ui.adsabs.harvard.edu/abs/2018AGUFMPA21D0986S/abstract)) combined AoT temperature observations with spatial interpolation methods (kriging) and city datasets — tree canopy cover, pavement type, building density — to analyze which neighborhoods in Chicago were most exposed to heat and which interventions would have the largest effect.

Shade trees, cool (high-albedo) pavements, reflective rooftops, and green roofs all reduce peak surface and air temperatures by different mechanisms and to different degrees. The analysis used sensor data to identify where the urban heat island effect was most severe and which physical conditions correlated with the highest temperatures — giving planners a data-driven basis for prioritizing where to plant trees or upgrade pavement rather than relying on intuition or rough regional statistics.

## What the urban ECP proposal was about

The seed proposal I led with Charlie Catlett made the case that urban environmental science is a legitimate exascale use case — not because a single building simulation is expensive, but because doing this at city scale, with dynamic feedback between weather models, hundreds of buildings, and street-level fluid dynamics, requires compute resources that only high-performance supercomputers can provide.

The proposal identified three gaps: validated open workflows connecting mesoscale atmospheric models to street-scale CFD; dense observational data (the Array of Things) to constrain and evaluate high-resolution simulations; and the software engineering to manage the coupling, geometry, and data movement across codes that were not designed to interoperate.

## What this work taught me

The urban computing work reinforced something I keep relearning: in multi-scale simulation, the hard problems are at the interfaces. Each code — WRF, EnergyPlus, Nek5000 — is a mature, well-validated tool within its own domain. Connecting them requires solving problems that none of the codes was designed for: coordinate transformations, time interpolation, mesh handoffs, and the organizational challenge of research groups who each own one layer of the stack collaborating on the coupling across it.

That is the same structural challenge that showed up in reactor simulation (geometry and mesh handoff to neutronics), in FLASH-X (checkpoint format compatibility between two AMR frameworks), and in UXarray (grid format interoperability across climate codes). The scientific domains differ; the problem of building connected workflows across independently developed codes does not change.

---

*Paper: Jain, R., Luo, X., Sever, G., Hong, T., and Catlett, C. ["Representation and evolution of urban weather boundary conditions in downtown Chicago."](https://doi.org/10.1080/19401493.2018.1534275) Journal of Building Performance Simulation, 2020. DOI: 10.1080/19401493.2018.1534275*
