import streamlit as st
import re
from datetime import datetime
import json

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

st.title("⚡ نظام تسجيل الأعطال")

def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def extract_materials(text):
    results = []

    cable_matches = re.findall(r"(\d+)\s*متر.*?(240|300|185|150|120|95|70|35)", text)
    for qty, size in cable_matches:
        results.append({"type": "كيبل", "size": size, "qty": int(qty)})

    straight_matches = re.findall(r"(\d+)\s*(?:ستريت|ستر ?يت|straight)", text, re.IGNORECASE)
    for qty in straight_matches:
        results.append({"type": "ستريت جوينت", "size": "-", "qty": int(qty)})

    t_matches = re.findall(r"(\d+)\s*(?:تي|t joint|tee)", text, re.IGNORECASE)
    for qty in t_matches:
        results.append({"type": "تي جوينت", "size": "-", "qty": int(qty)})

    boot_matches = re.findall(r"(\d+)\s*(?:بوت|boot)", text, re.IGNORECASE)
    for qty in boot_matches:
        results.append({"type": "بوت اند", "size": "-", "qty": int(qty)})

    return results

data = load_data()

st.subheader("➕ إضافة بلاغ")

raw_text = st.text_area("📋 الصق رسالة الواتساب")

if "materials" not in st.session_state:
    st.session_state.materials = []

if st.button("🔍 تحليل الرسالة"):
    st.session_state.materials = extract_materials(raw_text)

edited_materials = []

if st.session_state.materials:
    st.write("🔍 المواد المقترحة — عدّلها إذا فيها خطأ:")

    for i, m in enumerate(st.session_state.materials):
        col1, col2, col3 = st.columns(3)

        with col1:
            t = st.text_input(f"النوع {i+1}", m["type"], key=f"type{i}")
        with col2:
            s = st.text_input(f"الحجم {i+1}", m["size"], key=f"size{i}")
        with col3:
            q = st.number_input(f"الكمية {i+1}", value=int(m["qty"]), step=1, key=f"qty{i}")

        edited_materials.append({"type": t, "size": s, "qty": int(q)})

if st.button("💾 حفظ البلاغ"):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "text": raw_text,
        "materials": edited_materials
    }

    data.append(entry)
    save_data(data)

    st.session_state.materials = []
    st.success("تم حفظ البلاغ ✅")

st.subheader("📊 تقرير شهري")

month = st.text_input("اكتب رقم الشهر مثال: 05")

if st.button("📈 تحليل الشهر"):
    summary = {}

    for d in data:
        if f"-{month}-" in d["date"]:
            for m in d["materials"]:
                key = f"{m['type']} {m['size']}"
                summary[key] = summary.get(key, 0) + m["qty"]

    st.write("📦 ملخص المواد:")

    if summary:
        for k, v in summary.items():
            if "كيبل" in k:
                st.write(f"{k}: {v} متر")
            else:
                st.write(f"{k}: {v} عدد")
    else:
        st.info("لا توجد مواد مسجلة لهذا الشهر")
