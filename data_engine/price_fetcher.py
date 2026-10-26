import yfinance as yf
import pandas as pd

class PriceFetcher:
    def __init__(self):
        self.ticker_map = {
            "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "USDJPY=X",
            "AUD/USD": "AUDUSD=X", "USD/CAD": "USDCAD=X", "NZD/USD": "NZDUSD=X",
            "USD/CHF": "USDCHF=X", "EUR/GBP": "EURGBP=X", "EUR/JPY": "EURJPY=X",
            "GBP/JPY": "GBPJPY=X", "AUD/JPY": "AUDJPY=X", "EUR/AUD": "EURAUD=X",
            "GBP/AUD": "GBPAUD=X", "EUR/CHF": "EURCHF=X", "CHF/JPY": "CHFJPY=X",
            "XAU/USD": "GC=F", "XAG/USD": "SI=F"
        }

    def fetch_ohlcv(self, currency_pair: str, interval: str = "1h", period: str = "60d") -> pd.DataFrame:
        symbol = self.ticker_map.get(currency_pair, "EURUSD=X")
        try:
            # تحديد auto_adjust صراحةً لتجنب التحذير
            df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=True)
            
            if df.empty:
                return pd.DataFrame()
                
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in expected_columns:
                if col not in df.columns:
                    matched = [c for c in df.columns if c.lower() == col.lower()]
                    if matched:
                        df.rename(columns={matched[0]: col}, inplace=True)
                        
            return df
        except Exception as e:
            print(f"خطأ في جلب البيانات لـ {currency_pair}: {e}")
            return pd.DataFrame()

    def get_multi_timeframe_data(self, currency_pair: str) -> dict:
        data_1h = self.fetch_ohlcv(currency_pair, interval="1h", period="30d")
        data_1d = self.fetch_ohlcv(currency_pair, interval="1d", period="60d")
        
        data_4h = pd.DataFrame()
        if not data_1h.empty:
            try:
                # استخدام '4h' بحرف صغير لتجنب التحذير المستقبلي
                data_4h = data_1h.resample('4h').agg({
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }).dropna()
            except Exception:
                data_4h = data_1h.copy()

        return {
            "1h": data_1h,
            "4h": data_4h,
            "1d": data_1d
        }
