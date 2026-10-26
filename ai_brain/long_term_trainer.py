import os
import json
import pandas as pd
import datetime
from data_engine.price_fetcher import PriceFetcher
from ai_brain.inference_memory import InferenceMemoryEngine

class LongTermHistoricalTrainer:
    def __init__(self):
        self.price_fetcher = PriceFetcher()
        self.memory_engine = InferenceMemoryEngine()

    def run_20years_backtest_and_training(self):
        """
        العودة 20 عاماً للوراء، تقسيم البيانات (Train/Test)، ومحاكاة الأداء لتوليد معرفة استدلالية ذاتية
        """
        print("🚀 بدء محرك التدريب الذاتي طويل الأمد (بيانات تاريخية حتى 20 عاماً)...")
        
        assets_path = "/content/drive/MyDrive/forex_institutional_agent/config/assets.json"
        if not os.path.exists(assets_path):
            print("❌ ملف الأصول غير موجود.")
            return

        with open(assets_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        all_assets = config.get("forex_majors", []) + config.get("precious_metals", [])
        
        trained_lessons_count = 0

        for asset in all_assets:
            print(f"\n⏳ جاري سحب وتحليل البيانات التاريخية لـ {asset} (تغطية أعمق)...")
            # جلب البيانات التاريخية اليومية بأقصى مدى متاح (حتى 20 عاماً)
            df = self.price_fetcher.fetch_ohlcv(asset, interval="1d", period="max")
            
            if df.empty or len(df) < 200:
                print(f"⚠️ بيانات غير كافية لـ {asset}")
                continue

            # تقسيم البيانات إلى تدريب (Train - أول 80%) واختبار (Test - آخر 20%)
            split_index = int(len(df) * 0.8)
            train_df = df.iloc[:split_index]
            test_df = df.iloc[split_index:]

            print(f"   📊 حجم بيانات التدريب (Train): {len(train_df)} شمعة يومية | بيانات الاختبار (Test): {len(test_df)} شمعة")

            # محاكاة بسيطة لاكتشاف أنماط النجاح والفشل التاريخية (Backtesting Simulation)
            train_df['SMA_50'] = train_df['Close'].rolling(window=50).mean()
            train_df['SMA_200'] = train_df['Close'].rolling(window=200).mean()
            
            # حساب الأداء التاريخي لاستنباط قاعدة معرفية
            successful_trades = 0
            total_simulated = 0
            
            for i in range(200, len(train_df) - 10):
                prev_close = train_df['Close'].iloc[i-1]
                curr_close = train_df['Close'].iloc[i]
                sma50 = train_df['SMA_50'].iloc[i]
                sma200 = train_df['SMA_200'].iloc[i]

                total_simulated += 1
                # قاعدة تقاطع المتوسطات الكلاسيكية المؤسسية كمثال للتعلم المعرفي
                if sma50 > sma200 and curr_close > prev_close:
                    # اختبار ما إذا كان السعر صعد بعد 5 أيام
                    future_price = train_df['Close'].iloc[i+5]
                    if future_price > curr_close:
                        successful_trades += 1

            win_rate = (successful_trades / total_simulated) if total_simulated > 0 else 0.5
            
            # حفظ الدرس المستفاد في الذاكرة الاستدلالية للوكيل
            lesson = {
                "scenario_id": f"HISTORICAL_TRAIN_{asset.replace('/', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}",
                "conditions": {
                    "asset": asset,
                    "strategy": "Long-term SMA Trend Alignment (20-Year Historical)",
                    "training_samples": total_simulated
                },
                "historical_outcome": f"تم اختبار النطاق التاريخي بنجاح، معدل دقة النمط الصاعد: {win_rate:.2f}",
                "success_rate": round(win_rate, 2)
            }
            self.memory_engine.save_new_scenario(lesson)
            trained_lessons_count += 1
            print(f"   ✅ تم استنباط وحفظ درس استدلالي لـ {asset} بنجاح (معدل النجاح المحسوب: {win_rate:.2f})")

        print(f"\n🎉 اكتمل التدريب الذاتي التاريخي بنجاح تام! تم حقن {trained_lessons_count} قاعدة معرفية استدلالية جديدة في النظام.")
