#!/bin/bash
#
# update-sg.sh : A tiniy utility to update AWS Security Group
#   allowing the source (global IP) to connect to the security group.
#
#   Note that the below permits all the protocols from the source (unicast) IP.
#
set -x
#
PROFILE=${PROFILE:-YOUR_PROFILE}
REGION=${REGION:-YOUR_REGION}
# set your security group id. e.g. 
SG_ID=${SG_ID:-sg-0123456789abcdef0}
# set your security group rule id. e.g. sgr-0123456789abcdef0
SGR_ID=${SGR_ID:-sgr-0123456789abcdef0}
#
#
RANGE=${RANGE:-32}

export AWS_PROFILE=${PROFILE}
export AWS_DEFAULT_REGION=${REGION}

CURRENT_IP=`curl -s http://ifconfig.me`
echo "CURRENT_IP : " ${CURRENT_IP}

#
# get the current source IP (range) of the given SGR of SG.
#
SG_IP=`aws ec2 describe-security-group-rules --filters Name="group-id",Values="${SG_ID}" | jq -r '.SecurityGroupRules[] | select(.SecurityGroupRuleId == "'${SGR_ID}'") | .CidrIpv4'`

echo "SG_IP : "${SG_IP}

if [ "${SG_IP}" != "${CURRENT_IP}"/${RANGE} ]; then
    echo Source IP changed. Updating SG rule.
    #
    # Change detected, update the rule
    #
    aws ec2 modify-security-group-rules \
    --group-id ${SG_ID} \
    --security-group-rules "SecurityGroupRuleId=${SGR_ID},SecurityGroupRule={Description=\"mitoh home\",IpProtocol=-1,CidrIpv4=${CURRENT_IP}/${RANGE}}"
    #
    # show the updated rule
    #
    aws ec2 describe-security-group-rules --filters Name="group-id",Values="${SG_ID}" | jq -r '.SecurityGroupRules[] | select(.SecurityGroupRuleId == "'${SGR_ID}'")'
fi
