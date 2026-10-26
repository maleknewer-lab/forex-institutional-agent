import os
import json
from typing import Dict, List, Optional

class InferenceMemoryEngine:
    def __init__(self, db_path: str = "/content/drive/MyDrive/forex_institutional_agent/logs_and_backtest/history_db/scenarios.json"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """التأكد من وجود قاعدة بيانات السيناريوهات التاريخية"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            # إنشاء بيانات تاريخية افتراضية للمحاكاة (مثل سيناريو رفع الفائدة قبل 5 سنوات)
            initial_scenarios = [
                {
                    "scenario_id": "HIST_2021_EURUSD_RATE_HIKE",
                    "conditions": {
                        "base_interest_trend": "تشديد (Hawkish)",
                        "quote_interest_trend": "تيسير (Dovish)",
                        "geopolitical_state": "سلم وتضخم مرتفع",
                        "trend_context": "هابط رئيسي على 4H مع تصحيح صاعد"
                    },
                    "historical_outcome": "ارتد السعر من مقاومة قوية مؤقتاً ثم استأنف الهبوط الحاد بقوة مع تفوق الدولار.",
                    "success_rate": 0.88
                }
            ]
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(initial_scenarios, f, ensure_ascii=False, indent=4)

    def find_similar_historical_scenario(self, current_conditions: Dict) -> Optional[Dict]:
        """
        البحث في الذاكرة الاستدلالية عن سيناريو تاريخي يطابق أو يشابه الظروف الحالية
        """
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                scenarios = json.load(f)
            
            # محاكاة مطابقة بسيطة وذكية للظروف (يمكن تطويرها لاحقاً لتعمل بـ Vector Embeddings)
            for scenario in scenarios:
                cond = scenario["conditions"]
                # إذا تشابهت بعض المعطيات الأساسية
                if cond.get("geopolitical_state") == current_conditions.get("geopolitical_state"):
                    return scenario
            
            return scenarios[0] # إرجاع أقرب سيناريو افتراضي كمرجع
        except Exception as e:
            print(f"خطأ في قراءة الذاكرة الاستدلالية: {e}")
            return None

    def save_new_scenario(self, scenario_data: Dict):
        """حفظ سيناريو وناتج جديد للتعلم الذاتي المستقبلي"""
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                scenarios = json.load(f)
            scenarios.append(scenario_data)
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(scenarios, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"خطأ في حفظ السيناريو الجديد: {e}")
