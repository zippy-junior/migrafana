import click

from cli.utils import apply_flag, parse_patch
from cli.commands.flag_ref import flags
from core.api.dashboard import GrafanaDashboardManager
from core.context import using_manager
from core.json_parser.parser import apply_patch
from core.journaling import stdout_logger as c_logger


@click.group
def dashboard():
    ...


@dashboard.command
@apply_flag(flags.src)
@apply_flag(flags.dest)
@apply_flag(flags.patch)
@apply_flag(flags.uuid)
@using_manager(GrafanaDashboardManager)
def export(manager, src, dest, patch, uuid):
    patch_obj = parse_patch(patch)
    # Initialize grafana-client
    dash_dict = manager.get_by_uid(uuid)
    updated_dash_dict = apply_patch(dash_dict['dashboard'], patch_obj)
    dash_dict['dashboard'] = updated_dash_dict
    manager.update(dash_dict)
    return


@dashboard.command(name="list")
@apply_flag(flags.src)
@using_manager(GrafanaDashboardManager)
def list_dashboards(manager, source):
    dashboards = manager.get_all()
    c_logger.info(dashboards)
    return
