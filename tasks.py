from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# import invocations.packaging.release

# All of the official documentation for invoke makes it clear
# that saying
#
#   from invoke import task, Collection
#
# is fine, and it works. However, the VSCode default Python extension
# throws some warnings (maybe because it wants invoke's maintainers to
# explicitly declare an external API using the `__all__` variable?),
# so we appease it by installing stuff from the submodules like it
# thinks I should.
from invoke.collection import Collection
from invoke.tasks import task


def update_classifiers(context):
    from trove_classifiers import classifiers as official_classifiers

    def classifiers_from_file(path: Path) -> list[str]:
        if path.exists() is False:
            path.touch()  # create empty
            return []

        with path.open() as f:
            existing_classifiers = f.readlines()
            return existing_classifiers

    def pyproject_requires_python(file: Path):
        with file.open(mode="rb") as f:
            data = tomllib.load(f)

        try:
            python_required = data["project"]["requires-python"]
        except KeyError:
            return None

        # match python_required:
        #     case ...:
        #         ...

    classifiers_file = Path().cwd() / "tools" / "pypi" / "classifiers.txt"
    pyproject_file = Path().cwd() / "pyproject.toml"

    classifiers = classifiers_from_file(path=classifiers_file)
    for classifier in official_classifiers:
        part1, part2, part3, _ = classifier.split(" :: ")
        if (part1, part2) == ("Programming Language", "Python"):
            major_version, minor_version, _ = part3.split(".")
            if major_version == "3" and int(minor_version):
                ...


#
# REQUIREMENTS
# ------------
#
@task(
    name="deps",
    help={  # help text for this task's options
        "upgrade": "Upgrade dependencies if newer versions are available, "
        + "while still respecting constraints in the *.in files.",
        "install": "",
    },
)
def requirements(context, install=False, upgrade=False):
    """Housekeeping tasks to keep our dependencies neat, tidy.

    When run without any additional options, the `invoke requirements` task
    will run the necessary commands to create
    """

    def requirements_files():
        files = [
            file
            for file in (Path.cwd() / "requirements").iterdir()
            if file.suffix == ".in"
        ]
        return files

    def base_install_cmd(upgrade=upgrade) -> str:
        cmd = (
            "pip install"
            + (" --upgrade " if upgrade else " ")
            + "pip-tools pip setuptools"
        )
        return cmd

    def compile_requirements_cmd(input_file: Path, upgrade=upgrade) -> str:
        from importlib.metadata import version as package_version

        # Check the version of 'pip-tools', since we'll need to include
        # an extra flag for some versions
        piptools_major_version, *_ = package_version("pip-tools").split(".")

        #
        # The "--allow-unsafe" option for pip-compile may sound kinda scary,
        # but apparently there's been a shift in opinion that says that it's
        # best practice to allow it. It's a bit beyond my understanding. For
        # more reading, see:
        # 	https://github.com/jazzband/pip-tools/issues/806 for discussion
        # 	https://stackoverflow.com/q/58843905 for comment on best practice
        cmd = (
            "pip-compile --generate-hashes --build-isolation --allow-unsafe"
            + (" --resolver=backtracking " if int(piptools_major_version) < 7 else " ")
            + (" --upgrade " if upgrade else " ")
            + f" --output-file {input_file.with_suffix('.txt')}"
            + f" {input_file}"
        )
        return cmd

    def install_requirements_cmd():
        return "pip-sync"

    #
    #
    commands = [base_install_cmd(upgrade)]
    for file in requirements_files():
        commands.append(compile_requirements_cmd(input_file=file, upgrade=upgrade))
    if install is True:
        commands.append(install_requirements_cmd())

    for command in commands:
        context.run(command)


#
# BUILD
# -----
# Build our program so we can run it from our terminal.
#
@task
def build(context):
    # invocations.packaging.release.build()
    ...


@task
def publish(context):
    ...


@task
def test(context):
    ...


#
# VENV
# ----
# Create/activate a virtual environment.
#
# @task(help={"new": "Nuke everything and reinstall from a clean environment."})
# def venv(context, new=False):
#     """Checks to see if a suitable virtual environment exists, and creates it if it doesn't."""

#     def currently_in_venv() -> bool:
#         """Checks to see if we are currently in a virtual environment. This
#         function is probably not 100% reliable, but it's reliable enough.

#         Based on answers to [this question](https://stackoverflow.com/q/1871549)
#         on StackOverflow.
#         """
#         import os
#         import sys

#         if os.getenv("CONDA_DEFAULT_ENV") or os.getenv("VIRTUAL_ENV"):
#             # Anaconda or Venv or Virtualenv environment is active
#             return True
#         elif hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix:
#             # A virtual environment isn't "active" but the Python interpreter
#             # we're running is nonetheless not the base.
#             return True
#         elif hasattr(sys, "real_prefix"):
#             # Same as above, for Python 3.3 and earlier
#             return True
#         else:
#             return False

#     def venv_exists():
#         from pathlib import Path

#         directory = Path(__file__).parent

#         return (directory / ".venv").exists()

#     def create_venv():
#         ...

#     def remove_venv():
#         ...

#     def activate_venv():
#         ...

#     if new:
#         if venv_exists():
#             remove_venv()
#         create_venv()
#         activate_venv()

#     if not currently_in_venv:
#         if venv_exists() is False:
#             create_venv()
#         activate_venv()
