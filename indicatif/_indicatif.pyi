from __future__ import annotations

from datetime import timedelta
from typing import Literal


class TemplateError(Exception):
    def __init__(self) -> None: ...


class ProgressDrawTarget:
    pass


class ProgressStyle:
    def __init__(self, template: str | None, progress_chars: str | None) -> None: ...


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

    def inc(self, delta: int) -> None: ...

    def finish(self, msg: str | None = None) -> None: ...

    def tick(self) -> None: ...

    def is_hidden(self) -> bool: ...

    def is_finished(self) -> bool: ...

    def println(self, msg: str) -> None: ...

    def unset_length(self) -> None: ...

    def inc_length(self, delta: int) -> None: ...

    def set_style(self, style: ProgressStyle) -> None: ...

    def reset(self) -> None: ...

    def finish_and_clear(self) -> None: ...


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
