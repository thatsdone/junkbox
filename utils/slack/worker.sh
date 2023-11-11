#!/bin/bash
#
# * Slack API rate limite
#   * https://api.slack.com/docs/rate-limits
# * chat.delete
#   *  https://api.slack.com/methods/chat.delete
#   * 'chat.delete' is a Tier 3 API
set -x

CONFIG=${CONFIG:-slackutl.yaml}
P=
#P=${P:-echo}
COUNT=0
MAX=${MAX:-1}
while /bin/true
do
    JSON=`${P} python3 slackutl.py -c ${CONFIG} -o history`
    LOG=`basename ${JSON} .json`.log
    echo ${LOG}
    screen -m -S ${JSON} bash cleanup.sh ${JSON} ${LOG}
    COUNT=`expr ${COUNT} \+ 1`
    if [ ${COUNT} -lt ${MAX} ]; then
        break
    fi
    MSGS=`jq '.messages | length' ${JSON}`
    if [ ${MSGS} -lt 100 ]; then
        break
    fi
done
