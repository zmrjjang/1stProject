#!/usr/bin/env python3
"""Download 1h candles + 1h premium index (since 2024-01) of every USDT-M perpetual that is still
trading, from data.binance.vision. Output: research_pump/cache/ (about 600MB, 20-30 minutes)."""

import requests, xml.etree.ElementTree as ET, json, time, io, zipfile, os, concurrent.futures as cf
import numpy as np
LIST = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"; DL = "https://data.binance.vision/"
NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
S = requests.Session()
def get(url, **kw):
    for a in range(6):
        try:
            r = S.get(url, timeout=60, **kw)
            if r.status_code == 200: return r
            if r.status_code == 404: return None
        except Exception: pass
        time.sleep(2 ** a)
def keys(prefix, marker=""):
    out = []
    while True:
        root = ET.fromstring(get(LIST, params={"prefix": prefix, "marker": marker}).content)
        page = [c.findtext("s3:Key", namespaces=NS) for c in root.findall("s3:Contents", NS)]
        out += [k for k in page if k.endswith(".zip")]
        if root.findtext("s3:IsTruncated", namespaces=NS) != "true" or not page: return out
        marker = page[-1]
def rows(key):
    r = get(DL + key)
    if r is None: return []
    z = zipfile.ZipFile(io.BytesIO(r.content))
    return [x.split(",") for x in z.read(z.namelist()[0]).decode().strip().splitlines() if x and x[0].isdigit()]
def series(kind, sym, since="2024-01"):
    mp = f"data/futures/um/monthly/{kind}/{sym}/1h/"
    mk = sorted(k for k in keys(mp, f"{mp}{sym}-1h-{since}") if k.split("-1h-")[1][:7] >= since)
    last = mk[-1].split("-1h-")[1][:7] if mk else ""
    dp = f"data/futures/um/daily/{kind}/{sym}/1h/"
    dk = sorted(k for k in keys(dp, f"{dp}{sym}-1h-{last}-99" if last else f"{dp}{sym}-1h-{since}") if k.split("-1h-")[1][:7] > last)
    out = {}
    for k in mk + dk:
        for r in rows(k): out[int(r[0])] = r
    return out
def fetch(sym):
    path = f"npz/{sym}.npz"
    if os.path.exists(path): return sym, "cached"
    kl = series("klines", sym)
    if not kl: return sym, "empty"
    pr = series("premiumIndexKlines", sym)
    t = np.array(sorted(kl), dtype=np.int64)
    a = np.array([[float(kl[x][i]) for i in (1, 2, 3, 4, 5, 7, 10)] for x in t])
    p = np.array([float(pr[x][4]) if x in pr else np.nan for x in t])
    np.savez_compressed(path + ".tmp.npz", t=t, o=a[:, 0], h=a[:, 1], l=a[:, 2], c=a[:, 3], v=a[:, 4], qv=a[:, 5], tbq=a[:, 6], prem=p)
    os.replace(path + ".tmp.npz", path)
    return sym, f"{t.size} bars"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
os.makedirs(OUT, exist_ok=True)
os.chdir(OUT)
os.makedirs("npz", exist_ok=True)


def first_last(sym):
    ks = sorted(k for k in keys(f"data/futures/um/daily/klines/{sym}/1d/") if k.endswith(".zip"))
    return sym, ([ks[0].split("-1d-")[1][:10], ks[-1].split("-1d-")[1][:10]] if ks else [None, None])


def all_symbols():
    out, marker = [], ""
    while True:
        root = ET.fromstring(get(LIST, params={"prefix": "data/futures/um/daily/klines/", "delimiter": "/",
                                               "marker": marker}).content)
        page = [p.findtext("s3:Prefix", namespaces=NS).split("/")[-2] for p in root.findall("s3:CommonPrefixes", NS)]
        out += page
        if root.findtext("s3:IsTruncated", namespaces=NS) != "true" or not page:
            return [s for s in out if s.endswith("USDT")]
        marker = root.findtext("s3:NextMarker", namespaces=NS) or page[-1]


with cf.ThreadPoolExecutor(16) as ex:
    lst = dict(ex.map(first_last, all_symbols()))
json.dump(lst, open("listing.json", "w"), indent=0)
newest = max(b for a, b in lst.values() if b)
recent = str(np.datetime64(newest) - np.timedelta64(2, "D"))
syms = sorted(s for s, (a, b) in lst.items() if b and b >= recent)
print(len(syms), "trading symbols", flush=True)
n = 0
with cf.ThreadPoolExecutor(16) as ex:
    for sym, msg in ex.map(fetch, syms):
        n += 1
        if n % 50 == 0 or msg == "empty": print(n, sym, msg, flush=True)
print("done", n)
