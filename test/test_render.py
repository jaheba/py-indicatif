import time
from datetime import timedelta

import pytest

from indicatif import InMemoryTerm, MultiProgress, ProgressBar, ProgressStyle
from indicatif._indicatif import (
    ProgressDrawTarget,
    ProgressFinish,
    MultiProgressAlignment,
)


def test_basic_progress_bar():
    in_mem = InMemoryTerm(10, 80)

    pb = ProgressBar.with_draw_target(10, ProgressDrawTarget.term_like(in_mem))

    assert in_mem.contents() == ""

    pb.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )

    pb.inc(1)
    assert (
        in_mem.contents()
        == "███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/10"
    )

    pb.finish()
    assert (
        in_mem.contents()
        == "██████████████████████████████████████████████████████████████████████████ 10/10"
    )


def test_progress_bar_builder_method_order():
    in_mem = InMemoryTerm(10, 80)
    # Test that `with_style` doesn't overwrite the message or prefix
    pb = (
        ProgressBar.with_draw_target(
            10,
            ProgressDrawTarget.term_like(in_mem),
        )
        .with_message("crate")
        .with_prefix("Downloading")
        .with_style(
            ProgressStyle(
                template="{prefix:>12.cyan.bold} {msg}: {wide_bar} {pos}/{len}"
            )
        )
    )

    assert in_mem.contents() == ""

    pb.tick()
    assert (
        in_mem.contents()
        == " Downloading crate: ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )


def test_progress_bar_percent_with_no_length():
    in_mem = InMemoryTerm(10, 80)
    pb = ProgressBar.with_draw_target(
        None,
        ProgressDrawTarget.term_like(in_mem),
    ).with_style(ProgressStyle(template="{wide_bar} {percent}%"))

    assert in_mem.contents() == ""

    pb.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%"
    )

    pb.length = 10

    pb.inc(1)
    assert (
        in_mem.contents()
        == "███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10%"
    )

    pb.finish()
    assert (
        in_mem.contents()
        == "███████████████████████████████████████████████████████████████████████████ 100%"
    )


def test_progress_bar_percent_precise_with_no_length():
    in_mem = InMemoryTerm(10, 80)
    pb = ProgressBar.with_draw_target(
        None,
        ProgressDrawTarget.term_like(in_mem),
    ).with_style(ProgressStyle(template="{wide_bar} {percent_precise}%"))

    assert in_mem.contents() == ""

    pb.tick()

    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0.000%"
    )

    pb.length = 10

    pb.inc(1)
    assert (
        in_mem.contents()
        == "███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10.000%"
    )

    pb.finish()
    assert (
        in_mem.contents()
        == "███████████████████████████████████████████████████████████████████████ 100.000%"
    )


def test_multi_progress_single_bar_and_leave():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10).with_finish(ProgressFinish.AndLeave()))

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )

    del pb1
    assert (
        in_mem.contents()
        == "██████████████████████████████████████████████████████████████████████████ 10/10"
    )


def multi_progress_single_bar_and_clear():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10))

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )

    del pb1
    assert in_mem.contents() == ""


def test_multi_progress_two_bars():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10).with_finish(ProgressFinish.AndLeave()))
    pb2 = mp.add(ProgressBar(5))

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )

    pb2.tick()

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5
        """.strip()
    )

    del pb1
    assert (
        in_mem.contents()
        == """
██████████████████████████████████████████████████████████████████████████ 10/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5
        """.strip()
    )

    del pb2

    assert (
        in_mem.contents()
        == "██████████████████████████████████████████████████████████████████████████ 10/10"
    )


def test_multi_progress():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10).with_finish(ProgressFinish.AndLeave()))
    pb2 = mp.add(ProgressBar(5))
    pb3 = mp.add(ProgressBar(100))

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )

    pb2.tick()

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5
    """.strip()
    )

    pb3.tick()
    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100
        """.strip()
    )

    del pb1
    assert (
        in_mem.contents()
        == """
██████████████████████████████████████████████████████████████████████████ 10/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100
    """.strip()
    )

    del pb2
    assert (
        in_mem.contents()
        == """
