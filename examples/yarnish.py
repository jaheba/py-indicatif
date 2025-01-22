import random
import time
from threading import Thread

from indicatif import MultiProgress, ProgressBar, ProgressStyle
from indicatif.console import Emoji, style

PACKAGES = [
    "fs-events",
    "my-awesome-module",
    "emoji-speaker",
    "wrap-ansi",
    "stream-browserify",
    "acorn-dynamic-import",
]

COMMANDS = [
    "cmake .",
    "make",
    "make clean",
    "gcc foo.c -o foo",
    "gcc bar.c -o bar",
    "./helper.sh rebuild-cache",
    "make all-clean",
    "make test",
]

LOOKING_GLASS = Emoji("🔍  ", "")
TRUCK = Emoji("🚚  ", "")
CLIP = Emoji("🔗  ", "")
PAPER = Emoji("📃  ", "")
SPARKLE = Emoji("✨ ", ":-)")


spinner_style = ProgressStyle(
    template="{prefix:.bold.dim} {spinner} {wide_msg}",
    tick_chars="⠁⠂⠄⡀⢀⠠⠐⠈ ",
)

start = time.time()

print(f'{style("[1/4]", bold=True, dim=True)} {LOOKING_GLASS}Resolving packages...')
print(f'{style("[2/4]", bold=True, dim=True)} {TRUCK}Fetching packages...')
print(f'{style("[3/4]", bold=True, dim=True)} {CLIP}Linking dependencies...')

deps = 1232
pb = ProgressBar(deps)
for _ in range(deps):
    time.sleep(0.003)
    pb.inc(1)

pb.finish_and_clear()

print(f'{style("[3/4]", bold=True, dim=True)} {PAPER}Building fresh packages.....')


def worker(pb):
    pkg = random.choice(PACKAGES)
    for _ in range(count):
        cmd = random.choice(COMMANDS)
        time.sleep(random.uniform(25, 200) / 1000)
        pb.message = f"{pkg}: {cmd}"
        pb.inc(1)

    pb.finish("waiting...")


multi_progress = MultiProgress()


handles = []
for i in range(4):
    count = random.randrange(30, 80)
    pb = multi_progress.add(
        ProgressBar(
            count,
            style=spinner_style,
            prefix=f"[{ i + 1}/?]",
        )
    )

    handle = Thread(target=worker, args=(pb,))
    handle.start()
    handles.append(handle)


for handle in handles:
    handle.join()


multi_progress.clear()

elapsed = time.time() - start

print(f"{SPARKLE} Done in {elapsed:.2f}s")
