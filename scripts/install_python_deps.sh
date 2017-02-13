#!/usr/bin/env bash

here=$(realpath $(dirname "${0}"))
prefix=`pwd`

source ${here}/set_path.sh

# Update pip.
echo "Updating pip ..." &&
pip install -I pip --user &&
echo "Installing python dependencies ..." &&
pushd scripts &&
pip install -r requirements.txt --user &&
popd &&
echo "Python dependencies installed."

