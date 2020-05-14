import random
import string

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


test_data2 = [
    (config.config.instance_base_url, header.create_unauth_header(), "unauth"),
    (config.config.instance_base_url, header.create_auth_header(), "invalid_request"),
]

test_data3 = [
    (config.config.instance_base_url, header.create_unauth_header(), "unauth"),
    (config.config.instance_base_url, header.create_auth_header(), "invalid_request"),
    (config.config.instance_base_url, header.create_auth_header(), "bad_request")
]


@pytest.fixture(scope="module")
def create_policy_fixture(root_directory):
    """
    @summary: Creates policy which will be used by all test cases in this module.
    After execution of all test cases, created policy will be deleted
    :param root_directory: root directory of the project
    """
    instance_base_url = config.config.instance_base_url
    auth_header = header.create_auth_header()
    request_type = "auth"

    response = client.create_tag_schema_policy(
        root_directory, instance_base_url, auth_header, request_type, policy_type="standard")
    if response.status_code == 201:
        f_logger.info("policy created successfully and status code is '%s'" % response.status_code)
    else:
        f_logger.error("Failed to create policy and status code is '%s'" % response.status_code)

    yield response

    response_data = response.json()
    client.delete_tag_schema_policy(instance_base_url, auth_header, response_data["data"]["name"])
    f_logger.info(" Clean up---- '%s'  Policy deleted after execution of all test "
                  "cases in a module '%s' " % (response_data["data"]["name"], __name__))


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_get_policies_list(instance_base_url,
                           auth_header, request_type):
    """
    @summary: Test to return list of policies
    """
    response = client.get_policies_list(instance_base_url, auth_header, request_type)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "Fetched policies successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1002"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data2)
def test_get_policies_list_negative(instance_base_url,
                                    auth_header, request_type):
    """
    @summary: This test covers negative scenarios of list policies API
    """
    if request_type == "unauth":
        response = client.get_policies_list(instance_base_url, auth_header, request_type)
        assert response.status_code == 401
    elif request_type == "invalid_request":
        response = client.get_policies_list(instance_base_url, auth_header, request_type)
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["message"] == "Policy {0} does not exist"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_113"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_get_policy_details(create_policy_fixture, instance_base_url,
                            auth_header, request_type):
    """
    @summary: Test to get details about a single policy
    """
    response = create_policy_fixture

    response_data = response.json()

    policy_name = response_data["data"]["name"]

    response = client.get_policy_details(instance_base_url, auth_header, policy_name)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "Fetched policy {0} successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1003"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data2)
def test_get_policy_details_negative(create_policy_fixture, instance_base_url,
                                     auth_header, request_type):
    """
    @summary: Negative test to get details about a single policy
    """
    response = create_policy_fixture

    response_data = response.json()
    if request_type == "invalid_request":
        policy_name = "policy_name_doesnt_exist"
    else:
        policy_name = response_data["data"]["name"]

    if request_type == "unauth":
        response = client.get_policy_details(instance_base_url, auth_header, policy_name)
        assert response.status_code == 401
    elif request_type == "invalid_request":
        response = client.get_policy_details(instance_base_url, auth_header, policy_name)
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["message"] == "Policy {0} does not exist"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_113"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_standard_policy_with_mandatory_params(root_directory, instance_base_url,
                                                      auth_header, request_type):

    """
    @summary: Test to create a standard policy with mandatory parameters
    """
    if request_type == "auth":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data3)
