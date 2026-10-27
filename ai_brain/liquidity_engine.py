import numpy as np
import pandas as pd

class LiquiditySweepEngine:
    def __init__(self):
        pass

    def compute_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        prev_close = df["close"].shift(1)
        tr = pd.concat(
            [
                df["high"] - df["low"],
                (df["high"] - prev_close).abs(),
                (df["low"] - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)
        return tr.rolling(period).mean()

    def detect_buyside_sweeps(
        self,
        df: pd.DataFrame,
        n: int = 5,
        eq_tol: float = 0.1,
        expiry: int = 100,
        min_touches: int = 2,
        atr_period: int = 14,
    ) -> pd.DataFrame:
        if len(df) < (2 * n + atr_period):
            return pd.DataFrame()
            
        high = df["high"].to_numpy()
        close = df["close"].to_numpy()
        atr = self.compute_atr(df, atr_period).to_numpy()

        zones = []
        events = []

        for t in range(2 * n, len(df)):
            i = t - n
            window = high[i - n : t + 1]
            if high[i] == window.max() and (window == high[i]).sum() == 1:
                if not np.isnan(atr[t]):
                    merged = False
                    for z in zones:
                        if abs(high[i] - z["level"]) <= eq_tol * atr[t]:
                            z["level"] = max(z["level"], high[i])
                            z["touches"] += 1
                            z["last_idx"] = i
                            merged = True
                            break
                    if not merged:
                        zones.append({"level": high[i], "touches": 1, "last_idx": i})

            remaining = []
            for z in zones:
                if t - z["last_idx"] > expiry:
                    continue
                if high[t] > z["level"]:
                    if close[t] < z["level"]:
                        if z["touches"] >= min_touches:
                            events.append(
                                {
                                    "idx": t,
                                    "time": df.index[t] if hasattr(df.index, '__getitem__') else t,
                                    "level": z["level"],
                                    "touches": z["touches"],
                                    "sweep_depth_atr": (high[t] - z["level"]) / atr[t],
                                }
                            )
                    continue
                remaining.append(z)
            zones = remaining

        return pd.DataFrame(events)