import click
from core.api.datasource import GrafanaDataSourceManager
from core.json_parser.parser import apply_patch
from cli.commands.flag_ref import flags
from cli.context import apply_flag, using_manager
from core.journaling import stdout_logger as c_logger


@click.group()
def datasource():
    ...


@datasource.command
@apply_flag(flags.config)
@apply_flag(flags.patch)
@apply_flag(flags.uuid)
@using_manager(GrafanaDataSourceManager)
def export(manager, config, patch, uuid):
    # patch_obj = parse_patch(patch)
    datasource_dict = manager.get_datasource(uuid)
    updated_datasource_dict = apply_patch(datasource_dict, patch_obj)
    manager.update(uuid, updated_datasource_dict)
    return


@datasource.command(name="list")
@apply_flag(flags.config)
@using_manager(GrafanaDataSourceManager)
def list_datasources(manager, config):
    datasources = manager.get_all()
    c_logger.info(datasources)
    return
