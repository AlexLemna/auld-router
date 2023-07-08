#!/usr/bin/env python
""" initialize_repository.py

When run without any options, this script will ensure the existence 
of a minimally-provisioned virtual environment suitable for dev work.

This script can only deal with virtual environments in the common ".venv",
".env", "venv", and "env" folders. Additionally, it won't work when there
are multiple virtual environments already installed in this folder.

"""
#
# This is a single-file Python script that I've used as sort of a playground to
# over-engineer a solution to a problem... even though the problem, "What to do
# if someone clones this repo from GitHub and doesn't know how to get started?"
# doesn't *really* need to be solved.
#

__version_info__ = (0, 2023, 8, 7, 0)
__version__ = ".".join([str(version_part) for version_part in __version_info__])

import argparse
import os
import platform
import subprocess
import sys
import venv
from enum import Enum
from logging import Logger
from pathlib import Path

#
# Some custom exceptions
# ----------------------
#


class TooManyVenvsError(Exception):
    """An exception indicating that the script is not designed to handle repositories
    with multiple virtual environments."""

    def __init__(
        self,
        existing_venvs: list[Path],
        show_abs_paths=False,
        repository_path=Path(__file__).parent,
    ) -> None:
        self.existing_venvs = existing_venvs
        self.repository_path = repository_path

        self.message = """This script is not designed to handle repositories 
            with multiple virtual environments, but multiple virtual environments
            were detected: """ + ", ".join(
            [str(venv.absolute()) for venv in existing_venvs]
            if show_abs_paths is True
            else [str(venv.relative_to(repository_path)) for venv in existing_venvs]
        )

        super().__init__(self.message)


class InsideVenvError(Exception):
    ...


#
# Dealing with shells
# -------------------
#


class Shell(Enum):
    """The type of shell the current Python executable is running in."""

    NO_SHELL_DETECTED = 0
    SH_LIKE = 1
    """Shells like `ash`, `bash`, `ksh`, `zsh`."""
    CSH_LIKE = 2
    """Shells like `csh`, `tcsh`."""
    FISH = 3
    """The `fish` shell."""
    POWERSHELL = 4
    """Microsoft's `PowerShell`, usually found on modern Windows systems but
    also able to be run on Linux."""
    CMD_EXE = 5
    """The venerable Windows `cmd.exe`."""


def get_activate_file(venv_directory: Path, shell: Shell):
    if shell.SH_LIKE:
        return venv_directory / "bin" / "activate"
    elif shell.CSH_LIKE:
        return venv_directory / "bin" / "activate.csh"
    elif shell.FISH:
        return venv_directory / "bin" / "activate.fish"
    elif shell.CMD_EXE:
        return venv_directory / "bin" / "activate.bat"
    elif shell.POWERSHELL and platform.system == "Windows":
        return venv_directory / "Scripts" / "Activate.ps1"
    elif shell.POWERSHELL:
        return venv_directory / "bin" / "Activate.ps1"
    else:
        return None


def detect_shell(dry_run=False) -> Shell:
    ...


#
# Dealing with virtual environments
# ---------------------------------
#


def find_venv() -> Path | None:
    """In the directory where this script is located, look for a subdirectory
    containing a virtual environment. If such a subdirectory exists, return it
    (as a `Path` object). If not, return `None`.

    If multiple subdirectories exist that could contain virtual environments,
    raises `TooManyVenvsError`."""
    common_venv_directories = [".env", ".venv", "env", "venv"]
    repository = Path(__file__).parent

    existing_venvs = [
        repository / venv_dir
        for venv_dir in common_venv_directories
        if (repository / venv_dir).exists() and (repository / venv_dir).is_dir()
    ]

    if len(existing_venvs) == 1:
        return existing_venvs[0]

    elif len(existing_venvs) > 1:
        raise TooManyVenvsError(existing_venvs)

    else:
        return None


def currently_in_venv() -> bool:
    if os.getenv("CONDA_DEFAULT_ENV") or os.getenv("VIRTUAL_ENV"):
        # Anaconda or Venv or Virtualenv environment is active
        return True
    elif hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix:
        # A virtual environment isn't "active" but the Python interpreter
        # we're running is nonetheless not the base.
        return True
    else:
        return False


def create_venv(dry_run: bool, verbose: bool, force: bool = False):
    if currently_in_venv:
        raise InsideVenvError
    venv.EnvBuilder()


#
# Setting up our virtual environment
# ----------------------------------
#


def install_basic_tools(dry_run=False):
    basic_tools = ["invoke", "pip", "pip-tools", "setuptools"]


