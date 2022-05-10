#!/bin/bash
#set -x
#
# imulogger-compressor.sh
#
# This script is used accompany with the imulogger.py.
#
# * imulogger.py :
#   collect IMU data on a IoT device such as RaspberryPI, and
#   send out via some method such as scp.
#
# * imulogger-compressor.sh :
#   compress raw data via xz on the receiver side.
# 
# TODO:
#  * ...
#
INTERVAL=${INTERVAL:-`expr 3 \* 3600`}
#
PREFIX=${PREFIX:-zero1-imu}
#
P=${P:-}
DIR=${DIR:-`pwd`}
#
scan () {
    echo scanning: ${DIR}
    FILES=`ls -S ${DIR}/${PREFIX}-*.bin`
    NUM_FILES=`ls -S ${DIR}/${PREFIX}-*.bin | wc -l`
    if [ ${NUM_FILES} -gt 1 ]; then
	NUM=`expr ${NUM_FILES} \- 1`
	TARGET_FILES=`echo ${FILES} | head -${NUM}`
	for f in ${TARGET_FILES}
	do
	    echo compressing: ${f}
	    ${P} xz ${f}
	done
    fi
}
#
#
#
echo $0: compressing ${DIR} every ${INTERVAL} seconds
while true
do
    date
    scan
    sleep ${INTERVAL} 
done

