#!/usr/bin/env bash

here=$(realpath $(dirname "${0}"))

# Update pip.
echo "Updating pip ..." &&
pip install -I pip --user &&
echo "Installing python dependencies ..." &&
pip install -r "${here}/requirements.txt" --user &&
echo "Python dependencies installed."
