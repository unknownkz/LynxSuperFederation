import sys
from lsf import LOAD, NO_LOAD, LOGGER


def __list_all_plugins():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_plugins = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(
                any(mod == plugin_name for plugin_name in all_plugins)
                for mod in to_load
            ):
                LOGGER.error("[Alert] Invalid loadorder names. Quitting.")
                sys.exit(1)

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
LOGGER.info("[Alert] Plugins to load: %s", str(ALL_PLUGINS))
__all__ = ALL_PLUGINS + ["ALL_PLUGIN"]