import streamlit as st
from datetime import datetime
import json
import uuid

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

st.markdown("""
<style>
label {font-size: 13px !important;}
textarea, input {font-size: 13px !important;}
textarea {height: 80px !important; border-radius: 8px !important;}
h3, h4 {font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ نظام تقارير الأعطال")

DATA_FILE = "data.json"

CABLES = ["300","240","150","35"]
SJ_TYPES = ["300-300","300-150","150-150","150-35","35-35"]
TJ_TYPES = ["300-300","300-150","300-35"]

MONTHS = {
    "01":"يناير","02":"فبراير","03":"مارس","04":"ابريل",
    "05":"مايو","06":"يونيو","07":"يوليو","08":"اغسطس",
    "09":"سبتمبر","10":"اكتوبر","11":"نوفمبر","12":"ديسمبر"
}

def load():
    try:
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save(d):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

def empty_total():
    return {
        "cables":{c:{"count":0,"meter":0} for c in CABLES},
        "sj":{s:0 for s in SJ_TYPES},
        "tj":{t:0 for t in TJ_TYPES},
        "boot":0,
        "inspection":0
    }

def add_total(total,m):
    for c in CABLES:
        total["cables"][c]["count"]+=m["cables"][c]["count"]
        total["cables"][c]["meter"]+=m["cables"][c]["meter"]
    for s in SJ_TYPES:
        total["sj"][s]+=m["sj"][s]
    for t in TJ_TYPES:
        total["tj"][t]+=m["tj"][t]
    total["boot"]+=m["boot"]
    total["inspection"]+=m["inspection"]

def show_total(total,title):
    st.markdown(f"### 📦 {title}")
    for c in CABLES:
        st.write(f"كيبل {c}: {total['cables'][c]['count']} / {total['cables'][c]['meter']} متر")
    for s in SJ_TYPES:
        st.write(f"S/J {s}: {total['sj'][s]}")
    for t in TJ_TYPES:
        st.write(f"T/J {t}: {total['tj'][t]}")
    st.write("Boot:",total["boot"])
    st.write("فحص:",total["inspection"])

data = load()

tab1,tab2,tab3 = st.tabs(["➕ إضافة","📁 يومي","📊 شهري"])

# ================= التقرير الشهري =================
with tab3:
    st.subheader("📊 التقارير الشهرية")

    MONTHS = {
        "01":"يناير","02":"فبراير","03":"مارس","04":"ابريل",
        "05":"مايو","06":"يونيو","07":"يوليو","08":"اغسطس",
        "09":"سبتمبر","10":"اكتوبر","11":"نوفمبر","12":"ديسمبر"
    }

    year_total = empty_total()

    for m in MONTHS:
        month_reports = [r for r in data if f"-{m}-" in r.get("date","")]

        if not month_reports:
            continue

        month_total = empty_total()

        for r in month_reports:
            add_to_total(month_total, r.get("materials", {}))
            add_to_total(year_total, r.get("materials", {}))

        with st.expander(f"📅 تقارير شهر {MONTHS[m]}"):

            # 🔥 مربع ملخص الشهر (فوق)
            st.markdown("### 📦 مواد الشهر")

            for c in CABLES:
                st.write(f"كيبل {c}: {month_total['cables'][c]['count']} عدد / {month_total['cables'][c]['meter']} متر")

            for s in SJ_TYPES:
                st.write(f"S/J {s}: {month_total['sj'][s]} عدد")

            for t in TJ_TYPES:
                st.write(f"T/J {t}: {month_total['tj'][t]} عدد")

            st.write(f"Boot End 300: {month_total['boot']} عدد")
            st.write(f"عدد الفحص: {month_total['inspection']}")

            st.markdown("---")

            # 🔥 التقارير (نفس اليومي)
            for r in month_reports:
                with st.expander(f"تقرير {r.get('no','?')} - {r.get('time','')}"):

                    st.write("📍 الموقع:")
                    st.write(r.get("location",""))

                    st.write("⚡ بيانات المحطة:")
                    st.write(r.get("station",""))

                    st.write("🛠️ الأعمال:")
                    st.write(r.get("work",""))

                    st.write("📝 ملاحظات:")
                    st.write(r.get("notes",""))

                    st.write("📦 المواد:")
                    render_materials(r.get("materials",{}))

    st.markdown("---")

    # 🔥 مجموع السنة (تحت)
    st.markdown("## 📊 مجموع المواد خلال السنة")

    for c in CABLES:
        st.write(f"كيبل {c}: {year_total['cables'][c]['count']} عدد / {year_total['cables'][c]['meter']} متر")

    for s in SJ_TYPES:
        st.write(f"S/J {s}: {year_total['sj'][s]} عدد")

    for t in TJ_TYPES:
        st.write(f"T/J {t}: {year_total['tj'][t]} عدد")

    st.write(f"Boot End 300: {year_total['boot']} عدد")
    st.write(f"عدد الفحص: {year_total['inspection']}")
# ================= يومي =================
with tab2:
    days=sorted(set(d["date"] for d in data),reverse=True)

    for day in days:
        st.markdown(f"## 📅 {day}")
        for r in [x for x in data if x["date"]==day]:
            with st.expander(f"تقرير {r['no']} - {r['time']}"):
                st.write(r["location"])
                st.write(r["station"])
                st.write(r["work"])
                st.write(r["notes"])

# ================= شهري =================
with tab3:

    year_total=empty_total()

    for m in MONTHS:

        month_reports=[r for r in data if f"-{m}-" in r["date"]]

        if not month_reports:
            continue

        month_total=empty_total()

        for r in month_reports:
            add_total(month_total,r["materials"])
            add_total(year_total,r["materials"])

        with st.expander(f"📅 تقارير شهر {MONTHS[m]}"):

            # 🔥 مربع ملخص الشهر فوق
            show_total(month_total,"مواد الشهر")

            st.markdown("---")

            # 🔥 التقارير
            for r in month_reports:
                with st.expander(f"تقرير {r['no']} - {r['time']}"):
                    st.write(r["location"])
                    st.write(r["station"])
                    st.write(r["work"])
                    st.write(r["notes"])

    st.markdown("---")

    # 🔥 مربع السنة بالنهاية
    show_total(year_total,"مجموع السنة")
