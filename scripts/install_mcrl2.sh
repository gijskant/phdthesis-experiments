#!/usr/bin/env bash

MCRL2_SOURCE=dev # any other value than 'dev' will fetch release
MCRL2_DEV_URL=https://github.com/gijskant/mcrl2-pmc
MCRL2_RELEASE=mcrl2-201409.1
MCRL2_RELEASE_URL=http://www.mcrl2.org/download/release/${MCRL2_RELEASE}.tar.gz

# Fetch mcrl2, configure and build.
prefix=`pwd`

echo "Installing mCRL2 ..." && {
    echo "Fetching sources ..."
    if [ "${MCRL2_SOURCE}" == "dev" ]; then
        # Fetch dev version
        target=mcrl2-pmc && {
            [ -e "${target}" ] &&
            echo "mCRL2 repository already present."
        } || {
            git clone ${MCRL2_DEV_URL}
        }
    else
        # Fetch release version
        wget ${MCRL2_RELEASE_URL} &&
        tar xfz ${MCRL2_RELEASE}.tar.gz &&
        target=${MCRL2_RELEASE}
    fi
} &&
pushd ${target} &&
cmake . -DMCRL2_ENABLE_GUI_TOOLS=OFF -DMCRL2_ENABLE_EXPERIMENTAL=ON -DCMAKE_INSTALL_PREFIX=${prefix} &&
make && make install &&
popd &&
echo "mCRL2 installed."
