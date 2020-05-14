#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for common_tag_schema.
    Use setup.cfg to configure your project.
"""
import sys
from pathlib import Path

from setuptools import setup, find_packages


with open("README.rst") as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name='common_tag_schema',
        version='1.0',
        description='API automation framework for common tag schema service',
        long_description=long_description,
        author='Basavaraj Lamani',
        author_email='baslama1@in.ibm.com',
        # packages=find_packages(exclude=('tests*', 'docs')),
        install_requires=[
            'pytest-html',
            'pytest-cov',
            'pytest-xdist',
            'requests',
        ],
        classifiers=('Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'Natural Language :: English',
                     'License :: Other/Proprietary License',
                     'Operating System :: POSIX :: Linux',
                     'Programming Language :: Python :: 3.7'
                     ),
        # cmdclass={'install': install},
    )


def create_directories():
    """
    Creates ".common_tag" directory and following subdirectories(config, logs, data)
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


create_directories()
