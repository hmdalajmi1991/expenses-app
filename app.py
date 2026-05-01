import streamlit as st
import re

st.set_page_config(page_title="مساعد تقرير الأعطال", page_icon="⚡")

st.title("⚡ مساعد تقرير الأعطال (احترافي)")

raw_text = st.text_area("📋 الصق رسالة الواتساب هنا", height=200)

def extract(pattern, text):
    m = re.search(pattern, text)
    return m.group(1) if m else ""

# استخراج أولي
block = extract(r"ق\s*(\d+)", raw_text)
street = extract(r"ش\s*(\d+)", raw_text)
house = extract(r"قسيمه\s*(\d+)", raw_text)
station = extract(r"محطه\s*(\d+)", raw_text)
trans = extract(r"ترنس\s*(\d+)", raw_text)
unit = extract(r"يونت\s*(\d+)", raw_text)

# 🧠 واجهة التعديل
st.subheader("✏️ راجع وعدّل البيانات")

area = st.text_input("المنطقة", "")
block = st.text_input("القطعة", block)
street = st.text_input("الشارع", street)
house = st.text_input("المنزل/القسيمة", house)

station = st.text_input("المحطة", station)
trans = st.text_input("الترنس", trans)
unit = st.text_input("اليونت", unit)

work = st.text_area("🛠️ الأعمال المنجزة")
status_desc = st.text_area("❗ الوضع الحالي")
needed = st.text_area("📦 المطلوب")

status = st.selectbox("الحالة", ["جديد", "جاري", "يحتاج متابعة", "منتهي"])

# 🧾 إنشاء التقرير
if st.button("📊 إنشاء التقرير الرسمي"):

    report = "📊 تقرير متابعة عطل\n"
    report += "━━━━━━━━━━━━━━━━━━\n\n"

    report += "📍 الموقع:\n"
    report += f"{area} - قطعة {block} - شارع {street} - قسيمة {house}\n\n"

    report += "⚡ بيانات المحطة:\n"
    report += f"محطة {station} - ترنس {trans} - يونت {unit}\n\n"

    report += "🛠️ الأعمال المنجزة:\n"
    report += f"{work}\n\n"

    report += "❗ الوضع الحالي:\n"
    report += f"{status_desc}\n\n"

    report += "📦 المطلوب:\n"
    report += f"{needed}\n\n"

    report += f"➡️ الحالة: {status}\n"
    report += "━━━━━━━━━━━━━━━━━━"

    st.text_area("📋 انسخ التقرير", report, height=350)
