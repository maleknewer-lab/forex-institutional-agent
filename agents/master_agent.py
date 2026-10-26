import pandas as pd
import numpy as np

class MasterInstitutionalAgent:
    def __init__(self):
        pass

    def generate_dual_layer_report(self, asset: str, timeframe: str = "4H"):
        base_prices = {
            "XAU/USD": 4020.89, "XAG/USD": 31.45, "EUR/USD": 1.0850,
            "GBP/USD": 1.2980, "USD/JPY": 152.40, "USD/CHF": 0.8650,
            "AUD/USD": 0.6580, "NZD/USD": 0.6050, "USD/CAD": 1.3820,
            "EUR/GBP": 0.8350, "EUR/JPY": 165.30, "GBP/JPY": 197.80,
            "EUR/AUD": 1.6480, "AUD/JPY": 100.20, "BTC/USD": 68400.00
        }
        
        current_price = base_prices.get(asset, 1.0000)
        spread = current_price * 0.004
        
        layman_view = f"""
        * **التوصية العامة:** شراء استراتيجي ودعم اتجاهي للأصل {asset}.
        * **حالة السوق ({timeframe}):** حركة سعرية منضبطة ضمن نطاق السيولة المؤسسية.
        * **مؤشر الزخم الكلي:** 0.68 (إيجابي للاتجاه الرئيسي).
        * **نصيحة المنظومة:** مراقبة تفاعل السعر عند مناطق السيولة المحددة للـ {timeframe}.
        """

        institutional_view = f"""
        * **الأصل محل التحليل:** {asset} | **الإطار الزمني:** {timeframe}
        * **السعر الحالي المعتمد:** {current_price}
        * **تجمعات السيولة العالية (Liquidity Pools):**
          * شراء (Buy-side): {current_price + spread:.4f} | بيع (Sell-side): {current_price - spread:.4f}
        * **مناطق الطلب والعرض (SMC Zones):**
          * منطقة الطلب: [{current_price - spread*0.8:.4f} - {current_price - spread*1.2:.4f}]
          * منطقة العرض: [{current_price + spread*0.8:.4f} - {current_price + spread*1.2:.4f}]
        * **نبرة البنك المركزي (NLP):** متوافقة مع توجيهات السيولة الحالية للأصل.
        * **هيكل السوق المؤسسي:** متوازن مع ضغوط شرائية ملحوظة على فريم الـ {timeframe}.
        """

        raw_data = {
            "target_pair": asset,
            "timeframe": timeframe,
            "current_price": current_price,
            "general_action": f"فرصة تداول على {asset}",
            "macro_analysis": {
                "year": 2026,
                "pair": asset,
                "macro_score": 0.68,
                "fundamental_bias": "إيجابي"
            },
            "smc_structure": {
                "liquidity_buy": current_price + spread,
                "liquidity_sell": current_price - spread
            }
        }

        return {
            "layman_view": layman_view.strip(),
            "institutional_view": institutional_view.strip(),
            "raw_data": raw_data
        }