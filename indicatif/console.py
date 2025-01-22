from ._indicatif import Color, Style, StyledObject, Emoji

from typing import Literal

__all__ = ["Color", "Emoji", "Style", "style"]

type color_str = Literal[
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
]


#  underline=None, overline=None, italic=None, blink=None, reverse=None, strikethrough=None, reset=True)
def style(
    text: str,
    fg: color_str | None = None,
    bg: color_str | None = None,
    bold: bool = False,
    dim: bool = False,
) -> StyledObject:
    style = Style()

    if fg is not None:
        style = style.fg(Color(fg))

    if bg is not None:
        style = style.bg(Color(bg))

    if bold:
        style = style.bold()

    if dim:
        style = style.dim()

    return style.apply_to(text)
