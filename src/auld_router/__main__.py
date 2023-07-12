""""""
import argparse
from enum import Enum
from importlib.metadata import entry_points
from pathlib import Path
from typing import Callable

try:
    from . import commands as cmd
    from . import configuration as config
    from ._version import __version__


except ImportError:
    # VSCode users might find Pylance flagging these lines as errors,
    # depending on if it's installed in editable mode or not. (??? TODO ???)
    import commands as cmd  # type: ignore
    from _version import __version__  # type: ignore

DISPATCH_TABLE: dict[str, Callable] = {
    "configuration commit": cmd.config_commit,
    "configuration confirm": cmd.config_confirm,
    "configuration reset": cmd.config_reset,
    "configuration save": cmd.config_save,
    "configuration show": cmd.config_show,
    "show configuration": cmd.config_show,
    "show addresses": cmd.interface_address_show_all,
    "show dns": cmd.dns_status_show,
    "show interfaces": cmd.interface_status_show_all,
    "show nat": cmd.nat_status_show,
    "show nat translations": cmd.nat_translations_show,
    "show networks": cmd.routing_table_show_networks,
    "show ntp": cmd.ntp_status_show,
    "show router services": cmd.service_show_all,
    "show router version": cmd.version_show_full,
    "show routes": cmd.routing_table_show,
    "show version": cmd.version_show_app,
}
"""Foo bar"""


def main_program():
    ...


if __name__ == "__main__":
    main_program()
