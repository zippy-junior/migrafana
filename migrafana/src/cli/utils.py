import json
import click
from cli.commands.flag_ref import Flag
from functools import wraps

from core.api.base import GrafanaBaseManager
from core.api.models import GrafanaManagerConfig
from cli.commands.flag_ref import flags


def apply_flag(flag: Flag, **kwargs):
    """Full-featured flag application decorator that uses alias for parameter names"""
    def decorator(f):
        # Use the alias as the parameter name in the function
        # and the param_decls for the CLI options
        return click.option(
            # Add alias to param_decls list so that we get known param name in cli function
            *[*flag.param_decls, flag.alias],
            cls=click.Option,
            type=flag.type,
            required=flag.required,
            help=flag.help,
        )(f)
    return decorator


def using_manager(manager: GrafanaBaseManager):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            config = kwargs.get(flags.config, None)
            url = kwargs.get(flags.url.alias, None)
            config_path = kwargs.get(flags.config_path.alias, None)
            if not any([config, url, config_path]):
                raise click.MissingParameter("Neither of --conf, --url, --conf-path options is supplied")
            if url:
                pass
            if config:
                pass
            if config_path:
                pass 
            m = manager.from_config(conf=GrafanaManagerConfig())
            fn(m, *args, **kwargs)
        return wrapper
    return decorator


def parse_patch(patch_path):
    try:
        with open(f'{patch_path}', 'r+') as patch_file:
            patch = patch_file.read()
            return json.loads(patch)
    except Exception:
        return
