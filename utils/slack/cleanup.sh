#!/bin/bash
#
# * Slack API rate limite
#   * https://api.slack.com/docs/rate-limits
# * chat.delete
#   *  https://api.slack.com/methods/chat.delete
#   * 'chat.delete' is a Tier 3 API
set -x

DATAFILE=$1
LOGFILE=$2

INTERVAL=${INTERVAL:-2}
CONFIG=${CONFIG:-slackutl.yaml}
#P=${P:-echo}
P=
for f in ${DATAFILE}
do
    TIMESTAMPS=`jq -r '.messages[].ts' ${f}`
    echo deleteing messages in: ${f}
    for ts in ${TIMESTAMPS}
    do
        date
        echo deleting a message with timestamp: ${ts}
        ${P} python3 slackutl.py -c ${CONFIG} -o delete -t ${ts}
        sleep ${INTERVAL}
    done
    screen -S ${DATAFILE} -X hardcopy -h ${LOGFILE}
done

