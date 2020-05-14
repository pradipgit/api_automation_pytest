#!/bin/bash

set -o errexit
set -o nounset

docker ps -a | grep 'common-tag-schema-api-automation' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f

# Login to Docker
echo "==> Login to docker container..."
docker login -u "$1" -p "$2" ibmcb-docker-local.artifactory.swg-devops.com

# Pull Docker Image which has common tag schema API test suite
echo "==> Pull docker iamge..."
docker pull ibmcb-docker-local.artifactory.swg-devops.com/common-tag-schema-api-automation

# Start running docker container
echo "==> Running docker container..."
docker run --rm -e app_build_version=$3 -e instance_base_url=$4 -e user=$5 -e user_apikey=$6 \
       -e tag_schema_automation_slack_channel=$7 -e tag_schema_automation_slack_channel_bot_token=$8 \
       --name common-tag-schema-api-automation ibmcb-docker-local.artifactory.swg-devops.com/common-tag-schema-api-automation
