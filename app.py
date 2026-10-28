import os
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# استدعاء محركات النظام والوكلاء
from smc_engine.order_block_engine import MultiTimeframeSMCEngine
try:
    from agents.risk_supervisor import RiskSupervisor
except ImportError:
    RiskSupervisor = None

# إعداد الصفحة وتصميمها
st.set_page_config(
    page_title="Institutional Multi-Agent Trading System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 تنسيقات CSS للمستطيلات المتتالية (Sequential Cards Layout)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans Arabic', sans-serif;
    }
    .main { background-color: #0c1422; color: #e8eef9; }
    
    .hero-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 20px;
        margin-bottom: 25px;
        flex-wrap: wrap;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f0b84a;
        margin-bottom: 5px;
    }
    .hero-sub {
        color: #93a4bf;
        font-size: 1.05rem;
    }
    
    /* تصميم المستطيلات المتتالية */
    .card-section {
        background: #141f33;
        border: 1px solid #243452;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.35);
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f0b84a;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* شريط التوافق */
    .gauge-bar {
        height: 12px;
        border-radius: 99px;
        background: linear-gradient(90deg, #ff6b73 0%, #d99a1c 50%, #2dd4a0 100%);
        position: relative;
        margin: 20px 0 12px 0;
    }
    .gauge-pointer {
        position: absolute;
        top: 50%;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: #141f33;
        border: 4px solid #ffffff;
        transform: translate(-50%, -50%);
    }
    .gauge-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #93a4bf;
        font-weight: 600;
    }
    .signal-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .bg-strong-buy { background: rgba(45, 212, 160, 0.2); color: #2dd4a0; border: 1px solid #2dd4a0; }
    .bg-buy { background: rgba(45, 212, 160, 0.15); color: #2dd4a0; }
    .bg-neutral { background: rgba(217, 154, 28, 0.2); color: #f0b84a; }
    .bg-sell { background: rgba(255, 107, 115, 0.15); color: #ff6b73; }
    .bg-strong-sell { background: rgba(255, 107, 115, 0.2); color: #ff6b73; border: 1px solid #ff6b73; }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }
    .metric-box {
        background: #1b2942;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #243452;
    }
    .metric-label { font-size: 0.85rem; color: #93a4bf; }
    .metric-val { font-size: 1.2rem; font-weight: 700; color: #e8eef9; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# قائمة الأصول
fleet_assets = {
    "EURUSD=X": ("EUR/USD", "FX:EURUSD"),
    "GBPUSD=X": ("GBP/USD", "FX:GBPUSD"),
    "USDJPY=X": ("USD/JPY", "FX:USDJPY"),
    "AUDUSD=X": ("AUD/USD", "FX:AUDUSD"),
    "USDCAD=X": ("USD/CAD", "FX:USDCAD"),
    "USDCHF=X": ("USD/CHF", "FX:USDCHF"),
    "NZDUSD=X": ("NZD/USD", "FX:NZDUSD"),
    "EURGBP=X": ("EUR/GBP", "FX:EURGBP"),
    "EURJPY=X": ("EUR/JPY", "FX:EURJPY"),
    "GBPJPY=X": ("GBP/JPY", "FX:GBPJPY"),
    "AUDJPY=X": ("AUD/JPY", "OANDA:AUDJPY"),
    "EURAUD=X": ("EUR/AUD", "OANDA:EURAUD"),
    "GBPAUD=X": ("GBP/AUD", "OANDA:GBPAUD"),
    "NZDJPY=X": ("NZD/JPY", "OANDA:NZDJPY"),
    "GC=F": ("الذهب (Gold)", "OANDA:XAUUSD"),
    "SI=F": ("الفضة (Silver)", "OANDA:XAGUSD")
}

# ترويسة الصفحة وقائمة الاختيار
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
col_title, col_picker = st.columns([2, 1])

with col_title:
    st.markdown('<div class="hero-title">🏛️ Institutional Multi-Agent Trading & SMC Terminal</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">منصة التداول المؤسسي — نظام المستطيلات المتتالية وتحليل وكيل إدارة المخاطر.</div>', unsafe_allow_html=True)

with col_picker:
    selected_symbol = st.selectbox(
        "اختر زوج العملة / الأصل:",
        options=list(fleet_assets.keys()),
        format_func=lambda x: f"{fleet_assets[x][0]} ({x})"
    )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

display_name, tv_symbol = fleet_assets[selected_symbol]

# سحب البيانات والتحليل
@st.cache_data(ttl=300)
def fetch_analysis_data(symbol):
    try:
        df_daily = yf.download(symbol, period="1y", interval="1d", progress=False, auto_adjust=False)
        df_4h = yf.download(symbol, period="60d", interval="1h", progress=False, auto_adjust=False)
        
        for df in [df_daily, df_4h]:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0].lower() for col in df.columns]
            else:
                df.columns = [col.lower() for col in df.columns]

        smc_engine = MultiTimeframeSMCEngine(symbol)
        analysis = smc_engine.analyze_confluence(df_daily, df_4h)
        return analysis, df_daily
    except Exception as e:
        return None, None

analysis, df_daily = fetch_analysis_data(selected_symbol)

if analysis is not None:
    daily_bias = analysis.get("daily_trend", "محايد")
    dist_pips = analysis.get("distance_to_ob_pips", 0)
    is_noise = analysis.get("is_noise_detected", False)
    
    # حساب تقييم المؤشر
    if "صاعد" in daily_bias or "Bullish" in daily_bias:
        score_pct = 85 if dist_pips < 20 else 70
        badge_text = "شراء قوي" if score_pct >= 80 else "شراء"
        badge_class = "bg-strong-buy" if score_pct >= 80 else "bg-buy"
    elif "هابط" in daily_bias or "Bearish" in daily_bias:
        score_pct = 15 if dist_pips < 20 else 30
        badge_text = "بيع قوي" if score_pct <= 20 else "بيع"
        badge_class = "bg-strong-sell" if score_pct <= 20 else "bg-sell"
    else:
        score_pct = 50
        badge_text = "محايد"
        badge_class = "bg-neutral"

    # ==========================================
    # المستطيل الأول: المؤشر المؤسسي الحالي
    # ==========================================
    st.markdown(f"""
        <div class="card-section">
            <div class="card-title">📊 1. التقييم المؤسسي الشامل للإشارة</div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:15px;">
                <div>
                    <span style="color:#93a4bf; font-weight:600;">حالة الزوج ({display_name}):</span>
                    <span class="signal-badge {badge_class}" style="margin-inline-start: 15px;">{badge_text}</span>
                </div>
                <div style="color:#93a4bf; font-size:0.9rem;">الاتجاه المعتمد: <b style="color:#f0b84a;">{daily_bias}</b></div>
            </div>
            <div class="gauge-bar">
                <div class="gauge-pointer" style="left: {score_pct}%;"></div>
            </div>
            <div class="gauge-labels">
                <span>بيع قوي</span>
                <span>بيع</span>
                <span>محايد</span>
                <span>شراء</span>
                <span>شراء قوي</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # المستطيل الثاني: مناطق الـ Order Block (SMC)
    # ==========================================
    ob_min, ob_max = analysis['order_block_zone']
    st.markdown(f"""
        <div class="card-section">
            <div class="card-title">📦 2. مناطق الـ Order Blocks والسيولة المؤسسية</div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">نطاق الـ OB (إطار 4 ساعات)</div>
                    <div class="metric-val" style="color:#2dd4a0;">{ob_min} - {ob_max}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">المسافة الحالية عن السعر</div>
                    <div class="metric-val">{dist_pips} نقطة</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">طبيعة المنطقة</div>
                    <div class="metric-val" style="color:#f0b84a;">تجميع سيولة إعادة اختبار</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # المستطيل الثالث: شارت التداول اللحظي (TradingView)
    # ==========================================
    st.markdown(f"""
        <div class="card-section">
            <div class="card-title">📈 3. الرسم البياني المباشر واللحظي ({display_name})</div>
        </div>
    """, unsafe_allow_html=True)
    
    tv_embed_url = f"https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=240&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Etc/UTC&locale=ar"
    st.iframe(tv_embed_url, height=520)

    # ==========================================
    # المستطيل الرابع: تحليل وكيل المخاطر المشرف (Risk Supervisor & Noise)
    # ==========================================
    supervisor_status = "⚠️ تحذير: رصد تعارض تقاطعي وضوضاء عالية" if is_noise else "✅ استقرار تقاطعي: لا توجد تعارضات جوهرية"
    supervisor_color = "#ff6b73" if is_noise else "#2dd4a0"
    supervisor_desc = "يقوم وكيل المخاطر بمقارنة هذا الزوج مع أزواج العملات المتقاطعة (مثل ارتباطات الدولار). في حال وجود إشارات متعارضة (مثل بيع قوي على زوج وشراء على آخر بنفس العملة الأساسية)، يتم تصنيف السوق على أنه 'ضوضاء' لحماية رأس المال." if is_noise else "المسار الاتجاهي متوافق مع منظومة السيولة الكلية، ولا توجد تعارضات مع العملات المرتبطة."

    st.markdown(f"""
        <div class="card-section" style="border: 1px solid {supervisor_color};">
            <div class="card-title" style="color: {supervisor_color};">🛡️ 4. تقرير وكيل إدارة المخاطر المشرف (Risk Supervisor)</div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">حالة التعارض التقاطعي</div>
                    <div class="metric-val" style="color: {supervisor_color}; font-size:1.05rem;">{supervisor_status}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">حالة ضوضاء السوق</div>
                    <div class="metric-val">{'⚠️ ضوضاء مرتفعة' if is_noise else '✅ اتجاه نقي آمن'}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">قرار التوجيه الآلي</div>
                    <div class="metric-val" style="color:#f0b84a;">{'تجنب الدخول (فلتر حماية)' if is_noise else 'مسموح بالتنفيذ المؤسسي'}</div>
                </div>
            </div>
            <p style="margin-top: 15px; color: #93a4bf; font-size: 0.95rem; line-height: 1.6;">
                <b>تحليل الوكيل المشرف:</b> {supervisor_desc}
            </p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("⚠️ جاري سحب بيانات الأصل... يرجى إعادة المحاولة أو اختيار زوج آخر.")
