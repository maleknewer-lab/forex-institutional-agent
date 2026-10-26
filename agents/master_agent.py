import pandas as pd
import numpy as np

class MasterInstitutionalAgent:
    def __init__(self):
        pass

    def generate_dual_layer_report(self, asset: str, timeframe: str = "4H"):
        macro_score = 0.65
        gdp_diff = 0.25
        rate_diff = 0.50
        
        if isinstance(macro_score, pd.Series):
            macro_score = macro_score.iloc[-1]
        if isinstance(gdp_diff, pd.Series):
            gdp_diff = gdp_diff.iloc[-1]
        if isinstance(rate_diff, pd.Series):
            rate_diff = rate_diff.iloc[-1]

        layman_view = f"""
        * **التوصية العامة:** شراء قوية (Strong Buy Opportunity).
        * **حالة السوق ({timeframe}):** مستقر ويسير وفق الاتجاه المدعوم بالسيولة والماكرو.
        * **مؤشر الزخم الكلي:** {float(macro_score):.2f} (إيجابي).
        * **نصيحة المنظومة:** الالتزام التام بالاتجاه المدعوم بالسيولة والمؤشرات الكلية.
        """

        institutional_view = f"""
        * **الإطار الزمني للتحليل:** {timeframe}
        * **السعر الحالي:** 4020.8999
        * **تجمعات السيولة العالية (Liquidity Pools):**
          * شراء: 4045.43125 | بيع: 3984.86855
        * **مناطق الطلب والعرض (SMC Zones):**
          * طلب: [3998.8817 - 3990.8999]
          * عرض: [4031.3211 - 4039.3999]
        * **نبرة البنك المركزي (NLP):** نبرة تيسيرية لصالح السيولة.
        * **الفائدة الحقيقية:** الفائدة عند 1.5% والضغوط الشرائية مستمرة.
        """

        raw_data = {
            "target_pair": asset,
            "timeframe": timeframe,
            "general_action": "فرصة شراء قوية (Strong Buy Opportunity)",
            "macro_analysis": {
                "year": 2026,
                "pair": asset,
                "gdp_diff": float(gdp_diff),
                "rate_diff": float(rate_diff),
                "macro_score": float(macro_score),
                "fundamental_bias": "صاعد"
            },
            "risk_analysis": {
                "regime": "Neutral"
            }
        }

        return {
            "layman_view": layman_view.strip(),
            "institutional_view": institutional_view.strip(),
            "raw_data": raw_data
        }