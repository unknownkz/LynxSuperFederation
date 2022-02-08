# Copyleft © 2022 Unknown
# All Rights Reserved

import sys
from envparse import env
from . import LOGGER as LOG_LSF


MYPLUGIN = {
    "LOAD_PLUGINS": True,
}


def get_str_key(plugins_name, required=False):
    default = MYPLUGIN.get(plugins_name)

    if not (data_plugins := env.str(plugins_name, default=default)) and not required:
        LOG_LSF.warning("No str key: " + plugins_name)
        return None
    elif not data_plugins:
        LOG_LSF.critical("No str key: " + plugins_name)
        sys.exit(2)
    else:
        return data_plugins


def get_int_key(plugins_name, required=False):
    default = MYPLUGIN.get(plugins_name)

    if not (data_plugins := env.int(plugins_name, default=default)) and not required:
        LOG_LSF.warning("No int key: " + plugins_name)
        return None
    elif not data_plugins:
        LOG_LSF.critical("No int key: " + plugins_name)
        sys.exit(2)
    else:
        return data_plugins
