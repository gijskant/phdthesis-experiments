#!/usr/bin/env bash

MCRL2_SOURCE=dev # any other value than 'dev' will fetch release
MCRL2_DEV_URL=https://github.com/gijskant/mcrl2-pmc
MCRL2_DEV_TAG=kant-thesis-experiments
MCRL2_RELEASE=mcrl2-201409.1
MCRL2_RELEASE_URL=http://www.mcrl2.org/download/release/${MCRL2_RELEASE}.tar.gz

here=$(realpath $(dirname "${0}"))
prefix=`pwd`

source ${here}/set_path.sh

# Fetch mcrl2, configure and build.
echo "Installing mCRL2 ..." &&
mkdir -p deps &&
pushd deps && {
    echo "Fetching sources ..."
    if [ "${MCRL2_SOURCE}" == "dev" ]; then
        # Fetch dev version
        target=mcrl2-pmc && {
            [ -e "${target}" ] &&
            echo "mCRL2 repository already present."
        } || {
            git clone ${MCRL2_DEV_URL} --branch ${MCRL2_DEV_TAG}
        }
    else
        # Fetch release version
        wget ${MCRL2_RELEASE_URL} &&
        tar xfz ${MCRL2_RELEASE}.tar.gz &&
        target=${MCRL2_RELEASE}
    fi
} &&
pushd ${target} &&
cmake . -DMCRL2_ENABLE_GUI_TOOLS=OFF -DMCRL2_ENABLE_EXPERIMENTAL=ON -DCMAKE_INSTALL_PREFIX="${prefix}" &&
make && make install &&
popd &&
popd &&
echo "mCRL2 installed."
