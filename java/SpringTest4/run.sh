#!/bin/bash
set -x
#
# NOTE: kafka bootstrap server hostname must be resolvable from IP
export KAFKA_SERVER=192.168.0.1:9092
export KAFKA_TOPIC=test-topic
export KAFKA_GROUP=mygroup

APP=${APP:=target/SpringTest4-1.0-SNAPSHOT.jar}

java -jar ${APP}
