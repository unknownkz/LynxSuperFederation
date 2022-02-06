# Copyleft © 2022 Unknown
# All Rights Reserved

import sys
from envparse import env
from lsf import LOGGER as LOG_LSF

MYPLUGIN = {
    "LOAD_PLUGINS": True,
}


def get_str_key(plugin_name, required=False):
    default = MYPLUGIN.get(plugin_name, None)

    if not (data_plugin := env.str(plugin_name, default=default)) and not required:
        LOG_LSF.warning("No str key: " + plugin_name)
        return None
    elif not data_plugin:
        LOG_LSF.critical("No str key: " + plugin_name)
        sys.exit(2)
    else:
        return data_plugin


def get_int_key(plugin_name, required=False):
    default = MYPLUGIN.get(plugin_name, None)

    if not (data_plugin := env.int(plugin_name, default=default)) and not required:
        LOG_LSF.warning("No int key: " + plugin_name)
        return None
    elif not data_plugin:
        LOG_LSF.critical("No int key: " + plugin_name)
        sys.exit(2)
    else:
        return data_plugin
