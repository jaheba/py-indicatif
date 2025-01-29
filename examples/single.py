import time

from indicatif import ProgressBar


pb = ProgressBar(256)

for _ in range(256):
    time.sleep(0.005)
    pb.inc(1)

pb.finish()
