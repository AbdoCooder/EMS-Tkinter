FROM python:3.11-slim

# Install dependencies for Tkinter, X11, and VNC
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev \
    x11-apps \
    xauth \
    x11vnc \
    xvfb \
    fluxbox \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install websockify via pip
RUN pip install --no-cache-dir websockify numpy

# Install noVNC for web-based VNC access
RUN wget -qO- https://github.com/novnc/noVNC/archive/refs/tags/v1.4.0.tar.gz | tar xz -C /opt/ \
    && mv /opt/noVNC-1.4.0 /opt/novnc \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

WORKDIR /app

COPY . /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create startup script
RUN echo '#!/bin/bash\n\
Xvfb :99 -screen 0 1920x1080x24 &\n\
export DISPLAY=:99\n\
fluxbox &\n\
x11vnc -display :99 -nopw -listen 0.0.0.0 -xkb -forever -shared -threads &\n\
websockify --web /opt/novnc 6080 localhost:5900 &\n\
sleep 2\n\
python main.py\n\
tail -f /dev/null\n\
' > /start.sh && chmod +x /start.sh

EXPOSE 6080

CMD ["/start.sh"]