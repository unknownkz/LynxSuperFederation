# Copyleft © 2022 Unknown
from .. import LOAD, LOGGER, NO_LOAD


def __list_all_plugins():
    import glob
    import os
    from os import walk
    from os.path import basename, dirname, isfile

    path = r"./lsf/plugins/"
    list_of_files = []

    for root, dirs, files in walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))

    all_plugins = [
        basename(name)[:-3]
        for name in list_of_files
        if isfile(name)
        and name.endswith(".py")
        and not name.endswith("__init__.py")
        and not name.endswith("README.md")
        and not name.endswith("__help__.py")
    ]

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(any(mod == plugins_name for plugins_name in all_plugins) for mod in to_load):
                LOGGER.error("[Alert] Invalid loadorder names. Quitting.")
                exit(1)

            all_plugins = sorted(set(all_plugins) - set(to_load))
            to_load = list(all_plugins) + to_load

        else:
            to_load = all_plugins

        if NO_LOAD:
            LOGGER.info("[Alert] Not loading: {}".format(NO_LOAD))
            return [item for item in to_load if item not in NO_LOAD]

        return to_load

    return all_plugins


ALL_PLUGINS = __list_all_plugins()
LOGGER.info("[Build App] Plugins to load: %s", str(ALL_PLUGINS))
__all__ = ALL_PLUGINS + ["ALL_PLUGINS"]
