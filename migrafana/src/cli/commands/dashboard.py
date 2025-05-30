import json
from pathlib import Path
from typing import Optional
import click

from cli.context import apply_flag, using_manager, using_patch
from cli.flag_ref import flags
from core.api.dashboard import GrafanaDashboardManager
from core.json_parser.parser import apply_patch
from core.journaling import stdout_logger as c_logger
from core.models import Patch


@click.group
def dashboard():
    ...


@dashboard.command(name='export')
@apply_flag(flags.config)
@apply_flag(flags.url)
@apply_flag(flags.config_path)
@apply_flag(flags.patch)
@apply_flag(flags.uid)
@apply_flag(flags.export_to)
@using_patch()
@using_manager(GrafanaDashboardManager)
def export_from_grafana(manager, patch: Patch, uid, export_to, **kwargs):
    dash_dict = manager.get_by_uid(uid)
    if not dash_dict:
        print(f"Dashboard with uid {uid} not found")
        return
    updated_dash_dict = apply_patch(dash_dict, patch)
    is_path_valid = Path(export_to).parent.exists()
    if is_path_valid:
        with open(export_to, "w+") as export_file:
            export_file.write(json.dumps(updated_dash_dict))
    else:
        click.BadParameter("Destination export path does not exist")
    return


@dashboard.command(name="import")
@apply_flag(flags.config)
@apply_flag(flags.url)
@apply_flag(flags.config_path)
@apply_flag(flags.patch, required=False)
@apply_flag(flags.import_from)
@apply_flag(flags.overwrite)
@using_patch()
@using_manager(GrafanaDashboardManager)
def import_to_grafana(manager: GrafanaDashboardManager, patch: Optional[Patch], import_from, overwrite, **kwargs):
    is_path_valid = Path(import_from).exists()
    if is_path_valid:
        with open(import_from, "r") as import_file:
            dashboard = json.loads(import_file.read())
            # ToDO Make simple Dashboard pydantic model to verify necessary fields 
            if not dashboard.get('dashboard'):
                return  # ToDO raise an exception
            if patch:
                dashboard = apply_patch(dashboard, patch)
            uid = dashboard['dashboard'].get('uid')
            exist = manager.get_by_uid(uid)
            if overwrite and exist:
                manager.delete(uid)
                manager.create(dashboard)
            elif not overwrite and exist:
                print("++++++++")
                manager.update(dashboard)
            else:
                manager.create(dashboard)
    else:
        click.BadParameter("Destination export path does not exist")
    return


@dashboard.command
@apply_flag(flags.config)
@apply_flag(flags.url)
@apply_flag(flags.config_path)
@apply_flag(flags.patch)
@apply_flag(flags.uid)
@using_patch()
@using_manager(GrafanaDashboardManager)
def migrate(manager, patch: Patch, uid, **kwargs):
    dash_dict = manager.get_by_uid(uid)
    updated_dash_dict = apply_patch(dash_dict, patch)
    manager.update_slaves(updated_dash_dict)
    return


@dashboard.command(name="list")
@apply_flag(flags.config)
@apply_flag(flags.url)
@apply_flag(flags.config_path)
@using_manager(GrafanaDashboardManager)
def list_dashboards(manager, config, url, config_path):
    dashboards = manager.get_all()
    c_logger.info(dashboards)
    return
