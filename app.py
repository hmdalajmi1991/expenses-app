import streamlit as st
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

data = load_data()

st.subheader("➕ إضافة بلاغ")

raw_text = st.text_area("📋 رسالة القروب")

st.write("📦 المواد المستخدمة:")

c300 = st.number_input("كيبل 300 (متر)", min_value=0)
c240 = st.number_input("كيبل 240 (متر)", min_value=0)
c185 = st.number_input("كيبل 185 (متر)", min_value=0)
c35 = st.number_input("كيبل 35 (متر)", min_value=0)

straight = st.number_input("ستريت جوينت", min_value=0)
t_joint = st.number_input("تي جوينت", min_value=0)
boot = st.number_input("بوت اند", min_value=0)

if st.button("💾 حفظ البلاغ"):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
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
    st.success("تم حفظ البلاغ ✅")

st.subheader("📊 تقرير شهري")

month = st.text_input("اكتب رقم الشهر مثال: 05")

if st.button("📈 عرض تقرير الشهر"):
    total = {
        "300": 0,
        "240": 0,
        "185": 0,
        "35": 0,
        "straight": 0,
        "t_joint": 0,
        "boot": 0
    }

    month_reports = []

    for d in data:
        if f"-{month}-" in d["date"]:
            month_reports.append(d)
            m = d["materials"]

            for k in total:
                total[k] += m.get(k, 0)

    st.subheader("📦 ملخص المواد للشهر")

    st.write(f"كيبل 300: {total['300']} متر")
    st.write(f"كيبل 240: {total['240']} متر")
    st.write(f"كيبل 185: {total['185']} متر")
    st.write(f"كيبل 35: {total['35']} متر")
    st.write(f"ستريت جوينت: {total['straight']} عدد")
    st.write(f"تي جوينت: {total['t_joint']} عدد")
    st.write(f"بوت اند: {total['boot']} عدد")

    st.subheader("📋 البلاغات المحفوظة خلال الشهر")

    if len(month_reports) == 0:
        st.info("لا توجد بلاغات محفوظة لهذا الشهر")
    else:
        for i, r in enumerate(month_reports, start=1):
            with st.expander(f"بلاغ {i} - {r['date']}"):
                st.write("📋 رسالة القروب:")
                st.write(r["text"])

                st.write("📦 المواد المستخدمة:")
                st.write(f"كيبل 300: {r['materials'].get('300', 0)} متر")
                st.write(f"كيبل 240: {r['materials'].get('240', 0)} متر")
                st.write(f"كيبل 185: {r['materials'].get('185', 0)} متر")
                st.write(f"كيبل 35: {r['materials'].get('35', 0)} متر")
                st.write(f"ستريت جوينت: {r['materials'].get('straight', 0)} عدد")
                st.write(f"تي جوينت: {r['materials'].get('t_joint', 0)} عدد")
                st.write(f"بوت اند: {r['materials'].get('boot', 0)} عدد")
