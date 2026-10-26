import yfinance as yf
import pandas as pd

class RiskRegimeEngine:
    def __init__(self):
        pass

    def get_market_risk_regime(self) -> dict:
        """
        تحديد حالة السوق الحالية: (Risk-On: شهية مخاطر مرتفعة) أو (Risk-Off: حالة هلع وتفضيل للملاذات الآمنة)
        بناءً على مؤشر التقلبات الأمريكي VIX (^VIX)
        """
        try:
            vix = yf.download("^VIX", period="1mo", progress=False)
            if vix.empty:
                return {"regime": "Neutral", "vix_level": 20.0, "bias": "محايد"}
            
            current_vix = float(vix['Close'].iloc[-1])
            prev_vix = float(vix['Close'].iloc[-5])
            vix_trend = current_vix - prev_vix

            # التصنيف المؤسسي لمؤشر التقلبات VIX:
            # VIX < 18-20 -> Risk-On (صالح لعملات السلع والأسهم)
            # VIX >= 20-25 -> Risk-Off (حالة هلع تدعم الدولار، الين، والذهب)
            if current_vix < 18.5:
                regime = "Risk-On (شهية مخاطر عالية)"
                description = f"مؤشر التقلبات منخفض عند {current_vix:.2f}. السيولة تتدفق نحو أصول المخاطرة والسلع."
            elif current_vix > 22.0:
                regime = "Risk-Off (حالة هلع / ملاذات آمنة)"
                description = f"مؤشر التقلبات مرتفع عند {current_vix:.2f}. الأسواق تشهد حذراً وتتجه نحو الملاذات الآمنة (USD, JPY, Gold)."
            else:
                regime = "Neutral (نطاق انتقالي)"
                description = f"مؤشر التقلبات مستقر عند {current_vix:.2f}."

            return {
                "regime": regime,
                "vix_level": round(current_vix, 2),
                "description": description
            }
        except Exception as e:
            return {"regime": "Neutral", "vix_level": 20.0, "description": str(e)}
