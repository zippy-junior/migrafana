from typing import Any, Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Flag(BaseModel):
    param_decls: list[str]
    alias: str
    type: type
    required: bool
    default: Optional[Any] = None
    help: str


class Flags(BaseSettings):
    config: Flag = Flag(param_decls=['--conf'],
                     alias='config',
                     type=str,
                     required=False,
                     help='Connection config. '
                     'Accepts JSON string config: \'[{"url": "...", "master": "true"}, {"url": "..."}]\'')
    config_path: Flag = Flag(param_decls=['--conf-path'],
                      alias='config_path',
                      required=False,
                      type=str,
                      default=False,
                      help='Path to config JSON file')
    url: Flag = Flag(param_decls=['--url'],
                      alias='url',
                      required=False,
                      type=str,
                      default=False,
                      help='Single grafana url')
    patch: Flag = Flag(param_decls=['-p', '--patch'],
                       alias='patch',
                       type=str,
                       required=True,
                       help='Path to JSON patch file or json string in RFC6902 standard'
                            'patch = [{ '
                            '"op": "replace", '
                            '"path": "/dashboard/*/[?type==\'graph\']/title" '
                            '"value": "Updated" '
                            '}]')
    uuid: Flag = Flag(param_decls=['--uid'],
                      alias='uid',
                      type=str,
                      required=True,
                      help='UID of instance to change')
    folder: Flag = Flag(param_decls=['-f', '--folder'],
                        alias='folder',
                        type=str,
                        required=True,
                        help='Grafana folder name')


flags = Flags()
