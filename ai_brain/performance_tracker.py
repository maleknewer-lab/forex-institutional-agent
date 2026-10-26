import os
import json
import datetime
import pandas as pd
from typing import Dict, List
from data_engine.price_fetcher import PriceFetcher
from ai_brain.inference_memory import InferenceMemoryEngine

class PerformanceTracker:
    def __init__(self, log_path: str = "/content/drive/MyDrive/forex_institutional_agent/logs_and_backtest/history_db/trade_logs.json"):
        self.log_path = log_path
        self.price_fetcher = PriceFetcher()
        self.memory_engine = InferenceMemoryEngine()
        self._ensure_log_exists()

    def _ensure_log_exists(self):
        """التأكد من وجود سجل تتبع الصفقات والتوقعات"""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def log_prediction(self, currency_pair: str, decision_type: str, entry_price: float, target_price: float, stop_loss: float, reasoning_summary: str):
        """
        تسجيل توقع أو صفقة جديدة وقت حدوثها لتقييمها لاحقاً
        """
        prediction_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "pair": currency_pair,
            "decision": decision_type,
            "entry_price": entry_price,
            "target_price": target_price,
            "stop_loss": stop_loss,
            "reasoning": reasoning_summary,
            "status": "قيد التتبع (Pending)",
            "outcome": None
        }
        
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            logs.append(prediction_record)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=4)
            print(f"📝 تم تسجيل وتوثيق توقع جديد لـ {currency_pair} بنجاح.")
        except Exception as e:
            print(f"خطأ في تسجيل التوقع: {e}")

    def evaluate_past_predictions_with_time_travel(self):
        """
        العودة زمنياً للوراء (Backtracking) لفحص التوقعات السابقة ومقارنتها بالأسعار الفعلية التي حدثت لاحقاً
        """
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            
            updated = False
            for log in logs:
                if log["status"] == "قيد التتبع (Pending)":
                    pair = log["pair"]
                    df = self.price_fetcher.fetch_ohlcv(pair, interval="1h", period="7d")
                    if df.empty:
                        continue
                    
                    current_price = float(df['Close'].iloc[-1])
                    tp = log["target_price"]
                    sl = log["stop_loss"]
                    decision = log["decision"]

                    if decision == "بيع (Sell)":
                        if current_price <= tp:
                            log["status"] = "مكتمل (Completed)"
                            log["outcome"] = "نجح (Target Hit) - هبط السعر كما توقع الذكاء الاصطناعي."
                            updated = True
                        elif current_price >= sl:
                            log["status"] = "مكتمل (Completed)"
                            log["outcome"] = "فشل (Stop Loss Hit) - صعد السعر وضرب وقف الخسارة."
                            updated = True
                    elif decision == "شراء (Buy)":
                        if current_price >= tp:
                            log["status"] = "مكتمل (Completed)"
                            log["outcome"] = "نجح (Target Hit) - صعد السعر كما توقع الذكاء الاصطناعي."
                            updated = True
                        elif current_price <= sl:
                            log["status"] = "مكتمل (Completed)"
                            log["outcome"] = "فشل (Stop Loss Hit) - هبط السعر وضرب وقف الخسارة."
                            updated = True

                    if updated and log["status"] == "مكتمل (Completed)":
                        self._feedback_to_memory(log)

            if updated:
                with open(self.log_path, "w", encoding="utf-8") as f:
                    json.dump(logs, f, ensure_ascii=False, indent=4)
                print("🔄 تم إجراء المراجعة الزمنية الخلفية (Backtracking) وتحديث حلقة التعلم الذاتي بنجاح!")
            else:
                print("ℹ️ لا توجد توقعات جديدة بحاجة للتحديث الفوري حالياً.")
                
        except Exception as e:
            print(f"خطأ في مراجعة التوقعات الزمنية: {e}")

    def _feedback_to_memory(self, completed_log: Dict):
        new_lesson = {
            "scenario_id": f"AUTO_LEARNED_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "conditions": {
                "asset": completed_log["pair"],
                "decision_type": completed_log["decision"],
                "reasoning_context": completed_log["reasoning"]
            },
            "historical_outcome": completed_log["outcome"],
            "success_rate": 0.95 if "نجح" in completed_log["outcome"] else 0.10
        }
        self.memory_engine.save_new_scenario(new_lesson)
        print("✨ تعلم ذاتي: تم حفظ درس استدلالي جديد في الذاكرة بناءً على نتيجة التوقع السابق.")
