FROM python:3.11-slim

# Install dependencies for Tkinter and X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

ENV DISPLAY=:0

CMD ["python", "main.py"]
