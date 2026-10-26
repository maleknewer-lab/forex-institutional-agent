import sys
import os

class FundamentalAgent:
    def __init__(self):
        from data_engine.news_fetcher import NewsEngine
        self.news_engine = NewsEngine()

    def evaluate_fundamentals(self, currency_pair: str) -> dict:
        base_currency, quote_currency = currency_pair.split("/")
        events = self.news_engine.get_scheduled_events(currency_pair)
        rate_analysis = self.news_engine.analyze_interest_rate_expectations(base_currency, quote_currency)
        
        summary_notes = []
        for event in events:
            if "أسعار الفائدة" in event["event_name"]:
                curr = float(event["current_rate"].replace("%", ""))
                exp = float(event["expected_rate"].replace("%", ""))
                if exp < curr:
                    summary_notes.append(f"توقعات خفض الفائدة لـ {base_currency} تضغط سلباً على العملة (Dovish).")
                else:
                    summary_notes.append(f"توقعات رفع/تثبيت الفائدة لـ {base_currency} تدعم العملة (Hawkish).")
            
            if "CPI" in event["event_name"]:
                prev = float(event["previous_value"].replace("%", ""))
                fore = float(event["forecast_value"].replace("%", ""))
                if fore < prev:
                    summary_notes.append(f"تباطؤ التضخم لـ {quote_currency} قد يدفع الفيدرالي/البنك لتخفيف سياسته.")

        evaluation_report = {
            "pair": currency_pair,
            "events_schedule": events,
            "interest_rate_analysis": rate_analysis,
            "key_insights": summary_notes,
            "fundamental_bias": "محايد (Neutral)"
        }
        return evaluation_report
