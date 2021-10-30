#!/bin/bash
set -x

TARGET=target/Nd4jTest1-1.0-SNAPSHOT-jar-with-dependencies.jar
MAIN=com.github.thatsdone.junkbox.Nd4jTest1
LIBPATH=lib
LIB=${LIBPATH}/slf4j-nop-1.7.32.jar

java -cp ${TARGET}:${LIB} ${MAIN} $*
