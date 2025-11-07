---
title: 'PerMix: A Python Framework for Perovskite Precursor Mass Calculations'
tags:
  - Python
  - materials science
  - computational chemistry
  - high-throughput synthesis
  - halide perovskites
authors:
  - name: Arina P. Schmidberskaya
    orcid: 0009-0007-4416-0072
    affiliation: "1, 2"
  - name: Ilia O. Simonenko
    orcid: 0009-0007-5131-9934
    corresponding: true
    affiliation: "1, 2"
affiliations:
 - name: Joint Institute for Nuclear Research, Dubna, Russia
   index: 1
 - name: Dubna State University, Dubna, Russia
   index: 2
date: 05 November 2025
bibliography: paper.bib
---

## Summary

PerMix is a Python framework designed to address a critical bottleneck in perovskite materials science: the precise and reproducible calculation of precursor stoichiometry for multicomponent synthesis. The field's advancement via "compositional engineering" [@Zhang2023Composition; @Saliba2019Polyelemental] is often hindered by minor stoichiometric deviations that cause significant irreproducibility in device performance and stability [@Fassl2018Fractional; @Falk2020Effect]. PerMix automates high-precision mass calculations, bridging the gap between compositional design and experimental execution. It features an arbitrary-precision engine to eliminate floating-point errors, a combinatorial algorithm for generating and ranking all valid synthesis pathways, and an intuitive graphical user interface (GUI) built with standard Python libraries (Tkinter/ttk) for maximum cross-platform compatibility. Beyond calculations, PerMix now acts as a digital laboratory notebook, allowing researchers to archive successful recipes and track experimental parameters, capabilities essential for accelerating automated, high-throughput materials discovery workflows [@Higgins2020Chemical].

## Statement of Need

The synthesis of high-quality multicomponent perovskites requires extraordinary precision in precursor stoichiometry. The fundamental properties of the final perovskite material—including crystallinity, defect density, and even the reaction pathways at buried interfaces—are critically dependent on the exact composition of the precursor solution [@Ezike2022Perovskite; @Yuan2019Unveiling]. As researchers explore increasingly complex material systems, traditional methods for synthesis planning have become inadequate.

Current methodological approaches suffer from several critical limitations:

**Error Propagation and Reproducibility**: The work of Fassl et al. conclusively demonstrated that minute, fractional deviations in precursor stoichiometry are a primary driver of the inconsistencies and irreproducibility widely reported in perovskite literature [@Fassl2018Fractional]. These deviations, which can arise from simple weighing errors, directly impact device stability and performance metrics. The problem is exacerbated by the fact that commercial precursor salts like PbI₂ can themselves be substoichiometric, a variable that is almost never accounted for in standard lab procedures but has a profound effect on device outcomes [@Tsevas2021Controlling]. Without a tool for high-precision, error-aware calculations, achieving reproducible results remains a significant challenge.

**Computational Complexity for Combinatorial Science**: The future of perovskite research lies in the systematic, combinatorial exploration of "polyelemental" libraries to discover novel materials with optimized properties [@Saliba2019Polyelemental]. This approach is central to automated research platforms that can synthesize and characterize hundreds of unique compositions in a single run [@Higgins2020Chemical]. Manually calculating the precursor recipes for such a vast compositional space is not only prone to error but is fundamentally intractable, stifling the pace of materials discovery.

**Data Management and Archival**: As experimental complexity grows, so does the need for standardized digital tools to archive and retrieve complex synthesis recipes. Relying on scattered spreadsheets or handwritten notes leads to data loss and redundant experimentation. A centralized system to store not just the target composition, but the exact precursor masses, solvent volumes, and synthesis conditions used, is crucial for long-term reproducibility and knowledge transfer within research groups.

**Lack of a Standardized Framework**: The absence of a standardized computational tool means that each research group relies on bespoke, often unvalidated, calculation methods. A shared, transparent, and validated tool can provide a consistent foundation for the entire research community, from fundamental materials science to applied device engineering.

PerMix addresses these limitations by providing an integrated, high-precision computational framework that automates complex stoichiometric calculations, implements combinatorial strategies for precursor selection, and ensures reproducible data management through a robust local database.

## Software Description

PerMix is a Python package with a comprehensive GUI and integrated SQLite database, designed to streamline the entire experimental planning lifecycle in perovskite synthesis.

### Key Features
- **High-Precision Core Calculation Engine**: Utilizes Python's `decimal` library for arbitrary-precision arithmetic, robustly handling any number of A, B, and X-site substitutions while ensuring charge balance [@Fassl2018Fractional; @Falk2020Effect].
- **Combinatorial Synthesis Strategy Generator**: Programmatically generates all valid synthesis pathways from available precursor salts to achieve a target stoichiometry, enabling high-throughput screening workflows [@Saliba2019Polyelemental; @Higgins2020Chemical].
- **Integrated SQLite Database**: Replaces ad-hoc file storage with a robust relational database for managing precursors, solvents, and ionic radii, complete with dedicated GUI management tools.
- **Composition Lifecycle Management**: Enables researchers to archive their own successful syntheses ("Favorites") and curate a database of literature compositions alongside their reported optoelectronic device properties (e.g., PCE for solar cells, detectivity for sensors).
- **Geometric Stability Analysis**: Automatically calculates the Goldschmidt tolerance factor (t) and octahedral factor (μ) for mixed-ion systems, providing a rapid check for structural stability.
- **Bilingual Interface**: Fully localized in English and Russian to support a wider international user base.

### Architecture and Availability
The software has been refactored into a Model-View-Controller (MVC) architecture, strictly separating data persistence (SQLite interactions), core scientific logic, and the user interface. This ensures maintainability and facilitates future extensions. PerMix is implemented in pure Python, leveraging established libraries like NumPy and Pandas, and is available under the MIT license. The source code, comprehensive documentation, and installation instructions are hosted on GitHub at https://github.com/experientator/permix/.

## Acknowledgements

The authors would like to express their sincere gratitude to their scientific supervisor, Prof. R.G. Nazmitdinov, Doctor of Sciences (Physics and Mathematics) and Leading Researcher at the Bogoliubov Laboratory of Theoretical Physics, JINR, for his invaluable guidance and unwavering support throughout this project. This work was conducted as part of a university research project at Dubna State University (Order No. 167 of February 12, 2025). Financial support from the Russian Science Foundation under project no. 23-19-00884 is gratefully acknowledged.

## References
