from ._indicatif import Color, Style

from typing import Literal

__all__ = ["Color", "Style", "style"]

type color_str = Literal[
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
]


def style(
    text: str,
    fg: color_str | None = None,
    bg: color_str | None = None,
    bold: bool = False,
) -> str:
    style = Style()

    if fg is not None:
        style = style.fg(Color(fg))

    if bg is not None:
        style = style.bg(Color(bg))

    if bold:
        style = style.bold()

    return style.apply_to(text)
    # text, fg=None, bg=None, bold=None, dim=None, underline=None, overline=None, italic=None, blink=None, reverse=None, strikethrough=None, reset=True)
