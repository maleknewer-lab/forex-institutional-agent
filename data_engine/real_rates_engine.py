import yfinance as yf
import pandas as pd

class RealRatesEngine:
    def __init__(self):
        pass

    def get_real_interest_rates(self) -> dict:
        """
        حساب وتقييم أسعار الفائدة الحقيقية وتأثيرها على العملات والذهب
        """
        try:
            # استخدام عوائد السندات الأمريكية 10 سنوات (^TNX) كمؤشر اسمي
            tnx = yf.download("^TNX", period="1mo", progress=False)
            if tnx.empty:
                return {"real_rate": 1.5, "bias": "محايد", "description": "استقرار الفائدة الحقيقية."}
            
            nominal_yield = float(tnx['Close'].iloc[-1])
            # تقدير متوسط معدل التضخم الحالي (توقعات التضخم بحدود 2.3% إلى 2.5%)
            inflation_expectation = 2.4
            real_rate = nominal_yield - inflation_expectation

            # تحليل التأثير المؤسسي:
            # الفائدة الحقيقية السالبة أو المنخفضة جداً -> داعمة للصعود بقوة (Gold & Risk Assets)
            # الفائدة الحقيقية المرتفعة -> داعمة لقوة الدولار (USD Bullish)
            if real_rate < 1.0:
                bias = "دعم صعودي للأصول والذهب (Low/Negative Real Rates)"
                description = f"الفائدة الحقيقية منخفضة عند {real_rate:.2f}% (عائد {nominal_yield:.2f}% - تضخم {inflation_expectation}%). بيئة مثالية للذهب والعملات."
            else:
                bias = "قوة جاذبية الدولار (High Real Rates)"
                description = f"الفائدة الحقيقية مرتفعة عند {real_rate:.2f}%. تزيد جاذبية السندات والدولار وتضغط على الذهب."

            return {
                "nominal_yield": round(nominal_yield, 2),
                "real_rate": round(real_rate, 2),
                "bias": bias,
                "description": description
            }
        except Exception as e:
            return {"real_rate": 1.5, "bias": "محايد", "description": str(e)}