██████████████████████████████████████████████████████████████████████████ 10/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100
    """.strip()
    )

    del pb3

    assert (
        in_mem.contents()
        == "██████████████████████████████████████████████████████████████████████████ 10/10"
    )


def test_multi_progress_println():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10))
    pb2 = mp.add(ProgressBar(5))
    pb3 = mp.add(ProgressBar(100))

    assert in_mem.contents() == ""

    pb1.inc(2)
    mp.println("message printed :)")

    assert (
        in_mem.contents()
        == """
message printed :)
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
        """.strip()
    )

    mp.println("another great message!")
    assert (
        in_mem.contents()
        == """
message printed :)
another great message!
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
            """.strip()
    )

    pb2.inc(1)
    pb3.tick()
    mp.println("one last message")

    assert (
        in_mem.contents()
        == """
message printed :)
another great message!
one last message
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/5
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100
        """.strip()
    )

    del pb1
    del pb2
    del pb3

    assert (
        in_mem.contents()
        == """
message printed :)
another great message!
one last message
        """.strip()
    )


def test_multi_progress_suspend():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10))
    pb2 = mp.add(ProgressBar(10))

    assert in_mem.contents() == ""

    pb1.inc(2)
    mp.println("message printed :)")

    assert (
        in_mem.contents()
        == """
message printed :)
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
            """.strip()
    )

    def f():
        in_mem.write_line("This is write_line output!")
        in_mem.write_line("And so is this")
        in_mem.move_cursor_down(1)

    mp.suspend(f)

    assert (
        in_mem.contents()
        == """
message printed :)
This is write_line output!
And so is this

███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
        """.strip()
    )

    pb2.inc(1)
    mp.println("Another line printed")

    assert (
        in_mem.contents()
        == """
message printed :)
This is write_line output!
And so is this

Another line printed
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/10
        """.strip()
    )

    del pb1
    del pb2

    assert (
        in_mem.contents()
        == """
message printed :)
This is write_line output!
And so is this

Another line printed
        """.strip()
    )


def test_multi_progress_move_cursor():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))
    mp.set_move_cursor(True)

    pb1 = mp.add(ProgressBar(10))
    pb1.tick()
    assert (
        in_mem.moves_since_last_check()
        == r"""
Str("\r")
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
Flush
""".lstrip()
    )

    pb2 = mp.add(ProgressBar(10))
    pb2.tick()
    assert (
        in_mem.moves_since_last_check()
        == r"""Str("\r")
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
Flush
""".lstrip()
    )

    pb1.inc(1)
    assert (
        in_mem.moves_since_last_check()
        == r"""Up(1)
Str("\r")
Str("███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/10")
Str("")
NewLine
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
Flush
""".lstrip()
    )


def test_multi_progress_println_bar_with_target():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb = mp.add(ProgressBar.with_draw_target(10, ProgressDrawTarget.term_like(in_mem)))

    assert in_mem.contents() == ""

    pb.println("message printed :)")
    pb.inc(2)
    assert (
        in_mem.contents()
        == """
