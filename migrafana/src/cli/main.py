import json
import click
from dotenv import load_dotenv

from core.api.datasource import GrafanaDataSourceManager
from core.api.dashboard import GrafanaDashboardManager
from core.json_parser.parser import apply_patch
from core.journaling import stdout_logger as c_logger
from core.context import using_manager


load_dotenv()


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
@using_manager(GrafanaDashboardManager)
def dashboard(manager, src, dest, patch, uuid):
    patch_obj = parse_patch(patch)
    # Initialize grafana-client
    dash_dict = manager.get_by_uid(uuid)
    updated_dash_dict = apply_patch(dash_dict['dashboard'], patch_obj)
    dash_dict['dashboard'] = updated_dash_dict
    manager.update(dash_dict)
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
@using_manager(GrafanaDataSourceManager)
def datasource(manager, src, dest, patch, uuid):
    patch_obj = parse_patch(patch)
    datasource_dict = manager.get_datasource(uuid)
    updated_datasource_dict = apply_patch(datasource_dict, patch_obj)
    manager.update(uuid, updated_datasource_dict)
    return


@cli.command
@click.option('--src', required=True, help='URL of source Grafana instance')
@using_manager(GrafanaDataSourceManager)
def ls_datasources(manager, src):
    datasources = manager.get_all()
    c_logger.info(datasources)
    return


def main():
    cli()


if __name__ == "__main__":
    main()
