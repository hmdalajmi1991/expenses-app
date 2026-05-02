import streamlit as st
import re
from datetime import datetime
import json

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

st.title("⚡ نظام تسجيل الأعطال (نسخة احترافية)")

# ---------- قراءة البيانات ----------
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

data = load_data()

# ---------- استخراج المواد ----------
def extract_materials(text):
    results = []

    # كيابل (240 / 300 / 185 ...)
    cable_matches = re.findall(r"(\d+)\s*متر.*?(240|300|185|150|120|95|70|35)", text)
    for qty, size in cable_matches:
        results.append({
            "type": "كيبل",
            "size": size,
            "qty": int(qty)
        })

    # ستريت
    if "ستريت" in text or "straight" in text.lower():
        n = re.findall(r"(\d+)\s*(ستريت|straight)", text)
        for x in n:
            results.append({"type": "ستريت جوينت", "size": "-", "qty": int(x[0])})

    # تي جوينت
    if "تي" in text or "t joint" in text.lower():
        n = re.findall(r"(\d+)\s*(تي|t)", text)
        for x in n:
            results.append({"type": "تي جوينت", "size": "-", "qty": int(x[0])})

    # بوت
    if "بوت" in text or "boot" in text.lower():
        n = re.findall(r"(\d+)\s*(بوت|boot)", text)
        for x in n:
            results.append({"type": "بوت", "size": "-", "qty": int(x[0])})

    return results

# ---------- إدخال بلاغ ----------
st.subheader("➕ إضافة بلاغ")

raw_text = st.text_area("📋 الصق رسالة الواتساب")

materials = extract_materials(raw_text)

edited_materials = []

if materials:
    st.write("🔍 المواد المقترحة (عدلها إذا فيها خطأ):")

    for i, m in enumerate(materials):
        col1, col2, col3 = st.columns(3)

        with col1:
            t = st.text_input(f"نوع {i}", m["type"], key=f"type{i}")
        with col2:
            s = st.text_input(f"حجم {i}", m["size"], key=f"size{i}")
        with col3:
            q = st.number_input(f"كمية {i}", value=m["qty"], key=f"qty{i}")

        edited_materials.append({"type": t, "size": s, "qty": q})

if st.button("💾 حفظ البلاغ"):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "text": raw_text,
        "materials": edited_materials
    }
    data.append(entry)
    save_data(data)
    st.success("تم الحفظ ✅")

# ---------- تحليل الشهر ----------
st.subheader("📊 تقرير شهري")

month = st.text_input("اكتب رقم الشهر (مثال: 05)")

if st.button("📈 تحليل الشهر"):

    summary = {}

    for d in data:
        if f"-{month}-" in d["date"]:

            for m in d["materials"]:
                key = f"{m['type']} {m['size']}"

                if key not in summary:
                    summary[key] = 0

                summary[key] += m["qty"]

    st.write("📦 ملخص المواد:")

    for k, v in summary.items():
        if "كيبل" in k:
            st.write(f"{k}: {v} متر")
        else:
            st.write(f"{k}: {v} عدد")
        
