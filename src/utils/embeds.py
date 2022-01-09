from enum import Enum

from discord import Embed


class Kind(Enum):
    Success = 0
    Error = 1


def simple_embed(title='', description="", kind: Kind = Kind.Success) -> Embed:
    if kind.Success == kind:
        color = 0x738ADB
    else:
        color = 0xff9b9b
    embed = Embed(title=title, description=description, color=color)
    return embed
