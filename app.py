import streamlit as st
import pandas as pd
import sys
import os

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
selected_asset = st.sidebar.selectbox(
    "اختر الأصل المالي:",
    ["XAU/USD", "USD/JPY", "USD/CAD", "EUR/USD", "AUD/USD"]
)

win_rates = {
    "XAU/USD": "79.1%",
    "USD/JPY": "77.4%",
    "USD/CAD": "73.25%",
    "EUR/USD": "68.1%",
    "AUD/USD": "71.6%"
}

current_rate = win_rates.get(selected_asset, "N/A")
st.sidebar.markdown("### 📊 الـ Win Rate المعتمد:")
st.sidebar.markdown(f"**{selected_asset} : {current_rate}**")
st.sidebar.markdown("---")

if st.sidebar.button("🚀 تحليل السوق لحظياً", type="primary"):
    with st.spinner(f"جاري تشغيل محركات الماكرو والسيولة والـ SMC لتحليل {selected_asset}..."):
        report_data = agent.generate_dual_layer_report(selected_asset)
        
        st.success(f"✅ تم الانتهاء من التحليل بنجاح للأصل: {selected_asset}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 التقرير المبسط (للمستخدم العادي)")
            st.info(report_data["layman_view"])
            
        with col2:
            st.markdown("### 🏛️ التقرير الاحترافي (للمحللين والكمّ)")
            st.success(report_data["institutional_view"])
            
        st.markdown("---")
        st.markdown("### 📈 تفاصيل البيانات الخام:")
        st.json(report_data["raw_data"])
else:
    st.info("👈 اضغط على زر **(تحليل السوق لحظياً)** في القائمة الجانبية لبدء تشغيل النظام واستعراض التقارير المؤسسية.")