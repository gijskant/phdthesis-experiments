#!/usr/bin/env bash

# Fetch LTSmin from github, configure and build.
git clone https://github.com/utwente-fmt/ltsmin.git -b next # tacas2015
prefix=`pwd`
cd ltsmin
git submodule update --init
./ltsminreconf
./configure  --prefix=$prefix --with-mcrl2=$prefix
make && make install
