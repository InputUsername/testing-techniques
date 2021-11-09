#!/bin/sh

echo "runtests.sh"

echo "runtests.sh: Wait for Synapse"
# Wait untill synapse has fully loaded
sleep 2

echo "runtests.sh: Run tests with options"
# Tests with options here
python tests/new-user.py -u marnick -p marnickssecret123 --no-admin -c /synapseconfig/homeserver.yaml http://synapse:8008

echo "runtests.sh: Run tests without options"
# Tests without options
find tests-no-options -maxdepth 1 -type f -exec python {} \;
# find /tests -maxdepth 1 -type f -exec python {} \; > results.out

echo "runtests.sh: Done"