message printed :)
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
            """.strip()
    )


def test_ticker_drop():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    for i in range(5):
        spinner = mp.add(
            ProgressBar.new_spinner()
            .with_finish(ProgressFinish.AndLeave())
            .with_message(f"doing stuff {i}"),
        )
        spinner.enable_steady_tick(timedelta(milliseconds=100))

    del spinner

    assert (
        in_mem.contents()
        == "  doing stuff 0\n  doing stuff 1\n  doing stuff 2\n  doing stuff 3\n  doing stuff 4"
    )


def test_manually_inc_ticker():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    spinner = mp.add(ProgressBar.new_spinner().with_message("msg"))

    assert in_mem.contents() == ""

    spinner.inc(1)
    assert in_mem.contents() == "⠁ msg"

    spinner.inc(1)
    assert in_mem.contents() == "⠉ msg"

    # set_message / set_prefix shouldn't increase tick
    spinner.message = "new message"
    spinner.prefix = "prefix"
    assert in_mem.contents() == "⠉ new message"


def test_multi_progress_prune_zombies():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb0 = mp.add(ProgressBar(10)).with_finish(ProgressFinish.AndLeave())
    pb1 = mp.add(ProgressBar(15))
    pb0.tick()
    assert (
        in_mem.contents()
        == "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"
    )

    pb0.inc(1)
    assert (
        in_mem.contents()
        == "███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/10"
    )

    del pb0

    # Clear the screen
    mp.clear()

    # Write a line that we expect to remain. This helps ensure the adjustment to last_line_count is
    # working as expected, and `MultiState` isn't erasing lines when it shouldn't.
    in_mem.write_line("don't erase me plz")

    # pb0 is dead, so only pb1 should be drawn from now on
    pb1.tick()
    assert (
        in_mem.contents()
        == "don't erase me plz\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/15"
    )


def test_multi_progress_prune_zombies_2():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10).with_finish(ProgressFinish.AndLeave()))
    pb2 = mp.add(ProgressBar(5))
    pb3 = mp.add(ProgressBar(100)).with_finish(ProgressFinish.Abandon())
    pb4 = mp.add(ProgressBar(500)).with_finish(ProgressFinish.AndLeave())
    pb5 = mp.add(ProgressBar(7))

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == """░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"""
    )

    pb2.tick()

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5""".lstrip()
    )

    pb3.tick()
    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/5
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100""".lstrip()
    )

    del pb1
    del pb2
    del pb3

    assert (
        in_mem.contents()
        == """
██████████████████████████████████████████████████████████████████████████ 10/10
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100""".lstrip()
    )

    mp.clear()

    assert in_mem.contents() == ""

    # A sacrificial line we expect shouldn't be touched
    in_mem.write_line("don't erase plz")

    mp.println("Test friend :)")
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)""".lstrip()
    )

    pb4.tick()
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/500""".lstrip()
    )

    del pb4
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
████████████████████████████████████████████████████████████████████████ 500/500""".lstrip()
    )

    mp.clear()
    assert in_mem.contents() == "don't erase plz\nTest friend :)"

    pb5.tick()
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/7""".lstrip()
    )

    mp.println("not your friend, buddy")
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
not your friend, buddy
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/7""".lstrip()
    )

    pb5.inc(1)
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
not your friend, buddy
██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/7""".lstrip()
    )

    mp.clear()
    in_mem.write_line("don't erase me either")

    pb5.inc(1)
    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
not your friend, buddy
don't erase me either
█████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/7""".lstrip()
    )

    del pb5

    assert (
        in_mem.contents()
        == """
don't erase plz
Test friend :)
not your friend, buddy
don't erase me either""".lstrip()
    )


def test_basic_tab_expansion():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    spinner = mp.add(ProgressBar.new_spinner().with_message("Test\t:)"))
    spinner.tick()

    # 8 is the default number of spaces
    assert in_mem.contents() == "⠁ Test        :)"

    spinner.set_tab_width(4)
    assert in_mem.contents() == "⠁ Test    :)"


def test_tab_expansion_in_template():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    spinner = mp.add(
        ProgressBar.new_spinner()
        .with_message("Test\t:)")
        .with_prefix("Pre\tfix!")
        .with_style(ProgressStyle(template="{spinner}{prefix}\t{msg}")),
    )

    spinner.tick()
    assert in_mem.contents() == "⠁Pre        fix!        Test        :)"

    spinner.set_tab_width(4)
    assert in_mem.contents() == "⠁Pre    fix!    Test    :)"

    spinner.set_tab_width(2)
    assert in_mem.contents() == "⠁Pre  fix!  Test  :)"


def test_progress_style_tab_width_unification():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    # Style will have default of 8 spaces for tabs
    style = ProgressStyle(template="{msg}\t{msg}")

    spinner = mp.add(
        ProgressBar.new_spinner().with_message("OK").with_tab_width(4),
    )

    # Setting the spinner's style to |style| should override the style's tab width with that of bar
    spinner.style = style
    spinner.tick()
    assert in_mem.contents() == "OK    OK"


