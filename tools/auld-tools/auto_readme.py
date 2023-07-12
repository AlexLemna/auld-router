import os
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib  # type: ignore (<-- for Pylance, in VS Code)
except ModuleNotFoundError:
    import tomli as tomllib

__version_info__ = (0, 2023, 8, 12, 0)
__version__ = ".".join([str(version_part) for version_part in __version_info__])

#
# CONFIGURATION
# -------------
#


@dataclass
class ScriptConfig:
    use_gitignore: bool = True
    ignore_directories: list = []


def locate_script_config_file(config_file: str = "pyproject.toml") -> Path | None:
    """Locates the config file for this script. Returns the config file
    as a `Path` if found, or else returns `None`."""
    this_file = Path(__file__)

    for dir in this_file.parents:
        settings_file = dir / config_file
        if settings_file.exists():
            return settings_file

    return None


def load_config(config_file) -> ScriptConfig:
    ...


#
# CONTEXT
# -------
#


@dataclass
class ScriptContext:
    base: Path
    directories: list[Path]


def load_context() -> ScriptContext:
    ...

    def read_gitignore():
        ...


#
# MAKE README FILES
# -----------------
#


def create_readme(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    docstring = content.split('"""')[1] if '"""' in content else ""
                    files.append((filename, docstring.strip().split("\n")[0]))
    return files


def generate_tree(files):
    tree = ""
    for filename, description in files:
        tree += f"│   ├── {filename}"
        if description:
            tree += f" - {description}"
        tree += "\n"
    return tree


#
# MAIN FUNCTION
# -------------
#


def main():
    # Read settings from config file
    config_file = locate_script_config_file()
    if config_file:
        with config_file.open(mode="rb") as file:
            contents = tomllib.load(file)
            try:
                config = contents["tool"]["auld-tool"]["auto-readme"]
            except KeyError:
                raise FileNotFoundError(
                    "Found pyproject.toml file, but no configuration."
                )
    else:
        raise FileNotFoundError("Could not find a config file.")

    directories = config.get("directories", [])
    for directory in directories:
        readme_path = os.path.join(directory, "README.md")

        if os.path.exists(readme_path):
            with open(readme_path, "r") as file:
                readme_content = file.read()

            if "<!-- auld_auto_readme IGNORE -->" not in readme_content:
                os.remove(readme_path)
            else:
                continue

        files = create_readme(directory)

        if not files:
            continue

        tree = generate_tree(files)
        readme_content = f"```\n{tree}```\n"

        with open(readme_path, "w") as file:
            file.write(readme_content)

        print(f"Created README.md in {directory}")


#
# COMMAND LINE INTERFACE
# ----------------------
#


def cli():
    def get_parser():
        ...

    def dispatch():
        ...


if __name__ == "__main__":
    main()
