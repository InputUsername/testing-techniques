#!/bin/sh

echo "runtests.sh"

echo "runtests.sh: Wait for Synapse"
# Wait untill synapse has fully loaded
sleep 5

echo "runtests.sh: Run tests without options"
# Tests without options
find tests -maxdepth 1 -type f -exec python {} \; > results.out

echo "runtests.sh: Done"



