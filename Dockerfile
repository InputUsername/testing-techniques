FROM python:3

WORKDIR /app
RUN mkdir /synapseconfig

COPY ./testing/requirements.txt ./
COPY ./synapse/data/homeserver.yaml /synapseconfig
RUN pip install --no-cache-dir -r requirements.txt

CMD ["./runtests.sh"]