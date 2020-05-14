MCMP common tag schema API Automation Framework
===============================================

Description
===========
API automation framework for common tag schema service

Prerequisite:
=============
Install python version >= 3.7

Installation
============
* Create python virtual environment and activate it
* git clone git@github.ibm.com:cloudMatrix-CAM/common-tag-schema-api-automation.git
* cd to "common-tag-schema-api-automation" folder
* pip install .


Configuration file:
===================
If repo is installed in python virtual environment, then "/.common_tag/config" folder will be created automatically in
virtual environment home directory. Create a file name with name "common_tag_api_tests.conf" inside "/.common_tag/config/" folder
with below content and modify the content according into instance you are using to run automation.

Add below content to "common_tag_api_tests.conf" file
::
   [user]
   username=<Common Tag Schema User>
   apikey=<Common Tag Schema User API Key>

   [instance_environment]
   base_url=https://mcmp-stage-base-api.multicloud-ibm.com

   [slack]
   notification=true
   hcms_channel=#hcms_opsconsole_squad
   hcms_bot_token=<bot token associated with hcms_channel>


Note:
If repo is installed system wide, then "/.common_tag/config" folder will be created automatically in system home directory.

Logs
=======
logs will be captured in "home_directory/.common_tag/logs/common-tag-timestamp.log"
or in "virtual_environment_home_directory/.common_tag/logs/common-tag-timestamp.log"

Running test cases
==================
Use below command to run test cases from root directory
::
   pytest -s -v --html=report.html