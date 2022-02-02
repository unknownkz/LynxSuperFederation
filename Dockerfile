FROM debian:bookworm-slim
FROM python:3.10.2-slim-buster

# install dependencies
FROM ubuntu:16.04
RUN apt-get update -y
RUN apt-get -qq install g++ gcc libxml2 libxslt-dev -y

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
RUN apt-get -qq update -y && apt-get -qq upgrade -y

COPY . .

RUN chmod a+x startapp
CMD ["./startapp"]
