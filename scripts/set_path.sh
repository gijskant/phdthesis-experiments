#!/usr/bin/env bash

prefix=`pwd`
echo "Setting path to include ${prefix}."
export PATH=${prefix}/bin:${PATH}
export LD_LIBRARY_PATH=${prefix}/lib:${prefix}/lib/mcrl2:${LD_LIBRARY_PATH}
export PKG_CONFIG_LIBDIR=${prefix}/lib/pkgconfig
