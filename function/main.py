"""The composition function's main CLI."""

import click
from crossplane.function import cli as sdkcli

from function import fn


@click.command()
@sdkcli.standard_options
def cli(**kwargs):
    """A Crossplane composition function."""
    sdkcli.run(fn.FunctionRunner(), **kwargs)


if __name__ == "__main__":
    cli()
