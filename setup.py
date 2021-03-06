#!/usr/bin/env python

import argparse
import sys
from contextlib import suppress
from pathlib import Path
from shlex import split
from subprocess import run

RST = "\x1b[0m"
BOLD = "\x1b[1m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
CYAN = "\x1b[36m"

python = "python3"
nocache = f"{python} -B"

app = "bash startapp"
app_watch = f"{python} -m scripts.autoreload {app}"

black = "brunette --config=dev-setup.cfg ."
isort = "isort --settings-file=dev-setup.cfg ."
flake8 = "flake8 --config=dev-setup.cfg ."
prettyjson = f"{nocache} -m scripts.prettyjson"


def run_command(cmd) -> None:
    try:
        proc = run(split(cmd), shell=False)
        if proc.returncode != 0:
            print(f"Exit code {proc.returncode}")
            sys.exit(1)
    except BaseException:
        sys.exit(1)


def clean() -> None:
    with suppress(BaseException):
        for f in Path(".").rglob("*.py[cod]"):
            f.unlink(missing_ok=True)
        for d in Path(".").rglob("__pycache__"):
            d.rmdir()


def lint() -> None:
    print(f"{CYAN}> {black}{RST}")
    run_command(black)
    print(f"{CYAN}> {isort}{RST}")
    run_command(isort)
    print(f"{CYAN}> {flake8}{RST}")
    run_command(flake8)
    print(f"{CYAN}> {prettyjson}{RST}")
    run_command(prettyjson)


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if not prefix:
            prefix = "Usage: "
        return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)


parser = argparse.ArgumentParser(
    formatter_class=CapitalisedHelpFormatter,
    prog=f"{GREEN}{python} -m setup{RST}",
    usage="%(prog)s [options]",
    epilog="Source code https://github.com/unknownkz/LynxSuperFederation",
    add_help=False,
)
parser._optionals.title = "Options"
parser.add_argument("-p", "--prod", help="run in production mode", action="store_true")
parser.add_argument("-d", "--dev", help="run in development mode", action="store_true")
parser.add_argument("-w", "--watch", help="run and watch in development mode", action="store_true")
parser.add_argument("-l", "--lint", help="run linting and format code", action="store_true")
parser.add_argument("-c", "--clean", help="remove python caches", action="store_true")
parser.add_argument(
    "-h",
    "--help",
    help="show this help information",
    default=argparse.SUPPRESS,
    action="help",
)


def main() -> None:
    args = parser.parse_args()
    if args.prod:
        print(f"{BOLD}{GREEN}[ PRODUCTION MODE ]{RST}")
        clean()
        print(f"{BOLD}{BLUE}> {app}{RST}")
        run_command(app)
    elif args.dev:
        print(f"{BOLD}{GREEN}[ DEVELOPMENT MODE ]{RST}")
        clean()
        lint()
        print(f"{BOLD}{BLUE}> {app}{RST}")
        run_command(app)
    elif args.watch:
        print(f"{BOLD}{GREEN}[ WATCHED DEVELOPMENT MODE ]{RST}")
        clean()
        print(f"{BOLD}{BLUE}> {app_watch}{RST}")
        run_command(app_watch)
    elif args.lint:
        print(f"{BOLD}{YELLOW}Run linting and format code...{RST}")
        clean()
        lint()
        sys.exit(0)
    elif args.clean:
        clean()
        sys.exit(0)
    else:
        print(f"{python} -m setup --help")
        sys.exit(0)


if __name__ == "__main__":
    raise SystemExit(main())
