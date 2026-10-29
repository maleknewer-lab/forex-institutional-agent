import pandas as pd
import numpy as np

class MultiTimeframeSMCEngine:
    def __init__(self, symbol):
        self.symbol = symbol

    def analyze_confluence(self, df_daily, df_4h):
        try:
            current_price = float(df_4h['close'].iloc[-1])
            
            # الاتجاه اليومي
            close_daily = df_daily['close']
            sma20 = close_daily.rolling(20).mean().iloc[-1]
            sma50 = close_daily.rolling(50).mean().iloc[-1]
            
            if current_price > sma20 and sma20 > sma50:
                daily_trend = "Bullish (صاعد)"
            elif current_price < sma20 and sma20 < sma50:
                daily_trend = "Bearish (هابط)"
            else:
                daily_trend = "Neutral (محايد)"

            # استخراج مناطق الـ Order Block (إطار 4 ساعات)
            df_4h_recent = df_4h.tail(30)
            ob_min = round(float(df_4h_recent['low'].min()), 4)
            ob_max = round(float(df_4h_recent['high'].max()), 4)
            
            mid_price = (ob_min + ob_max) / 2
            if 'JPY' in self.symbol or 'GC' in self.symbol or 'SI' in self.symbol:
                distance_to_ob_pips = round(abs(current_price - mid_price) / 0.01, 1)
            else:
                distance_to_ob_pips = round(abs(current_price - mid_price) / 0.0001, 1)

            # استخراج هيكل السوق (BOS / CHOCH)
            highs = df_4h['high'].values
            lows = df_4h['low'].values
            
            recent_high_max = highs[-15:].max()
            recent_low_min = lows[-15:].min()
            
            if current_price >= recent_high_max * 0.9995:
                market_structure = "Bullish BOS (كسر هيكل صاعد - استمرار الاتجاه)"
            elif current_price <= recent_low_min * 1.0005:
                market_structure = "Bearish BOS (كسر هيكل هابط - استمرار الاتجاه)"
            elif "صاعد" in daily_trend and current_price < lows[-5]:
                market_structure = "Bullish CHOCH (تغير طابع - تصحيح محتمل)"
            elif "هابط" in daily_trend and current_price > highs[-5]:
                market_structure = "Bearish CHOCH (تغير طابع - انعكاس محتمل)"
            else:
                market_structure = "Consolidation / Range (تداول عرضي متوازن)"

            # رصد الضوضاء السوقية
            volatility = df_4h['high'].tail(14).sub(df_4h['low'].tail(14)).mean()
            is_noise_detected = volatility > (current_price * 0.006)

            return {
                "current_price": current_price,
                "daily_trend": daily_trend,
                "order_block_zone": (ob_min, ob_max),
                "distance_to_ob_pips": distance_to_ob_pips,
                "market_structure": market_structure,
                "is_noise_detected": is_noise_detected
            }
        except Exception as e:
            cp = float(df_4h['close'].iloc[-1]) if not df_4h.empty else 1.0
            return {
                "current_price": cp,
                "daily_trend": "Neutral (محايد)",
                "order_block_zone": (round(cp*0.99, 4), round(cp*1.01, 4)),
                "distance_to_ob_pips": 10.0,
                "market_structure": "Range / Consolidation",
                "is_noise_detected": False
            }
