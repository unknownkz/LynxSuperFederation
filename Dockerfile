# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src/lsf

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add g++ gcc libxml2 libxslt-dev
RUN python -m pip install --upgrade pip
# install dependencies

CMD [python3]

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
RUN apt-get -qq update -y && apt-get -qq upgrade -y

COPY . .

RUN chmod a+x startapp
CMD ["./startapp"]
