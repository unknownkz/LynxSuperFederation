# Copyleft © 2022 Unknown

from envparse import env
from lsf import LOGGER as LOG_LSF

MYPLUGIN = {
    "LOAD_MODULES": True,
}


def get_str_key(plugin_name, required=False):
    if plugin_name in MYPLUGIN:
        default = MYPLUGIN[plugin_name]
    else:
        default = None

    if not (data_plugin := env.str(plugin_name, default=default)) and not required:
        LOG_LSF.warn("No str key: " + plugin_name)
        return None
    elif not data_plugin:
        LOG_LSF.critical("No str key: " + plugin_name)
        sys.exit(2)
    else:
        return data_plugin


def get_int_key(plugin_name, required=False):
    if plugin_name in MYPLUGIN:
        default = MYPLUGIN[plugin_name]
    else:
        default = None

    if not (data_plugin := env.int(plugin_name, default=default)) and not required:
        LOG_LSF.warn("No int key: " + plugin_name)
        return None
    elif not data_plugin:
        LOG_LSF.critical("No int key: " + plugin_name)
        sys.exit(2)
    else:
        return data_plugin
