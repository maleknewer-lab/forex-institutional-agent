class AssetSentimentAgent:
    """
    وكيل المشاعر والماكرو: يحلل الأخبار الفورية الخاصة بالزوج
    ويستخرج معامل ترجيح المعنويات (Sentiment Score & Bias Multiplier).
    """
    def __init__(self, symbol: str):
        self.symbol = symbol

    def analyze_sentiment(self) -> dict:
        # يمكن دمج محرك الأخبار news_fetcher هنا مستقبلاً
        # حالياً نحسب انحياز المشاعر بناءً على سياق الزوج
        sentiment_score = 0.65  # مؤشر محايد إلى إيجابي افتراضي

        # أمثلة لسياق الأصول:
        if "GOLD" in self.symbol:
            sentiment_score = 0.75  # ملاذ آمن
        elif "JPY" in self.symbol:
            sentiment_score = 0.55  # شديد الحساسية للفائدة

        return {
            "symbol": self.symbol,
            "sentiment_score": sentiment_score,
            "bias": "BULLISH" if sentiment_score > 0.5 else "BEARISH",
            "multiplier": 1.1 if sentiment_score > 0.7 else (0.9 if sentiment_score < 0.3 else 1.0)
        }
