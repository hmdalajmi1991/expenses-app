import streamlit as st
import re

st.set_page_config(page_title="محلل رسائل الأعطال", page_icon="⚡")

st.title("⚡ محلل رسائل الأعطال")
st.write("الصق رسالة الواتساب، والتطبيق يرتبها لك بشكل احترافي.")

raw_text = st.text_area("📋 الصق الرسالة هنا", height=250)

def clean_text(text):
    # حذف توقيت واتساب
    text = re.sub(r"\[\d{2}/\d{2}/\d{4}.*?\]", "", text)
    text = re.sub(r"\+\d+\s*\d+", "", text)
    return text.strip()

def format_text(text):
    # تقسيم الجمل
    parts = re.split(r"تم|لم|وبرجاء|and|Found|need", text)

    result = ""
    for p in parts:
        p = p.strip()
        if p:
            result += f"- {p}\n"

    return result

if st.button("📊 إنشاء التقرير"):

    if raw_text.strip() == "":
        st.warning("الصق الرسالة أولاً")
    else:
        text = clean_text(raw_text)

        report = "📊 تقرير عطل\n"
        report += "━━━━━━━━━━━━━━━━━━\n\n"

        report += "📌 تفاصيل البلاغ:\n"
        report += format_text(text)
        report += "\n"

        # تحديد الحالة بشكل ذكي
        if "لم" in text or "not find" in text.lower():
            status = "🔴 يحتاج متابعة"
        elif "تم" in text:
            status = "🟡 جاري"
        else:
            status = "🆕 جديد"

        report += f"➡️ الحالة: {status}\n"
        report += "━━━━━━━━━━━━━━━━━━"

        st.text_area("📋 التقرير الجاهز", report, height=300)
