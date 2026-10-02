"""Backtest engines (1x notional, returns as fraction of equity).

Execution model (no look-ahead):
  * signals are evaluated on the CLOSE of bar i and filled at the OPEN of bar i+1
  * stop-loss / take-profit are checked intrabar against high/low; if both are
    touched in the same bar the stop is assumed to fill first (conservative);
    gaps through the stop fill at the open
  * every fill pays `cost` (taker fee + slippage) on the traded notional
  * longs pay `fund` per bar (average positive funding); shorts receive nothing
"""

import numpy as np
from numba import njit


@njit(cache=True)
def run_single(o, h, l, c, atr_, long_entry, short_entry, long_exit, short_exit,
               sl_k, tp_k, max_hold, cost, fund, n_end):
    """Returns (bar_returns, trades) where trades rows are
    [entry_idx, exit_idx, side, net_return, max_adverse_excursion]."""
    n = min(n_end, c.size)
    ret = np.zeros(c.size)
    trades = np.zeros((n // 2 + 2, 5))
    nt = 0
    pos = 0
    ref = 0.0
    entry = 0.0
    stop = 0.0
    take = 0.0
    held = 0
    mae = 0.0
    entry_idx = 0
    pending = 0
    has_pending = False
    armed_long = True
    armed_short = True

    for i in range(1, n):
        r = 0.0
        # 1) fill the order decided at the previous close
        if has_pending and pending != pos:
            px = o[i]
            if pos != 0:
                r += pos * (px / ref - 1.0) - cost
                trades[nt, 0] = entry_idx
                trades[nt, 1] = i
                trades[nt, 2] = pos
                trades[nt, 3] = pos * (px / entry - 1.0) - 2.0 * cost - (fund * held if pos > 0 else 0.0)
                trades[nt, 4] = mae
                nt += 1
                pos = 0
            if pending != 0:
                pos = pending
                entry = px
                ref = px
                r -= cost
                held = 0
                mae = 0.0
                entry_idx = i
                a = atr_[i - 1]
                stop = entry - pos * sl_k * a if sl_k > 0 else 0.0
                take = entry + pos * tp_k * a if tp_k > 0 else 0.0
        has_pending = False

        # 2) intrabar stop / take-profit
        if pos != 0:
            exit_px = 0.0
            if pos > 0:
                adverse = l[i] / entry - 1.0
                if adverse < mae:
                    mae = adverse
                if sl_k > 0 and l[i] <= stop:
                    exit_px = min(o[i], stop)
                elif tp_k > 0 and h[i] >= take:
                    exit_px = max(o[i], take)
            else:
                adverse = 1.0 - h[i] / entry
                if adverse < mae:
                    mae = adverse
                if sl_k > 0 and h[i] >= stop:
                    exit_px = max(o[i], stop)
                elif tp_k > 0 and l[i] <= take:
                    exit_px = min(o[i], take)
            if exit_px > 0:
                r += pos * (exit_px / ref - 1.0) - cost
                trades[nt, 0] = entry_idx
                trades[nt, 1] = i
                trades[nt, 2] = pos
                trades[nt, 3] = pos * (exit_px / entry - 1.0) - 2.0 * cost - (fund * held if pos > 0 else 0.0)
                trades[nt, 4] = mae
                nt += 1
                # after a stop/target, wait for the entry signal to reset before re-entering
                if pos > 0:
                    armed_long = False
                else:
                    armed_short = False
                pos = 0

        # 3) mark to market at the close
        if pos != 0:
            r += pos * (c[i] / ref - 1.0)
            ref = c[i]
            held += 1
            if pos > 0:
                r -= fund
        ret[i] = r

        # 4) decide the next order on this close
        if not long_entry[i]:
            armed_long = True
        if not short_entry[i]:
            armed_short = True
        desired = pos
        if pos > 0:
            if long_exit[i] or (max_hold > 0 and held >= max_hold):
                desired = 0
            if short_entry[i] and armed_short:
                desired = -1
        elif pos < 0:
            if short_exit[i] or (max_hold > 0 and held >= max_hold):
                desired = 0
            if long_entry[i] and armed_long:
                desired = 1
        else:
            if long_entry[i] and armed_long:
                desired = 1
            elif short_entry[i] and armed_short:
                desired = -1
        if desired != pos:
            pending = desired
            has_pending = True

    if pos != 0:  # mark the open trade at the last close (no exit cost booked in returns)
        trades[nt, 0] = entry_idx
        trades[nt, 1] = n - 1
        trades[nt, 2] = pos
        trades[nt, 3] = pos * (c[n - 1] / entry - 1.0) - cost - (fund * held if pos > 0 else 0.0)
        trades[nt, 4] = mae
        nt += 1
    return ret, trades[:nt]


@njit(cache=True)
def run_weights(o, w, cost, fund, n_end):
    """Portfolio engine. w[i, j] = target weight decided at close i, held from open i+1
    to open i+2. Returns per-bar portfolio returns and the number of position changes."""
    n = min(n_end, o.shape[0])
    k = o.shape[1]
    ret = np.zeros(o.shape[0])
    changes = np.zeros(o.shape[0])
    prev = np.zeros(k)
    for i in range(1, n - 1):
        r = 0.0
        ch = 0.0
        for j in range(k):
            wj = w[i - 1, j]
            if wj != wj:
                wj = 0.0
            if wj != prev[j]:
                r -= cost * abs(wj - prev[j])
                if (wj > 0) != (prev[j] > 0) or (wj < 0) != (prev[j] < 0):
                    ch += 1.0
                prev[j] = wj
            if wj != 0.0:
                a = o[i, j]
                b = o[i + 1, j]
                if a == a and b == b and a > 0:
                    r += wj * (b / a - 1.0)
                if wj > 0:
                    r -= fund * wj
        ret[i] = r
        changes[i] = ch
    return ret, changes
