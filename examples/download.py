import time

from indicatif import ProgressBar, ProgressStyle


downloaded = 0
total_size = 231231231

pb = ProgressBar(
    total_size,
    style=ProgressStyle(
        template="{spinner:.green} [{elapsed_precise}] [{wide_bar:.cyan/blue}] {bytes}/{total_bytes} ({eta})",
        progress_chars="#>-",
    ),
)

while downloaded < total_size:
    downloaded = min(downloaded + 223211, total_size)
    pb.position = downloaded
    time.sleep(0.012)


pb.finish("downloaded")
