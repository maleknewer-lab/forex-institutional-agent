import yfinance as yf
import pandas as pd

class CommodityCorrelationEngine:
    def __init__(self):
        # تصنيف حساسية العملات للنفط والذهب
        self.oil_sensitivity = {
            "CAD": "positive",  # إيجابي بارتفاع النفط
            "NOK": "positive",
            "RUB": "positive",
            "EUR": "negative",  # سلبي (مستورد للطاقة)
            "JPY": "negative",  # سلبي (مستورد للطاقة)
            "GBP": "neutral",
            "AUD": "positive"   # ارتباط سلعي عام
        }
        
    def _get_commodity_trends(self):
        """
        جلب اتجاهات النفط والذهب الحية عبر yfinance
        """
        try:
            oil = yf.download("CL=F", period="1mo", progress=False)
            gold = yf.download("GC=F", period="1mo", progress=False)
            
            oil_change = 0.0
            gold_change = 0.0
            
            if not oil.empty and len(oil) > 5:
                oil_start = float(oil['Close'].iloc[0])
                oil_end = float(oil['Close'].iloc[-1])
                oil_change = ((oil_end - oil_start) / oil_start) * 100
                
            if not gold.empty and len(gold) > 5:
                gold_start = float(gold['Close'].iloc[0])
                gold_end = float(gold['Close'].iloc[-1])
                gold_change = ((gold_end - gold_start) / gold_start) * 100
                
            return {
                "oil_trend": "صاعد (Bullish)" if oil_change > 0 else "هابط (Bearish)",
                "oil_change_pct": round(oil_change, 2),
                "gold_trend": "صاعد (Bullish)" if gold_change > 0 else "هابط (Bearish)",
                "gold_change_pct": round(gold_change, 2)
            }
        except:
            return {"oil_trend": "مستقر", "oil_change_pct": 0.0, "gold_trend": "مستقر", "gold_change_pct": 0.0}

    def analyze_commodity_impact(self, currency_pair: str) -> dict:
        """
        تحليل تأثير النفط والذهب على الزوج المحدد
        """
        base, quote = currency_pair.split('/')
        comm_data = self._get_commodity_trends()
        
        oil_pct = comm_data["oil_change_pct"]
        gold_pct = comm_data["gold_change_pct"]
        
        base_oil_sens = self.oil_sensitivity.get(base, "neutral")
        quote_oil_sens = self.oil_sensitivity.get(quote, "neutral")
        
        # حساب التقييم الاستراتيجي بناءً على حركة النفط والعملة
        impact_score = 0.0
        description = f"النفط يتغير بنسبة {oil_pct}% | الذهب يتغير بنسبة {gold_pct}%."
        
        if base_oil_sens == "positive" and oil_pct > 0:
            impact_score += 0.5
            description += f" صعود النفط يدعم عملة الأساس ({base}) بقوة."
        elif base_oil_sens == "negative" and oil_pct > 0:
            impact_score -= 0.5
            description += f" صعود النفط يضغط سلباً على عملة الأساس ({base})."
            
        if "XAU" in base:
            if gold_pct > 0:
                impact_score += 0.8
                description += f" صعود الذهب يدعم الأصول المقومة به."

        return {
            "commodities": comm_data,
            "impact_score": impact_score,
            "description": description
        }
