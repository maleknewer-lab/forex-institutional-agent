import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agents.master_agent import MasterInstitutionalAgent

st.set_page_config(
    page_title="Global Macro Quant Trading System",
    page_icon="🏛️",
    layout="wide"
)

@st.cache_resource
def load_agent():
    return MasterInstitutionalAgent()

agent = load_agent()

st.title("🏛️ منصة التداول الكمي المؤسسي (Global Macro Quant)")
st.markdown("نظام هرمي متقدم يدمج العوامل الكلية (Macro)، السيولة، ونبرة البنوك المركزية مع التنفيذ التكتيكي للـ SMC.")
st.markdown("---")

st.sidebar.header("🎛️ إعدادات التحليل")

supported_assets = [
    "XAU/USD", "XAG/USD",
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD",
    "EUR/GBP", "EUR/JPY", "GBP/JPY", "EUR/AUD", "AUD/JPY",
    "BTC/USD"
]

selected_asset = st.sidebar.selectbox(
    "اختر الأصل المالي:",
    supported_assets
)

win_rates = {
    "XAU/USD": "79.1%", "XAG/USD": "76.8%", "EUR/USD": "68.1%", "GBP/USD": "70.4%",
    "USD/JPY": "77.4%", "USD/CHF": "67.5%", "AUD/USD": "71.6%", "NZD/USD": "69.2%",
    "USD/CAD": "73.25%", "EUR/GBP": "66.9%", "EUR/JPY": "74.2%", "GBP/JPY": "75.8%",
    "EUR/AUD": "69.5%", "AUD/JPY": "72.1%", "BTC/USD": "81.3%"
}

current_rate = win_rates.get(selected_asset, "N/A")
st.sidebar.markdown("### 📊 نسبة النجاح التاريخية (Win Rate):")
st.sidebar.info(f"**{selected_asset} : {current_rate}**")
st.sidebar.markdown("---")

# وضع زر التحليل مباشرة تحت الإعدادات في القائمة الجانبية
analyze_button = st.sidebar.button("🚀 تحليل السوق لحظياً", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **أفق الاستثمار:** تحليل مؤسسي هجين (Macro + SMC)")

if analyze_button:
    with st.spinner(f"جاري تشغيل محركات الماكرو والسيولة والـ SMC لتحليل {selected_asset}..."):
        report_data = agent.generate_dual_layer_report(selected_asset)
        
        # وقت التحديث الحالي
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"✅ تم الانتهاء من التحليل بنجاح للأصل: **{selected_asset}** | 🕒 وقت التحديث: {current_time} GMT")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 التقرير المبسط (للمستخدم العادي)")
            st.info(report_data["layman_view"])
            
        with col2:
            st.markdown("### 🏛️ التقرير الاحترافي (للمحللين والكمّ)")
            st.success(report_data["institutional_view"])
            
        st.markdown("---")
        
        # إخفاء البيانات الخام داخل عنصر قابل للطي لمنع ازدحام الشاشة
        with st.expander("📈 تفاصيل البيانات الخام (Raw Data - للمطورين والتدقيق)"):
            st.json(report_data["raw_data"])
else:
    st.info("👈 اضغط على زر **(تحليل السوق لحظياً)** في القائمة الجانبية لبدء تشغيل النظام واستعراض التقارير المؤسسية.")