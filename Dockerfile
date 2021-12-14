FROM ubuntu:20.04

WORKDIR /app
RUN mkdir /synapseconfig
ENV DEBIAN_FRONTEND=noninteractive 
ARG GRAPHWALKER_VERSION="4.3.0"
RUN apt-get update && \
    apt-get install -y \
        wget \
        openjdk-11-jdk \
        python3-venv \
        git \
        curl \
        expect \
        libfuse-dev \
        software-properties-common

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

RUN curl -L -O https://github.com/TorXakis/TorXakis/releases/download/v0.9.0/torxakis-0.9.0.x86_64.AppImage
RUN chmod u+x torxakis-0.9.0.x86_64.AppImage
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.10 python3-pip -y
COPY ./requirements.txt ./
COPY ./synapse/data/homeserver.yaml /synapseconfig
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install --upgrade pip setuptools wheel
COPY install-graphwalker.sh .
RUN chmod +x install-graphwalker.sh
RUN ./install-graphwalker.sh ${GRAPHWALKER_VERSION}
ARG ALTWALKER_VERSION="0.3.1"
RUN python3 -m pip install idna==2.8
RUN python3 -m pip install altwalker==${ALTWALKER_VERSION}


CMD ["./testing/runtests.sh"]
# ./adapter/adapter.py 7890 &
# ./adapter/adapter.py 7891 &
# ./torxakis-0.9.0.x86_64.AppImage --appimage-extract-and-run ./model/Matrix.txs