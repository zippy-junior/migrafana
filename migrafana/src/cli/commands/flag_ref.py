from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Flag(BaseModel):
    param_decls: list[str]
    alias: str
    type: type
    required: bool
    help: str


class Flags(BaseSettings):
    src: Flag = Flag(param_decls=['-s', '--source'],
                     alias='source',
                     type=str,
                     required=True,
                     help='URL of source Grafana instance')
    dest: Flag = Flag(param_decls=['-d', '--destination'],
                      alias='destination',
                      type=str,
                      required=True,
                      help='URL of destination Grafana instance')
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
