"""Per-coin position state machine shared by the backtest and the live/paper runner.

Candle i is processed in four steps (identical to the research engine):
  1. fill the order decided at the previous close at this candle's OPEN
  2. check stop-loss / take-profit against this candle's LOW/HIGH
     (stop first if both are touched; a gap through the level fills at the open)
  3. mark the position to this candle's CLOSE
  4. on this close, decide the order for the next candle's open
After a stop/target exit the same-side entry must switch off and on again before
re-entering ("re-arming"), so a still-true entry signal does not re-enter immediately.
"""


class CoinTrader:
    FIELDS = ("pos", "entry", "ref", "stop", "take", "held", "mae", "entry_time",
              "pending", "pending_reason", "armed_long", "armed_short")

    def __init__(self, sl_k, tp_k, max_hold, cost, fund_per_bar, state=None):
        self.sl_k, self.tp_k, self.max_hold = sl_k, tp_k, max_hold
        self.cost, self.fund = cost, fund_per_bar
        self.pos = 0
        self.entry = self.ref = self.stop = self.take = 0.0
        self.held = 0
        self.mae = 0.0
        self.entry_time = None
        self.pending = None  # target position for the next open, or None
        self.pending_reason = ""
        self.armed_long = self.armed_short = True
        if state:
            for k in self.FIELDS:
                setattr(self, k, state[k])

    def state(self):
        return {k: getattr(self, k) for k in self.FIELDS}

    def _close(self, t, px, reason, trades):
        trades.append({"side": self.pos, "entry_time": self.entry_time, "exit_time": t,
                       "entry": self.entry, "exit": px, "reason": reason,
                       "ret": self.pos * (px / self.entry - 1.0) - 2 * self.cost
                       - (self.fund * self.held if self.pos > 0 else 0.0),
                       "mae": self.mae})
        r = self.pos * (px / self.ref - 1.0) - self.cost
        self.pos = 0
        return r

    def step(self, t, o, h, l, c, long_entry, short_entry, long_exit, short_exit, atr_prev, trades):
        """Process one closed candle. Returns this candle's return on 1x notional."""
        r = 0.0
        # 1) fill the pending order at the open
        if self.pending is not None and self.pending != self.pos:
            if self.pos != 0:
                r += self._close(t, o, self.pending_reason, trades)
            if self.pending != 0:
                self.pos = self.pending
                self.entry = self.ref = o
                self.entry_time = t
                r -= self.cost
                self.held = 0
                self.mae = 0.0
                self.stop = self.entry - self.pos * self.sl_k * atr_prev if self.sl_k > 0 else 0.0
                self.take = self.entry + self.pos * self.tp_k * atr_prev if self.tp_k > 0 else 0.0
        self.pending = None

        # 2) intrabar stop-loss / take-profit
        if self.pos != 0:
            exit_px, reason = 0.0, ""
            if self.pos > 0:
                self.mae = min(self.mae, l / self.entry - 1.0)
                if self.sl_k > 0 and l <= self.stop:
                    exit_px, reason = min(o, self.stop), "stop"
                elif self.tp_k > 0 and h >= self.take:
                    exit_px, reason = max(o, self.take), "take"
            else:
                self.mae = min(self.mae, 1.0 - h / self.entry)
                if self.sl_k > 0 and h >= self.stop:
                    exit_px, reason = max(o, self.stop), "stop"
                elif self.tp_k > 0 and l <= self.take:
                    exit_px, reason = min(o, self.take), "take"
            if exit_px > 0:
                side = self.pos
                r += self._close(t, exit_px, reason, trades)
                if side > 0:
                    self.armed_long = False
                else:
                    self.armed_short = False

        # 3) mark to the close
        if self.pos != 0:
            r += self.pos * (c / self.ref - 1.0)
            self.ref = c
            self.held += 1
            if self.pos > 0:
                r -= self.fund

        # 4) decide the next order
        if not long_entry:
            self.armed_long = True
        if not short_entry:
            self.armed_short = True
        desired, reason = self.pos, ""
        timed_out = self.max_hold > 0 and self.held >= self.max_hold
        if self.pos > 0:
            if long_exit or timed_out:
                desired, reason = 0, "exit_signal" if long_exit else "time_limit"
            if short_entry and self.armed_short:
                desired, reason = -1, "reverse"
        elif self.pos < 0:
            if short_exit or timed_out:
                desired, reason = 0, "exit_signal" if short_exit else "time_limit"
            if long_entry and self.armed_long:
                desired, reason = 1, "reverse"
        else:
            if long_entry and self.armed_long:
                desired = 1
            elif short_entry and self.armed_short:
                desired = -1
        if desired != self.pos:
            self.pending, self.pending_reason = desired, reason
        return r
