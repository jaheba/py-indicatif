import random
import time
from threading import Thread

from indicatif import MultiProgress, ProgressBar, ProgressStyle


def worker_1(pb, n):
    for i in range(n):
        time.sleep(0.015)

        if i == n / 3:
            time.sleep(2)

        pb.inc(1)

    pb.finish("all jobs started")


def worker_2(pb, n):
    def step():
        time.sleep(random.uniform(1.0, 5.0))
        pb.inc(1)

    threads = [Thread(target=step) for _ in range(n)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def worker_3(pb, n):
    for i in range(n):
        time.sleep(0.002)

        pb.message = f"item #{i + 1}"
        pb.inc(1)


def main():
    multi_progress = MultiProgress()

    style = ProgressStyle(
        template="[{elapsed_precise}] {bar:40.cyan/blue} {pos:>7}/{len:7} {msg}",
        progress_chars="##-",
    )

    n = 200
    pb1 = multi_progress.add(
        ProgressBar(
            n,
            style=style,
            message="first",
        )
    )
    pb3 = multi_progress.add(ProgressBar(n, style=style, message="third"))

    pb2 = multi_progress.insert_after(
        pb1, ProgressBar(n, style=style, message="second")
    )

    threads = [
        Thread(target=worker_1, args=(pb1, n)),
        Thread(target=worker_2, args=(pb2, n)),
        Thread(target=worker_3, args=(pb3, n)),
    ]

    multi_progress.println("starting!")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