def test_multi_progress_clear_println():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    mp.println("Test of println")
    # Should have no effect
    mp.clear()
    assert in_mem.contents() == "Test of println"


# In the old (broken) implementation, zombie handling sometimes worked differently depending on
# how many draws were between certain operations. Let's make sure that doesn't happen again.
def _multi_progress_clear_zombies(ticks: int):
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))
    style = ProgressStyle(template="{msg}")

    pb1 = mp.add(
        ProgressBar.new_spinner().with_style(style).with_message("pb1"),
    )
    pb1.tick()

    pb2 = mp.add(
        ProgressBar.new_spinner().with_style(style).with_message("pb2"),
    )

    pb2.tick()
    assert in_mem.contents() == "pb1\npb2"

    pb1.finish_with_message("pb1 done")
    del pb1
    assert in_mem.contents() == "pb1 done\npb2"

    for _ in range(ticks):
        pb2.tick()

    mp.clear()
    assert in_mem.contents() == ""


def test_multi_progress_clear_zombies_no_ticks():
    _multi_progress_clear_zombies(0)


def test_multi_progress_clear_zombies_one_tick():
    _multi_progress_clear_zombies(1)


def test_multi_progress_clear_zombies_two_ticks():
    _multi_progress_clear_zombies(2)


# This test reproduces examples/multi.rs in a simpler form
#
def test_multi_zombie_handling():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))
    style = ProgressStyle(template="{msg}")

    pb1 = mp.add(
        ProgressBar.new_spinner().with_style(style).with_message("pb1"),
    )
    pb1.tick()
    pb2 = mp.add(
        ProgressBar.new_spinner().with_style(style).with_message("pb2"),
    )
    pb2.tick()
    pb3 = mp.add(
        ProgressBar.new_spinner().with_style(style).with_message("pb3"),
    )
    pb3.tick()

    mp.println("pb1 done!")
    pb1.finish_with_message("done")
    assert in_mem.contents() == "pb1 done!\ndone\npb2\npb3"
    del pb1

    assert in_mem.contents() == "pb1 done!\ndone\npb2\npb3"

    pb2.tick()
    assert in_mem.contents() == "pb1 done!\ndone\npb2\npb3"
    pb3.tick()
    assert in_mem.contents() == "pb1 done!\ndone\npb2\npb3"

    mp.println("pb3 done!")
    assert in_mem.contents() == "pb1 done!\npb3 done!\npb2\npb3"

    pb3.finish_with_message("done")
    del pb3

    pb2.tick()

    mp.println("pb2 done!")
    pb2.finish_with_message("done")
    del pb2

    assert in_mem.contents() == "pb1 done!\npb3 done!\npb2 done!\ndone\ndone"

    mp.clear()

    assert in_mem.contents() == "pb1 done!\npb3 done!\npb2 done!"


def test_multi_progress_multiline_msg():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar.new_spinner().with_message("test1"))
    pb2 = mp.add(ProgressBar.new_spinner().with_message("test2"))

    assert in_mem.contents() == ""

    pb1.inc(1)
    pb2.inc(1)

    assert (
        in_mem.contents()
        == """
⠁ test1
⠁ test2
            """.strip()
    )

    pb1.message = "test1\n  test1 line2\n  test1 line3"

    assert (
        in_mem.contents()
        == """
⠁ test1
  test1 line2
  test1 line3
⠁ test2
            """.strip()
    )

    pb1.inc(1)
    pb2.inc(1)

    assert (
        in_mem.contents()
        == """
⠉ test1
  test1 line2
  test1 line3
⠉ test2
            """.strip()
    )

    pb2.message = "test2\n  test2 line2"

    assert (
        in_mem.contents()
        == """
⠉ test1
  test1 line2
  test1 line3
⠉ test2
  test2 line2
            """.strip()
    )

    pb1.message = "single line again"

    assert (
        in_mem.contents()
        == """
⠉ single line again
⠉ test2
  test2 line2
            """.strip()
    )

    pb1.finish_with_message("test1 done!")
    pb2.finish_with_message("test2 done!")

    assert (
        in_mem.contents()
        == """  test1 done!
  test2 done!"""
    )


