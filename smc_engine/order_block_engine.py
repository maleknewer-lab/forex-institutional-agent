import pandas as pd
import numpy as np

class MultiTimeframeSMCEngine:
    """
    محرك تحليل بنية الأموال الذكية متعدد الأطر الزمنية (Multi-Timeframe SMC Engine):
    - يقارن بين الإطار اليومي (Daily - 1D) والإطار الفرعي (4H).
    - يكتشف الـ Order Blocks الحقيقية ويفلتر الضوضاء والإشارات الكاذبة.
    """
    def __init__(self, symbol: str):
        self.symbol = symbol

    def analyze_confluence(self, df_daily: pd.DataFrame, df_4h: pd.DataFrame):
        """
        تحليل التوافق بين الإطار اليومي والأربع ساعات وكشف الضوضاء
        """
        if df_daily is None or len(df_daily) < 50 or df_4h is None or len(df_4h) < 50:
            return {"status": "error", "message": "بيانات غير كافية لتحليل التوافق الزمني"}

        # 1. تحليل الهيكل اليومي (Daily Macro Bias)
        daily_close = df_daily['close'].iloc[-1]
        daily_sma50 = df_daily['close'].rolling(50).mean().iloc[-1]
        daily_trend = "Bullish (صاعد)" if daily_close > daily_sma50 else "Bearish (هابط)"

        # 2. تحليل الأربع ساعات (4H Tactical Order Block)
        df_4h['is_green'] = df_4h['close'] > df_4h['open']
        current_price = df_4h['close'].iloc[-1]
        
        recent_4h = df_4h.tail(40)
        bullish_obs = recent_4h[~recent_4h['is_green']] # آخر شمعات هابطة (مراكز طلب)
        
        if not bullish_obs.empty:
            ob_row = bullish_obs.iloc[-1]
            ob_level = float(ob_row['low'])
            ob_high = float(ob_row['high'])
        else:
            ob_level = float(recent_4h['low'].min())
            ob_high = ob_level * 1.002

        multiplier = 100.0 if "JPY" in self.symbol else (10000.0 if "=" in self.symbol else 10.0)
        distance_to_ob_pips = (current_price - ob_level) * multiplier

        # 3. كشف الضوضاء والإشارات الكاذبة (Confluence & Noise Filtering)
        is_noise = False
        warning_msg = ""

        if daily_trend == "Bearish (هابط)" and distance_to_ob_pips < 5.0:
            is_noise = True
            warning_msg = "[⚠️ تنبيه ضوضاء]: الـ Order Block على فريم الـ 4H يعاكس الاتجاه العام الهابط على الإطار اليومي. احتمالية فخ صانع السوق (Stop Hunt) عالية!"
        elif daily_trend == "Bullish (صاعد)" and distance_to_ob_pips < 5.0:
            warning_msg = "[✅ توافق مؤسسي قوي]: الـ 4H Order Block متوافق تماماً مع الاتجاه الصاعد للإطار اليومي."
        else:
            warning_msg = f"[⏳ بانتظار التصحيح]: السعر يحتاج لارتداد بقيمة {round(distance_to_ob_pips, 1)} نقطة نحو الـ Order Block."

        return {
            "symbol": self.symbol,
            "daily_trend": daily_trend,
            "current_price": round(current_price, 5),
            "order_block_zone": (round(ob_level, 5), round(ob_high, 5)),
            "distance_to_ob_pips": round(distance_to_ob_pips, 1),
            "is_noise_detected": is_noise,
            "analysis_report": warning_msg
        }
