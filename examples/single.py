import time

from indicatif import ProgressBar


def main():
    pb = ProgressBar(256)

    for _ in range(256):
        time.sleep(0.005)
        pb.inc(1)

    pb.finish()


if __name__ == "__main__":
    main()
