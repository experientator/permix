# Welcome to PerMix Documentation

PerMix is a graphical user interface (GUI) application designed to address a critical bottleneck in materials science: the precise and reproducible calculation of precursor stoichiometry for multicomponent perovskite synthesis. It provides a standardized, high-precision tool to eliminate a major source of experimental variation, allowing for more reliable comparison of results between different laboratories and studies.

## Quick Start

Choose your installation method:

- [**Ready-to-Use**](installation.md#ready-to-use-versions) - Download pre-built binaries
- [**Docker**](docker.md) - Run with Docker containers  
- [**From Source**](installation.md#from-source) - Build from source code

Once installed, proceed directly to our comprehensive guide:
- [**User Guide & Quick Start**](user_guide.md) — Learn how to run your first calculation, manage the SQLite database, and understand validation rules.

## Features

- **High-Precision Engine**: Uses arbitrary-precision arithmetic (`Decimal`) to eliminate floating-point errors, ensuring accurate stoichiometric calculations down to $10^{-6}$ g.
- **Combinatorial Strategy Generation**: Automatically generates and ranks all valid synthesis pathways from available precursors.
- **Extensible Database**: Comes with a built-in local SQLite database of common materials that users can easily extend through the GUI using automated chemical parsing.
- **Accelerates High-Throughput Research**: Directly supports automated and combinatorial materials discovery workflows.
- 