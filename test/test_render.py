from indicatif import InMemoryTerm
from indicatif._indicatif import ProgressBar, ProgressDrawTarget


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
