import pandas as pd
import numpy as np
import yfinance as yf

class AssetTechAgent:
    """
    وكيل الزوج التقني المُصحح: يجلب بيانات الشموع الحية بدقة،
    يحسب مستويات SMC (Swing High / Low)، ويجهز مصفوفة الخصائص لـ XGBoost.
    """
    def __init__(self, symbol: str, spread: float):
        self.symbol = symbol
        self.spread = spread

    def fetch_and_validate_data(self) -> dict:
        try:
            # جلب البيانات التاريخية مباشرة عبر yfinance لضمان الاستقرار
            df = yf.download(self.symbol, period="1mo", interval="1d", progress=False)
            if df is not None and not df.empty:
                # معالجة أعمدة DataFrame لتفادي مشاكل الحروف الكبيرة والصغيرة أو الـ MultiIndex
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[0].lower() for col in df.columns]
                else:
                    df.columns = [col.lower() for col in df.columns]

                close_col = 'close' if 'close' in df.columns else 'adj close'
                high_col = 'high' if 'high' in df.columns else df.columns[0]
                low_col = 'low' if 'low' in df.columns else df.columns[1]

                current_price = float(df[close_col].iloc[-1])
                swing_high = float(df[high_col].iloc[-10:].max())
                swing_low = float(df[low_col].iloc[-10:].min())

                if swing_high <= current_price:
                    swing_high = current_price + (self.spread * 2)
                if swing_low >= current_price:
                    swing_low = current_price - (self.spread * 2)

                ma_trend = "BULLISH" if current_price >= df[close_col].rolling(5).mean().iloc[-1] else "BEARISH"

                return {
                    "status": "success",
                    "current_price": current_price,
                    "swing_high": swing_high,
                    "swing_low": swing_low,
                    "trend": ma_trend,
                    "feature_vector": [current_price, swing_high, swing_low]
                }
        except Exception as e:
            print(f"[!] Error in AssetTechAgent for {self.symbol}: {e}")

        # قيم احتياطية آمنة
        fallback = 100.0
        return {
            "status": "fallback",
            "current_price": fallback,
            "swing_high": fallback + 2.0,
            "swing_low": fallback - 2.0,
            "trend": "BULLISH",
            "feature_vector": [fallback, fallback + 2.0, fallback - 2.0]
        }
