import ipywidgets as widgets
from IPython.display import display, HTML
from agents.master_agent import MasterInstitutionalAgent
import json
import os

class InstitutionalDashboard:
    def __init__(self):
        self.master_agent = MasterInstitutionalAgent()
        self.assets = [
            "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "NZD/USD", "USD/CHF",
            "EUR/GBP", "EUR/JPY", "GBP/JPY", "AUD/JPY", "EUR/AUD", "GBP/AUD", "EUR/CHF", "CHF/JPY",
            "XAU/USD", "XAG/USD"
        ]
        self.log_path = "/content/drive/MyDrive/forex_institutional_agent/logs_and_backtest/history_db/trade_logs.json"

    def _get_performance_metrics(self):
        if not os.path.exists(self.log_path):
            return {"total": 0, "completed": 0, "win_rate": 0.0}
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            completed = [l for l in logs if l.get("status") == "مكتمل (Completed)"]
            total_completed = len(completed)
            if total_completed == 0:
                return {"total": len(logs), "completed": 0, "win_rate": 0.0}
            wins = [l for l in completed if "نجح" in l.get("outcome", "")]
            win_rate = (len(wins) / total_completed) * 100
            return {"total": len(logs), "completed": total_completed, "win_rate": round(win_rate, 2)}
        except Exception:
            return {"total": 0, "completed": 0, "win_rate": 0.0}

    def render(self):
        title_widget = widgets.HTML(
            value="<h2 style='color: #1E3A8A; text-align: center; font-family: Tahoma;'>🏛️ لوحة تحكم صندوق التحوط المؤسسي (AI Global Macro Hedge Fund)</h2>"
        )
        
        metrics = self._get_performance_metrics()
        metrics_widget = widgets.HTML(
            value=f"""
            <div style="background: #E0E7FF; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-family: Tahoma; text-align: center;">
                <b>📊 مؤشرات دقة الذكاء الاصطناعي:</b> 
                إجمالي الصفقات: <b>{metrics['total']}</b> | 
                الصفقات المقيّمة: <b>{metrics['completed']}</b> | 
                ⭐ معدل النجاح الميداني (Win Rate): <span style="color: #16A34A; font-weight: bold;">{metrics['win_rate']}%</span>
            </div>
            """
        )
        
        dropdown = widgets.Dropdown(
            options=self.assets,
            value="XAU/USD",
            description="اختر الأصل:",
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px', height='40px')
        )
        
        button = widgets.Button(
            description="🔍 توليد التقرير الاستراتيجي الشامل",
            button_style='primary',
            layout=widgets.Layout(width='250px', height='40px', margin='0px 0px 0px 15px')
        )
        
        output = widgets.Output()

        def on_button_clicked(b):
            with output:
                output.clear_output()
                selected_asset = dropdown.value
                
                print(f"⏳ جاري تحليل الأسواق والبيانات الاقتصادية الكبرى (GDP & Rates) لـ {selected_asset}...")
                report = self.master_agent.synthesize_market_analysis(selected_asset)
                ai_decision = self.master_agent.generate_local_ai_decision(selected_asset)
                
                macro_info = report.get('macro_analysis', {})
                
                html_report = f"""
                <div style="background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #CBD5E1; font-family: Tahoma; direction: rtl; text-align: right;">
                    <h3 style="color: #0F172A; border-bottom: 2px solid #3B82F6; padding-bottom: 8px;">
                        📊 تقرير التحليل الشامل للأصل: <span style="color: #2563EB;">{report['target_pair']}</span>
                    </h3>
                    
                    <!-- 1. التحليل الاقتصادي الكلي والناتج المحلي -->
                    <div style="background: #ffffff; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-right: 5px solid #6366F1; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="color: #4338CA; margin-top: 0;">🌐 1. التحليل الاقتصادي الكلي (GDP Differentials & Interest Rates)</h4>
                        <p style="color: #334155; font-size: 14px;"><b>درجة التقييم الاقتصادي (Macro Score):</b> <span style="color: #4F46E5; font-weight: bold;">{macro_info.get('macro_score', 0.0)}</span></p>
                        <p style="color: #334155; font-size: 14px;"><b>الاتجاه الأساسي للهيكل:</b> {macro_info.get('fundamental_bias', 'محايد')}</p>
                        <p style="color: #334155; font-size: 14px;"><b>تقييم فوارق الناتج المحلي والفائدة:</b> دمج فارق نمو الـ GDP بفوارق تشديد/تيسير البنوك المركزية.</p>
                    </div>

                    <!-- 2. التحليل الفني -->
                    <div style="background: #ffffff; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-right: 5px solid #10B981; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="color: #065F46; margin-top: 0;">📈 2. التحليل الفني متعدد الأطر</h4>
                        <ul style="color: #334155; font-size: 14px; list-style-type: square;">
                            <li><b>فريم الساعة (1h):</b> {report['technical_trends'].get('1h', 'غير متوفر')}</li>
                            <li><b>فريم 4 ساعات (4h):</b> {report['technical_trends'].get('4h', 'غير متوفر')}</li>
                            <li><b>فريم اليومي (1d):</b> {report['technical_trends'].get('1d', 'غير متوفر')}</li>
                        </ul>
                    </div>

                    <!-- 3. مناطق SMC -->
                    <div style="background: #ffffff; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-right: 5px solid #F59E0B; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="color: #B45309; margin-top: 0;">💧 3. سيولة الفوليوم ومناطق الأموال الذكية (SMC)</h4>
                        <p style="color: #334155; font-size: 14px;"><b>السعر الفعلي الحالي:</b> <span style="color: #D97706; font-weight: bold;">{report['smc_structures'].get('current_market_price', 'غير متوفر')}</span></p>
                        <p style="color: #334155; font-size: 14px;"><b>منطقة الطلب المؤسسية:</b> {report['smc_structures'].get('dynamic_order_blocks', {}).get('bullish_demand_zone', 'غير متوفر')}</p>
                        <p style="color: #334155; font-size: 14px;"><b>منطقة العرض المؤسسية:</b> {report['smc_structures'].get('dynamic_order_blocks', {}).get('bearish_supply_zone', 'غير متوفر')}</p>
                    </div>

                    <!-- 4. التوصية الاستراتيجية -->
                    <div style="background: #EFF6FF; padding: 15px; border-radius: 8px; border-right: 5px solid #2563EB; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="color: #1E40AF; margin-top: 0;">🤖 4. التوصية الاستراتيجية الشاملة</h4>
                        <div style="background: #ffffff; padding: 12px; border-radius: 6px; color: #1E293B; font-size: 14px; white-space: pre-wrap; line-height: 1.6;">
                            {ai_decision}
                        </div>
                    </div>
                </div>
                """
                display(HTML(html_report))

        button.on_click(on_button_clicked)
        controls = widgets.HBox([dropdown, button])
        display(title_widget, metrics_widget, controls, output)
