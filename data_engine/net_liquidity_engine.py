import yfinance as yf
import pandas as pd

class NetLiquidityEngine:
    def __init__(self):
        pass

    def get_net_liquidity_status(self) -> dict:
        """
        تقييم حالة سيولة البنوك المركزية وصافي تدفقاتها في النظام المالي
        """
        try:
            # استخدام مؤشر السيولة العامة أو متابعة أصول البنك المركزي كمؤشر مرجعي
            # مثل مؤشر السيولة العالمية أو حركة S&P / تتبع الميزانية
            fed_assets = yf.download("^GSPC", period="1mo", progress=False) # مؤشر تقريبي لتدفقات الأصول والسيولة
            
            if fed_assets.empty:
                return {"liquidity_bias": "محايد", "description": "سيولة البنوك المركزية مستقرة."}
            
            # حساب الزخم في تدفق السيولة عبر الأسواق
            start_price = float(fed_assets['Close'].iloc[0])
            end_price = float(fed_assets['Close'].iloc[-1])
            momentum = ((end_price - start_price) / start_price) * 100

            if momentum > 1.0:
                bias = "توسع سيولة البنوك المركزية (Liquidity Expansion - Bullish Risk)"
                description = f"السيولة الصافية في النظام تشهد توسعاً (مؤشر الزخم عند {momentum:.2f}%). يدعم الأصول والعملات الرئيسية ويضعف الضغط على الدولار."
            elif momentum < -1.0:
                bias = "انكماش سيولة البنوك المركزية (Liquidity Contraction - Bearish Risk)"
                description = f"السيولة الصافية تشهد انكماشاً وسحباً من النظام (مؤشر الزخم عند {momentum:.2f}%). بيئة ضاغطة على الأصول وتدعم الدولار كاش."
            else:
                bias = "سيولة محايدة (Neutral Liquidity)"
                description = "حالة تدفقات السيولة في نطاق عرضي ومستقر."

            return {
                "momentum": round(momentum, 2),
                "liquidity_bias": bias,
                "description": description
            }
        except Exception as e:
            return {"liquidity_bias": "محايد", "description": str(e)}
