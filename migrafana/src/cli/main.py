import click
from dotenv import load_dotenv
from importlib.metadata import version

from cli.commands.dashboard import dashboard
from cli.commands.datasource import datasource


load_dotenv()


version_message = f"""migrafana {version('migrafana')}
Copyright (C) 2025
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law."""


@click.group
@click.version_option(package_name='migrafana',
                      message=version_message,
                      help='Show migrafana version information')
@click.help_option(help='Show manual')
def cli():
    ...


def main():
    cli.add_command(dashboard)
    cli.add_command(datasource)
    cli()


if __name__ == "__main__":
    main()
