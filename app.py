import streamlit as st

st.set_page_config(
    page_title="Institutional Quant Terminal",
    page_icon="🚀",
    layout="wide"
)

st.markdown("<h1 style='color: #0dcaf0;'>🚀 تم تحميل الواجهة الجديدة بنجاح تام! (نسخة الإنتاج الحي)</h1>", unsafe_allow_html=True)
st.success("إذا ظهرت هذه الرسالة باللون الأخضر والعنوان الأزرق على موقع Render، فهذا يثبت أن السيرفر تحول بنجاح إلى النسخة الجديدة!")

# اختبار عرض أزواج التداول
asset = st.selectbox("اختر الزوج التجريبي:", ["GOLD", "GBP_JPY", "EUR_USD"])
st.write(f"الزوج المختار حالياً: {asset}")
