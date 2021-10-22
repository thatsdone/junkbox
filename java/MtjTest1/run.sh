#!/bin/bash
set -x

TARGET=target/MtjTest1-1.0-SNAPSHOT-jar-with-dependencies.jar
LIB=lib/algorithmfoundry-shade-culled-1.3.jar
MAIN=com.github.thatsdone.junkbox.MtjTest1


java -cp ${TARGET}:${LIB} ${MAIN} $*
