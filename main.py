import os
import json
import sys
import time

PROJECT_ROOT = "/content/drive/MyDrive/forex_institutional_agent"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from agents.master_agent import MasterInstitutionalAgent
from ai_brain.performance_tracker import PerformanceTracker

def run_institutional_pipeline():
    print("🏛️ بدء تشغيل منظومة التداول المؤسسية المستقلة (Forex & Metals AI Agent)...")
    
    # تحميل ملف الأصول
    assets_path = os.path.join(PROJECT_ROOT, "config", "assets.json")
    if os.path.exists(assets_path):
        with open(assets_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            majors = config.get("forex_majors", ["EUR/USD"])
            metals = config.get("precious_metals", ["XAU/USD"])
            target_assets = majors[:3] + metals  # اختيار عينة تحليلية (الرئيسيات + الذهب) للتنفيذ السريع
    else:
        target_assets = ["EUR/USD", "XAU/USD"]

    master_agent = MasterInstitutionalAgent()
    tracker = PerformanceTracker()

    print(f"📊 جاري تحليل الأصول المستهدفة: {target_assets}\n" + "="*50)

    for asset in target_assets:
        print(f"\n🔍 فحص وتحليل الأصل: {asset}")
        
        # 1. توليد التحليل الشامل المجمع
        report = master_agent.synthesize_market_analysis(asset)
        
        print(f"   🔹 الاتجاهات الفنية: {report['technical_trends']}")
        print(f"   🔹 السعر الحالي ومناطق SMC: {report['smc_structures'].get('current_market_price', 'غير متوفر')} | {report['smc_structures'].get('dynamic_order_blocks', {})}")
        print(f"   🔹 السيناريو التاريخي المسترجع: {report['historical_analogue'].get('historical_outcome', 'لا يوجد')}")

        # 2. توليد القرار الذكي عبر نموذج علام / Ollama
        ai_decision = master_agent.generate_local_ai_decision(asset)
        print(f"   🤖 التوصية الاستراتيجية للذكاء الاصطناعي:\n{ai_decision[:350]}...")

        # 3. توثيق توقع تجريبي لتفعيل حلقة التعلم
        current_price = report['smc_structures'].get('current_market_price', 1.0)
        if current_price > 1.0:
            tracker.log_prediction(
                currency_pair=asset,
                decision_type="بيع (Sell)",
                entry_price=current_price,
                target_price=current_price * 0.99,
                stop_loss=current_price * 1.01,
                reasoning_summary=f"تحليل آلي مؤسسي بناءً على هيكل 4h ومناطق العرض لـ {asset}"
            )

    print("\n" + "="*50)
    print("⏳ تشغيل حلقة المراجعة الزمنية الخلفية (Backtracking & Self-Learning Loop)...")
    tracker.evaluate_past_predictions_with_time_travel()
    print("✅ تم الانتهاء من دورة العمل بنجاح تام!")

if __name__ == "__main__":
    run_institutional_pipeline()
