#!/usr/bin/env python3
"""Download 1h candles + funding of every USDT-M perpetual listed since --since from
data.binance.vision (works where fapi.binance.com is blocked). Output: research_lowcap/cache/."""

import argparse
import concurrent.futures as cf
import io
import json
import os
import time
import xml.etree.ElementTree as ET
import zipfile

import numpy as np
import requests

LIST = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
DL = "https://data.binance.vision/"
NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
S = requests.Session()


def get(url, **kw):
    for a in range(6):
        try:
            r = S.get(url, timeout=60, **kw)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(2 ** a)
    return None


def listing(prefix, marker="", folders=False):
    out = []
    while True:
        params = {"prefix": prefix, "marker": marker}
        if folders:
            params["delimiter"] = "/"
        root = ET.fromstring(get(LIST, params=params).content)
        if folders:
            page = [p.findtext("s3:Prefix", namespaces=NS) for p in root.findall("s3:CommonPrefixes", NS)]
        else:
            page = [c.findtext("s3:Key", namespaces=NS) for c in root.findall("s3:Contents", NS)]
        out += page
        if root.findtext("s3:IsTruncated", namespaces=NS) != "true" or not page:
            return out
        marker = root.findtext("s3:NextMarker", namespaces=NS) or page[-1]


def rows(key):
    r = get(DL + key)
    if r is None:
        return []
    z = zipfile.ZipFile(io.BytesIO(r.content))
    return [x.split(",") for x in z.read(z.namelist()[0]).decode().strip().splitlines() if x and x[0].isdigit()]


def first_day(sym):
    ks = [k for k in listing(f"data/futures/um/daily/klines/{sym}/1d/") if k.endswith(".zip")]
    return sym, (min(k.split("-1d-")[1][:10] for k in ks) if ks else None)


def fetch(sym):
    path = os.path.join(OUT, sym + ".npz")
    if os.path.exists(path):
        return
    mk = sorted(k for k in listing(f"data/futures/um/monthly/klines/{sym}/1h/") if k.endswith(".zip"))
    last = mk[-1].split("-1h-")[1][:7] if mk else ""
    dp = f"data/futures/um/daily/klines/{sym}/1h/"
    dk = sorted(k for k in listing(dp, f"{dp}{sym}-1h-{last}-99" if last else "")
                if k.endswith(".zip") and k.split("-1h-")[1][:7] > last)
    kl = {}
    for k in mk + dk:
        for r in rows(k):
            kl[int(r[0])] = (float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[7]))
    fr = {}
    for k in sorted(k for k in listing(f"data/futures/um/monthly/fundingRate/{sym}/") if k.endswith(".zip")):
        for r in rows(k):
            fr[int(r[0])] = float(r[2])
    if not kl:
        return
    t = np.array(sorted(kl), dtype=np.int64)
    a = np.array([kl[x] for x in t])
    ft = np.array(sorted(fr), dtype=np.int64)
    np.savez_compressed(path + ".tmp.npz", t=t, o=a[:, 0], h=a[:, 1], l=a[:, 2], c=a[:, 3], qv=a[:, 4],
                        ft=ft, fr=np.array([fr[x] for x in ft]))
    os.replace(path + ".tmp.npz", path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since", default="2024-01-01", help="first listing date to include")
    p.add_argument("--until", default="2099-01-01")
    p.add_argument("--workers", type=int, default=16)
    args = p.parse_args()
    os.makedirs(OUT, exist_ok=True)
    syms = sorted(x.split("/")[-2] for x in listing("data/futures/um/daily/klines/", folders=True))
    syms = [s for s in syms if s.endswith("USDT")]
    with cf.ThreadPoolExecutor(args.workers) as ex:
        days = dict(ex.map(first_day, syms))
    with open(os.path.join(OUT, "listing.json"), "w") as f:
        json.dump(days, f, indent=0)
    todo = [s for s, d in days.items() if d and args.since <= d <= args.until]
    print(f"{len(todo)} perpetuals listed {args.since} .. {args.until}")
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for i, _ in enumerate(ex.map(fetch, todo), 1):
            if i % 50 == 0:
                print(i, "/", len(todo), flush=True)


if __name__ == "__main__":
    main()
