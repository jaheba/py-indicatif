from indicatif import ProgressBar


def many_units_of_easy_work(n: int, label: str):
    pb = ProgressBar(n)

    sum = 0
    for i in range(n):
        # Any quick computation, followed by an update to the progress bar.
        sum += 2 * i + 3
        pb.inc(1)

    pb.finish()

    print(f"[{label}] Sum ({sum}) calculated in {pb.elapsed().total_seconds():.2f}s")


N = 1 << 20
# Perform a long sequence of many simple computations monitored by a
# default progress bar.
many_units_of_easy_work(N, "Default progress bar ")
