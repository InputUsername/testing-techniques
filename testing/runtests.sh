#!/bin/bash
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
echo "tester Matrix Sut
test 100
exit" | ./torxakis-0.9.0.x86_64.AppImage --appimage-extract-and-run ./model/Matrix.txs ./model/MatrixPurp.txs