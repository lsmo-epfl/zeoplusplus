#!/bin/bash
set -ex

cd voro++
make
cd ../

cd zeo++
CFLAGS="$CFLAGS -I$PREFIX/include/eigen3" make
cd ../
