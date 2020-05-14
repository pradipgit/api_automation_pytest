#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

echo "pwd"
pwd


echo "[user]
username=$user
apikey=$user_apikey

[instance_environment]
instance_base_url=https://$instance_base_url

[slack]
notification=true
hcms_channel=#$tag_schema_automation_slack_channel
hcms_bot_token=$tag_schema_automation_slack_channel_bot_token
" > common_tag_api_tests.conf

cp common_tag_api_tests.conf /usr/.common_tag/config/

echo "ls -la /usr/.common_tag/config/"
ls -la /usr/.common_tag/config/

echo "cat /usr/.common_tag/config/common_tag_api_tests.conf"
cat /usr/.common_tag/config/common_tag_api_tests.conf

echo "Started running tests....."
pytest -s -v --html=report.html

exec "$@"