def test_multi_progress_bottom_alignment():
    in_mem = InMemoryTerm(10, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))
    mp.set_alignment(MultiProgressAlignment.Bottom)

    pb1 = mp.add(ProgressBar.new_spinner().with_message("test1"))
    pb2 = mp.add(ProgressBar.new_spinner().with_message("test2"))

    pb1.tick()
    pb2.tick()
    pb1.finish_and_clear()

    assert in_mem.contents() == "\n⠁ test2"

    pb2.finish_and_clear()
    # `InMemoryTerm.contents` normally gets rid of trailing newlines, so write some text to ensure
    # the newlines are seen.
    in_mem.write_line("anchor")
    assert in_mem.contents() == "\n\nanchor"


def test_progress_bar_terminal_wrap():
    in_mem = InMemoryTerm(10, 20)

    downloaded = 0
    total_size = 231231231

    pb = ProgressBar.with_draw_target(
        None,
        ProgressDrawTarget.term_like(in_mem),
    )
    pb.style = (
        ProgressStyle.default_bar()
        .template(
            "{msg:>12.cyan.bold} {spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {bytes}/{total_bytes}"
        )
        .progress_chars(">-")
    )

    pb.message = "Downloading"
    assert (
        in_mem.contents()
        == """ Downloading ⠁ [00:0
0:00] [-------------
--------------------
-------] 0 B/0 B"""
    )

    new = min(downloaded + 223211, total_size)
    downloaded = new
    pb.position = new
    assert (
        in_mem.contents()
        == """ Downloading ⠁ [00:0
0:00] [-------------
--------------------
-------] 217.98 KiB/
217.98 KiB"""
    )

    new = min(downloaded + 223211, total_size)
    pb.position = new
    assert (
        in_mem.contents()
        == """ Downloading ⠉ [00:0
0:00] [-------------
--------------------
-------] 435.96 KiB/
435.96 KiB"""
    )

    pb.style = ProgressStyle.default_bar().template(
        "{msg:>12.green.bold} downloading {total_bytes:.green} in {elapsed:.green}"
    )
    pb.finish_with_message("Finished")
    assert (
        in_mem.contents()
        == """    Finished downloa
ding 435.96 KiB in 0
s"""
    )


def test_spinner_terminal_cleared_log_line_with_ansi_codes():
    in_mem = InMemoryTerm(10, 100)

    pb = ProgressBar.with_draw_target(
        10,
        ProgressDrawTarget.term_like(in_mem),
    )
    pb.style = ProgressStyle.default_spinner()
    assert in_mem.contents() == ""

    pb.finish_and_clear()
    # Visually empty, but consists of an ANSII code
    pb.println("\u001b[1m")

    pb.println("text\u001b[0m")
    assert in_mem.contents() == "\ntext"


def test_multi_progress_println_terminal_wrap():
    in_mem = InMemoryTerm(10, 48)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10))
    pb2 = mp.add(ProgressBar(5))
    pb3 = mp.add(ProgressBar(100))

    assert in_mem.contents() == ""

    pb1.inc(2)
    mp.println("message printed that is longer than terminal width :)")

    assert (
        in_mem.contents()
        == """message printed that is longer than terminal wid
th :)
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10"""
    )

    mp.println("another great message!")
    assert (
        in_mem.contents()
        == """message printed that is longer than terminal wid
th :)
another great message!
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10"""
    )

    pb2.inc(1)
    pb3.tick()
    mp.println("one last message but this one is also longer than terminal width")

    assert (
        in_mem.contents()
        == """message printed that is longer than terminal wid
th :)
another great message!
one last message but this one is also longer tha
n terminal width
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/10
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/5
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/100""".strip()
    )

    del pb1
    del pb2
    del pb3

    assert (
        in_mem.contents()
        == """message printed that is longer than terminal wid
th :)
another great message!
one last message but this one is also longer tha
n terminal width""".strip()
    )


