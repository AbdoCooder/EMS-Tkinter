# Docker Setup for macOS

This guide explains how to run the Employee Management System (EMS) on macOS using Docker.

## Prerequisites

1. **Docker Desktop for Mac** - Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Make sure Docker is running before starting the application

2. **XQuartz** (for displaying Tkinter GUI) - Download from [xquartz.org](https://www.xquartz.org/)
   - After installation, restart your Mac
   - Open XQuartz and go to: **XQuartz > Preferences > Security**
   - Check the box for "Allow connections from network clients"
   - Restart XQuartz

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Navigate to the project directory:**
   ```bash
   cd /path/to/EMS-Tkinter
   ```

2. **Open XQuartz first:**
   ```bash
   open -a XQuartz
   ```

3. **Get your IP address (needed for X11 display):**
   ```bash
   ipconfig getifaddr en0
   ```
   (If that doesn't work, try: `ifconfig | grep inet`)

4. **Update the environment variable in the docker-compose.yml or use this command:**
   ```bash
   DISPLAY=<YOUR_IP>:0 docker-compose up
   ```
   Replace `<YOUR_IP>` with the IP address from step 3.

   Example:
   ```bash
   DISPLAY=192.168.1.100:0 docker-compose up
   ```

### Option 2: Using Docker Commands Directly

1. **Build the Docker image:**
   ```bash
   docker build -t ems-app .
   ```

2. **Open XQuartz:**
   ```bash
   open -a XQuartz
   ```

3. **Get your IP address:**
   ```bash
   ipconfig getifaddr en0
   ```

4. **Run the container:**
   ```bash
   docker run -it \
     --rm \
     -e DISPLAY=<YOUR_IP>:0 \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     -v ~/.Xauthority:/home/appuser/.Xauthority:rw \
     -v $(pwd):/app \
     ems-app
   ```
   Replace `<YOUR_IP>` with your actual IP address.

## Alternative: Using socat for X11 Forwarding (Advanced)

If the above method doesn't work, you can use socat to bridge X11:

1. **Install socat:**
   ```bash
   brew install socat
   ```

2. **Start socat in a terminal window:**
   ```bash
   socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CONNECT:/private/tmp/com.apple.launchd.YOUR_UID/org.macosforge.xquartz:0
   ```

3. **Get your IP address:**
   ```bash
   ipconfig getifaddr en0
   ```

4. **Run the container with the socat method:**
   ```bash
   docker run -it \
     --rm \
     -e DISPLAY=<YOUR_IP>:6000 \
     -v $(pwd):/app \
     ems-app
   ```

## Troubleshooting

### "Cannot connect to X server"
- Make sure XQuartz is running
- Verify the IP address is correct
- Check that "Allow connections from network clients" is enabled in XQuartz preferences

### "Permission denied" for .Xauthority
- Try running with sudo or check file permissions
- Alternatively, use the socat method above

### Container exits immediately
- Check Docker logs: `docker logs ems-tkinter-app`
- Verify all volumes are mounted correctly

## Stopping the Application

- Press `Ctrl+C` in the terminal running Docker
- Or run: `docker-compose down` (if using Docker Compose)

## Notes

- The application data (database files) will persist in the current directory
- All dependencies are automatically installed in the Docker container
- You don't need to install Python or any packages on your macOS system
- The container runs in user mode for security

## For Your Friend

Share this directory with your friend and they only need to:
1. Install Docker Desktop and XQuartz
2. Run the appropriate command from the "Quick Start" section above
3. No need to manually install Python or dependencies!
