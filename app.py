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

# ================= إضافة =================
with tab1:
    with st.form("form",clear_on_submit=True):

        st.markdown("### 📍 الموقع")
        location=st.text_input("")

        st.markdown("### ⚡ بيانات المحطة")
        station=st.text_input(" ")

        st.markdown("### 🛠️ الأعمال")
        work=st.text_area("  ")

        st.markdown("### 📝 ملاحظات")
        notes=st.text_area("   ")

        st.markdown("### 📦 المواد")

        cols=st.columns(4)
        cables={}
        for i,c in enumerate(CABLES):
            with cols[i]:
                cables[c]={
                    "count":st.number_input(f"{c} عدد",0,key=f"c{c}"),
                    "meter":st.number_input(f"{c} متر",0,key=f"m{c}")
                }

        cols2=st.columns(5)
        sj={}
        for i,s in enumerate(SJ_TYPES):
            with cols2[i]:
                sj[s]=st.number_input(s,0,key=f"sj{s}")

        cols3=st.columns(3)
        tj={}
        for i,t in enumerate(TJ_TYPES):
            with cols3[i]:
                tj[t]=st.number_input(t,0,key=f"tj{t}")

        boot=st.number_input("Boot End 300",0)
        inspect=st.number_input("عدد الفحص",0)

        submit=st.form_submit_button("💾 حفظ")

    if submit:
        now=datetime.now()
        data.append({
            "id":str(uuid.uuid4()),
            "no":len(data)+1,
            "date":now.strftime("%Y-%m-%d"),
            "time":now.strftime("%H:%M"),
            "location":location,
            "station":station,
            "work":work,
            "notes":notes,
            "materials":{
                "cables":cables,
                "sj":sj,
                "tj":tj,
                "boot":int(boot),
                "inspection":int(inspect)
            }
        })
        save(data)
        st.success("تم الحفظ")

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
