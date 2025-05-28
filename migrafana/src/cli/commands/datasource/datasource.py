import click
from core.context import using_manager
from core.api.datasource import GrafanaDataSourceManager
from cli.utils import parse_patch
from core.json_parser.parser import apply_patch
from cli.commands.flag_ref import flags
from cli.utils import apply_flag
from core.journaling import stdout_logger as c_logger


@click.group()
def datasource():
    ...


@datasource.command
@apply_flag(flags.src)
@apply_flag(flags.dest)
@apply_flag(flags.patch)
@apply_flag(flags.uuid)
@using_manager(GrafanaDataSourceManager)
def export(manager, src, dest, patch, uuid):
    patch_obj = parse_patch(patch)
    datasource_dict = manager.get_datasource(uuid)
    updated_datasource_dict = apply_patch(datasource_dict, patch_obj)
    manager.update(uuid, updated_datasource_dict)
    return


@datasource.command(name="list")
@apply_flag(flags.src)
@using_manager(GrafanaDataSourceManager)
def list_datasources(manager, source):
    datasources = manager.get_all()
    c_logger.info(datasources)
    return
