# PerMix: A Python Framework for Perovskite Precursor Mass Calculations

**Authors**: [Your Name], [Your Affiliation]

**DOI**: [To be assigned]

**Software**
*   Review
*   Repository
*   Archive

**Editor**: [To be assigned]

**Reviewers**: [To be assigned]

**Submitted**: [Date]
**Published**: [Date]

**License**
Authors of papers retain copyright and release the work under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

## Summary

The synthesis of multicomponent perovskite materials represents a pivotal frontier in materials science, driven by the strategy of "compositional engineering" to create highly efficient and stable optoelectronic devices [@Zhang2023Composition; @Igbari2025Strategies]. By systematically exploring a vast combinatorial space of cations, anions, and metals, researchers can fine-tune the thermodynamic and structural properties of perovskites to stabilize desired phases and enhance performance [@Saliba2019Polyelemental; @Kim2020Thermodynamics]. This approach has led to the development of complex, "polyelemental" perovskites that significantly outperform their simpler counterparts [@Turren-Cruz2024Multicomponent].

However, the immense potential of compositional engineering is directly hampered by a critical computational bottleneck: the precise calculation of precursor stoichiometry. The literature provides definitive evidence that fractional, and often unintentional, deviations in precursor molar ratios as small as 0.5–1% can dramatically alter surface composition, defect physics, device performance, and storage stability, accounting for significant irreproducibility across research groups [@Fassl2018Fractional; @Falk2020Effect]. This challenge is compounded by variations in the stoichiometry of the precursor salts themselves, which introduces a hidden source of error that can degrade final film quality [@Tsevas2021Controlling]. As the field moves towards automated, high-throughput robotic platforms for materials discovery [@Higgins2020Chemical], the need for an automated, high-precision, and systematic calculation tool has become urgent.

To address these challenges, we developed PerMix, a comprehensive Python framework for the automated, high-precision calculation of perovskite precursor masses. PerMix streamlines synthesis planning by providing accurate mass calculations for multicomponent systems, combinatorial algorithms to explore diverse synthesis strategies, and a user-friendly graphical interface for both novice and expert researchers, thereby bridging the gap between compositional design and reproducible experimental execution.

## Statement of Need

The synthesis of high-quality multicomponent perovskites requires extraordinary precision in precursor stoichiometry. The fundamental properties of the final perovskite material—including crystallinity, defect density, and even the reaction pathways at buried interfaces—are critically dependent on the exact composition of the precursor solution [@Ezike2022Perovskite; @Yuan2019Unveiling]. As researchers explore increasingly complex material systems, traditional methods for synthesis planning have become inadequate.

Current methodological approaches suffer from several critical limitations:

**Error Propagation and Reproducibility**: The work of Fassl et al. conclusively demonstrated that minute, fractional deviations in precursor stoichiometry are a primary driver of the inconsistencies and irreproducibility widely reported in perovskite literature [@Fassl2018Fractional]. These deviations, which can arise from simple weighing errors, directly impact device stability and performance metrics. The problem is exacerbated by the fact that commercial precursor salts like PbI₂ can themselves be substoichiometric, a variable that is almost never accounted for in standard lab procedures but has a profound effect on device outcomes [@Tsevas2021Controlling]. Without a tool for high-precision, error-aware calculations, achieving reproducible results remains a significant challenge.

**Computational Complexity for Combinatorial Science**: The future of perovskite research lies in the systematic, combinatorial exploration of "polyelemental" libraries to discover novel materials with optimized properties [@Saliba2019Polyelemental]. This approach is central to automated research platforms that can synthesize and characterize hundreds of unique compositions in a single run [@Higgins2020Chemical]. Manually calculating the precursor recipes for such a vast compositional space is not only prone to error but is fundamentally intractable, stifling the pace of materials discovery.

**Optimization for Advanced Materials**: Modern synthesis strategies often involve complex multicomponent systems, such as methylammonium-free tin-lead perovskites or all-perovskite nanocrystal superlattices, which require careful balancing of multiple additives and components to control crystallization and enhance stability [@Turren-Cruz2024Multicomponent; @Sekh2024All-Perovskite]. Furthermore, creating advanced structures like 2D-3D heterojunctions requires precise control over the reactants that form the capping layers [@He2020Compositional]. Simple spreadsheet methods lack the flexibility to generate and rank various synthesis pathways based on user-defined criteria (e.g., minimizing cost, number of reagents, or avoiding certain chemicals), which is essential for optimizing these complex syntheses.

**Lack of a Standardized Framework**: The absence of a standardized computational tool means that each research group relies on bespoke, often unvalidated, calculation methods. This contributes to the widespread variation in reported results and makes it difficult to compare findings between labs. A shared, transparent, and validated tool can provide a consistent foundation for the entire research community, from fundamental materials science to applied device engineering.

PerMix directly addresses these limitations by providing an integrated, high-precision computational framework that automates complex stoichiometric calculations, implements combinatorial strategies for precursor selection, and ensures reproducible, transparent results across diverse research environments.

## Software Features

