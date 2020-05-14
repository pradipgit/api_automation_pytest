import json
import random
import string

import requests

from common_tag_schema import config
from common_tag_schema import tag_schema_logging


verify = config.config.is_myminikube_instance
logger = tag_schema_logging.create_logger(logger_name=__name__)
f_logger = tag_schema_logging.create_file_logger(logger=logger)


def generate_random_policy_name():
    """
    @summary: Generates random filter name. allowed filter name length is
    5 to 22 characters.
    :return: returns random name
    """
    random_string = ""
    random_characters = random.randint(5, 22)
    for i in range(0, random_characters):
        random_string += random.choice(string.ascii_letters + string.digits)
    return random_string


def generate_random_values():
    """
    @summary: Generates random values. It's temporary function, need to change
    based on further requirement.
    5 to 22 characters.
    :return: returns random name
    """
    random_string = ""
    random_characters = random.randint(5, 22)
    for i in range(0, random_characters):
        random_string += random.choice(string.ascii_letters + string.digits)
    return random_string


def generate_random_description():
    """
    @summary: Generates random values. It's temporary function, need to change
    based on further requirement.
    5 to 22 characters.
    :return: returns random name
    """
    random_string = ""
    random_characters = random.randint(1, 200)
    for i in range(0, random_characters):
        random_string += random.choice(string.ascii_letters + string.digits)
    return random_string


def get_policies_list(instance_base_url, header, request_type, **kwargs):
    """
    @summary: Get list of all policies
    :param instance_base_url: Instance url
    :param header: dictionary with username, api key, and application/json
    :param request_type: auth/unauth/invalid endpoint request
    :return:
    """
    response = None
    url = '{base_url}/api/v1/policies'.format(
        base_url=instance_base_url)
    if request_type == "invalid_request":
        url = url + "/url_doesnt_exist"
    try:
        if kwargs:
            response = requests.get(url=url, headers=header, params=kwargs, verify=verify)
        else:
            response = requests.get(url=url, headers=header, verify=verify)
    except requests.exceptions.Timeout as timeout:
        f_logger.info(timeout)
        return response
    except requests.exceptions.RequestException as e:
        f_logger.info(e)
        return response
    else:
        return response


def get_policy_details(instance_base_url, header, policy_name):
    """
    @summary: Get a single policy details
    :param instance_base_url: Instance url
    :param header: dictionary with username, api key, and application/json
    :param policy_name: name of standard/custom policy
    :return:
    """
    response = None
    url = '{base_url}/api/v1/policies/{policy_name}'.format(
        base_url=instance_base_url, policy_name=policy_name)
    try:
        response = requests.get(url=url, headers=header, verify=verify)
    except requests.exceptions.Timeout as timeout:
        f_logger.info(timeout)
        return response
    except requests.exceptions.RequestException as e:
        f_logger.info(e)
        return response
    else:
        return response


def create_tag_schema_policy(root_dir, instance_base_url, header,
                             request_type, policy_type=None, optional_policy_params=None,
                             policy_name=None, **kwargs):
    """
    @summary: Create a standard policy
    :param instance_base_url: Instance url
    :param header: dictionary with username, api key, and application/json
    :param request_type: auth/unauth/invalid_request/bad_request
    :param root_dir: root directory
    :return:
    """
    response = None
    url = '{base_url}/api/v1/policies'.format(base_url=instance_base_url)
    file_path = root_dir + "/api/common_tag_schema/payloads/policy.json"
    with open(file_path) as fh:
        payload = json.load(fh)
    if policy_name is None:
        payload["name"] = generate_random_policy_name()
    else:
        payload["name"] = policy_name

    if request_type == "auth":
        payload["status"] = "active"
        payload["policy_units"][0]["applies_to"] = "key"
        payload["policy_units"][0]["providers"] = ["aws"]
        payload["policy_units"][0]["conditions"][0]["name"] = "category"
        payload["policy_units"][0]["conditions"][0]["values"] = [generate_random_values()]
        payload["policy_units"][0]["conditions"][0]["operator"] = "is"
        payload["policy_units"][0]["schema"]["edit_authorised_roles"] = ["TEAM-SETUP-ADMIN"]
        payload["policy_units"][0]["schema"]["delete_authorised_roles"] = ["TEAM-SETUP-ADMIN"]
        payload["policy_units"][0]["schema"]["is_required"] = True
        payload["policy_units"][0]["schema"]["provider_push"] = False

        if policy_type == "standard":
            payload["policy_units"][0]["policy_type"] = "standard"
        if policy_type == "custom":
            payload["policy_units"][0]["policy_type"] = "custom"
        if optional_policy_params:
            payload["description"] = generate_random_description()
            payload["policy_units"][0]["combinator"] = "ALL"
            payload["policy_units"][0]["applies_to"] = "value"
            payload["policy_units"][0]["tag_key"] = "tag_key1"
            payload["policy_units"][0]["schema"]["allowed_list"] = []
            # payload["policy_units"][0]["schema"]["regex"] = ""
            payload["policy_units"][0]["schema"]["max_length"] = 0

        if "status" in kwargs:
            payload["status"] = kwargs["status"]
        if "combinator" in kwargs:
            payload["policy_units"][0]["combinator"] = kwargs["combinator"]
        if "description" in kwargs:
            payload["description"] = kwargs["description"]
        if "applies_to" in kwargs:
            if kwargs["applies_to"] == "key":
                payload["policy_units"][0]["applies_to"] = kwargs["applies_to"]
            elif kwargs["applies_to"] == "value" or kwargs["applies_to"] == "both":
                payload["policy_units"][0]["tag_key"] = generate_random_values()
            else:
                payload["policy_units"][0]["applies_to"] = kwargs["applies_to"]
        if "providers" in kwargs:
            payload["policy_units"][0]["providers"] = kwargs["providers"]
        if "conditions_name" in kwargs:
            payload["policy_units"][0]["conditions"][0]["name"] = kwargs["conditions_name"]
        if "conditions_name" in kwargs and kwargs["conditions_name"] == "duplicate_conditions":
            payload["policy_units"][0]["conditions"].append({})
            payload["policy_units"][0]["conditions"][1]["name"] = payload["policy_units"][0]["conditions"][0]["name"]
            payload["policy_units"][0]["conditions"][1]["values"] = payload["policy_units"][0]["conditions"][0]["values"]
            payload["policy_units"][0]["conditions"][1]["operator"] = payload["policy_units"][0]["conditions"][0]["operator"]

        if "operator" in kwargs:
            payload["policy_units"][0]["conditions"][0]["operator"] = kwargs["operator"]
        if "allowed_list" in kwargs:
            payload["policy_units"][0]["schema"]["allowed_list"] = kwargs["allowed_list"]
        if "regex" in kwargs:
            payload["policy_units"][0]["schema"]["regex"] = kwargs["regex"]

    elif request_type == "bad_request":
        mandatory_params = [
            payload["name"], payload["status"], payload["policy_units"][0]["applies_to"],
            payload["policy_units"][0]["providers"],
            payload["policy_units"][0]["conditions"][0]["name"],
            payload["policy_units"][0]["conditions"][0]["values"],
            payload["policy_units"][0]["conditions"][0]["operator"],
            payload["policy_units"][0]["schema"]["edit_authorised_roles"],
            payload["policy_units"][0]["schema"]["delete_authorised_roles"],
            payload["policy_units"][0]["schema"]["is_required"],
            payload["policy_units"][0]["schema"]["provider_push"]
        ]

        random_mandatory_param = random.choice(mandatory_params)
        del random_mandatory_param

    elif request_type == "invalid_request":
        url = url + "/url_doesnt_exist"

    try:
        response = requests.post(url=url, headers=header, json=payload, verify=verify)
    except requests.exceptions.Timeout as timeout:
        f_logger.info(timeout)
        return response
    except requests.exceptions.RequestException as e:
        f_logger.info(e)
        return response
    else:
        return response


