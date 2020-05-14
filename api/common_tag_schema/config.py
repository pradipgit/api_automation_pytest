import configparser
import sys
from pathlib import Path


def create_directories():
    """
    Creates .aiops directory and following subdirectories(config, logs, data)
    in home directory of any platform
    or in home directory of python virtual environment based on where you
    are installing the package.
    :return: home directory of virtual environment or home directory
    of any platform
    """
    if sys.base_prefix:
        base_path = sys.prefix
    else:
        base_path = Path.home()
    conf_dir_path = base_path + '/.common_tag/config/'
    Path(conf_dir_path).mkdir(parents=True, exist_ok=True)
    log_dir_path = base_path + '/.common_tag/logs/'
    Path(log_dir_path).mkdir(parents=True, exist_ok=True)
    return conf_dir_path, log_dir_path


config_dir_path, logs_dir_path = create_directories()
config_file_path = config_dir_path + 'common_tag_api_tests.conf'


class Config(object):
    def __init__(self, config_file_path=None):
        if Path(config_file_path).exists():
            print("config file path", config_file_path)
        else:
            raise Exception("Make sure that 'common_tag_api_tests.conf' "
                            "configuration file exist in "
                            "the path {}".format(config_file_path))
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file_path)

    @property
    def username(self):
        return self.parser.get('user', 'username')

    @property
    def apikey(self):
        return self.parser.get('user', 'apikey')

    @property
    def instance_base_url(self):
        return self.parser.get('instance_environment', 'instance_base_url')

    @property
    def is_myminikube_instance(self):
        instance = self.parser.get('instance_environment', 'instance_base_url')
        if instance.startswith("https://myminikube"):
            return False
        return True

    @property
    def notification(self):
        return self.parser.get('slack', 'notification')

    @property
    def hcms_channel(self):
        return self.parser.get('slack', 'hcms_channel')

    @property
    def hcms_bot_token(self):
        return self.parser.get('slack', 'hcms_bot_token')


config = Config(config_file_path=config_file_path)
