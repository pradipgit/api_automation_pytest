#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    conftest.py for common tag schema API tests.
"""
import json
from pathlib import Path

import pytest

from common_tag_schema import config
from common_tag_schema import tag_schema_logging
from common_tag_schema.header import create_auth_header
from common_tag_schema.reports_to_slack import post_reports_to_slack


logger = tag_schema_logging.create_logger(logger_name=__name__)
f_logger = tag_schema_logging.create_file_logger(logger=logger)

base_url = config.config.instance_base_url
header = create_auth_header()
slack_notification = bool(json.loads(config.config.notification))
root_dir = str(Path(__file__).resolve().parent.parent)


@pytest.fixture(scope='session', autouse=True)
def root_directory(request):
    """
    :return:
    """
    return str(request.config.rootdir)


# # pytest plugin hook
# def pytest_sessionstart(session):
#     global test_provider_accounts_data
#     aiops_setup(root_dir)
#     test_provider_accounts_data = test_provider_discovery(root_dir)
#     time.sleep(5)
#     # after completing mock discovery, remove system admin role from the user teams
#     unassign_system_admin_role_from_user_teams(root_dir)
#
#
# @pytest.fixture(scope='session', autouse=True)
# def init_cache_total_resources_of_all_accounts(request):
#     data = {
#         "test_provider_accounts_data": test_provider_accounts_data
#     }
#     request.config.cache.set("test_data", data)
#
#
def pytest_unconfigure(config):
    #  provides the value passed with --html command line option
    if slack_notification:
        html_report = config.option.htmlpath
        post_reports_to_slack(root_dir, html_report)

    # provides full path of generated html report
    # if bool(config.config.notification):
    #     html_report_path = config._html.logfile
    #     post_reports_to_slack(html_report_path)
