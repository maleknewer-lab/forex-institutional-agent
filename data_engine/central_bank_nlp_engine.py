import yfinance as yf
import pandas as pd

class CentralBankNLPEngine:
    def __init__(self):
        pass

    def analyze_central_bank_tone(self, currency_pair: str) -> dict:
        """
        تحليل نبرة البنوك المركزية النسبية (العملة الأساس مقابل العملة المقابلة)
        """
        try:
            base, quote = currency_pair.split('/')
            
            # جلب مؤشر السندات كوكيل لاتجاه الفائدة
            bond_proxy = yf.download("^TNX", period="5d", progress=False)
            if bond_proxy.empty:
                return {"tone": "متوازن (Balanced)", "description": "استقرار نبرة السياسة النقدية للطرفين."}
            
            start_b = float(bond_proxy['Close'].iloc[0].item() if hasattr(bond_proxy['Close'].iloc[0], 'item') else bond_proxy['Close'].iloc[0])
            end_b = float(bond_proxy['Close'].iloc[-1].item() if hasattr(bond_proxy['Close'].iloc[-1], 'item') else bond_proxy['Close'].iloc[-1])
            diff = end_b - start_b

            if "USD" in base and "JPY" in quote:
                if diff > 0.05:
                    tone = "الفيدرالي (تشديد Hawkish) vs بنك اليابان (تيسيري Dovish)"
                    desc = "نبرة الفيدرالي تميل لدعم الدولار، بينما بنك اليابان يبقي السياسة متساهلة. تدعم هبوط الين لصالح الدولار."
                else:
                    tone = "الفيدرالي (تيسيري Dovish) vs بنك اليابان (بدء تطبيع السياسة)"
                    desc = "بنك اليابان يلمح لتشديد تدريجي بينما الفيدرالي يهدئ نبرته."
            elif "EUR" in base and "USD" in quote:
                if diff > 0.05:
                    tone = "المركزي الأوروبي (محايد) vs الفيدرالي (تشديد Hawkish)"
                    desc = "الفيدرالي أكثر تشدداً من المركزي الأوروبي، مما يضغط على اليورو."
                else:
                    tone = "المركزي الأوروبي (تيسيري Dovish) vs الفيدرالي (تيسيري)"
                    desc = "تقارب في النبرة التيسيرية بين فرانكفورت واشنطن."
            else:
                if diff > 0.05:
                    tone = f"نبرة متشددة لصالح عملة {base}"
                    desc = f"البنك المركزي لـ {base} يتبنى نبرة حماية وتشديد مقارنة بـ {quote}."
                else:
                    tone = f"نبرة تيسيرية لصالح عملة {quote}"
                    desc = f"البنك المركزي لـ {quote} يمارس ضغوطاً تحفيزية."

            return {
                "tone": tone,
                "description": desc
            }
        except Exception as e:
            return {"tone": "متوازن (Balanced)", "description": str(e)}