def test_basic_progress_bar_newline():
    in_mem = InMemoryTerm(10, 80)
    pb = ProgressBar.with_draw_target(
        10,
        ProgressDrawTarget.term_like(in_mem),
    )

    assert in_mem.contents() == ""

    pb.println("\nhello")
    pb.tick()
    assert (
        in_mem.contents()
        == """
hello
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"""
    )

    pb.inc(1)
    pb.println("")
    assert (
        in_mem.contents()
        == """
hello

███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1/10"""
    )

    pb.finish()
    assert (
        in_mem.contents()
        == """
hello

██████████████████████████████████████████████████████████████████████████ 10/10"""
    )


# @pytest.mark.xfail
def test_multi_progress_many_bars():
    in_mem = InMemoryTerm(4, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10).with_finish(ProgressFinish.AndLeave()))

    spinners = [
        mp.add(ProgressBar.new_spinner().with_message(str(i))) for i in range(7)
    ]

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == """░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"""
    )
    assert (
        in_mem.moves_since_last_check()
        == """Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
Flush
"""
    )

    for spinner in spinners:
        spinner.tick()

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
⠁ 0
⠁ 1
⠁ 2""".lstrip()
    )
    assert (
        in_mem.moves_since_last_check()
        == """Clear
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("                                                                             ")
Flush
Up(1)
Clear
Down(1)
Clear
Up(1)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("                                                                             ")
Flush
Up(2)
Clear
Down(1)
Clear
Down(1)
Clear
Up(2)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Str("                                                                             ")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
"""
    )

    del pb1
    assert (
        in_mem.contents()
        == """
██████████████████████████████████████████████████████████████████████████ 10/10
⠁ 0
⠁ 1
⠁ 2""".lstrip()
    )
    assert (
        in_mem.moves_since_last_check()
        == """Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("██████████████████████████████████████████████████████████████████████████ 10/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
"""
    )

    # Note: we call finish_using_style since `del spinners` appears to not finish all spinners
    for spinner in spinners:
        spinner.finish_using_style()

    del spinners

    assert in_mem.contents() == ""
    assert (
        in_mem.moves_since_last_check()
        == """Up(2)
Clear
Down(1)
Clear
Down(1)
Clear
Up(2)
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Str("")
NewLine
Str("⠁ 3")
Str("")
NewLine
Str("⠁ 4")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("⠁ 2")
Str("")
NewLine
Str("⠁ 3")
Str("")
NewLine
Str("⠁ 4")
Str("")
NewLine
Str("⠁ 5")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("⠁ 3")
Str("")
NewLine
Str("⠁ 4")
Str("")
NewLine
Str("⠁ 5")
Str("")
NewLine
Str("⠁ 6")
Str("                                                                             ")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("⠁ 4")
Str("")
NewLine
Str("⠁ 5")
Str("")
NewLine
Str("⠁ 6")
Str("                                                                             ")
Flush
Up(2)
Clear
Down(1)
Clear
Down(1)
Clear
Up(2)
Str("⠁ 5")
Str("")
NewLine
Str("⠁ 6")
Str("                                                                             ")
Flush
Up(1)
Clear
Down(1)
Clear
Up(1)
Str("⠁ 6")
Str("                                                                             ")
Flush
Clear
Flush
"""
    )


def test_multi_progress_many_spinners():
    in_mem = InMemoryTerm(4, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb1 = mp.add(ProgressBar(10).with_finish(ProgressFinish.AndLeave()))

    spinners = [
        mp.add(ProgressBar.new_spinner().with_message(str(i))) for i in range(7)
    ]

    assert in_mem.contents() == ""

    pb1.tick()
    assert (
        in_mem.contents()
        == """░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"""
    )
    assert (
        in_mem.moves_since_last_check()
        == """Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
Flush
"""
    )

    for spinner in spinners:
        spinner.tick()

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
⠁ 0
⠁ 1
⠁ 2""".lstrip()
    )

    assert (
        in_mem.moves_since_last_check()
        == """Clear
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("                                                                             ")
Flush
Up(1)
Clear
Down(1)
Clear
Up(1)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("                                                                             ")
Flush
Up(2)
Clear
Down(1)
Clear
Down(1)
Clear
Up(2)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Str("                                                                             ")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
"""
    )

    spinners.pop(3)

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
⠁ 0
⠁ 1
⠁ 2""".lstrip()
    )

    assert (
        in_mem.moves_since_last_check()
        == """Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
