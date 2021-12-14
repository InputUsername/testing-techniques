FROM ubuntu:20.04

WORKDIR /app
RUN mkdir /synapseconfig

RUN apt-get update
RUN apt-get install curl -y
RUN apt-get install expect -y
RUN apt-get install libfuse-dev -y
RUN curl -L -O https://github.com/TorXakis/TorXakis/releases/download/v0.9.0/torxakis-0.9.0.x86_64.AppImage
RUN chmod u+x torxakis-0.9.0.x86_64.AppImage
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.10 -y
RUN apt-get install python3-pip -y
COPY ./requirements.txt ./
COPY ./synapse/data/homeserver.yaml /synapseconfig
RUN pip install --no-cache-dir -r requirements.txt
COPY ./adapter ./adapter
COPY ./model ./model

CMD ["./testing/runtests.sh"]
# ./adapter/adapter.py 7890 &
# ./adapter/adapter.py 7891 &
# ./torxakis-0.9.0.x86_64.AppImage --appimage-extract-and-run ./model/Matrix.txs