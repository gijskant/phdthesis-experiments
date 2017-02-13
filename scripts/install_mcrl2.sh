#!/usr/bin/env bash

# Fetch mcrl2, configure and build.
prefix=`pwd`

# Release version:
# wget http://www.mcrl2.org/download/release/mcrl2-201409.1.tar.gz
# tar xfz mcrl2-201409.1.tar.gz
# cd mcrl2-201409.1

# Experimental clone:
git clone https://github.com/gijskant/mcrl2-pmc
cd mcrl2-pmc

cmake . -DMCRL2_ENABLE_GUI_TOOLS=OFF -DMCRL2_ENABLE_EXPERIMENTAL=ON -DCMAKE_INSTALL_PREFIX=$prefix
make && make install
cd ..
echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:${prefix}/lib/mcrl2/" > scripts/set_librarypath.sh
chmod +x scripts/set_librarypath.sh
