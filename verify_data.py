#!/usr/bin/env python3
"""Check every data/<SYMBOL>/<SYMBOL>_<interval>.csv.gz for gaps, duplicates and ordering."""

import csv
import glob
import gzip
import os
import sys
from datetime import datetime, timezone

from binance_futures_collector import INTERVAL_MS


def fmt(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")


def check(path):
    interval = os.path.basename(path).rsplit("_", 1)[1].split(".")[0]
    step = INTERVAL_MS[interval]
    rows = dups = 0
    gaps = []
    first = prev = None
    with gzip.open(path, "rt", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            t = int(row[1])
            rows += 1
            if prev is None:
                first = t
            elif t <= prev:
                dups += 1
                continue
            elif t != prev + step:
                gaps.append((prev, t))
            prev = t
    missing = sum((b - a) // step - 1 for a, b in gaps)
    return interval, rows, first, prev, dups, gaps, missing


def main(data_dir="data"):
    ok = True
    print(f"{'file':<28}{'rows':>9}  {'first':<17} {'last':<17} gaps(missing candles)")
    for path in sorted(glob.glob(os.path.join(data_dir, "*", "*.csv.gz"))):
        interval, rows, first, last, dups, gaps, missing = check(path)
        note = f"{len(gaps)} ({missing})"
        if dups:
            note += f"  DUPLICATES/UNORDERED: {dups}"
            ok = False
        print(f"{os.path.basename(path):<28}{rows:>9}  {fmt(first):<17} {fmt(last):<17} {note}")
        for a, b in gaps[:3]:
            print(f"{'':<30}gap {fmt(a)} -> {fmt(b)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
