import json
import os
import click
from dotenv import load_dotenv

from core.api.datasource import GrafanaDataSourceManager
from core.json_parser.parser import apply_patch
from core.api.dashboard import GrafanaDashboardManager
from core.api.models import Creds, GrafanaConfig
from core.journaling import stdout_logger as c_logger


load_dotenv()


def get_credentials() -> Creds:
    """Try multiple secure sources"""

    grafana_user = os.getenv('GRAFANA_USER')
    grafana_pass = os.getenv('GRAFANA_PASS')
    grafana_api_token = os.getenv('GRAFANA_API_TOKEN')
    if grafana_user and grafana_pass:
        return Creds(login=grafana_user, password=grafana_pass, token=grafana_api_token)

    raise click.BadParameter("No credentials found")


def parse_patch(patch):
    try:
        with open(f'{patch}', 'r+') as patch_file:
            patch = patch_file.read()
            return json.loads(patch)
    except Exception:
        return


@click.group
def cli():
    ...


@cli.command
@click.option('--src', help='URL of source Grafana instance')
@click.option('--dest', help='URL of destination Grafana instance')
@click.option('--patch', help='JSON patch file using RFC6902 standard '
                              'with mapping to change dashboard components '
                              'patch = [{ '
                              '"op": "replace", '
                              '"path": "/dashboard/*/[?type==\'graph\']/title" '
                              '"value": "Updated" '
                              '}]')
@click.option('--uuid', help='UUID of dashboard to change')
def dashboard(src, dest, patch, uuid):
    patch_obj = parse_patch(patch)
    creds = get_credentials()
    # Initialize grafana-client
    dash_manager = GrafanaDashboardManager.from_config(conf=GrafanaConfig(creds=creds, url=src))
    dash_dict = dash_manager.get_dashboard(uuid)
    updated_dash_dict = apply_patch(dash_dict['dashboard'], patch_obj)
    dash_dict['dashboard'] = updated_dash_dict
    dash_manager.update_dashboard(dash_dict)
    return


@cli.command
@click.option('--src', help='URL of source Grafana instance')
@click.option('--dest', help='URL of destination Grafana instance')
@click.option('--patch', help='JSON patch file using RFC6902 standard '
                              'with mapping to change dashboard components '
                              'patch = [{ '
                              '"op": "replace", '
                              '"path": "/dashboard/*/[?type==\'graph\']/title" '
                              '"value": "Updated" '
                              '}]')
@click.option('--uuid', help='UUID of datasource to change')
def datasource(src, dest, patch, uuid):
    patch_obj = parse_patch(patch)
    creds = get_credentials()
    # Initialize grafana-client
    dash_manager = GrafanaDataSourceManager(src, creds)
    datasource_dict = dash_manager.get_datasource(uuid)
    updated_dash_dict = apply_patch(datasource_dict, patch_obj)
    dash_manager.update_datasource(uuid, updated_dash_dict)


@cli.command
@click.option('--src', required=True, help='URL of source Grafana instance')
def ls_datasources(src):
    creds = get_credentials()
    # Initialize grafana-client
    dash_manager = GrafanaDataSourceManager.from_config(conf=GrafanaConfig(creds=creds, url=src))
    datasources = dash_manager.list_datasources()
    c_logger.info(datasources)


def main():
    cli()


if __name__ == "__main__":
    main()
