#!/bin/bash
cd altwalker-tests
# ls -la
# altwalker --version
gw --version
altwalker online tests -m models/matrix.json "quick_random(vertex_coverage(100) && edge_coverage(100))"
cd ..

echo "Start first adapter"
python3 ./adapter/adapter.py 7890 &

echo "Start second adapter"
python3 ./adapter/adapter.py 7891 &

echo "
****************************************
Start Torxakis test 100
****************************************
"
echo "tester Matrix Sut
test 100
exit" | ./torxakis-0.9.0.x86_64.AppImage --appimage-extract-and-run ./model/Matrix.txs

echo "Kill old adapters"
kill $(jobs -p)

echo "Start first adapter"
python3 ./adapter/adapter.py 7890 &

echo "Start second adapter"
python3 ./adapter/adapter.py 7891 &

echo "
****************************************
Start Torxakis test 100 w/ purpose
****************************************
"
echo "tester Matrix PurpMessageRedaction Sut
test 100
exit" | ./torxakis-0.9.0.x86_64.AppImage --appimage-extract-and-run ./model/Matrix.txs ./model/MatrixPurp.txs
