#!/bin/bash
set -x

ESDK=esdk-obs-java-optimization-3.21.4.jar
LIBS=libs/annotations-13.0.jar:libs/esdk-obs-java-3.21.4.jar:libs/jackson-annotations-2.11.1.jar:libs/jackson-core-2.11.1.jar:libs/jackson-databind-2.11.1.jar:libs/java-xmlbuilder-1.3.jar:libs/kotlin-stdlib-1.3.72.jar:libs/kotlin-stdlib-common-1.3.70.jar:libs/log4j-api-2.13.3.jar:libs/log4j-core-2.13.3.jar:libs/okhttp-2.7.5.jar:libs/okio-2.7.0.jar

TARGET=target/ObsTest1-1.0-SNAPSHOT-jar-with-dependencies.jar
MAIN=com.github.thatsdone.junkbox.ObsTest1


#java -cp ${ESDK}:${LIBS}:${TARGET} ${MAIN}
java -cp ${TARGET} ${MAIN} $*
