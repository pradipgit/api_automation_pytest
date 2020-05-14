from common_tag_schema import config


def create_auth_header():
    auth_header = {
        "username": config.config.username,
        "apikey": config.config.apikey,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    return auth_header


def create_unauth_header():
    unauth_header = {
        "Username": config.config.username,
        "apikey": config.config.apikey + "_invalid",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    return unauth_header