#
# Running our script
# ------------------
#


def cli():
    """The human interface to this script. It accepts commands when this script is
    invoked (from the terminal, etc.) and then calls other functions defined in
    this script according to those commands."""
    #
    # The "cli" function is really two sub-functions stitched together. The
    # first function, "get_parser", creates a "ArgumentParser" object and
    # defines its expected input. The second function .
    #

    def get_parser() -> argparse.ArgumentParser:
        file_name = Path(__file__).name
        program_name = file_name.removesuffix(".py")

        _, first_paragraph_of_file_docstring, *rest_of_file_docstring = [
            paragraph.replace("\n", " ") for paragraph in __doc__.split("\n\n")
        ]
        first_paragraph_of_file_docstring_oneline = (
            first_paragraph_of_file_docstring.replace("\n", " ")
        )
        SHORT_DESCRIPTION = (
            f"{file_name.upper()}: {first_paragraph_of_file_docstring_oneline}"
        )
        FULL_DESCRIPTION = "".join(rest_of_file_docstring)

        p = argparse.ArgumentParser(
            prog=program_name,
            # usage=f"<PYTHON INTERPRETER> -m {program_name} [OPTIONS]",
            description=SHORT_DESCRIPTION,
            epilog=FULL_DESCRIPTION,
            add_help=False,  # We override the built-in help message with out own
        )

        # --dry-run
        p.add_argument(
            "--dry-run",
            action="store_true",
            help="Attempts to preview the results of a command, but does not take any action.",
        )
        # --force
        p.add_argument(
            "--force",
            action="store_true",
            help="Destroys the existing virtual environment and creates a fresh one.",
        )
        # --help
        p.add_argument(
            "--help",
            "-h",
            action="help",
            help="Show this help message and exit.",
        )
        # --verbose
        args = ["--verbose", "-v"]
        msg = "Display additional output while the program runs."
        p.add_argument(*args, action="store_true", help=msg)
        # p.add_argument(
        #     "--verbose",
        #     "-v",
        #     action="store_true",
        #     help="Display additional output while the program runs.",
        # )
        # --version
        p.add_argument(
            "--version",
            "-V",
            action="version",
            version=__version__,
            help="Show this script's version.",
        )

        return p

    def dispatch(parsed: argparse.Namespace):
        """Based on the results (a `Namespace` of commands, options, etc) from
        the Argparse parser, trigger whatever actions correspond to the user's
        input."""

        #
        # I Like to have seperate "cmd_*" functions defined in my dispatch
        # function, just to make it clear to myself what sorts of "logical
        # commands" I'm expecting this script to perform.
        #
        def cmd_initialize(dry_run: bool, verbose: bool):
            print("INITIALIZING")
            create_venv(dry_run=parsed.dry_run, verbose=parsed.verbose)

        def cmd_destroy_and_initialize(dry_run: bool, verbose: bool):
            print("DESTROYING AND INITIALIZING")
            create_venv(dry_run=parsed.dry_run, verbose=parsed.verbose, force=True)

        #
        # Next comes the actual "dispatch" logic, connecting the Namespace of commands,
        # options, etc., to the functions that determine what this script is going
        # to do, and how it's going to do it.
        #
        #
        # Namespace objects are kinda interesting - they're part of the built-in
        # argparse library, and they represent the "parsed results" generated by an
        # ArgumentParser. If you have a Namespace `ns` and you issue the command
        # `print(ns)`, you'll be able to see some what's inside it. Here's an example:
        #
        #   Namespace(dry_run=False, force=False, verbose=False)
        #
        if parsed.dry_run:
            print("PERFORMING DRY RUN")

        if parsed.verbose:
            print("RUNNING IN VERBOSE MODE")
            # Print the Namespace that we recieved from our ArgumentParser
            print(f"Parsed command-line input: {parsed}")

        if parsed.force:
            cmd_destroy_and_initialize(dry_run=parsed.dry_run, verbose=parsed.verbose)
        else:
            cmd_initialize(dry_run=parsed.dry_run, verbose=parsed.verbose)

    #
    # And now, the entirety of the cli function.
    #

    # Create the parser, and have it parse the input.
    user_input = get_parser().parse_args()
    print(user_input)
    # Pass off whatever the parser understood to the dispatch function.
    dispatch(parsed=user_input)
    # ...and yes, once you've created an ArgumentParser `bob_the_parser`,
    # using it really is as simple as typing `bob_the_parser.parse_args()`.


# Only run this script when directly called. Otherwise, do nothing.
if __name__ == "__main__":
    cli()
