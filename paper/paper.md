---
title: 'PerMix: A Python Framework for Perovskite Precursor Mass Calculations'
tags:
  - Python
  - materials science
  - computational chemistry
  - high-throughput synthesis
  - halide perovskites
authors:
  - name: Ilia O. Simonenko
    orcid: 0009-0007-5131-9934
    corresponding: true
    affiliation: "1, 2"
  - name: Arina P. Schmidberskaya
    orcid: 0009-0007-4416-0072
    affiliation: "1, 2"
affiliations:
 - name: Joint Institute for Nuclear Research, Dubna, Russia
   index: 1
 - name: Dubna State University, Dubna, Russia
   index: 2
date: 08 October 2025
bibliography: paper.bib
---

## Summary

PerMix is a Python framework designed to address a critical bottleneck in perovskite materials science: the precise and reproducible calculation of precursor stoichiometry for multicomponent synthesis. The field's advancement via "compositional engineering" [@Zhang2023Composition; @Saliba2019Polyelemental] is often hindered by minor stoichiometric deviations that cause significant irreproducibility in device performance and stability [@Fassl2018Fractional; @Falk2020Effect]. PerMix automates high-precision mass calculations, bridging the gap between compositional design and experimental execution. It features an arbitrary-precision engine to eliminate floating-point errors, a combinatorial algorithm for generating and ranking all valid synthesis pathways, and an intuitive graphical user interface (GUI) built with Tkinter. These capabilities are essential for accelerating automated, high-throughput materials discovery workflows [@Higgins2020Chemical].

## Statement of Need

The synthesis of high-quality multicomponent perovskites requires extraordinary precision in precursor stoichiometry. The fundamental properties of the final perovskite material—including crystallinity, defect density, and even the reaction pathways at buried interfaces—are critically dependent on the exact composition of the precursor solution [@Ezike2022Perovskite; @Yuan2019Unveiling]. As researchers explore increasingly complex material systems, traditional methods for synthesis planning have become inadequate.

Current methodological approaches suffer from several critical limitations:

**Error Propagation and Reproducibility**: The work of Fassl et al. conclusively demonstrated that minute, fractional deviations in precursor stoichiometry are a primary driver of the inconsistencies and irreproducibility widely reported in perovskite literature [@Fassl2018Fractional]. These deviations, which can arise from simple weighing errors, directly impact device stability and performance metrics. The problem is exacerbated by the fact that commercial precursor salts like PbI₂ can themselves be substoichiometric, a variable that is almost never accounted for in standard lab procedures but has a profound effect on device outcomes [@Tsevas2021Controlling]. Without a tool for high-precision, error-aware calculations, achieving reproducible results remains a significant challenge.

**Computational Complexity for Combinatorial Science**: The future of perovskite research lies in the systematic, combinatorial exploration of "polyelemental" libraries to discover novel materials with optimized properties [@Saliba2019Polyelemental]. This approach is central to automated research platforms that can synthesize and characterize hundreds of unique compositions in a single run [@Higgins2020Chemical]. Manually calculating the precursor recipes for such a vast compositional space is not only prone to error but is fundamentally intractable, stifling the pace of materials discovery.

**Optimization for Advanced Materials**: Modern synthesis strategies often involve complex multicomponent systems, such as methylammonium-free tin-lead perovskites or all-perovskite nanocrystal superlattices, which require careful balancing of multiple additives and components to control crystallization and enhance stability [@Turren-Cruz2024Multicomponent; @Sekh2024All-Perovskite]. Furthermore, creating advanced structures like 2D-3D heterojunctions requires precise control over the reactants that form the capping layers [@He2020Compositional]. Simple spreadsheet methods lack the flexibility to generate and rank various synthesis pathways based on user-defined criteria (e.g., minimizing cost, number of reagents, or avoiding certain chemicals), which is essential for optimizing these complex syntheses.

**Lack of a Standardized Framework**: The absence of a standardized computational tool means that each research group relies on bespoke, often unvalidated, calculation methods. This contributes to the widespread variation in reported results and makes it difficult to compare findings between labs. A shared, transparent, and validated tool can provide a consistent foundation for the entire research community, from fundamental materials science to applied device engineering.

PerMix directly addresses these limitations by providing an integrated, high-precision computational framework that automates complex stoichiometric calculations, implements combinatorial strategies for precursor selection, and ensures reproducible, transparent results across diverse research environments.

## Software Description

PerMix - a Python-based GUI application with SQLite backend for perovskite syntesis experiment planning.

### Key Features
- **High-Precision Core Calculation Engine**: Utilizes Python's `decimal` library for arbitrary-precision arithmetic, robustly handling any number of A, B, and X-site substitutions while ensuring charge balance for complex compositions [@Fassl2018Fractional; @Falk2020Effect].
- **Combinatorial Synthesis Strategy Generator**: Programmatically generates all valid synthesis pathways from available precursor salts to achieve a target stoichiometry, directly enabling high-throughput and combinatorial screening workflows [@Saliba2019Polyelemental; @Higgins2020Chemical].
- **Optimization and Sorting Framework**: Ranks the generated synthesis recipes based on user-defined criteria, such as cost, precursor availability, or chemical properties, crucial for practical experimental design.
- **Extensible Materials Database**: Includes an integrated, user-extensible JSON database of common precursors, solvents, and additives.
- **Geometric Stability Factor Calculation**: Automatically calculates the Goldschmidt tolerance factor (t) and octahedral factor (μ) for mixed-ion systems, providing a rapid check for structural stability.

### Architecture and Availability
The software is architected with a modular design that separates core logic (`business_logic`) from the user interface (`ui`), ensuring maintainability and extensibility. PerMix is implemented in Python, leveraging established libraries like NumPy and Pandas, using SQLite database and is available under the MIT license. The source code, comprehensive documentation, and installation instructions are hosted on GitHub at [https://github.com/experientator/permix/tree/main].

## Acknowledgements

The work was carried out within the state assignment of Russian Science Foundation (project No. 23-19-00884).

## References
