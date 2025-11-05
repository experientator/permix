## Run with Docker

### Initial Setup (First Time Only)

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

### Run Application

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
