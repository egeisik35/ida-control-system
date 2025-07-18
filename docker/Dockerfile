FROM arm64v8/ubuntu:22.04

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    python3-pygame \
    libxml2-dev libxslt1-dev zlib1g-dev \
    libudev-dev libusb-1.0-0-dev \
    libdbus-1-dev libdbus-glib-1-dev python3-dbus \
    git sudo curl \
    x11-apps \
    && apt-get clean

# Copy requirements.txt and install all Python packages
COPY ../requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip \
    && pip3 install -r /app/requirements.txt

# Optional: install dbus-python if needed via pip
RUN pip3 install dbus-python

WORKDIR /app

# Copy all project files
COPY .. /app

CMD ["python3", "main.py"]
