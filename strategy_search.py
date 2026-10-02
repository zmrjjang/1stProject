#!/usr/bin/env python3
"""Run the endless strategy search (see STRATEGY_LAB.md).

    python strategy_search.py                 # run forever (Ctrl+C to stop, resumes later)
    python strategy_search.py --hours 5.5     # stop after 5.5 hours (used by GitHub Actions)
"""

import argparse
import logging
import os
import sys

from lab.search import Search


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--hours", type=float, default=0, help="time limit in hours (0 = forever)")
    p.add_argument("--workers", type=int, default=0, help="worker processes (0 = all cores)")
    p.add_argument("--push", action="store_true", help="git commit + push each discovery immediately")
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()
    root = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(os.path.join(root, "research", "search.log"))])
    Search(root, args.workers, args.hours, args.push, args.seed).run()


if __name__ == "__main__":
    main()
