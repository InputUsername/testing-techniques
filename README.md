# testing-techniques

## Setup

```bash
docker build -t matrixdotorg/synapse -f docker/Dockerfile .
```

```bash
docker run -d --name synapse \
    --mount type=volume,src=synapse-data,dst=/data \
    -p 8008:8008 \
    matrixdotorg/synapse:latest
```

You can then check that it has started correctly with:

```bash
docker logs synapse
```

## Test suite

### Creating test users

- See https://github.com/matrix-org/synapse/blob/develop/synapse/_scripts/register_new_matrix_user.py

- Example: python register_test.py -u marnick -p marnickssecret123 --no-admin -c /data/homeserver.yaml http://localhost:8008