def test_create_standard_policy_with_mandatory_params_negative(root_directory, instance_base_url,
                                                      auth_header, request_type):

    """
    @summary: Negative test to create a standard policy with mandatory parameters
    """
    if request_type == "unauth":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False)
        assert response.status_code == 401
    elif request_type == "invalid_request":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False)
        assert response.status_code == 401
    elif request_type == "bad_request":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False)
        response_data = response.json()
        assert response.status_code == 400
        assert response_data["message"] == "Invalid payload: {0}"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_standard_policy_with_optional_params(root_directory, instance_base_url,
                                                     auth_header, request_type):
    """
    @summary: Test to create a standard policy with optional parameters
    :param root_directory:
    :param instance_base_url:
    :param auth_header:
    :param request_type:
    :return:
    """
    if request_type == "auth":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=True)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_custom_policy_with_mandatory_params(root_directory, instance_base_url,
                                                    auth_header, request_type):
    """
    @summary: Test to create a custom policy with mandatory parameters
    :param root_directory:
    :param instance_base_url:
    :param auth_header:
    :param request_type:
    :return:
    """
    if request_type == "auth":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="custom",
                                                   optional_policy_params=False)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_custom_policy_with_optional_params(root_directory, instance_base_url,
                                                   auth_header, request_type):
    """
    @summary: Test to create a custom policy with optional parameters
    :param root_directory:
    :param instance_base_url:
    :param auth_header:
    :param request_type:
    :return:
    """
    if request_type == "auth":
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="custom",
                                                   optional_policy_params=True)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_existing_same_policy_name(root_directory, create_policy_fixture, instance_base_url,
                                                      auth_header, request_type):
    """
    @summary: Test to create a policy with existing policy name
    :param root_directory:
    :param create_policy_fixture:
    :param instance_base_url:
    :param auth_header:
    :param request_type:
    :return:
    """
    response = create_policy_fixture
    response_data = response.json()
    policy_name = response_data["data"]["name"]

    if request_type == "auth":
        policy_details_response = client.get_policy_details(instance_base_url, auth_header, policy_name)
        policy_details_response = policy_details_response.json()
        # policy_name = policy_details_response["data"]["name"]
        policy_type = policy_details_response["data"]["policy_units"][0]["policy_type"]

        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type=policy_type, policy_name=policy_name)
        response_data = response.json()
        assert response.status_code == 409
        assert response_data["message"] == "Policy with same name/conditions already exists"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_116"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_status(root_directory, instance_base_url,
                                         auth_header, request_type):

    """
    @summary: Test to create a single policy
    """
    for valid_status in ["active", "inactive"]:
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False, status=valid_status)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_status(root_directory, instance_base_url,
                                           auth_header, request_type):

    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False, status="invalid_status")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Invalid payload: {0}"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_max_description(root_directory, instance_base_url,
                                            auth_header, request_type):
    max_description = ""
    random_characters = random.randint(202, 210)
    for i in range(0, random_characters):
        max_description += random.choice(string.ascii_letters + string.digits)

    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False, description=max_description)
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Invalid payload: {0}"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_combinator(root_directory, instance_base_url,
                                             auth_header, request_type):
    for valid_combinator_value in ["ALL", "ANY"]:
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False, combinator=valid_combinator_value)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_combinator(root_directory, instance_base_url,
                                               auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False, combinator="invalid_combinator_value")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Combinator can be only 'ANY/ALL'"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_118"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_applies_to(root_directory, instance_base_url,
                                             auth_header, request_type):
    for valid_applies_to_value in ["key", "value", "both"]:
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False, applies_to=valid_applies_to_value)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_applies_to(root_directory, instance_base_url,
                                               auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False, applies_to="invalid_applies_to_value")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Invalid payload: {0}"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_providers(root_directory, instance_base_url,
                                            auth_header, request_type):
    providers = ["amazon", "aws", "azure", "gcp",
                 "google", "ibm", "vra", "snow"]
    number_of_items = random.randint(1, len(providers))
    providers = random.sample(providers, number_of_items)
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False, providers=providers)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["message"] == "Created policy {0} successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_providers(root_directory, instance_base_url,
                                              auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False, providers=["invalid_providers_value"])
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Provider not supported."
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_122"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_conditions(root_directory, instance_base_url,
                                             auth_header, request_type):
    conditions_name = ["category", "service_type", "tag_purpose", "context.app", "context.org"]
    for condition_name in conditions_name:
        if condition_name == "tag_purpose" or \
                condition_name == "context.app" or \
                condition_name == "context.org":
            operator = "is"
        else:
            operator = random.choice(["is", "not", "contains", "starts_with", "ends_with"])
        response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                                   request_type, policy_type="standard",
                                                   optional_policy_params=False,
                                                   conditions_name=condition_name,
                                                   operator=operator)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Created policy {0} successfully"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_conditions(root_directory, instance_base_url,
                                               auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               conditions_name="invalid_conditions_name")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Condition name {0} is not supported"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_114"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_two_valid_duplicate_conditions(root_directory, instance_base_url,
                                                           auth_header, request_type):

    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               conditions_name="duplicate_conditions",
                                               )
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Invalid payload: {0}"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_operator_for_tag_purpose(root_directory, instance_base_url,
                                                             auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               conditions_name="tag_purpose",
                                               operator="starts_with")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Condition name {0} and operator {1} do not match"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_106"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_operator_for_context(root_directory, instance_base_url,
                                                         auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               conditions_name="context.app",
                                               operator="ends_with")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Condition name {0} and operator {1} do not match"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_106"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_operator_for_category(root_directory, instance_base_url,
                                                          auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               conditions_name="category",
                                               operator="invalid_operator_value")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Condition name {0} and operator {1} do not match"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_106"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_operator_for_service_type(root_directory, instance_base_url,
                                                              auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               conditions_name="service_type",
                                               operator="invalid_operator_value")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Condition name {0} and operator {1} do not match"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_106"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_allowed_list(root_directory, instance_base_url,
                                               auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               allowed_list=[{"tag_key": "k1", "tag_values": ["v1"]}])
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["message"] == "Created policy {0} successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_allowed_list(root_directory, instance_base_url,
                                                 auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               allowed_list=["t_key1", "t_value1"])
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Invalid payload: {0}"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_valid_regex(root_directory, instance_base_url,
                                        auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               regex="abcd")
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["message"] == "Created policy {0} successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1006"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_invalid_regex(root_directory, instance_base_url,
                                          auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               regex=["abcd"])
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "Invalid payload: {0}"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_create_policy_with_allowed_list_and_regex(root_directory, instance_base_url,
                                                   auth_header, request_type):
    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="standard",
                                               optional_policy_params=False,
                                               allowed_list=[{"tag_key": "k1", "tag_values": ["v1"]}],
                                               regex="abcd")
    response_data = response.json()
    assert response.status_code == 400
    assert response_data["message"] == "allowed_list and regex cannot be used together"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_107"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_update_standard_policy_with_mandatory_params(root_directory, create_policy_fixture, instance_base_url,
                                                      auth_header, request_type):
    response = create_policy_fixture
    response_data = response.json()
    policy_name = response_data["data"]["name"]

    response = client.get_policy_details(instance_base_url, auth_header, policy_name)
    policy_data = response.json()

    response = client.update_tag_schema_policy(root_directory, instance_base_url, auth_header, request_type,
                                               policy_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "Updated policy {0} successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1004"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data3)
