import random
import time
from threading import Thread

from multiprocessing.pool import ThreadPool

from queue import Empty, Queue

from indicatif import ProgressBar, ProgressStyle, console


CRATES = [
    ("console", "v0.14.1"),
    ("lazy_static", "v1.4.0"),
    ("libc", "v0.2.93"),
    ("regex", "v1.4.6"),
    ("regex-syntax", "v0.6.23"),
    ("terminal_size", "v0.1.16"),
    ("libc", "v0.2.93"),
    ("unicode-width", "v0.1.8"),
    ("lazy_static", "v1.4.0"),
    ("number_prefix", "v0.4.0"),
    ("regex", "v1.4.6"),
    ("rand", "v0.8.3"),
    ("getrandom", "v0.2.2"),
    ("cfg-if", "v1.0.0"),
    ("libc", "v0.2.93"),
    ("rand_chacha", "v0.3.0"),
    ("ppv-lite86", "v0.2.10"),
    ("rand_core", "v0.6.2"),
    ("getrandom", "v0.2.2"),
    ("rand_core", "v0.6.2"),
    ("tokio", "v1.5.0"),
    ("bytes", "v1.0.1"),
    ("pin-project-lite", "v0.2.6"),
    ("slab", "v0.4.3"),
    ("indicatif", "v0.15.0"),
]


def compile_crate(thread_no: int, input: Queue, output: Queue):
    while True:
        try:
            name, version = input.get_nowait()
        except Empty:
            output.put((thread_no, None, None))
            return

        # inform that crate is being compiled
        output.put((thread_no, name, version))

        if name == CRATES[-1][0]:
            time.sleep(random.uniform(1, 2))
        else:
            time.sleep(random.uniform(0.25, 1))


compiling = console.style(f"{'Compiling':>12}", fg="green", bold=True)
finished = console.style(f"{'Finished':>12}", fg="green", bold=True)


def main():
    NUM_CPUS = 4

    start = time.time()

    # mimic cargo progress bar although it behaves a bit different
    pb = ProgressBar(
        length=len(CRATES),
        prefix="Building",
        style=ProgressStyle(
            template="{prefix:>12.cyan.bold} [{bar:57}] {pos}/{len} {wide_msg}",
            progress_chars="=> ",
        ),
    )

    # setup channels
    input_queue = Queue()
    output_queue = Queue()

    for crate in CRATES:
        input_queue.put(crate)

    with ThreadPool(NUM_CPUS) as pool:
        processing = [None] * NUM_CPUS

        for thread_no in range(NUM_CPUS):
            pool.apply_async(compile_crate, args=(thread_no, input_queue, output_queue))

        finished = 0
        while finished < NUM_CPUS:
            thread_n, name, version = output_queue.get()
            processing[thread_n] = name
            pb.message = ", ".join(filter(None, processing))

            if name is None:
                finished += 1
            else:
                pb.println(f"{compiling} {name} {version}")
                pb.inc(1)

        pool.join()

    pb.finish_and_clear()
    elapsed = time.time() - start
    print(f"{finished} dev [unoptimized + debuginfo] target(s) in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
