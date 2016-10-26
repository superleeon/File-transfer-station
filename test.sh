#!/bin/bash
GERRIT_URL=$1
PROJECT=$2
TAG=$3
VM_IP=$4
VM_DOCKER_PORT=$5
BDTCENTER_URL=$6

DIR=$( cd $(dirname ${BASH_SOURCE[0]});pwd ) 
BIN=$(dirname $DIR)
TESTCASE=$(dirname $BIN)
REST_API=${BDTCENTER_URL}/testsuiteTask/pictRobotTest

cd ${TESTCASE}/vnfplugin
zip -r testcase.zip testcase/

curl -F testcase=@testcase.zip -F buildUrl=${GERRIT_URL} -F project=${PROJECT} -F TAG=${TAG} -F vmIp=${VM_IP} -F vmDockerPort=${VM_DOCKER_PORT} ${REST_API}