def test_update_standard_policy_with_mandatory_params_negative(root_directory, create_policy_fixture, instance_base_url,
                                                               auth_header, request_type):
    response = create_policy_fixture
    response_data = response.json()
    policy_name = response_data["data"]["name"]

    policy_data = None
    if request_type != "unauth":
        response = client.get_policy_details(instance_base_url, auth_header, policy_name)
        policy_data = response.json()

    if request_type == "unauth":
        response = client.update_tag_schema_policy(root_directory, instance_base_url, auth_header, request_type, policy_data)
        assert response.status_code == 401
    elif request_type == "invalid_request":
        response = client.update_tag_schema_policy(root_directory, instance_base_url, auth_header, request_type, policy_data)
        assert response.status_code == 401
    elif request_type == "bad_request":
        response = client.update_tag_schema_policy(root_directory, instance_base_url, auth_header, request_type, policy_data)
        response_data = response.json()
        assert response.status_code == 400
        assert response_data["message"] == "Invalid payload: {0}"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_101"


@pytest.mark.positive
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data1)
def test_delete_standard_policy_with_mandatory_params(root_directory, create_policy_fixture, instance_base_url,
                                                      auth_header, request_type):

    response = client.create_tag_schema_policy(root_directory, instance_base_url, auth_header,
                                               request_type, policy_type="custom",
                                               optional_policy_params=False)
    response_data = response.json()
    policy_name = response_data["data"]["name"]

    response = client.delete_tag_schema_policy(instance_base_url, auth_header, policy_name)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "Deleted policy {0} successfully"
    assert response_data["translateCode"] == "CS_TAG_SCHEMA_1005"


@pytest.mark.negative
@pytest.mark.parametrize("instance_base_url, auth_header, request_type", test_data2)
def test_delete_standard_policy_with_mandatory_params_negative(root_directory, create_policy_fixture, instance_base_url,
                                                               auth_header, request_type):

    if request_type == "unauth":
        response = client.delete_tag_schema_policy(instance_base_url, auth_header, policy_name="policy_name")
        assert response.status_code == 401
    elif request_type == "invalid_request":
        response = client.delete_tag_schema_policy(instance_base_url, auth_header, policy_name="policy_name")
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["message"] == "Policy {0} does not exist"
        assert response_data["translateCode"] == "CS_TAG_SCHEMA_113"
