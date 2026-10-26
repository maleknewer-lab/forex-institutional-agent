import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agents.master_agent import MasterInstitutionalAgent

# إعداد الصفحة وتوسيع العرض
st.set_page_config(
    page_title="Global Macro Quant Trading System",
    page_icon="🏛️",
    layout="wide"
)

@st.cache_resource
def load_agent():
    return MasterInstitutionalAgent()

agent = load_agent()

# العنوان الرئيسي مع تنسيق أنيق
st.title("🏛️ منصة التداول الكمي المؤسسي (Global Macro Quant)")
st.markdown("---")

# القائمة الجانبية (Sidebar)
st.sidebar.header("🎛️ لوحة التحكم وإعدادات التحليل")

supported_assets = [
    "XAU/USD", "XAG/USD",
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD",
    "EUR/GBP", "EUR/JPY", "GBP/JPY", "EUR/AUD", "AUD/JPY",
    "BTC/USD"
]

selected_asset = st.sidebar.selectbox("🎯 اختر الأصل المالي:", supported_assets)
selected_timeframe = st.sidebar.selectbox("⏱️ الإطار الزمني للتحليل:", ["H1", "H4", "Daily", "Weekly"])

win_rates = {
    "XAU/USD": "79.1%", "XAG/USD": "76.8%", "EUR/USD": "68.1%", "GBP/USD": "70.4%",
    "USD/JPY": "77.4%", "USD/CHF": "67.5%", "AUD/USD": "71.6%", "NZD/USD": "69.2%",
    "USD/CAD": "73.25%", "EUR/GBP": "66.9%", "EUR/JPY": "74.2%", "GBP/JPY": "75.8%",
    "EUR/AUD": "69.5%", "AUD/JPY": "72.1%", "BTC/USD": "81.3%"
}

current_rate = win_rates.get(selected_asset, "N/A")
st.sidebar.markdown("### 📊 نسبة النجاح (Win Rate):")
st.sidebar.info(f"**{selected_asset} : {current_rate}**")
st.sidebar.markdown("---")

analyze_button = st.sidebar.button("🚀 تشغيل التحليل اللحظي", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **النظام:** تحليل مؤسسي هجين (Macro + SMC)")

# منطقة العرض الرئيسية
if analyze_button:
    with st.spinner(f"جاري تشغيل محركات الماكرو والسيولة والـ SMC للأصل {selected_asset} على فريم {selected_timeframe}..."):
        report_data = agent.generate_dual_layer_report(selected_asset, selected_timeframe)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"✅ تم الانتهاء من التحليل بنجاح للأصل: **{selected_asset}** | الإطار الزمني: **{selected_timeframe}** | 🕒 {current_time} GMT")
        
        # تقسيم الشاشة إلى عمودين منظمين تماماً
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 التقرير المبسط (للمستخدم العادي)")
            # استخدام container لتشكيل صندوق بطاقة أنيق
            with st.container(border=True):
                st.markdown(report_data["layman_view"])
            
        with col2:
            st.markdown("### 🏛️ التقرير الاحترافي (للمحللين والكمّ)")
            with st.container(border=True):
                st.markdown(report_data["institutional_view"])
            
        st.markdown("---")
        
        # البيانات الخام للمطورين داخل صندوق قابل للطي
        with st.expander("📈 تفاصيل البيانات الخام والبرمجية (Raw Data - للمتدربين والمطورين)"):
            st.json(report_data["raw_data"])
else:
    # شاشة الترحيب قبل الضغط على الزر
    st.info("👈 يرجى اختيار الأصل المالي والإطار الزمني من القائمة الجانبية، ثم الضغط على زر **(تشغيل التحليل اللحظي)** لاستعراض التقارير.")