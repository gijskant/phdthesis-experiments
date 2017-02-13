#!/usr/bin/env bash

CMAKE_VERSION=cmake-3.7.2
CMAKE_SOURCE_URL=https://cmake.org/files/v3.7/${CMAKE_VERSION}.tar.gz

prefix=`pwd`

# Fetch build and install cmake.
echo "Installing cmake ..." &&
mkdir -p deps &&
pushd deps &&
wget ${CMAKE_SOURCE_URL} &&
tar -xf ${CMAKE_VERSION}.tar.gz &&
pushd ${CMAKE_VERSION} &&
./bootstrap --prefix="${prefix}" &&
make && make install &&
popd &&
popd &&
echo "cmake installed."
