import datetime
from data_engine.macro_historical_engine import MacroHistoricalEngine
from data_engine.commodity_correlation_engine import CommodityCorrelationEngine

class MacroCommodityAgent:
    """
    وكيل الماكرو والسلع (Macro & Commodity Agent):
    يجمع بين البيانات الأساسية للناتج المحلي الإجمالي، الفائدة، والارتباطات بالذهب والنفط
    لكل زوج عملات، ويوفر تقييماً رقمياً متكاملاً يغذّي وكيل القرار الفردي ونموذج XGBoost.
    """
    def __init__(self):
        self.macro_engine = MacroHistoricalEngine()
        self.commodity_engine = CommodityCorrelationEngine()

    def evaluate(self, currency_pair: str, current_date: datetime.datetime = None) -> dict:
        if current_date is None:
            current_date = datetime.datetime.now()
            
        # 1. جلب تحليل الماكرو (GDP، الفائدة، الأزمات)
        macro_data = self.macro_engine.get_macro_score(currency_pair, current_date)
        
        # 2. جلب تأثير السلع (الذهب والنفط)
        commodity_data = self.commodity_engine.analyze_commodity_impact(currency_pair)
        
        # 3. دمج النتائج في مخرج موحد
        macro_score = macro_data.get("macro_score", 0.0)
        commodity_score = commodity_data.get("commodity_score", 0.0)
        
        # وزنية الدمج: 60% للماكرو الأساسي و 40% لارتباطات السلع
        combined_score = round((macro_score * 0.6) + (commodity_score * 0.4), 2)
        
        bias = "محايد (Neutral)"
        if combined_score > 0.2:
            bias = "إيجابي مؤسسي (Bullish Macro-Commodity Bias)"
        elif combined_score < -0.2:
            bias = "سلبي مؤسسي (Bearish Macro-Commodity Bias)"

        return {
            "pair": currency_pair,
            "macro_details": macro_data,
            "commodity_details": commodity_data,
            "combined_score": combined_score,
            "macro_commodity_bias": bias
        }
