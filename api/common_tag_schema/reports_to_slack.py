import requests

from common_tag_schema import config
from common_tag_schema import tag_schema_logging


logger = tag_schema_logging.create_logger(logger_name=__name__)
f_logger = tag_schema_logging.create_file_logger(logger=logger)


def post_reports_to_slack(root_dir, html_report):
    """

    :return:
    """
    url = "https://slack.com/api/files.upload"
    css_file_path = root_dir + "/assets/style.css"

    with open(css_file_path) as fh:
        css_data = fh.read()

    with open(html_report, "r") as fh:
        html_lines = fh.readlines()
        for index, line in enumerate(html_lines):
            if line == '<link href="assets/style.css" rel="stylesheet" type="text/css"/></head>\n' \
                    or line == '    <link href="assets/style.css" rel="stylesheet" type="text/css"/></head>\n':
                html_lines.remove(line)
                html_lines.insert(index, "<style>\n")
                html_lines.insert(index+1, css_data)
                html_lines.insert(index+2, "</style>\n")
                html_lines.insert(index+3, "</head>\n")

            if config.config.apikey in line:
                new_line = line.replace(config.config.apikey, "##### Blacked out API KEY #####")
                html_lines.remove(line)
                html_lines.insert(index, new_line)

        html_data = "".join(html_lines)

    data = {
        "token": config.config.hcms_bot_token,
        "channels": config.config.hcms_channel,
        "content": html_data,
        "filename": html_report,
        "filetype": "html",
        "initial_comment": "Common Tag Schema API Automation Test Report",
        "title": "Common Tag Schema API Automation Test Report"
    }

    response = requests.post(
        url=url, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    response_data = response.json()
    if response_data["ok"] is True:
        print("successfully sent test report to slack channel 'hcms_opsconsole_squad'"
              "and status code is %s" % response.status_code)
    else:
        print("Failed to send test report to slack channel 'hcms_opsconsole_squad'"
              "and status code is %s" % response_data, response.status_code)
