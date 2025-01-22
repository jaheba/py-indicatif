import time

from indicatif import ProgressBar, ProgressStyle


downloaded = 69369369
total_size = 231231231

pb = ProgressBar(
    total_size,
    style=ProgressStyle(
        template="{spinner:.green} [{wide_bar:.cyan/blue}] {bytes}/{total_bytes} ({eta})",
        progress_chars="#>-",
    ),
)

pb.position = downloaded
pb.reset_eta()

while downloaded < total_size:
    downloaded = min(downloaded + 123211, total_size)
    pb.position = downloaded
    time.sleep(0.012)

pb.finish("downloaded")
