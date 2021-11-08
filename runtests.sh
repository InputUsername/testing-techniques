#!/bin/sh

# Wait untill synapse has fully loaded
sleep 2

# Tests with options here
python tests/new-user.py -u marnick -p marnickssecret123 --no-admin -c sdata/homeserver.yaml http://synapse:8008

# Tests without options
find /tests-no-options -maxdepth 1 -type f -exec python {} \;
# find /tests -maxdepth 1 -type f -exec python {} \; > results.out



