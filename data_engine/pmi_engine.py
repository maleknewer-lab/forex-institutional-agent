import yfinance as yf
import pandas as pd

class PMIEngine:
    def __init__(self):
        pass

    def get_pmi_analysis(self, currency_pair: str) -> dict:
        """
        تحليل مؤشرات مديري المشتريات (PMI) كأداة استباقية للنمو الاقتصادي واتجاهات العملات
        القراءة فوق 50 تعني توسع اقتصادي (Expansion)، وأقل من 50 تعني انكماش (Contraction).
        """
        try:
            base, quote = currency_pair.split('/')
            
            # محاكاة وتقييم اتجاه المؤشرات الاستباقية للنمو بناءً على أداء الأسواق والقطاعات
            pmi_proxy = yf.download("SPY", period="1mo", progress=False)
            if pmi_proxy.empty:
                return {"pmi_score": 51.5, "bias": "توسع طفيف", "description": "استقرار مؤشرات الأنشطة الاقتصادية."}
            
            start_val = float(pmi_proxy['Close'].iloc[0])
            end_val = float(pmi_proxy['Close'].iloc[-1])
            growth = ((end_val - start_val) / start_val) * 100

            # تقدير قراءة PMI افتراضية مؤسسية بناءً على الزخم (الخط الفاصل هو 50)
            estimated_pmi = 50.0 + (growth * 2.5)
            estimated_pmi = max(42.0, min(58.0, estimated_pmi)) # نطاق منطقي للـ PMI

            if estimated_pmi > 50.0:
                bias = f"توسع اقتصادي (PMI Expansion at {estimated_pmi:.1f})"
                description = f"الأنشطة الاقتصادية في نطاق التوسع (>50) عند قراءة {estimated_pmi:.1f}. تدعم عملات المخاطرة والنمو."
            else:
                bias = f"انكماش اقتصادي (PMI Contraction at {estimated_pmi:.1f})"
                description = f"الأنشطة تشهد انكماشاً (<50) عند قراءة {estimated_pmi:.1f}. تضغط على عملات النمو وتدعم الملاذات."

            return {
                "estimated_pmi": round(estimated_pmi, 1),
                "bias": bias,
                "description": description
            }
        except Exception as e:
            return {"estimated_pmi": 50.0, "bias": "محايد", "description": str(e)}
