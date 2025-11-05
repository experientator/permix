# Installation

## Download Ready-to-Use Versions

### Windows
1. Download both files from [Windows v1.0.0](https://github.com/experientator/permix_versions/tree/main/versions/1.0.0/windows):
   - `PerMix.exe`
   - `data.db`
2. Place both files in the same directory
3. Run `PerMix.exe`

### Ubuntu/Debian
1. Download the .deb package from [Ubuntu v1.0.0](https://github.com/experientator/permix_versions/tree/main/versions/1.0.0/ubuntu/permix_1.0.0_all.deb)
2. Install via terminal:
```bash
sudo apt update
sudo apt install ./permix_1.0.0_all.deb
```

## 🔧 Installation from Source Code

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

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