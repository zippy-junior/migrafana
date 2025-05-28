import click
from dotenv import load_dotenv

from cli.commands.dashboard.dashboard import dashboard
from cli.commands.datasource.datasource import datasource


load_dotenv()


@click.group
def cli():
    ...


def main():
    cli.add_command(dashboard)
    cli.add_command(datasource)
    cli()


if __name__ == "__main__":
    main()
