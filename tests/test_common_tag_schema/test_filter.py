import pytest

from common_tag_schema.policies import client
from common_tag_schema import tag_schema_logging
from common_tag_schema import config
from common_tag_schema import header


logger = tag_schema_logging.create_logger(logger_name=__name__)
f_logger = tag_schema_logging.create_file_logger(logger=logger)


test_data1 = [
    (config.config.instance_base_url, header.create_auth_header(), "auth")
]


def _iterate_json(json_data):
    if isinstance(json_data, dict):
        for item in json_data.values():
            yield from _iterate_json(item)
    elif any(isinstance(json_data, t) for t in (list, tuple)):
        for item in json_data:
            yield from _iterate_json(item)
    else:
        yield json_data


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_search_for_complete_text(instance_base_url,
                                  auth_header, request_type):
    """
    @summary: Test to return list of policies
    """
    count_of_text_standard = 0
    response = client.get_policies_list(instance_base_url, auth_header, request_type,
                                        size=100000000, searchtext="standard")
    response_data = response.json()

    for item in _iterate_json(response_data["data"]["records"]):
        if isinstance(item, str) and item.startswith("standard"):
            count_of_text_standard += 1

    assert response_data["data"]["count"] == count_of_text_standard
    assert response.status_code == 200
    assert response_data["message"] == "Fetched policies successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1002"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_search_for_texts_stem_from_same_text(instance_base_url,
                                              auth_header, request_type):
    """
    @summary: Test to return list of policies
    """
    count_of_texts_stem_from_search_rext = 0
    response = client.get_policies_list(instance_base_url, auth_header, request_type,
                                        size=100000000, searchtext="context")
    response_data = response.json()

    for item in _iterate_json(response_data["data"]["records"]):
        if isinstance(item, str) and item.startswith("context"):
            count_of_texts_stem_from_search_rext += 1

    assert response_data["data"]["count"] == count_of_texts_stem_from_search_rext
    assert response.status_code == 200
    assert response_data["message"] == "Fetched policies successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1002"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_search_for_partial_text(instance_base_url,
                                 auth_header, request_type):
    """
    @summary: Test to return list of policies
    """
    response = client.get_policies_list(instance_base_url, auth_header, request_type,
                                        size=100000000, searchtext="stan")
    response_data = response.json()

    assert response_data["data"]["count"] == 0
    assert response.status_code == 200
    assert response_data["message"] == "Fetched policies successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1002"