"""
    )

    spinners.pop(4)

    assert (
        in_mem.contents()
        == """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10
⠁ 0
⠁ 1
⠁ 2""".lstrip()
    )
    assert (
        in_mem.moves_since_last_check()
        == """Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 0")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Flush
"""
    )

    for spinner in spinners:
        spinner.finish_using_style()

    del spinners

    assert (
        in_mem.contents()
        == """░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10"""
    )
    assert (
        in_mem.moves_since_last_check()
        == """Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 1")
Str("")
NewLine
Str("⠁ 2")
Str("")
NewLine
Str("⠁ 4")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 2")
Str("")
NewLine
Str("⠁ 4")
Str("")
NewLine
Str("⠁ 6")
Str("                                                                             ")
Flush
Up(3)
Clear
Down(1)
Clear
Down(1)
Clear
Down(1)
Clear
Up(3)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 4")
Str("")
NewLine
Str("⠁ 6")
Str("                                                                             ")
Flush
Up(2)
Clear
Down(1)
Clear
Down(1)
Clear
Up(2)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
NewLine
Str("⠁ 6")
Str("                                                                             ")
Flush
Up(1)
Clear
Down(1)
Clear
Up(1)
Str("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0/10")
Str("")
Flush
"""
    )


def test_orphan_lines():
    in_mem = InMemoryTerm(10, 80)

    pb = ProgressBar.with_draw_target(
        10,
        ProgressDrawTarget.term_like(in_mem),
    )
    assert in_mem.contents() == ""

    for i in range(11):
        if i != 0:
            pb.inc(1)

        n = 5 + i

        pb.println("\n" * n)

    pb.finish()


def test_orphan_lines_message_above_progress_bar():
    in_mem = InMemoryTerm(10, 80)

    pb = ProgressBar.with_draw_target(
        10,
        ProgressDrawTarget.term_like(in_mem),
    )

    orphan_lines_message_above_progress_bar_test(pb, in_mem)


def test_orphan_lines_message_above_multi_progress_bar():
    in_mem = InMemoryTerm(10, 80)

    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))

    pb = mp.add(ProgressBar(10))

    orphan_lines_message_above_progress_bar_test(pb, in_mem)


def orphan_lines_message_above_progress_bar_test(pb: ProgressBar, in_mem: InMemoryTerm):
    assert in_mem.contents() == ""

    for i in range(11):
        if i != 0:
            pb.inc(1)

        n = 5 + i

        # Test with messages of differing numbers of lines. The messages have the form:
        # n - 1 newlines followed by n * 11 dashes (`-`). The value of n ranges from 5
        # (less than the terminal height) to 15 (greater than the terminal height). The
        # number 11 is intentionally not a factor of the terminal width (80), but large
        # enough that the strings of dashes eventually wrap.
        pb.println("{}{}".format("\n" * (n - 1), "-" * (n * 11)))

        # Check that the line above the progress bar is a string of dashes of length
        # n * 11 mod the terminal width.
        assert "-" * (n * 11 % 80) == in_mem.contents().splitlines()[-2]

    pb.finish()


# Test proper wrapping of the text lines before a bar is added. #447 on github.


def test_barless_text_wrapping():
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec viverra massa. Nunc nisl lectus, auctor in lorem eu, maximus elementum est."

    in_mem = InMemoryTerm(40, 80)
    mp = MultiProgress.with_draw_target(ProgressDrawTarget.term_like(in_mem))
    assert in_mem.contents() == ""

    for _ in range(2):
        # This is primordial. The bug came from writing multiple text lines in a row on different ticks.
        mp.println(lorem)
        time.sleep(0.1)

    assert (
        in_mem.contents()
        == """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec viverra massa
. Nunc nisl lectus, auctor in lorem eu, maximus elementum est.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec viverra massa
. Nunc nisl lectus, auctor in lorem eu, maximus elementum est."""
    )
