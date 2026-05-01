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
    status = st.selectbox(
        f"الحالة {i+1}",
        ["جديد", "جاري", "يحتاج متابعة", "منتهي"]
    )

    reports.append((location, station, work, issue, status))

if st.button("📊 إنشاء التقرير"):

    result = "📊 ملخص الأعطال\n"
    result += "━━━━━━━━━━━━━━━━━━\n\n"

    total = len(reports)
    new_count = sum(1 for r in reports if r[4] == "جديد")
    in_progress = sum(1 for r in reports if r[4] == "جاري")
    need_follow = sum(1 for r in reports if r[4] == "يحتاج متابعة")
    done = sum(1 for r in reports if r[4] == "منتهي")

    result += f"📌 الإجمالي: {total}\n"
    result += f"🆕 جديد: {new_count}\n"
    result += f"🟡 جاري: {in_progress}\n"
    result += f"🔴 تحتاج متابعة: {need_follow}\n"
    result += f"🟢 منتهي: {done}\n"
    result += "━━━━━━━━━━━━━━━━━━\n\n"

    for r in reports:
        result += f"📍 {r[0]}\n"
        result += f"⚡ {r[1]}\n\n"

        result += "🛠️ العمل:\n"
        result += f"{r[2]}\n\n"

        result += "❗ المشكلة:\n"
        result += f"{r[3]}\n\n"

        result += f"➡️ الحالة: {r[4]}\n"
        result += "━━━━━━━━━━━━━━━━━━\n\n"

    st.text_area("📋 انسخ التقرير", result, height=400)
