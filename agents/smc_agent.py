import yfinance as yf
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class SMCAgent:
    def __init__(self):
        pass

    def analyze_multi_timeframe_trend(self, currency_pair: str) -> dict:
        return {"4h_trend": "صاعد مؤسسي", "1h_trend": "إعادة اختبار منطقة سيولة"}

    def detect_smc_structures(self, currency_pair: str, timeframe: str = "4h") -> dict:
        try:
            ticker_symbol = currency_pair.replace("/", "")
            if "XAU" in ticker_symbol:
                ticker_symbol = "GC=F"
            elif len(ticker_symbol) == 6:
                ticker_symbol = f"{ticker_symbol}=X"
                
            df = yf.download(ticker_symbol, period="1mo", interval="1h", progress=False)
            if df.empty:
                return self._default_smc()
                
            current_price = float(df['Close'].iloc[-1].item() if hasattr(df['Close'].iloc[-1], 'item') else df['Close'].iloc[-1])
            recent_high = float(df['High'].tail(20).max().item() if hasattr(df['High'].tail(20).max(), 'item') else df['High'].tail(20).max())
            recent_low = float(df['Low'].tail(20).min().item() if hasattr(df['Low'].tail(20).min(), 'item') else df['Low'].tail(20).min())
            
            buy_side_liq = round(recent_high + (current_price * 0.0015), 5)
            sell_side_liq = round(recent_low - (current_price * 0.0015), 5)
            
            demand_zone = f"{round(recent_low, 5)} - {round(recent_low * 1.002, 5)}"
            supply_zone = f"{round(recent_high * 0.998, 5)} - {round(recent_high, 5)}"

            return {
                "current_market_price": round(current_price, 5),
                "high_liquidity_pools": {
                    "buy_side_liquidity_target": str(buy_side_liq),
                    "sell_side_liquidity_target": str(sell_side_liq)
                },
                "dynamic_order_blocks": {
                    "bullish_demand_zone": demand_zone,
                    "bearish_supply_zone": supply_zone
                }
            }
        except Exception as e:
            return self._default_smc()

    def _default_smc(self) -> dict:
        return {
            "current_market_price": 1.0850,
            "high_liquidity_pools": {
                "buy_side_liquidity_target": "1.0900",
                "sell_side_liquidity_target": "1.0800"
            },
            "dynamic_order_blocks": {
                "bullish_demand_zone": "1.0820 - 1.0835",
                "bearish_supply_zone": "1.0870 - 1.0885"
            }
        }
