FROM debian:bookworm-slim
FROM python:3.10.2-slim-buster

RUN apt-get -qq update -y && apt-get -qq upgrade -y

RUN set -eux; \
	\
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
                libxml2 \
                libxslt

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
