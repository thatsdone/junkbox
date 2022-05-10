#!/bin/bash
#set -x
#
# imulogger-cleaner.sh
#
# This script is used accompany with the imulogger.py.
#
# * imulogger.py :
#   collect IMU data on a IoT device such as RaspberryPI, and
#   send out via some method such as scp.
# * imulogger-cleaner.sh :
#   compress raw data via xz on the receiver side.
# 
# TODO:
#  * ...
#

INTERVAL=${INTERVAL:-`expr 3 \* 3600`}

P=${P:-}
DIR=${DIR:-/home/mitoh/junkbox/iot}


scan () {
    echo scanning: ${DIR}
    NUM_FILES=`ls -S ${DIR}/zero1-imu-*.bin | wc -l`
    if [ ${NUM_FILES} -gt 1 ]; then
	NUM=`expr ${NUM_FILES} \- 1`
	FILES=`ls -S ${DIR}/zero1-imu-*.bin | head -${NUM}`
	for f in ${FILES}
	do
            if [ -e ${f}.saved ]; then
		echo deleting: ${f}
		${P} /bin/rm -f ${f} ${f}.saved
            fi
	done
    fi
}

echo $0: cleaning ${DIR} every ${INTERVAL} seconds
while true
do
    date
    scan
    sleep ${INTERVAL} 
done

