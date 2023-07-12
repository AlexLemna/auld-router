import argparse

try:
    from . import commands as cmd

except ImportError:
    import commands as cmd  # type: ignore