def update_tag_schema_policy(root_dir, instance_base_url, header, request_type, policy_data=None):
    """
    @summary: Update a standard policy
    :param instance_base_url: Instance url
    :param header: dictionary with username, api key, and application/json
    :param request_type: auth/unauth/invalid_request/bad_request
    :param root_dir: root directory
    :return:
    """
    response = None

    file_path = root_dir + "/api/common_tag_schema/payloads/policy.json"
    with open(file_path) as fh:
        payload = json.load(fh)

    if request_type != "unauth":
        url = '{base_url}/api/v1/policies/{policy_name}'.format(
            base_url=instance_base_url, policy_name=policy_data["data"]["name"])

        payload["name"] = policy_data["data"]["name"]
    else:
        url = '{base_url}/api/v1/policies/{policy_name}'.format(
            base_url=instance_base_url, policy_name="policy_name")

    if request_type == "auth":
        # updating below fields
        payload["status"] = "active"
        payload["policy_units"][0]["applies_to"] = "key"
        payload["policy_units"][0]["providers"] = ["aws", "azure"]
        payload["policy_units"][0]["conditions"][0]["name"] = "service_type"
        payload["policy_units"][0]["conditions"][0]["values"] = [generate_random_values()]
        payload["policy_units"][0]["conditions"][0]["operator"] = "is"
        payload["policy_units"][0]["schema"]["edit_authorised_roles"] = ["TEAM-SETUP-ADMIN"]
        payload["policy_units"][0]["schema"]["delete_authorised_roles"] = ["TEAM-SETUP-ADMIN"]
        payload["policy_units"][0]["policy_type"] = "standard"
        payload["policy_units"][0]["schema"]["is_required"] = True
        payload["policy_units"][0]["schema"]["provider_push"] = False

    elif request_type == "bad_request":
        del payload["name"]

    elif request_type == "invalid_request":
        url = url + "/url_doesnt_exist"

    try:
        response = requests.put(url=url, headers=header, json=payload, verify=verify)
    except requests.exceptions.Timeout as timeout:
        f_logger.info(timeout)
        return response
    except requests.exceptions.RequestException as e:
        f_logger.info(e)
        return response
    else:
        return response


def delete_tag_schema_policy(instance_base_url, header, policy_name):
    """
    @summary: Delete a standard policy
    :param instance_base_url: Instance url
    :param header: dictionary with username, api key, and application/json
    :param request_type: auth/unauth/invalid_request/bad_request
    :param root_dir: root directory
    :return:
    """
    response = None
    url = '{base_url}/api/v1/policies/{policy_name}'.format(
        base_url=instance_base_url, policy_name=policy_name)
    try:
        response = requests.delete(url=url, headers=header, verify=verify)
    except requests.exceptions.Timeout as timeout:
        f_logger.info(timeout)
        return response
    except requests.exceptions.RequestException as e:
        f_logger.info(e)
        return response
    else:
        return response
