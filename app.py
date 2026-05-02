import streamlit as st
import re

st.set_page_config(page_title="مساعد تقرير الأعطال", page_icon="⚡")

st.title("⚡ مساعد تقرير الأعطال")

raw_text = st.text_area("📋 الصق رسالة الواتساب هنا", height=220)

def extract(patterns, text):
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""

# 🔥 سحب ذكي بدون تحديد منطقة
block = extract([
    r"(?:ق|قطعة)\s*[-:]?\s*([0-9٠-٩]+)",
    r"(?:Block)\s*[-:]?\s*([0-9]+)"
], raw_text)

street = extract([
    r"(?:ش|شارع)\s*[-:]?\s*([0-9٠-٩]+)",
    r"(?:Street|St)\s*[-:]?\s*([0-9]+)"
], raw_text)

house = extract([
    r"(?:قسيمه|قسيمة|منزل)\s*[-:]?\s*([0-9٠-٩]+)",
    r"(?:Building|B|House)\s*[-:]?\s*([0-9\+]+)"
], raw_text)

station = extract([
    r"(?:محطه|محطة)\s*[-:]?\s*([0-9٠-٩]+)",
    r"(?:S/S|SS)\s*[-:]?\s*([0-9]+)"
], raw_text)

trans = extract([
    r"(?:ترنس|ترانز)\s*[-:]?\s*([0-9٠-٩]+)",
    r"(?:Trans)\s*[-:]?\s*([0-9]+)"
], raw_text)

unit = extract([
    r"(?:يونت|وحدة)\s*[-:]?\s*([0-9٠-٩]+)",
    r"(?:Unit)\s*[-:]?\s*([0-9]+)"
], raw_text)

st.subheader("✏️ راجع وعدّل البيانات")

area = st.text_input("المنطقة (اكتبها يدوي)", "")
block = st.text_input("القطعة", block)
street = st.text_input("الشارع", street)
house = st.text_input("المنزل / المبنى / القسيمة", house)

station = st.text_input("المحطة", station)
trans = st.text_input("الترنس", trans)
unit = st.text_input("اليونت", unit)

work = st.text_area("🛠️ الأعمال المنجزة")
materials = st.text_area("📦 المواد المطلوبة")
note = st.text_area("📝 ملاحظة")

status = st.selectbox(
    "الحالة",
    ["يرجى المتابعة", "تم الانتهاء"]
)

if st.button("📊 إنشاء التقرير الرسمي"):

    report = "📊 تقرير متابعة عطل\n"
    report += "━━━━━━━━━━━━━━━━━━\n\n"

    report += "📍 الموقع:\n"
    report += f"{area} - قطعة {block} - شارع {street} - منزل/مبنى {house}\n\n"

    report += "⚡ بيانات المحطة:\n"
    report += f"محطة {station} - ترنس {trans} - يونت {unit}\n\n"

    report += "🛠️ الأعمال المنجزة:\n"
    report += f"{work}\n\n"

    report += "📦 المواد المطلوبة:\n"
    report += f"{materials}\n\n"

    report += "📝 ملاحظة:\n"
    report += f"{note}\n\n"

    report += f"➡️ الحالة: {status}\n"
    report += "━━━━━━━━━━━━━━━━━━"

    st.text_area("📋 انسخ التقرير", report, height=400)
