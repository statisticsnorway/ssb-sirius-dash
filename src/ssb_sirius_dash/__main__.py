"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Sirius Dash."""


if __name__ == "__main__":
    main(prog_name="ssb-sirius-dash")  # pragma: no cover
