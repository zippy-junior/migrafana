from typing import Any, Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Flag(BaseModel):
    param_decls: list[str]
    alias: str
    type: type
    required: bool
    default: Optional[Any] = None
    is_flag: Optional[bool] = False
    help: str
    visible: bool = True


class Flags(BaseSettings):
    config: Flag = Flag(param_decls=['--conf'],
                        alias='config',
                        type=str,
                        required=False,
                        visible=False,
                        help='Connection config. '
                        'Accepts JSON string config: \'[{"url": "...", "master": "true"}, {"url": "..."}]\'')
    config_path: Flag = Flag(param_decls=['--conf-path'],
                             alias='config_path',
                             required=False,
                             type=str,
                             default=False,
                             visible=False,
                             help='Path to config JSON file')
    url: Flag = Flag(param_decls=['--url'],
                     alias='url',
                     required=False,
                     type=str,
                     default=False,
                     visible=False,
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
    uid: Flag = Flag(param_decls=['--uid'],
                      alias='uid',
                      type=str,
                      required=True,
                      help='UID of instance to change')
    folder: Flag = Flag(param_decls=['-f', '--folder'],
                        alias='folder',
                        type=str,
                        required=True,
                        help='Grafana folder name')
    export_to: Flag = Flag(param_decls=['--export-to'],
                        alias='export_to',
                        type=str,
                        required=True,
                        help='Path where to save exported files')
    import_from: Flag = Flag(param_decls=['--import-from'],
                       alias='import_from',
                       type=str,
                       required=True,
                       help='Path of file to import')
    overwrite: Flag = Flag(param_decls=['--overwrite'],
                     alias='overwrite',
                     type=bool,
                     required=False,
                     is_flag=True,
                     help='Overwrite existing data')


flags = Flags()
