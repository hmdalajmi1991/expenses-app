import streamlit as st
import re

st.set_page_config(page_title="محلل رسائل الأعطال", page_icon="⚡")

st.title("⚡ محلل رسائل الأعطال")
st.write("الصق رسائل الواتساب كاملة، والتطبيق يرتبها لك كتقرير.")

raw_text = st.text_area("📋 الصق رسائل الواتساب هنا", height=300)

def find_match(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "غير مذكور"

def detect_status(text):
    if "تم الانتهاء" in text or "تم الاصلاح" in text or "خلص" in text or "انتهى" in text:
        return "منتهي"
    elif "برجاء" in text or "المتابعة" in text or "turn over" in text.lower() or "continue" in text.lower():
        return "يحتاج متابعة"
    elif "تم الحفر" in text or "digged" in text.lower() or "جاري" in text:
        return "جاري"
    else:
        return "جديد"

def clean_message(text):
    # يشيل التاريخ والرقم من بداية رسالة واتساب
    text = re.sub(r"\[\d{2}/\d{2}/\d{4}.*?\]\s*.*?:", "", text).strip()
    return text

if st.button("📊 إنشاء التقرير"):
    if raw_text.strip() == "":
        st.warning("الصق رسالة أولاً")
    else:
        messages = re.split(r"\[\d{2}/\d{2}/\d{4}.*?\]", raw_text)
        messages = [m.strip() for m in messages if m.strip()]

        result = "📊 ملخص الأعطال من رسائل الواتساب\n"
        result += "━━━━━━━━━━━━━━━━━━\n\n"
        result += f"📌 عدد الرسائل/البلاغات: {len(messages)}\n"
        result += "━━━━━━━━━━━━━━━━━━\n\n"

        for i, msg in enumerate(messages, start=1):
            text = clean_message(msg)

            area = find_match(r"(الصباحية|المهبولة|صباحية|mehabulla|mahaboula|mahboula)", text)
            block = find_match(r"(?:ق|قطعة|Block)[\s\-]*([0-9٠-٩]+)", text)
            street = find_match(r"(?:ش|شارع|Street|St)[\s\-]*([0-9٠-٩]+)", text)
            house = find_match(r"(?:قسيمة|منزل|House|Building|B)[\s\-]*([0-9٠-٩\+]+)", text)

            station = find_match(r"(?:محطه|محطة|S/S|SS)[\s\-]*([0-9٠-٩]+)", text)
            trans = find_match(r"(?:ترنس|Trans)[\s\-]*([0-9٠-٩]+)", text)
            unit = find_match(r"(?:يونت|Unit)[\s\-]*([0-9٠-٩]+)", text)

            status = detect_status(text)

            result += f"🔹 بلاغ {i}\n\n"

            result += "📍 الموقع:\n"
            result += f"- المنطقة: {area}\n"
            result += f"- القطعة: {block}\n"
            result += f"- الشارع: {street}\n"
            result += f"- المنزل/المبنى: {house}\n\n"

            result += "⚡ بيانات المحطة:\n"
            result += f"- المحطة: {station}\n"
            result += f"- الترانز: {trans}\n"
            result += f"- اليونت: {unit}\n\n"

            result += "🛠️ تفاصيل العمل / الملاحظات:\n"
            result += f"{text}\n\n"

            result += f"➡️ الحالة المقترحة: {status}\n"
            result += "━━━━━━━━━━━━━━━━━━\n\n"

        st.text_area("📋 التقرير الجاهز للنسخ", result, height=500)
