import pandas as pd
import yfinance as yf

class AssetTechAgent:
    """
    وكيل الزوج التقني: مسؤول عن إدارة محركات الجلب للزوج،
    حساب مستويات SMC (Swing High / Low)، وتنظيف البيانات الخام.
    """
    def __init__(self, symbol: str, spread: float):
        self.symbol = symbol
        self.spread = spread

    def fetch_and_validate_data(self) -> dict:
        try:
            df = yf.download(self.symbol, period="1mo", interval="1d", progress=False)
            if df is not None and not df.empty:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[0].lower() for col in df.columns]
                else:
                    df.columns = [col.lower() for col in df.columns]
                
                current_price = float(df['close'].iloc[-1])
                swing_high = float(df['high'].iloc[-10:].max())
                swing_low = float(df['low'].iloc[-10:].min())
                
                # ضمان منطقية النطاق السعري
                if swing_high <= current_price:
                    swing_high = current_price + (self.spread * 2)
                if swing_low >= current_price:
                    swing_low = current_price - (self.spread * 2)
                    
                ma_trend = "BULLISH" if current_price >= df['close'].rolling(5).mean().iloc[-1] else "BEARISH"
                
                return {
                    "status": "success",
                    "current_price": current_price,
                    "swing_high": swing_high,
                    "swing_low": swing_low,
                    "trend": ma_trend,
                    "feature_vector": [current_price, swing_high, swing_low]
                }
        except Exception as e:
            print(f"Error fetching data for {self.symbol}: {e}")
            
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
