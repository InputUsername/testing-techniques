#!/bin/sh

echo "runtests.sh"

echo "runtests.sh: Wait for Synapse"
# Wait untill synapse has fully loaded
sleep 5

echo "runtests.sh: Running tests"
# Tests without options
find tests -maxdepth 1 -type f -exec python {} \; > results.out 2>&1

echo "runtests.sh: Done"



