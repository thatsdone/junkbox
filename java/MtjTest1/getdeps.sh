#!/bin/bash
set -x
SRC="https://github.com/numenta/htm.java/raw/master/libs/algorithmfoundry-shade-culled-1.3.jar"

mkdir -p lib
pushd .
cd lib
wget ${SRC} 
popd

