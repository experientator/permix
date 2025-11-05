<p align="center">
  <!-- ACTION ITEM: If you have a logo, place its path here. If not, this block can be deleted. -->
  <img src="path/to/your/logo.png" height="120">
  <h1 align="center">PerMix</h1>
  <p align="center">
    <i>A Python Framework for Perovskite Precursor Mass Calculations</i>
  </p>

<!-- ACTION ITEM: This is the MOST IMPORTANT change. Replace 'your-github-username/PerMix' with your actual repository path in ALL links below (e.g., 'iosimonenko/PerMix'). -->
<p align="center">
    <a href="https://www.repostatus.org/#active">
        <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active">
    </a>
    <a href="https://permix.readthedocs.io/en/latest/">
        <img src="https://img.shields.io/badge/docs-latest-green?logo=readthedocs" alt="Documentation">
    </a>
    <a href="https://github.com/your-github-username/PerMix/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/your-github-username/PerMix" alt="GitHub license">
    </a>
    <a href="https://github.com/your-github-username/PerMix/actions/workflows/tests.yml">
        <img src="https://github.com/your-github-username/PerMix/actions/workflows/tests.yml/badge.svg" alt="Build Status">
    </a>
    <a href="https://codecov.io/gh/your-github-username/PerMix">
        <img src="https://codecov.io/gh/your-github-username/PerMix/branch/main/graph/badge.svg" alt="Codecov">
    </a>
    <a href="https://pypi.org/project/permix/">
        <img src="https://img.shields.io/pypi/v/permix?logo=pypi" alt="PyPI - Version">
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/pypi/pyversions/permix.svg" alt="Python Versions">
    </a>
    <!-- ACTION ITEM: Once your JOSS paper is accepted, replace this with the real badge. -->
    <a href="https://joss.theoj.org/">
        <img src="https://joss.theoj.org/papers/10.21105/joss.01234/status.svg" alt="JOSS Status">
    </a>
    <!-- ACTION ITEM: Once you have a DOI from Zenodo, replace this with the real badge. -->
    <a href="https://zenodo.org/">
        <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg" alt="DOI">
    </a>
</p>

---

**PerMix** is a graphical user interface (GUI) application designed to address a critical bottleneck in materials science: the precise and reproducible calculation of precursor stoichiometry for multicomponent perovskite synthesis. It provides a standardized, high-precision tool to eliminate a major source of experimental variation, allowing for more reliable comparison of results between different laboratories and studies.

<!-- ACTION ITEM: A GIF showcasing your application is HIGHLY recommended. It significantly increases the appeal of the README. Replace this with your GIF. -->
<!-- You can use tools like LICEcap or ScreenToGif to create it easily. -->
![](path/to/your/showcase.gif)

## ✨ Highlights

- **High-Precision Engine**: Uses arbitrary-precision arithmetic to eliminate floating-point errors, ensuring accurate stoichiometric calculations.
- **Combinatorial Strategy Generation**: Automatically generates and ranks all valid synthesis pathways from available precursors.
- **User-Friendly GUI**: An intuitive interface built with Tkinter that guides users from material definition to recipe export.
- **Extensible Database**: Comes with a built-in database of common materials that users can easily extend.
- **Accelerates High-Throughput Research**: Directly supports automated and combinatorial materials discovery workflows.

## 📦 Installation

### 📥 Download Ready-to-Use Versions

#### Windows
1. Download both files from [Windows v1.0.0](https://github.com/experientator/permix_versions/tree/main/versions/1.0.0/windows):
   - `PerMix.exe`
   - `data.db`
2. Place both files in the same directory
3. Run `PerMix.exe`

#### Ubuntu/Debian
1. Download the .deb package from [Ubuntu v1.0.0](https://github.com/experientator/permix_versions/tree/main/versions/1.0.0/ubuntu/permix_1.0.0_all.deb)
2. Install via terminal:
```bash
sudo apt update
sudo apt install ./permix_1.0.0_all.deb
```

### 🐳 Run with Docker

#### *Initial Setup (First Time Only)*

#### Windows:
1. Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Launch **XLaunch** from Start Menu
3. Settings:
   - **Multiple windows**
   - **Display number**: 0
   - **Start no client**
   - ✅ **Disable access control** (important!)
4. Save configuration for future use

#### macOS:
1. Install [XQuartz](https://www.xquartz.org/)
2. Restart your computer
3. Launch XQuartz
4. In terminal execute:
```bash
xhost +localhost
```
#### Linux:
X11 is usually pre-installed. If not:
```bash
# Ubuntu/Debian
sudo apt install x11-xserver-utils
xhost +local:docker
```

#### *Run Application*

#### Windows:
```bash
# Double click the file:
docker/start.bat

# Or via command line:
cd docker
start.bat
```

#### Linux/macOS:
```bash
cd docker
chmod +x docker.sh
./docker.sh
```

### 🔧 Installation from Source Code

#### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/experientator/permixrem.git
cd permixrem
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📖 Documentation

For a complete guide, tutorials, and API reference, please visit the official documentation:

**[permix.readthedocs.io](https://permix.readthedocs.io/en/latest/)**

## 🔬 Key Features and Architecture

PerMix is designed to directly address the challenges identified in current perovskite research.

- **High-Precision Core Calculation Engine**: At its core, PerMix uses Python's `decimal` library for arbitrary-precision arithmetic, robustly handling any number of A, B, and X-site substitutions while ensuring charge balance for complex, multi-element compositions.
- **Combinatorial Synthesis Strategy Generator**: A key innovation is its ability to programmatically generate multiple valid synthesis pathways, enabling the "combinatorial screening" approach to materials discovery essential for robotic high-throughput synthesis workflows.
- **Optimization and Sorting Framework**: PerMix allows users to rank generated synthesis equations based on a multi-level sorting framework (e.g., by cost, availability, or chemical properties).
- **Extensible Materials Database**: An integrated database contains essential data for common perovskite precursors, solvents, and additives, and is user-extensible.
- **Geometric Stability Factor Calculation**: The software automatically calculates the Goldschmidt tolerance factor (t) and octahedral factor (μ) for a rapid, first-pass check for structural stability.

The software is architected with a modular design that separates core logic from the user interface, ensuring the software is highly maintainable and extensible.

## ✒️ Citing PerMix

If you use PerMix in your research, please cite our paper in the *Journal of Open Source Software*.

<!-- ACTION ITEM: Replace placeholders with real data after publication. -->
> Schmidberskaya & Simonenko, (2025). PerMix: A Python Framework for Perovskite Precursor Mass Calculations. *Journal of Open Source Software*, X(XX), 12345. https://doi.org/10.21105/joss.01234

```bibtex
@article{Schmidberskaya2025,
  doi = {10.21105/joss.01234},
  url = {https://doi.org/10.21105/joss.01234},
  year = {2025},
  publisher = {The Open Journal},
  volume = {X},
  number = {XX},
  pages = {12345},
  author = {Schmidberskaya, Arina P. and Simonenko, Ilia O.},
  title = {PerMix: A Python Framework for Perovskite Precursor Mass Calculations},
  journal = {Journal of Open Source Software}
}
```

## 🤝 Contributing

Contributions are welcome! Whether it's reporting a bug, suggesting a new feature, or submitting a pull request, your help is appreciated.

Please read our [**Contributing Guidelines**](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests to us.

## 📄 License

<!-- ACTION ITEM: Choose a license and replace the placeholder. MIT License is a great default choice for open-source projects. -->
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
