import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

st.title("⚡ نظام تسجيل الأعطال")

# ---------- تحميل البيانات ----------
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

# ---------- إدخال بلاغ ----------
st.subheader("➕ إضافة بلاغ")

raw_text = st.text_area("📋 رسالة القروب (مرجع فقط)")

st.write("📦 أدخل المواد المستخدمة:")

c300 = st.number_input("كيبل 300 (متر)", 0)
c240 = st.number_input("كيبل 240 (متر)", 0)
c185 = st.number_input("كيبل 185 (متر)", 0)
c35 = st.number_input("كيبل 35 (متر)", 0)

straight = st.number_input("ستريت جوينت", 0)
t_joint = st.number_input("تي جوينت", 0)
boot = st.number_input("بوت اند", 0)

if st.button("💾 حفظ البلاغ"):

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "text": raw_text,
        "materials": {
            "300": c300,
            "240": c240,
            "185": c185,
            "35": c35,
            "straight": straight,
            "t_joint": t_joint,
            "boot": boot
        }
    }

    data.append(entry)
    save_data(data)

    st.success("تم الحفظ ✅")

# ---------- تقرير شهري ----------
st.subheader("📊 تقرير شهري")

month = st.text_input("اكتب رقم الشهر مثال: 05")

if st.button("📈 تحليل الشهر"):

    total = {
        "300": 0,
        "240": 0,
        "185": 0,
        "35": 0,
        "straight": 0,
        "t_joint": 0,
        "boot": 0
    }

    for d in data:
        if f"-{month}-" in d["date"]:
            m = d["materials"]

            for k in total:
                total[k] += m.get(k, 0)

    st.subheader("📦 ملخص المواد")

    st.write(f"كيبل 300: {total['300']} متر")
    st.write(f"كيبل 240: {total['240']} متر")
    st.write(f"كيبل 185: {total['185']} متر")
    st.write(f"كيبل 35: {total['35']} متر")

    st.write(f"ستريت جوينت: {total['straight']}")
    st.write(f"تي جوينت: {total['t_joint']}")
    st.write(f"بوت اند: {total['boot']}")