PerMix is a comprehensive Python package with a user-friendly graphical interface built with CustomTkinter. Its features are designed to directly address the challenges identified in current perovskite research.

**High-Precision Core Calculation Engine**: At its core, PerMix uses Python's `decimal` library for arbitrary-precision arithmetic, eliminating floating-point errors. This is a critical feature, as it allows for the accurate management of the fractional stoichiometric deviations that have been shown to drastically impact device stability and performance [@Fassl2018Fractional; @Falk2020Effect; @Saliba2019Polyelemental]. The engine robustly handles any number of A, B, and X-site substitutions, ensuring charge balance and proper molar ratios for complex, multi-element compositions.

**Combinatorial Synthesis Strategy Generator**: A key innovation of PerMix is its ability to programmatically generate multiple valid synthesis pathways. This feature directly enables the "combinatorial screening" approach to materials discovery by allowing users to explore all valid combinations of available precursor salts to achieve a target stoichiometry. This is essential for populating the well plates used in robotic high-throughput synthesis workflows [@Saliba2019Polyelemental; @Higgins2020Chemical].

**Optimization and Sorting Framework**: PerMix allows users to rank the generated synthesis equations based on a multi-level sorting framework. This is crucial for practical experimental design where factors like cost, precursor availability, or the need to minimize hygroscopic materials are paramount.

**Extensible Materials Database**: An integrated JSON database contains essential data for common perovskite precursors, solvents, and additives, including chemical formulas and ionic radii. The database is user-extensible, allowing researchers to incorporate novel components as the field of compositional engineering expands to include new organic cations, metal halides, and functional additives.

**Geometric Stability Factor Calculation**: The software automatically calculates the Goldschmidt tolerance factor (t) and octahedral factor (μ) for mixed-ion systems. This provides a rapid, first-pass check for the structural stability of a target composition, a key consideration in the thermodynamic analysis of multicomponent perovskites.

**User Interface and Workflow**:
- An intuitive graphical user interface (GUI) guides users through the entire process, from defining a target material to exporting final recipes.
- A "favorites" system allows users to save and recall complex configurations, streamlining the planning of recurring experiments.
- Results are presented in clear text format and visualized with interactive charts, facilitating quick comparison and selection of synthesis plans.

## Implementation and Architecture

PerMix is implemented in pure Python, leveraging established scientific libraries such as NumPy, SciPy, and Pandas. This ensures cross-platform compatibility and easy integration into existing scientific computing environments. The software is architected with a modular design that separates core logic from the user interface:
-   **`business_logic`**: Contains the core scientific algorithms for stoichiometry, strategy generation, and geometric calculations.
-   **`data_processing`**: Manages all data interactions, including loading from JSON databases and handling user input.
-   **`ui`**: Encapsulates all GUI components, ensuring the user interface can be modified or replaced without affecting the core calculations.
-   **`services`**: An orchestration layer that coordinates actions between the other modules.

This separation of concerns makes the software highly maintainable and extensible, allowing for the future development of a command-line interface (CLI) or a web-based API without altering the validated scientific core.

## Applications and Impact

PerMix is poised to have a significant impact on the perovskite research community by addressing fundamental issues of reproducibility, scalability, and the speed of discovery.

Its primary applications include:
- **Accelerating High-Throughput Materials Discovery**: PerMix serves as the essential software bridge between the combinatorial design of novel perovskites [@Saliba2019Polyelemental] and their physical creation using robotic synthesis platforms [@Higgins2020Chemical]. It automates the tedious and error-prone task of generating thousands of unique precursor recipes.
- **Enhancing Research Reproducibility**: By providing a standardized, high-precision tool, PerMix helps eliminate a major source of experimental variation: unintentional stoichiometric errors [@Fassl2018Fractional]. This allows for more reliable comparison of results between different laboratories and studies.
- **Optimizing Complex Synthesis**: The software provides a systematic framework for planning the synthesis of advanced materials, such as 2D-3D heterojunctions or multicomponent nanocrystals, where precise control over multiple precursors is essential [@He2020Compositional; @Sekh2024All-Perovskite].
- **Supporting Industrial R&D and Education**: For industrial applications, PerMix enables cost optimization and reproducible scale-up. In academic settings, it serves as an interactive tool for teaching the principles of multicomponent materials synthesis.

By automating computational logistics and enforcing precision, PerMix empowers researchers to focus on experimental innovation and materials characterization, thereby accelerating the path toward commercially viable perovskite technologies.

## Acknowledgements

[Include funding acknowledgments, computational resources, and collaborator contributions as appropriate]

## References

[@Higgins2020Chemical]
[@Turren-Cruz2024Multicomponent]
[@Ezike2022Perovskite]
[@Falk2020Effect]
[@Tsevas2021Controlling]
[@Saliba2019Polyelemental]
[@Kim2020Thermodynamics]
[@Zhang2023Composition]
[@Sekh2024All-Perovskite]
[@He2020Compositional]
[@Igbari2025Strategies]
[@Yuan2019Unveiling]
[@Fassl2018Fractional]
[@Ling2018Machine]
