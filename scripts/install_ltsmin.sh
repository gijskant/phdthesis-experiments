#!/usr/bin/env bash

SYLVAN_VERSION=1.1.0
SYLVAN_URL=https://github.com/trolando/sylvan/archive/v${SYLVAN_VERSION}.tar.gz
SYLVAN_NAME=sylvan-${SYLVAN_VERSION}

LTSMIN_URL=https://github.com/utwente-fmt/ltsmin.git
LTSMIN_BRANCH=next

here=$(realpath $(dirname "${0}"))
prefix=`pwd`

source ${here}/set_path.sh

# Fetch Sylvan, build, install.
if [ ! -f "${prefix}/lib/libsylvan.a" ]; then
    echo "Installing Sylvan ..." &&
    {
        mkdir -p deps/sylvan &&
        pushd deps/sylvan &&
        wget "$SYLVAN_URL" &&
        tar -xf "v${SYLVAN_VERSION}.tar.gz" &&
        pushd sylvan-${SYLVAN_VERSION} &&
        mkdir build &&
        cd build &&
        cmake .. -DSYLVAN_BUILD_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX="${prefix}" &&
        make &&
        make install &&
        popd &&
        popd &&
        echo "Sylvan installed."
    } || {
        echo "Sylvan could not be installed."
        exit 1
    }
fi

# Fetch LTSmin from github, configure and build.
echo "Installing LTSmin ..." &&
mkdir -p deps &&
pushd deps &&
{
    git clone ${LTSMIN_URL} -b ${LTSMIN_BRANCH} ||
    echo "LTSmin repository already present."
} &&
pushd ltsmin &&
git checkout ${LTSMIN_BRANCH} &&
git pull &&
git submodule update --init &&
./ltsminreconf &&
./configure  --prefix="${prefix}" --with-mcrl2="${prefix}" &&
make && make install &&
popd &&
popd &&
echo "LTSmin installed."
