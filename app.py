import os
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# استدعاء محرك الـ SMC
from smc_engine.order_block_engine import MultiTimeframeSMCEngine

# إعداد الصفحة وتصميمها (بدون قائمة جانبية، تصميم عصري واسع)
st.set_page_config(
    page_title="Institutional Multi-Agent Trading System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 تنسيقات CSS عصرية (Dark Theme)
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
    .gauge-container {
        background: #141f33;
        border: 1px solid #243452;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.35);
        margin-bottom: 20px;
    }
    .gauge-bar {
        height: 12px;
        border-radius: 99px;
        background: linear-gradient(90deg, #ff6b73 0%, #d99a1c 50%, #2dd4a0 100%);
        position: relative;
        margin: 15px 0 10px 0;
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
    .metric-card {
        background: #141f33;
        border: 1px solid #243452;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .metric-label { font-size: 0.85rem; color: #93a4bf; }
    .metric-val { font-size: 1.25rem; font-weight: 700; color: #e8eef9; margin-top: 4px; }
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

# ترويسة الصفحة والقائمة المنسدلة في نفس السطر
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
col_title, col_picker = st.columns([2, 1])

with col_title:
    st.markdown('<div class="hero-title">🏛️ Institutional Multi-Agent Trading & SMC Terminal</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">اختر زوج العملة أو الأصل المالي لعرض الشارت اللحظي، مناطق الـ Order Blocks، وتقييم النموذج.</div>', unsafe_allow_html=True)

with col_picker:
    selected_symbol = st.selectbox(
        "اختر زوج العملة / الأصل:",
        options=list(fleet_assets.keys()),
        format_func=lambda x: f"{fleet_assets[x][0]} ({x})"
    )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

display_name, tv_symbol = fleet_assets[selected_symbol]

# سحب البيانات عبر yfinance
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

    # المؤشر ومناطق الـ OB
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.markdown(f"""
            <div class="gauge-container">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#93a4bf; font-weight:600;">الإشارة المؤسسية الحالية:</span>
                    <span class="signal-badge {badge_class}">{badge_text}</span>
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

    with col_top2:
        ob_min, ob_max = analysis['order_block_zone']
        st.markdown(f"""
            <div class="gauge-container">
                <h4 style="margin:0 0 10px 0; color:#f0b84a;">📦 منطقة الـ Order Block ({display_name})</h4>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px;">
                    <div>
                        <span style="color:#93a4bf; font-size:0.85rem;">نطاق الـ OB (4H)</span>
                        <div style="font-weight:700; font-size:1.1rem; color:#2dd4a0;">{ob_min} - {ob_max}</div>
                    </div>
                    <div>
                        <span style="color:#93a4bf; font-size:0.85rem;">المسافة عن السعر</span>
                        <div style="font-weight:700; font-size:1.1rem; color:#e8eef9;">{dist_pips} نقطة</div>
                    </div>
                    <div>
                        <span style="color:#93a4bf; font-size:0.85rem;">الاتجاه اليومي</span>
                        <div style="font-weight:700; font-size:1.1rem; color:#f0b84a;">{daily_bias}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # شارت TradingView اللحظي
    st.subheader(f"📈 الرسم البياني المباشر ({display_name})")
    tv_embed_url = f"https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=240&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Etc/UTC&locale=ar"
    st.iframe(tv_embed_url, height=560)

    # المؤشرات المؤسسية
    st.markdown("---")
    st.subheader("📊 المؤشرات والقياسات المؤسسية")
    
    col_ind1, col_ind2, col_ind3, col_ind4 = st.columns(4)
    
    with col_ind1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🧠 فلتر الضوضاء السوقية</div>
                <div class="metric-val">{'⚠️ ضوضاء عالية' if analysis['is_noise_detected'] else '✅ اتجاه نقي'}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_ind2:
        curr_p = analysis['current_price']
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💵 السعر الحالي</div>
                <div class="metric-val">{curr_p}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_ind3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🤖 توقع نموذج XGBoost</div>
                <div class="metric-val" style="color:#2dd4a0;">{daily_bias} (توافق)</div>
            </div>
        """, unsafe_allow_html=True)

    with col_ind4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⏳ الإطار الزمني للتحليل</div>
                <div class="metric-val">1D + 4H Confluence</div>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error("⚠️ جاري سحب بيانات الأصل... يرجى إعادة المحاولة أو اختيار زوج آخر.")
