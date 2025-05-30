import os
from pathlib import Path
from typing import Optional
import click
from dotenv import load_dotenv
from pydantic import ValidationError
from cli.flag_ref import Flag, flags
from functools import wraps
from urllib.parse import parse_qs, urlparse

from core.api.base import GrafanaBaseManager
from core.api.models import GrafanaInstanceConfig, GrafanaInstanceCredentials, GrafanaManagerConfig
from core.models import Patch


def apply_flag(flag: Flag, **kwargs):
    """Full-featured flag application decorator that uses alias for parameter names"""
    def decorator(f):
        # Use the alias as the parameter name in the function
        # and the param_decls for the CLI options
        overwrite_required = kwargs.get('required', None)
        # Apply overwrites if specified
        required = overwrite_required if overwrite_required is not None else flag.required
        return click.option(

            # Add alias to param_decls list so that we get known param name in cli function
            *[*flag.param_decls, flag.alias],
            cls=click.Option,
            type=flag.type,
            required=required,
            help=flag.help,
            is_flag=flag.is_flag
        )(f)
    return decorator


def get_env_credentials(dotenv_path: Optional[str] = None) -> Optional[GrafanaInstanceCredentials]:
    if dotenv_path:
        load_dotenv(dotenv_path)
    username = os.getenv("GRAFANA_API_USERNAME")
    password = os.getenv("GRAFANA_API_PASSWORD")
    token = os.getenv("GRAFANA_API_TOKEN")
    if (username and password) or token:
        return GrafanaInstanceCredentials(
            username,
            password,
            token
        )
    else:
        return None


def get_url_credentials(url: str) -> Optional[GrafanaInstanceCredentials]:
    parsed_url = urlparse(url)
    username = parsed_url.username
    password = parsed_url.password
    token = parse_qs(parsed_url.query).get('auth_token', None)
    if (username and password) or token:
        return GrafanaInstanceCredentials(
            username=username,
            password=password,
            token=token
        )
    else:
        return None


def get_config_from_file(config_path: str) -> GrafanaManagerConfig:
    path_exists = Path(config_path).exists
    if not path_exists:
        raise click.BadParameter(f"No config on path {config_path}")
    with open(config_path) as file:
        raw_config = file.read()
        try:
            parsed_config = GrafanaManagerConfig.model_validate_json(raw_config)
            return parsed_config
        except ValidationError:
            raise click.BadParameter(f"""Config not valid. {e.errors(include_url=False,
                                                                   include_input=False,
                                                                   include_context=False)}""")


def using_manager(manager: GrafanaBaseManager):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            raw_config = kwargs.get(flags.config.alias, None)
            url = kwargs.get(flags.url.alias, None)
            config_path = kwargs.get(flags.config_path.alias, None)
            if not any([raw_config, url, config_path]):
                raise click.MissingParameter("Neither of --conf, --url, --conf-path options is supplied")
            if url:
                env_creds = get_env_credentials()
                url_creds = get_url_credentials(url)
                if not any([env_creds, url_creds]):
                    raise click.BadParameter("Grafana credentials not provided (not url nor .env file)")
                config = GrafanaManagerConfig(
                    instances=[GrafanaInstanceConfig(
                        url=url,
                        master=True,
                        credentials=env_creds or url_creds
                    )]
                )
            elif raw_config:
                try:
                    config = GrafanaManagerConfig.model_validate_json(raw_config)
                except ValidationError as e:
                    raise click.BadParameter(f"""Config not valid. {e.errors(include_url=False,
                                                                           include_input=False,
                                                                           include_context=False)}""")
            elif config_path:
                config = get_config_from_file(config_path)
            m = manager.from_config(conf=config)
            fn(m, *args, **kwargs)
        return wrapper
    return decorator


def using_patch():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            raw_patch = kwargs.get(flags.patch.alias, None)
            if not raw_patch:
                fn(*args, **kwargs)
                return
            is_path = Path(raw_patch).is_file()
            if is_path:
                with open(f'{raw_patch}', 'r+') as patch_file:
                    raw_patch = patch_file.read()
            try:
                parsed_patch = Patch.model_validate_json(raw_patch)
            except ValidationError as e:
                raise click.BadParameter(f"""Patch not valid. {e.errors(include_url=False,
                                                                        include_input=False,
                                                                        include_context=False)}""")
            kwargs[flags.patch.alias] = parsed_patch
            fn(*args, **kwargs)
        return wrapper
    return decorator
