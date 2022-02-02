FROM python:3.9-alpine AS python-build

RUN apk add --no-cache \
        g++ \
        gcc \
        libxml2 \
        libxslt-dev

RUN mkdir -p /opt/venv
WORKDIR /opt/venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /src
WORKDIR /src

# Install bot package and dependencies
COPY . .
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install aiohttp[speedups]
RUN pip install uvloop
RUN pip install .

# Build Programs
FROM debian:bookworm-slim
FROM python:3.10.2-slim-buster

RUN apt-get -qq install -y \
    git \
    python3-pip \
    curl \
    bash \
    neofetch \
    ffmpeg \
    software-properties-common

RUN git clone https://github.com/unknownkz/LynxSuperFederation /usr/src/lsf

COPY requirements.txt .

WORKDIR /usr/src/lsf

RUN pip3 install --no-cache-dir -U -r requirements.txt

COPY . .

RUN chmod a+x startapp
CMD ["./startapp"]
