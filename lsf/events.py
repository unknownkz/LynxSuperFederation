from telethon import events

from . import lynx_client


def register(**args):
    """Registers a new message."""
    pattern = args.get("pattern")

    r_pattern = r"^[.$!/;@]"

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        lynx_client.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator
