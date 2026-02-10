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

# Summary

`PerMix` is a Python framework designed to address a critical bottleneck in perovskite materials science: the precise and reproducible calculation of precursor stoichiometry for multicomponent synthesis. The field's advancement via "compositional engineering" [@Zhang2023Composition; @Saliba2019Polyelemental] is often hindered by minor stoichiometric deviations that cause significant irreproducibility in device performance and stability [@Fassl2018Fractional; @Falk2020Effect]. `PerMix` automates high-precision mass calculations, bridging the gap between compositional design and experimental execution. It features an arbitrary-precision engine to eliminate floating-point errors, a combinatorial algorithm for generating and ranking all valid synthesis pathways, and an intuitive graphical user interface (GUI) built with standard Python libraries (Tkinter/ttk) for maximum cross-platform compatibility. Beyond calculations, `PerMix` now acts as a digital laboratory notebook, allowing researchers to archive successful recipes and track experimental parameters, capabilities essential for accelerating automated, high-throughput materials discovery workflows [@Higgins2020Chemical].

# Statement of need

The synthesis of high-quality multicomponent perovskites requires extraordinary precision in precursor stoichiometry. The fundamental properties of the final perovskite material, including crystallinity, defect density, and even the reaction pathways at buried interfaces, are critically dependent on the exact composition of the precursor solution [@Ezike2022Perovskite; @Yuan2019Unveiling]. As researchers explore increasingly complex material systems, traditional methods for synthesis planning have become inadequate.

Current methodological approaches suffer from several critical limitations:

**Error Propagation and Reproducibility**: The work of Fassl et al. conclusively demonstrated that minute, fractional deviations in precursor stoichiometry are a primary driver of the inconsistencies and irreproducibility widely reported in perovskite literature [@Fassl2018Fractional]. These deviations, which can arise from simple weighing errors, directly impact device stability and performance metrics. The problem is exacerbated by the fact that commercial precursor salts like PbI₂ can themselves be substoichiometric, a variable that is almost never accounted for in standard lab procedures but has a profound effect on device outcomes [@Tsevas2021Controlling]. Without a tool for high-precision, error-aware calculations, achieving reproducible results remains a significant challenge.

**Computational Complexity for Combinatorial Science**: The future of perovskite research lies in the systematic, combinatorial exploration of "polyelemental" libraries to discover novel materials with optimized properties [@Saliba2019Polyelemental]. This approach is central to automated research platforms that can synthesize and characterize hundreds of unique compositions in a single run [@Higgins2020Chemical]. Manually calculating the precursor recipes for such a vast compositional space is not only prone to error but is fundamentally intractable, stifling the pace of materials discovery.

**Data Management and Archival**: As experimental complexity grows, so does the need for standardized digital tools to archive and retrieve complex synthesis recipes. Relying on scattered spreadsheets or handwritten notes leads to data loss and redundant experimentation. A centralized system to store not just the target composition, but the exact precursor masses, solvent volumes, and synthesis conditions used, is crucial for long-term reproducibility and knowledge transfer within research groups.

`PerMix` addresses these limitations by providing an integrated, high-precision computational framework. Key features enabling this include a **Combinatorial Synthesis Strategy Generator** that programmatically generates all valid synthesis pathways from available precursor salts; a **Geometric Stability Analysis** module that automatically calculates Goldschmidt tolerance and octahedral factors; and **Composition Lifecycle Management** tools that allow researchers to archive successful syntheses and curate a database of literature compositions.

# State of the field

The ecosystem for perovskite stoichiometry calculation is currently fragmented and largely informal. Unlike other mature areas of computational materials science that benefit from established packages (e.g., `pymatgen` for crystallography), the specific domain of experimental precursor planning lacks standardized open-source tools. The prevailing "state of the art" often consists of ad-hoc spreadsheets, bespoke laboratory scripts, or manual calculations recorded in physical notebooks. While general chemical calculators exist, they do not handle the specific geometric stability factors (e.g., Goldschmidt tolerance factor) or the combinatorial complexity of multi-site substitution required for perovskite research.

`PerMix` was built as a new package rather than a contribution to an existing one because no suitable Python-based open-source framework existed that addressed these specific needs. Existing general-purpose chemistry libraries do not support the specific logic required for A/B/X site management in perovskite structures combined with mass-balance optimization for synthesis. By providing a standalone, validated calculator with a GUI, `PerMix` aims to standardize these protocols across the community, replacing error-prone manual methods with a reproducible digital workflow.

# Software design

The application is built on the **MVC (Model-View-Controller)** architecture, a design choice that strictly isolates the stoichiometric calculation logic from the **Tkinter**-based graphical user interface. This separation of concerns is critical for research software, as it ensures that the core computational engine remains portable; for instance, the backend can be migrated to a web-based framework or integrated into a laboratory automation system without modifying the underlying code. To manage chemical reference data, the system utilizes an embedded **SQLite** database. This approach decouples chemical constants such as ionic radii and compound templates from the application logic, allowing for seamless updates to the chemical library without altering the source code.

