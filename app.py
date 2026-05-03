import streamlit as st
from datetime import datetime
import json
import uuid

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")

# 🎨 تنسيق احترافي
st.markdown("""
<style>
label {font-size: 13px !important;}
textarea, input {font-size: 13px !important;}
textarea {height: 80px !important; border-radius: 8px !important;}
.block-container {padding-top: 1rem; padding-bottom: 1rem;}
h3, h4 {font-size: 16px !important;}
div[data-testid="stNumberInput"] input {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ نظام تقارير الأعطال")

DATA_FILE = "data.json"

CABLES = ["300", "240", "150", "35"]
SJ_TYPES = ["300-300", "300-150", "150-150", "150-35", "35-35"]
TJ_TYPES = ["300-300", "300-150", "300-35"]

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_total():
    return {
        "cables": {c: {"count": 0, "meter": 0} for c in CABLES},
        "sj": {s: 0 for s in SJ_TYPES},
        "tj": {t: 0 for t in TJ_TYPES},
        "boot_300": 0,
        "inspection": 0
    }

def add_total(total, m):
    for c in CABLES:
        total["cables"][c]["count"] += m["cables"][c]["count"]
        total["cables"][c]["meter"] += m["cables"][c]["meter"]

    for s in SJ_TYPES:
        total["sj"][s] += m["sj"][s]

    for t in TJ_TYPES:
        total["tj"][t] += m["tj"][t]

    total["boot_300"] += m["boot_300"]
    total["inspection"] += m["inspection"]

data = load_data()

tab1, tab2, tab3 = st.tabs(["➕ إضافة تقرير", "📁 التقارير اليومية", "📊 تقرير شهري"])

# ================= إضافة =================
with tab1:
    with st.form("form", clear_on_submit=True):

        st.markdown("### 📍 الموقع")
        location = st.text_input("")

        st.markdown("### ⚡ بيانات المحطة")
        station = st.text_input(" ")

        st.markdown("### 🛠️ الأعمال المنجزة")
        work = st.text_area("  ")

        st.markdown("### 📝 ملاحظات")
        notes = st.text_area("   ")

        st.markdown("### 📦 المواد")

        st.write("🔌 الكيابل")
        cols = st.columns(4)
        cables = {}

        for i, c in enumerate(CABLES):
            with cols[i]:
                count = st.number_input(f"{c} عدد", 0, key=f"c_count_{c}")
                meter = st.number_input(f"{c} متر", 0, key=f"c_meter_{c}")
                cables[c] = {"count": int(count), "meter": int(meter)}

        st.write("🔩 S/J")
        cols2 = st.columns(5)
        sj = {}

        for i, s in enumerate(SJ_TYPES):
            with cols2[i]:
                sj[s] = st.number_input(f"{s}", 0, key=f"sj_{s}")

        st.write("🔧 T/J")
        cols3 = st.columns(3)
        tj = {}

        for i, t in enumerate(TJ_TYPES):
            with cols3[i]:
                tj[t] = st.number_input(f"{t}", 0, key=f"tj_{t}")

        colb, coli = st.columns(2)
        with colb:
            boot = st.number_input("Boot End 300", 0)
        with coli:
            inspect = st.number_input("عدد الفحص", 0)

        submit = st.form_submit_button("💾 حفظ")

    if submit:
        now = datetime.now()
        entry = {
            "id": str(uuid.uuid4()),
            "no": len(data)+1,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "location": location,
            "station": station,
            "work": work,
            "notes": notes,
            "materials": {
                "cables": cables,
                "sj": sj,
                "tj": tj,
                "boot_300": int(boot),
                "inspection": int(inspect)
            }
        }
        data.append(entry)
        save_data(data)
        st.success("تم الحفظ ✅")

# ================= عرض =================
with tab2:
    if not data:
        st.info("لا يوجد تقارير")
    else:
        days = sorted(set(d["date"] for d in data), reverse=True)

        for day in days:
            st.markdown(f"## 📅 {day}")
            for r in [x for x in data if x["date"] == day]:
                with st.expander(f"تقرير {r['no']} - {r['time']}"):

                    st.write("📍", r["location"])
                    st.write("⚡", r["station"])
                    st.write("🛠️", r["work"])
                    st.write("📝", r["notes"])

                    m = r["materials"]

                    for c in CABLES:
                        if m["cables"][c]["count"] or m["cables"][c]["meter"]:
                            st.write(f"كيبل {c}: {m['cables'][c]['count']} / {m['cables'][c]['meter']} متر")

                    for s in SJ_TYPES:
                        if m["sj"][s]:
                            st.write(f"S/J {s}: {m['sj'][s]}")

                    for t in TJ_TYPES:
                        if m["tj"][t]:
                            st.write(f"T/J {t}: {m['tj'][t]}")

                    if m["boot_300"]:
                        st.write("Boot:", m["boot_300"])

                    if m["inspection"]:
                        st.write("فحص:", m["inspection"])

# ================= شهري =================
with tab3:
    month = st.text_input("الشهر مثال 05")

    if st.button("تحليل"):
        total = get_total()

        for r in data:
            if f"-{month}-" in r["date"]:
                add_total(total, r["materials"])

        st.subheader("📦 المجموع")

        for c in CABLES:
            st.write(f"{c}: {total['cables'][c]['count']} / {total['cables'][c]['meter']} متر")

        for s in SJ_TYPES:
            st.write(f"S/J {s}: {total['sj'][s]}")

        for t in TJ_TYPES:
            st.write(f"T/J {t}: {total['tj'][t]}")

        st.write("Boot:", total["boot_300"])
        st.write("فحص:", total["inspection"])
