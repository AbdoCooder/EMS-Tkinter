# Running EMS-Tkinter with Docker on macOS, Linux, and Windows

This guide helps you run the Employee Management System (Tkinter app) in Docker on your platform.

## Prerequisites by Platform

### macOS
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **XQuartz** for X11 support ([Download](https://www.xquartz.org/))

### Linux
- **Docker** and **Docker Compose** installed
- **X11** (usually pre-installed on Linux desktops like Ubuntu, Fedora, Debian)
- X11 socket at `/tmp/.X11-unix`

### Windows
- **Docker Desktop** with WSL2 backend ([Download](https://www.docker.com/products/docker-desktop))
- **VcXsrv** or **Xming** for X11 support
  - [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (Recommended)
  - [Xming](http://www.straightrunning.com/XmingNotes/)

---

## Setup by Platform

### 🍎 macOS Setup

#### Step 1: Install XQuartz
```bash
# Using Homebrew
brew install --cask xquartz

# Or download from: https://www.xquartz.org/
```

#### Step 2: Start XQuartz and Configure Access
```bash
# Launch XQuartz
open -a XQuartz

# In XQuartz → Preferences → Security: Enable "Allow connections from network clients"

# Grant Docker access to X11
xhost + local:docker
```

#### Step 3: Build and Run
```bash
cd /path/to/EMS-Tkinter

# Using Docker Compose (Recommended)
docker-compose up

# Or with Docker CLI
docker run -it \
  -e DISPLAY=host.docker.internal:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/.Xauthority:/root/.Xauthority \
  -v $(pwd):/app \
  --name ems-app \
  ems-tkinter
```

---

### 🐧 Linux Setup

#### Step 1: Install Docker and Docker Compose
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER
newgrp docker

# Or for Fedora/RHEL
sudo dnf install docker docker-compose
sudo usermod -aG docker $USER
```

#### Step 2: Verify X11 is Available
```bash
# Check if X11 socket exists
ls -la /tmp/.X11-unix/

# Or check DISPLAY variable
echo $DISPLAY
# Should output something like :0 or :1
```

#### Step 3: Grant X11 Access (if needed)
```bash
# Allow local connections to X11
xhost + local:docker

# Or use a simpler approach:
xhost +
```

#### Step 4: Build and Run
```bash
cd /path/to/EMS-Tkinter

# Get your DISPLAY value (usually :0)
echo $DISPLAY

# Run with Docker Compose
docker-compose up

# Or with Docker CLI
docker run -it \
  -e DISPLAY=${DISPLAY} \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v ~/.Xauthority:/root/.Xauthority:rw \
  -v $(pwd):/app \
  --name ems-app \
  ems-tkinter
```

**Note:** On Wayland (GNOME on newer systems), X11 forwarding may not work. Check with:
```bash
echo $XDG_SESSION_TYPE
# If output is "wayland", see Wayland section below
```

#### Wayland Support (GNOME 40+)
If you're using Wayland:

```bash
# Option 1: Use Xvfb (virtual X server)
docker run -it \
  -e DISPLAY=:99 \
  -v $(pwd):/app \
  --name ems-app \
  ems-tkinter

# Option 2: Switch back to X11 session at login screen

# Option 3: Use XWayland (if available)
DISPLAY=:0 docker-compose up
```

---

### 🪟 Windows (WSL2) Setup

#### Step 1: Install Docker Desktop with WSL2
- Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- Enable WSL2 in Docker settings

#### Step 2: Install X Server

**Option A: VcXsrv (Recommended)**
```powershell
# Using Chocolatey
choco install vcxsrv

# Or download from: https://sourceforge.net/projects/vcxsrv/
```

**Option B: Xming**
```powershell
# Using Chocolatey
choco install xming

# Or download from: http://www.straightrunning.com/XmingNotes/
```

#### Step 3: Configure and Start X Server

**For VcXsrv:**
1. Launch "XLaunch" from Start Menu
2. Select "Multiple windows"
3. Select "Start no client"
4. **IMPORTANT:** In "Extra settings", enable "Disable access control"
5. Click "Finish" and save configuration
6. The X server icon should appear in system tray

**For Xming:**
1. Launch Xming from Start Menu
2. Use default settings
3. Allow through Windows Firewall if prompted

#### Step 4: Find Your Windows IP Address
```powershell
# In PowerShell or CMD
ipconfig

# Look for "IPv4 Address" under your active connection
# Usually something like 192.168.x.x or 172.x.x.x
```

#### Step 5: Build and Run in WSL2

```bash
# Open WSL2 terminal
wsl

# Navigate to project
cd /mnt/c/path/to/EMS-Tkinter

# Export your Windows IP (replace with your actual IP)
export DISPLAY=192.168.1.100:0

# Run Docker Compose
docker-compose up

# Or with Docker CLI
docker run -it \
  -e DISPLAY=192.168.1.100:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /mnt/c/path/to/EMS-Tkinter:/app \
  --name ems-app \
  ems-tkinter
```

**Troubleshooting Windows IP:**
```bash
# If you don't know your Windows IP, use:
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
```

---

## Universal Commands

### Build the Image
```bash
docker-compose build --no-cache
```

### Start Container
```bash
# Foreground (see output)
docker-compose up

# Background (daemon mode)
docker-compose up -d

# View logs
docker-compose logs -f ems
```

### Stop Container
```bash
docker-compose down
```

### Access Container Shell
```bash
docker-compose exec ems /bin/bash
```

### Verify App is Running
```bash
docker ps
docker logs ems-tkinter
```

---

## Troubleshooting by Platform

### All Platforms: "Cannot connect to X server"
```bash
# 1. Verify X server is running
# macOS: XQuartz in menu bar
# Linux: Check DISPLAY value
# Windows: VcXsrv/Xming in system tray

# 2. Grant Docker access
# macOS: xhost + local:docker
# Linux: xhost + local:docker
# Windows: Make sure VcXsrv has "Disable access control" enabled
```

### macOS Specific
```bash
# XQuartz not starting?
open -a XQuartz

# Display not found?
echo $DISPLAY
# Update docker-compose.yml to use the correct DISPLAY value
```

### Linux Specific
```bash
# X11 socket not found?
ls -la /tmp/.X11-unix/

# Check DISPLAY
echo $DISPLAY
# Update DISPLAY value in docker-compose.yml if needed

# Wayland conflict?
echo $XDG_SESSION_TYPE
# If "wayland", consider switching to X11 session or using Xvfb
```

### Windows Specific
```bash
# VcXsrv not responding?
# 1. Kill VcXsrv in Task Manager
# 2. Restart it via XLaunch
# 3. Enable "Disable access control"

# Can't find Windows IP?
# Run in PowerShell: ipconfig | findstr "IPv4"

# DISPLAY error?
# Make sure WSL can reach Windows IP:
ping 192.168.1.100  # Replace with your IP
```

---

## Performance Tips

### macOS
```bash
# Enable GPU acceleration (if available)
defaults write org.macosforge.xquartz.X11 enable_iglx -bool true

# Restart XQuartz after changing
killall XQuartz
open -a XQuartz
```

### Linux
```bash
# For Wayland users, use Xvfb instead:
# Install: sudo apt install xvfb
# Run: xvfb-run -a docker-compose up
```

### Windows
```bash
# Allocate more resources to WSL2
# Edit: %UserProfile%\.wslconfig

[wsl2]
memory=4GB
processors=4
swap=2GB
```

---

## Persistence and Database

The database file (`employeesDB.db`) will be:
- **macOS/Windows:** Created in your project directory (persisted via volume mount)
- **Linux:** Created in your project directory (persisted via volume mount)

### Backup Your Database
```bash
# Copy database to backup location
docker-compose exec ems cp employeesDB.db /app/backup/employeesDB.db

# Or from host (after stopping container)
cp employeesDB.db employeesDB.db.backup
```

---

## Docker Cleanup

```bash
# Remove stopped containers
docker-compose down

# Remove unused images
docker image prune

# Complete cleanup (WARNING: removes all unused Docker resources)
docker system prune -a
```

---

## Success! 🎉

Once the app window appears:
- Test creating employees
- Try search and filtering
- Import/export XML data
- Verify database operations

Enjoy your Employee Management System!

