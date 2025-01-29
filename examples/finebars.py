import random
import time
from indicatif import MultiProgress, ProgressBar, ProgressStyle
from threading import Thread

styles = [
    ("Rough bar:", "█  ", "red"),
    ("Fine bar: ", "█▉▊▋▌▍▎▏  ", "yellow"),
    ("Vertical: ", "█▇▆▅▄▃▂▁  ", "green"),
    ("Fade in:  ", "█▓▒░  ", "blue"),
    ("Blocky:   ", "█▛▌▖  ", "magenta"),
]

multi_progress = MultiProgress()


def worker(pb):
    wait = random.uniform(0.01, 0.03)

    for i in range(512):
        time.sleep(wait)
        pb.inc(1)
        pb.message = f"{int(100 * i / 512):3d}%"

    pb.finish("100%")


handles = []

for prefix, progress_chars, colour in styles:
    pb = multi_progress.add(
        ProgressBar(
            512,
            style=ProgressStyle(
                template=f"{{prefix:.bold}}▕{{bar:.{colour}}}▏{{msg}}",
                progress_chars=progress_chars,
            ),
            prefix=prefix,
        )
    )

    handle = Thread(target=worker, args=(pb,))
    handle.start()
    handles.append(handle)


for handle in handles:
    handle.join()
