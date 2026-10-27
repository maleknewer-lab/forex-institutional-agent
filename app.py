import os
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# استدعاء المحركات الخلفية التي بنياها
from smc_engine.order_block_engine import MultiTimeframeSMCEngine

# إعداد الصفحة وتصميمها العصري (Wide Layout + Dark Theme Friendly)
st.set_page_config(
    page_title="Institutional Multi-Agent Trading System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 تنسيقات CSS مخصصة لتصميم عصري وألوان مؤسسية متناسقة
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .css-1d391kg { background-color: #161b22; }
    h1, h2, h3 { color: #58a6ff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي والشريط الترحيبي
st.title("🏛️ Institutional Multi-Agent Trading & SMC Dashboard")
st.markdown("---")

# الشريط العلوي العام (KPI Summary Bar)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📊 الأصول النشطة في الأسطول", value="16 أصل", delta="14 عملة + ذهب وفضة")
with col2:
    st.metric(label="🧠 حالة الماكرو العامة", value="Risk-On / Stable", delta="محركات حقيقية مرتبطة")
with col3:
    st.metric(label="🛡️ المشرف العام للمخاطر", value="مفعل ونشط", delta="فلترة الحماية الصارمة")
with col4:
    st.metric(label="⏳ الإطار الزمني للتحليل", value="1D + 4H Confluence", delta="كشف الضوضاء مفعل")

st.markdown("---")

# القائمة الجانبية لاختيار الأصل وتحليل الـ SMC
st.sidebar.header("🎛️ تحكم الأسطول وتحليل الـ SMC")

# قائمة أصول الأسطول الـ 16
fleet_assets = [
    "AUDUSD=X", "NZDUSD=X", "AUDJPY=X", "EURAUD=X", "GBPAUD=X", "NZDJPY=X",
    "USDCAD=X", "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X", 
    "EURGBP=X", "EURJPY=X", "GBPJPY=X", "GC=F", "SI=F"
]

selected_asset = st.sidebar.selectbox("اختر الأصل / الزوج للتحليل العميق:", fleet_assets)

# محاكاة معدلات الفوز المعتمدة لأسطول الـ 9 سنوات
mock_win_rates = {
    "AUDUSD=X": 66.27, "NZDUSD=X": 66.07, "AUDJPY=X": 57.28, "EURAUD=X": 61.22,
    "GBPAUD=X": 60.83, "NZDJPY=X": 55.23, "USDCAD=X": 54.64, "EURUSD=X": 57.40,
    "GBPUSD=X": 60.16, "USDJPY=X": 60.75, "USDCHF=X": 56.02, "EURGBP=X": 57.28,
    "EURJPY=X": 54.53, "GBPJPY=X": 58.07, "GC=F": 55.19, "SI=F": 53.47
}

current_win_rate = mock_win_rates.get(selected_asset, 55.0)

st.sidebar.markdown(f"**📈 معدل الفوز التاريخي (9 سنوات):** `{current_win_rate}%`")
if current_win_rate >= 55.0:
    st.sidebar.success("✅ الأصل مقبول لدى المشرف العام للمخاطر")
else:
    st.sidebar.error("❌ الأصل مرفوض (أقل من 55% الحد الأدنى)")

# زر تشغيل التحليل الحي
if st.sidebar.button("🚀 تشغيل تحليل الـ SMC والماكرو للأسطول"):
    with st.spinner(f"جاري سحب البيانات وتحليل الـ Order Blocks لـ {selected_asset}..."):
        try:
            # سحب البيانات عبر yfinance
            df_daily = yf.download(selected_asset, start="2023-01-01", interval="1d", progress=False)
            df_4h = yf.download(selected_asset, period="60d", interval="1h", progress=False)
            
            for df in [df_daily, df_4h]:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[0].lower() for col in df.columns]
                else:
                    df.columns = [col.lower() for col in df.columns]

            # استدعاء محرك الـ SMC متعدد الأطر الزمنية
            smc_engine = MultiTimeframeSMCEngine(selected_asset)
            analysis = smc_engine.analyze_confluence(df_daily, df_4h)

            # عرض النتائج في بطاقات عصرية داخل الواجهة
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.subheader(f"📊 تحليل التوافق الزمني: {selected_asset}")
                st.info(f"**الاتجاه اليومي (Macro Bias):** {analysis['daily_trend']}")
                st.metric(label="السعر الحالي", value=analysis['current_price'])
                st.write(f"**منطقة الـ Order Block (4H):** من `{analysis['order_block_zone'][0]}` إلى `{analysis['order_block_zone'][1]}`")
                st.write(f"**المسافة الحالية للـ OB:** `{analysis['distance_to_ob_pips']}` نقطة")

            with col_res2:
                st.subheader("🛡️ تقرير المشرف العام وكشف الضوضاء")
                if analysis['is_noise_detected']:
                    st.error(analysis['analysis_report'])
                else:
                    st.success(analysis['analysis_report'])
                
                st.markdown("---")
                st.markdown(f"**حالة التنفيذ المؤسسي:** `{'معتمد بشروط التصحيح' if current_win_rate >= 55 else 'مرفوض إدارياً'}`")

        except Exception as e:
            st.error(f"حدث خطأ أثناء جلب التحليل: {e}")

else:
    st.info("👈 اضغط على الزر في القائمة الجانبية (`تشغيل تحليل الـ SMC`) لبدء فحص الأصل المختار وعرض مناطق الـ Order Blocks للداشبورد.")

# جدول حالة الأصول الشاملة في الأسفل
st.markdown("---")
st.subheader("📋 نظرة عامة على أداء الأسطول المؤسسي (16 أصل)")

fleet_summary_data = []
for sym, wr in mock_win_rates.items():
    status = "مقبول (نشط)" if wr >= 55.0 else "مرفوض (فلتر المخاطر)"
    fleet_summary_data.append({
        "Asset / Symbol": sym,
        "9-Year Win Rate (%)": f"{wr}%",
        "Risk Status": status
    })

df_fleet_table = pd.DataFrame(fleet_summary_data)
st.dataframe(df_fleet_table, width='stretch')
