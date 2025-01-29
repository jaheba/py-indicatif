# py-indicatif

`py-indicatif` provides bindings for Rust's [`indicatif`](https://github.com/console-rs/indicatif) library.

Install:

```sh
$ pip install py-indicatif
```

Usage:

```py
from indicatif import ProgressBar


pb = ProgressBar(256)

for _ in range(256):
    time.sleep(0.005)
    pb.inc(1)

pb.finish()
```
