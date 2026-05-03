import streamlit as st
from datetime import datetime
import json
import uuid

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

# تنسيق
st.markdown("""
<style>
label {font-size: 13px !important;}
textarea, input {font-size: 13px !important;}
textarea {height: 80px !important; border-radius: 8px !important;}
h3 {font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ نظام تقارير الأعطال")

DATA_FILE = "data.json"

CABLES = ["300","240","150","35"]
SJ_TYPES = ["300-300","300-150","150-150","150-35","35-35"]
TJ_TYPES = ["300-300","300-150","300-35"]

def load():
    try:
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save(d):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

data = load()

tab1,tab2 = st.tabs(["➕ إضافة","📁 التقارير"])

# ================= إضافة =================
with tab1:
    with st.form("form",clear_on_submit=True):

        st.markdown("### 📍 الموقع")
        location = st.text_input("")

        st.markdown("### ⚡ بيانات المحطة")
        station = st.text_input(" ")

        st.markdown("### 🛠️ الأعمال")
        work = st.text_area("  ")

        st.markdown("### 📝 ملاحظات")
        notes = st.text_area("   ")

        st.markdown("### 📦 المواد")

        cols = st.columns(4)
        cables={}
        for i,c in enumerate(CABLES):
            with cols[i]:
                count=st.number_input(f"{c} عدد",0,key=f"c_count_{c}")
                meter=st.number_input(f"{c} متر",0,key=f"c_meter_{c}")
                cables[c]={"count":int(count),"meter":int(meter)}

        cols2=st.columns(5)
        sj={}
        for i,s in enumerate(SJ_TYPES):
            with cols2[i]:
                sj[s]=st.number_input(s,0,key=f"sj_{s}")

        cols3=st.columns(3)
        tj={}
        for i,t in enumerate(TJ_TYPES):
            with cols3[i]:
                tj[t]=st.number_input(t,0,key=f"tj_{t}")

        colb,coli=st.columns(2)
        with colb:
            boot=st.number_input("Boot End 300",0)
        with coli:
            inspect=st.number_input("عدد الفحص",0)

        submit=st.form_submit_button("💾 حفظ")

    if submit:
        now=datetime.now()
        entry={
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
                "inspect":int(inspect)
            }
        }
        data.append(entry)
        save(data)
        st.success("تم الحفظ")

# ================= عرض + تعديل =================
with tab2:

    for r in data:
        with st.expander(f"تقرير {r['no']} - {r['time']}"):

            st.write("📍",r["location"])
            st.write("⚡",r["station"])
            st.write("🛠️",r["work"])
            st.write("📝",r["notes"])

            m=r["materials"]

            for c in CABLES:
                if m["cables"][c]["count"] or m["cables"][c]["meter"]:
                    st.write(f"{c}: {m['cables'][c]['count']} / {m['cables'][c]['meter']}")

            # ===== زر تعديل =====
            if st.button(f"✏️ تعديل {r['id']}"):
                st.session_state["edit_id"]=r["id"]

            # ===== نموذج التعديل =====
            if st.session_state.get("edit_id")==r["id"]:
                st.markdown("### ✏️ تعديل التقرير")

                new_loc=st.text_input("الموقع",r["location"],key="edit_loc")
                new_stat=st.text_input("المحطة",r["station"],key="edit_stat")
                new_work=st.text_area("الأعمال",r["work"],key="edit_work")
                new_notes=st.text_area("ملاحظات",r["notes"],key="edit_notes")

                if st.button("💾 حفظ التعديل"):
                    for i,x in enumerate(data):
                        if x["id"]==r["id"]:
                            data[i]["location"]=new_loc
                            data[i]["station"]=new_stat
                            data[i]["work"]=new_work
                            data[i]["notes"]=new_notes
                            save(data)
                            st.success("تم التعديل")
                            st.session_state["edit_id"]=None
                            st.rerun()

            # ===== حذف =====
            if st.button(f"🗑️ حذف {r['id']}"):
                data=[x for x in data if x["id"]!=r["id"]]
                save(data)
                st.success("تم الحذف")
                st.rerun()
