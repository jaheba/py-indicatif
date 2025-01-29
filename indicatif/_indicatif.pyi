from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Callable, Literal, Never


class TemplateError(Exception):
    def __init__(self) -> Never: ...


class ProgressDrawTarget:
    pass


class ProgressStyle:
    def __init__(
        self,
        template: str | None = None,
        progress_chars: str | None = None,
        tick_chars: str | None = None,
    ) -> None: ...


class ProgressBar:
    length: int | None
    message: str
    position: int
    prefix: str
    style: ProgressStyle

    def __init__(
        self,
        length: int | None = None,
        message: str | None = None,
        prefix: str | None = None,
        style: ProgressStyle | None = None,
    ) -> None: ...

    @staticmethod
    def new(len: int) -> ProgressBar: ...

    @staticmethod
    def no_length() -> ProgressBar: ...

    @staticmethod
    def hidden() -> ProgressBar: ...

    @staticmethod
    def new_spinner() -> ProgressBar: ...

    @staticmethod
    def with_draw_target(
        len: int | None, draw_target: ProgressDrawTarget
    ) -> ProgressBar: ...

    def abandon(self, msg: str | None = None): ...

    def enable_steady_tick(self, interval: timedelta) -> None: ...

    def disable_steady_tick(self) -> None: ...

    def duration(self) -> timedelta: ...

    def elapsed(self) -> timedelta: ...

    def eta(self) -> timedelta: ...

    def per_sec(self) -> timedelta: ...

    def inc(self, delta: int) -> None: ...

    def dec(self, delta: int) -> None: ...

    def tick(self) -> None: ...

    def is_hidden(self) -> bool: ...

    def is_finished(self) -> bool: ...

    def println(self, msg: str) -> None: ...

    def unset_length(self) -> None: ...

    def inc_length(self, delta: int) -> None: ...

    def dec_length(self, delta: int) -> None: ...

    def set_style(self, style: ProgressStyle) -> None: ...

    def reset(self) -> None: ...

    def reset_eta(self) -> None: ...

    def reset_elapsed(self) -> None: ...

    def finish(self, msg: str | None = None) -> None: ...

    def finish_with_message(self, msg: str) -> None: ...

    def finish_and_clear(self) -> None: ...

    def finish_using_style(self) -> None: ...

    def suspend[T](self, f: Callable[[], T]) -> T: ...

    def set_tab_width(self, tab_width: int) -> None: ...

    def set_draw_target(self, draw_target: ProgressDrawTarget) -> None: ...

    def with_style(self, style: ProgressStyle) -> ProgressBar: ...

    def with_tab_width(self, tab_width: int) -> ProgressBar: ...


class MultiProgressAlignment(Enum):
    Top = 0
    Bottom = 1


class MultiProgress:
    def __init__(self) -> None: ...

    @staticmethod
    def with_draw_target(draw_target: ProgressDrawTarget) -> MultiProgress: ...

    def set_draw_target(self, draw_target: ProgressDrawTarget) -> None: ...

    def set_move_cursor(self, move_cursor: bool) -> None: ...

    def set_alignment(self, alignment: MultiProgressAlignment) -> None: ...

    def add(self, pb: ProgressBar) -> ProgressBar: ...

    def insert(self, index: int, pb: ProgressBar) -> ProgressBar: ...

    def insert_from_back(self, index: int, pb: ProgressBar) -> ProgressBar: ...

    def insert_before(self, before: ProgressBar, pb: ProgressBar) -> ProgressBar: ...

    def insert_after(self, after: ProgressBar, pb: ProgressBar) -> ProgressBar: ...

    def remove(self, pb: ProgressBar) -> ProgressBar: ...

    def println(self, msg: str) -> None: ...

    def suspend[R](self, f: Callable[[], R]) -> R: ...

    def clear(self) -> None: ...

    def is_hidden(self) -> bool: ...


class BinaryBytes:
    def __init__(self, bytes: int) -> None: ...

    def __str__(self) -> str: ...


class DecimalBytes:
    def __init__(self, bytes: int) -> None: ...

    def __str__(self) -> str: ...


class HumanBytes:
    def __init__(self, bytes: int) -> None: ...

    def __str__(self) -> str: ...


class HumanCount:
    def __init__(self, count: int) -> None: ...

    def __str__(self) -> str: ...


class HumanDuration:
    def __init__(self, duration: timedelta) -> None: ...

    def __str__(self) -> str: ...


class HumanFloatCount:
    def __init__(self, count: float) -> None: ...

    def __str__(self) -> str: ...


## console.rs stuff


class Style:
    def __init__(self) -> None: ...

    @staticmethod
    def from_dotted_str(s: str) -> Style: ...

    def apply_to(self, val: str) -> StyledObject: ...

    def force_styling(self, value: bool) -> Style: ...

    def for_stderr(self) -> Style: ...

    def for_stdout(self) -> Style: ...

    def fg(self, color: Color) -> Style: ...

    def bg(self, color: Color) -> Style: ...

    def bold(self) -> Style: ...

    def dim(self) -> Style: ...

    def black(self) -> Style: ...

    def red(self) -> Style: ...

    def green(self) -> Style: ...

    def yellow(self) -> Style: ...

    def blue(self) -> Style: ...

    def magenta(self) -> Style: ...

    def cyan(self) -> Style: ...

    def white(self) -> Style: ...

    def color256(self, color: int) -> Style: ...


class StyledObject:
    def __str__(self) -> str: ...

    def force_styling(self, value: bool) -> Style: ...

    def for_stderr(self) -> Style: ...

    def for_stdout(self) -> Style: ...

    def fg(self, color: Color) -> Style: ...

    def bg(self, color: Color) -> Style: ...

    def bold(self) -> Style: ...

    def dim(self) -> Style: ...

    def black(self) -> Style: ...

    def red(self) -> Style: ...

    def green(self) -> Style: ...

    def yellow(self) -> Style: ...

    def blue(self) -> Style: ...

    def magenta(self) -> Style: ...

    def cyan(self) -> Style: ...

    def white(self) -> Style: ...

    def color256(self, color: int) -> Style: ...


class Color:
    def __init__(
        self,
        color: Literal[
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
        ],
    ) -> None: ...

    @staticmethod
    def Black() -> Color: ...

    @staticmethod
    def Red() -> Color: ...

    @staticmethod
    def Green() -> Color: ...

    @staticmethod
    def Yellow() -> Color: ...

    @staticmethod
    def Blue() -> Color: ...

    @staticmethod
    def Magenta() -> Color: ...

    @staticmethod
    def Cyan() -> Color: ...

    @staticmethod
    def White() -> Color: ...

    @staticmethod
    def Color256(color: int) -> Color: ...


class Emoji:
    def __init__(self, emoji: str, fallback: str) -> None: ...
