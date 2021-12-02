FROM python:3

WORKDIR /app
RUN mkdir /synapseconfig

COPY ./requirements.txt ./
COPY ./synapse/data/homeserver.yaml /synapseconfig
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install ./torxakis_0.6.0_amd64.deb -y
RUN python ./sut/adapter.py &

ENTRYPOINT torxakis