Precision is maintained by employing the Python **Decimal** module in conjunction with the **periodictable** library for all primary calculations. Unlike standard floating-point arithmetic, this combination eliminates cumulative rounding errors, guaranteeing the high-fidelity accuracy required for calculating precursor masses ($10^{-6}$ g) and complex geometric factors. By integrating these robust software engineering principles, the application provides a stable, extensible, and scientifically rigorous tool for perovskite synthesis. The software is available under the MIT license, with source code hosted on GitHub.

# Research impact statement

`PerMix` has already demonstrated tangible impact in experimental perovskite research. It was the core computational tool used to develop a theory-guided approach for the growth of centimeter-scale CsPbBr$_3$ single crystals [@Simonenko2026]. 

Furthermore, the software enabled the synthesis of complex mixed-cation and mixed-anion single crystals: (MA$_{1-z}$Cs$_z$)Pb(Br$_w$Y$_{1-w}$)$_3$ (where Y = Cl, I). `PerMix` was used to programmatically generate and optimize reaction equations based on laboratory inventory constraints (e.g., the absence of MAI or MACl). The software successfully calculated optimal pathways using the minimum number of reagents, as shown in **Table 1**.

**Table 1**: Optimal reaction equations generated by `PerMix` for (MA$_z$Cs$_{1-z}$)Pb(Br$_w$Y$_{1-w}$)$_3$ (Y = Cl, I) synthesis.
| № | z | X | w | Equations Count | Optimal Reaction Equation |
|:-:|:-:|:-:|:-:|:---------------:|:-------------------------|
| 1 | 0 | Cl| 0.1| 3 | 1.0 MABr + 0.15 PbCl$_2$ + 0.85 PbBr$_2$ $\longrightarrow$ MAPb(Br$_{0.9}$Cl$_{0.1}$)$_3$ |
| 2 | 0 | - | 0 | 1 | 1.0 MABr + 1.0 PbBr$_2$ $\longrightarrow$ MAPbBr$_3$ |
| 3 | 0 | I | 0.1| 3 | 1.0 MABr + 0.15 PbI$_2$ + 0.85 PbBr$_2$ $\longrightarrow$ MAPb(Br$_{0.9}$I$_{0.1}$)$_3$ |
| 4 | 0.1| Cl| 0.1| 7 | 0.1 CsBr + 0.9 MABr + 0.15 PbCl$_2$ + 0.85 PbBr$_2$ $\longrightarrow$ (MA$_{0.9}$Cs$_{0.1}$)Pb(Br$_{0.9}$Cl$_{0.1}$)$_3$ |
| 5 | 0.1| - | 0 | 3 | 0.1 CsBr + 0.9 MABr + 1.0 PbBr$_2$ $\longrightarrow$ (MA$_{0.9}$Cs$_{0.1}$)PbBr$_3$ |
| 6 | 0.1| I | 0.1| 7 | 0.1 CsBr + 0.9 MABr + 0.15 PbI$_2$ + 0.85 PbBr$_2$ $\longrightarrow$ (MA$_{0.9}$Cs$_{0.1}$)Pb(Br$_{0.9}$I$_{0.1}$)$_3$ |
| 7 | 0.2| Cl| 0.1| 7 | 0.2 CsBr + 0.8 MABr + 0.15 PbCl$_2$ + 0.85 PbBr$_2$ $\longrightarrow$ (MA$_{0.8}$Cs$_{0.2}$)Pb(Br$_{0.9}$Cl$_{0.1}$)$_3$ |
| 8 | 0.2| - | 0 | 3 | 0.2 CsBr + 0.8 MABr + 1.0 PbBr$_2$ $\longrightarrow$ (MA$_{0.8}$Cs$_{0.2}$)PbBr$_3$ |
| 9 | 0.2| I | 0.1| 7 | 0.2 CsBr + 0.8 MABr + 0.15 PbI$_2$ + 0.85 PbBr$_2$ $\longrightarrow$ (MA$_{0.8}$Cs$_{0.2}$)Pb(Br$_{0.9}$I$_{0.1}$)$_3$ |

The experimental validation (see \autoref{fig:crystals}) confirmed that the varying cationic and anionic phases resulted in distinct crystal morphologies and colors, validating the accuracy of the `PerMix` stoichiometry engine. This demonstrates that the software effectively automates experimental planning for complex, multi-component materials.

![Photos of (MA$_{1-z}$Cs$_z$)Pb(Br$_w$Y$_{1-w}$)$_3$ (Y = Cl, I) single crystals synthesized using `PerMix`. The numbering corresponds to the compositions in Table 1.\label{fig:crystals}](crystals.png)

# AI usage disclosure

Generative AI tools (Gemini 3 Pro by Google Inc.) were used during the development process to assist in writing repetitive boilerplate code, specifically for the localization strings and database interaction methods. All AI-generated code was manually reviewed, tested, and validated by the authors to ensure correctness and adherence to the project's logic and coding standards. No AI tools were used to generate the scientific content or the core calculation algorithms of this manuscript.

# Acknowledgements

The authors would like to express their sincere gratitude to their scientific supervisor, Prof. R.G. Nazmitdinov, Doctor of Sciences (Physics and Mathematics) and Leading Researcher at the Bogoliubov Laboratory of Theoretical Physics, JINR, for his invaluable guidance and unwavering support throughout this project. The work was carried out with financial support from the Russian Science Foundation (project No. 25-29-01209).

# References
```
