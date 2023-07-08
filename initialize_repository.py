""" initialize_repository.py

When run without any options, this script will ensure the existence 
and activation of a minimally-provisioned virtual environment suitable 
for dev work.

This script can only deal with virtual environments in the common ".venv",
".env", "venv", and "env" folders. Additionally, it won't work when there
are multiple virtual environments already installed in this folder.

"""
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


class TooManyVenvsError(Exception):
    """
    An exception indicating that the script is not designed to handle repositories with
    multiple virtual environments.

    Parameters
    ----------
    existing_venvs : list[Path]
        A list of paths to the existing virtual environments.
    show_abs_paths : bool, optional
        Specifies whether to show absolute paths or relative paths. Defaults to False.
    repository_path : Path, optional
        The path to the repository. Defaults to the parent directory of the current file.

    Attributes
    ----------
    message : str
        The error message indicating the detection of multiple virtual environments.
    """

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


def find_venv() -> Path | None:
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


def create_venv(dry_run=False):
    venv.EnvBuilder()


def destroy_venv(dry_run=False):
    ...


def activate_venv(dry_run=False):
    ...


def deactivate_venv(dry_run=False):
    ...


class Shell(Enum):
    SH_LIKE = 1
    """Shells like ash, bash, ksh, zsh."""
    CSH_LIKE = 2
    """Shells like csh, tcsh."""
    FISH = 3
    """The fish shell."""
    POWERSHELL = 4
    """Windows Powershell."""
    CMD_EXE = 5
    """Windows cmd.exe"""


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


def install_basic_tools(dry_run=False):
    basic_tools = ["invoke", "pip", "pip-tools", "setuptools"]


def cli():
    def get_parser():
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
        p.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Display additional output while the program runs.",
        )
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
        def cmd_initialize(dry_run: bool, verbose: bool):
            print("INITIALIZING")

        def cmd_destroy_and_initialize(dry_run: bool, verbose: bool):
            print("DESTROYING AND INITIALIZING")

        if parsed.dry_run:
            print("PERFORMING DRY RUN")

        if parsed.verbose:
            print("RUNNING IN VERBOSE MODE")
            print(f"Parsed command-line input: {parsed}")

        if parsed.force:
            cmd_destroy_and_initialize(dry_run=parsed.dry_run, verbose=parsed.verbose)
        else:
            cmd_initialize(dry_run=parsed.dry_run, verbose=parsed.verbose)

    parser = get_parser()
    user_input = parser.parse_args()
    dispatch(parsed=user_input)


if __name__ == "__main__":
    cli()
