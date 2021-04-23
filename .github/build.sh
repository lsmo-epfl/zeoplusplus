#!/bin/bash
set -ex

# download eigen-3
wget https://gitlab.com/libeigen/eigen/-/archive/3.2.7/eigen-3.2.7.tar.bz2
tar xf eigen-3.2.7.tar.bz2

cd voro++
make
cd ../

cd zeo++
CFLAGS="$CFLAGS -I$PREFIX/include/eigen3" make
cd ../
