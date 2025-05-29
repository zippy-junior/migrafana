import click

from cli.context import apply_flag, parse_patch, using_manager
from cli.commands.flag_ref import flags
from core.api.dashboard import GrafanaDashboardManager
from core.json_parser.parser import apply_patch
from core.journaling import stdout_logger as c_logger


@click.group
def dashboard():
    ...


@dashboard.command
@apply_flag(flags.config)
@apply_flag(flags.url)
@apply_flag(flags.config_path)
@apply_flag(flags.patch)
@apply_flag(flags.uuid)
@using_manager(GrafanaDashboardManager)
def export(manager, config, patch, uuid):
    patch_obj = parse_patch(patch)
    dash_dict = manager.get_by_uid(uuid)
    updated_dash_dict = apply_patch(dash_dict, patch_obj)
    manager.update(updated_dash_dict)
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
