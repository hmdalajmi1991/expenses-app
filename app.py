import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

st.title("⚡ تسجيل عطل سريع")

# تحميل البيانات
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

st.subheader("📋 رسالة القروب (اختياري)")
raw_text = st.text_area("", height=100)

st.subheader("📦 المواد المستخدمة")

# --------- الكيابل ----------
st.write("🔌 الكيابل")

col1, col2, col3 = st.columns(3)
with col1:
    c300_count = st.number_input("300 عدد", min_value=0)
    c300_meter = st.number_input("300 متر", min_value=0)

with col2:
    c240_count = st.number_input("240 عدد", min_value=0)
    c240_meter = st.number_input("240 متر", min_value=0)

with col3:
    c150_count = st.number_input("150 عدد", min_value=0)
    c150_meter = st.number_input("150 متر", min_value=0)

col4, col5 = st.columns(2)
with col4:
    c35_count = st.number_input("35 عدد", min_value=0)
    c35_meter = st.number_input("35 متر", min_value=0)

# --------- الوصلات ----------
st.write("🔩 الوصلات (S/J)")

col6, col7, col8 = st.columns(3)
with col6:
    sj_300_300 = st.number_input("S/J 300-300", min_value=0)
    sj_300_150 = st.number_input("S/J 300-150", min_value=0)

with col7:
    sj_150_150 = st.number_input("S/J 150-150", min_value=0)
    sj_150_35 = st.number_input("S/J 150-35", min_value=0)

with col8:
    sj_35_35 = st.number_input("S/J 35-35", min_value=0)

# --------- بوت ----------
st.write("🧩 البوت اند")

boot_300 = st.number_input("Boot End 300", min_value=0)

# --------- حفظ ----------
if st.button("💾 حفظ البلاغ"):

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "text": raw_text,
        "materials": {
            "cables": {
                "300": {"count": c300_count, "meter": c300_meter},
                "240": {"count": c240_count, "meter": c240_meter},
                "150": {"count": c150_count, "meter": c150_meter},
                "35": {"count": c35_count, "meter": c35_meter}
            },
            "sj": {
                "300-300": sj_300_300,
                "300-150": sj_300_150,
                "150-150": sj_150_150,
                "150-35": sj_150_35,
                "35-35": sj_35_35
            },
            "boot": boot_300
        }
    }

    data.append(entry)
    save_data(data)

    st.success("تم الحفظ ✅")

# --------- تقرير ----------
st.subheader("📊 تقرير شهري")

month = st.text_input("رقم الشهر مثال: 05")

if st.button("📈 تحليل الشهر"):

    total = {
        "cables": {
            "300": {"count":0, "meter":0},
            "240": {"count":0, "meter":0},
            "150": {"count":0, "meter":0},
            "35": {"count":0, "meter":0}
        },
        "sj": {
            "300-300":0,
            "300-150":0,
            "150-150":0,
            "150-35":0,
            "35-35":0
        },
        "boot":0
    }

    for d in data:
        if f"-{month}-" in d["date"]:
            m = d["materials"]

            for k in total["cables"]:
                total["cables"][k]["count"] += m["cables"][k]["count"]
                total["cables"][k]["meter"] += m["cables"][k]["meter"]

            for k in total["sj"]:
                total["sj"][k] += m["sj"][k]

            total["boot"] += m["boot"]

    st.subheader("📦 ملخص المواد")

    for k in total["cables"]:
        st.write(f"كيبل {k}: {total['cables'][k]['meter']} متر / {total['cables'][k]['count']} عدد")

    for k in total["sj"]:
        st.write(f"S/J {k}: {total['sj'][k]}")

    st.write(f"Boot End 300: {total['boot']}")
