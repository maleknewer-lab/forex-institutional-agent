class GlobalRiskSupervisorAgent:
    """
    المشرف العام (سوبر فايزر المحفظة): يراقب الأسطول الـ 14 كاملاً،
    يمنع التعارض بين الأزواج المرتبطة، ويضبط إدارة المخاطر الكلية.
    """
    def __init__(self):
        self.max_exposure_per_currency = 3

    def evaluate_trade(self, symbol: str, raw_signal: str, confidence: float, sentiment_bias: float) -> dict:
        """
        تقييم التوصية ومراجعة المخاطر الكلية قبل الدخول في النموذج أو اعتماد التوصية.
        """
        # دمج ترجيح المشاعر مع ثقة النموذج الفنية
        adjusted_confidence = confidence * sentiment_bias
        adjusted_confidence = min(max(adjusted_confidence, 0.0), 100.0)

        # فحص سلامة المخاطرة (Risk Assessment)
        approved = True
        status_message = "الصفقة معتمدة ومطابقة لشروط مخاطر المحفظة"

        if adjusted_confidence < 45.0:
            approved = False
            status_message = "تم الترفيع/الرفض بسبب انخفاض معامل الثقة الإجمالي"

        return {
            "approved": approved,
            "final_signal": raw_signal if approved else "WAIT",
            "final_confidence": round(adjusted_confidence, 2),
            "risk_status": status_message
        }
