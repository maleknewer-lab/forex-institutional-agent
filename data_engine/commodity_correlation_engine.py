import yfinance as yf
import pandas as pd

class CommodityCorrelationEngine:
    def __init__(self):
        # تصنيف حساسية العملات للنفط (إيجابي، سلبي، محايد)
        self.oil_sensitivity = {
            "CAD": 1.0,   # مرتبط ارتباطاً وثيقاً بأسعار النفط
            "NOK": 1.0,
            "RUB": 0.8,
            "AUD": 0.5,   # سلعة عامة وترابط تجاري
            "EUR": -0.5,  # مستورد للطاقة
            "JPY": -0.7,  # مستورد صافي للطاقة
            "GBP": 0.0,   # محايد نسبيًا
            "USD": -0.2   # علاقة عكسية طفيفة غالباً مع تسعير السلع بالدولار
        }
        
        # حساسية العملات للذهب (كملاذ آمن أو ارتباط إنتاج)
        self.gold_sensitivity = {
            "AUD": 0.7,   # منتجون رئيسيون للذهب
            "CAD": 0.3,
            "EUR": 0.4,   # الذهب كبديل أحياناً للعملات في الأزمات
            "JPY": 0.5,   # الذهب ملاذ آمن مثل الين
            "GBP": 0.1,
            "USD": -0.5,  # علاقة عكسية قوية بين الذهب والدولار الأمريكي
            "CHF": 0.4    # ملاذ آمن
        }

    def _get_commodity_trends(self):
        """ جلب اتجاهات النفط والذهب الحية عبر yfinance """
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
        except Exception as e:
            return {
                "oil_trend": "مستقر", "oil_change_pct": 0.0,
                "gold_trend": "مستقر", "gold_change_pct": 0.0
            }

    def analyze_commodity_impact(self, currency_pair: str) -> dict:
        """ 
        تحليل تأثير النفط والذهب على الزوج المحدد (Base/Quote)
        وإرجاع درجة تأثير مئوية ورقمية (-1 إلى +1) لتغذية نماذج الذكاء الاصطناعي.
        """
        try:
            base, quote = currency_pair.split('/')
        except:
            if "CAD" in currency_pair:
                base, quote = "USD", "CAD"
            elif "EUR" in currency_pair:
                base, quote = "EUR", "USD"
            else:
                base, quote = "GBP", "USD"

        trends = self._get_commodity_trends()
        
        oil_chg = trends["oil_change_pct"]
        gold_chg = trends["gold_change_pct"]
        
        base_oil_sens = self.oil_sensitivity.get(base, 0.0)
        quote_oil_sens = self.oil_sensitivity.get(quote, 0.0)
        
        base_gold_sens = self.gold_sensitivity.get(base, 0.0)
        quote_gold_sens = self.gold_sensitivity.get(quote, 0.0)
        
        oil_impact = (oil_chg * (base_oil_sens - quote_oil_sens)) / 100.0
        gold_impact = (gold_chg * (base_gold_sens - quote_gold_sens)) / 100.0
        
        total_commodity_score = round(max(min(oil_impact + gold_impact, 1.0), -1.0), 2)
        
        bias = "محايد"
        if total_commodity_score > 0.2:
            bias = "دعم سلعي لصعود الزوج (Bullish Commodity Impact)"
        elif total_commodity_score < -0.2:
            bias = "ضغط سلعي لهبوط الزوج (Bearish Commodity Impact)"

        return {
            "pair": currency_pair,
            "trends": trends,
            "commodity_score": total_commodity_score,
            "commodity_bias": bias
        }
