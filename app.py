import streamlit as st

st.set_page_config(page_title="مولد تقرير الأعطال", page_icon="⚡")

st.title("⚡ مولد تقرير الأعطال")

reports = []

num = st.number_input("كم عدد البلاغات؟", min_value=1, step=1)

for i in range(int(num)):
    st.subheader(f"بلاغ {i+1}")

    location = st.text_input(f"📍 الموقع {i+1}")
    station = st.text_input(f"⚡ المحطة {i+1}")
    work = st.text_area(f"🛠️ العمل {i+1}")
    issue = st.text_area(f"❗ المشكلة {i+1}")
    status = st.selectbox(f"الحالة {i+1}", ["جديد", "جاري", "يحتاج متابعة", "منتهي"])

    reports.append((location, station, work, issue, status))

if st.button("📊 إنشاء التقرير"):
    result = "📊 ملخص الأعطال\n\n"

    for i, r in enumerate(reports):
        result += f"📍 {r[0]}\n"
        result += f"⚡ {r[1]}\n"
        result += f"🛠️ {r[2]}\n"
        result += f"❗ {r[3]}\n"
        result += f"➡️ الحالة: {r[4]}\n\n"

    st.text_area("📋 انسخ التقرير", result, height=300)
