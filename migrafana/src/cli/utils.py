import json
import click
from cli.commands.flag_ref import Flag


def apply_flag(flag: Flag, **kwargs):
    """Full-featured flag application decorator"""
    def decorator(f):

        return click.option(
            *flag.param_decls,
            cls=click.Option,
            type=flag.type,
            required=flag.required,
            help=flag.help,
            **kwargs
        )(f)
    return decorator


def parse_patch(patch_path):
    try:
        with open(f'{patch_path}', 'r+') as patch_file:
            patch = patch_file.read()
            return json.loads(patch)
    except Exception:
        return
