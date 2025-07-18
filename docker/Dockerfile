
FROM arm64v8/ubuntu:22.04 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    python3-pygame \
    libxml2-dev libxslt1-dev zlib1g-dev \
    libudev-dev libusb-1.0-0-dev \
    libdbus-1-dev libdbus-glib-1-dev python3-dbus \
    git sudo curl \
    x11-apps \
    && apt-get clean

COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

RUN pip3 install dbus-python

WORKDIR /app
COPY . /app

CMD ["python3", "main.py"]
