from .. import run_as_module

if not run_as_module:
    from ..exceptions import RunningAsFunctionLibError

    raise RunningAsFunctionLibError(
        "You are running 'Kazu' as a functions lib, not as run module. You can't access this folder.."
    )

from .. import *

CMD_HANDLER = os.environ.get("CMD_HANDLER") or "."

DEVLIST = [
    
    6218149232, # @amwang
    6228635168,
]

cmd = CMD_HANDLER
CMD_LIST = {}

DEFAULT = [
    6218149238, # @asaaqali
    6228635168,
]

KAZU_IMAGES = [
    f"https://graph.org/file/{_}.jpg"
    for _ in [
        "file/b23bdfbaa9a7c650f9383",
    ]
]

stickers = [

]
