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

CABLES = ["300", "240", "150", "35"]
SJ_TYPES = ["300-300", "300-150", "150-150", "150-35", "35-35"]
TJ_TYPES = ["300-300", "300-150", "300-35"]

MONTHS = {
    "01": "يناير", "02": "فبراير", "03": "مارس", "04": "ابريل",
    "05": "مايو", "06": "يونيو", "07": "يوليو", "08": "اغسطس",
    "09": "سبتمبر", "10": "اكتوبر", "11": "نوفمبر", "12": "ديسمبر"
}

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

def empty_total():
    return {
        "cables": {c: {"count": 0, "meter": 0} for c in CABLES},
        "sj": {s: 0 for s in SJ_TYPES},
        "tj": {t: 0 for t in TJ_TYPES},
        "boot": 0,
        "inspection": 0
    }

def normalize_materials(m):
    base = empty_total()

    if not isinstance(m, dict):
        return base

    for c in CABLES:
        old = m.get("cables", {}).get(c, {})
        base["cables"][c]["count"] = int(old.get("count", 0))
        base["cables"][c]["meter"] = int(old.get("meter", 0))

    for s in SJ_TYPES:
        base["sj"][s] = int(m.get("sj", {}).get(s, 0))

    for t in TJ_TYPES:
        base["tj"][t] = int(m.get("tj", {}).get(t, 0))

    base["boot"] = int(m.get("boot", m.get("boot_300", 0)))
    base["inspection"] = int(m.get("inspection", m.get("inspect", m.get("inspection_count", 0))))

    return base

def add_to_total(total, materials):
    m = normalize_materials(materials)

    for c in CABLES:
        total["cables"][c]["count"] += m["cables"][c]["count"]
        total["cables"][c]["meter"] += m["cables"][c]["meter"]

    for s in SJ_TYPES:
        total["sj"][s] += m["sj"][s]

    for t in TJ_TYPES:
        total["tj"][t] += m["tj"][t]

    total["boot"] += m["boot"]
    total["inspection"] += m["inspection"]

def render_materials(m):
    m = normalize_materials(m)

    st.markdown("#### 🔌 الكيابل")
    for c in CABLES:
        count = m["cables"][c]["count"]
        meter = m["cables"][c]["meter"]
        if count > 0 or meter > 0:
            st.write(f"كيبل {c}: {count} عدد / {meter} متر")

    st.markdown("#### 🔩 S/J")
    for s in SJ_TYPES:
        if m["sj"][s] > 0:
            st.write(f"S/J {s}: {m['sj'][s]} عدد")

    st.markdown("#### 🔧 T/J")
    for t in TJ_TYPES:
        if m["tj"][t] > 0:
            st.write(f"T/J {t}: {m['tj'][t]} عدد")

    st.markdown("#### 🧩 Boot End / الفحص")
    if m["boot"] > 0:
        st.write(f"Boot End 300: {m['boot']} عدد")
    if m["inspection"] > 0:
        st.write(f"عدد الفحص: {m['inspection']}")

def render_total(total, title):
    st.markdown(f"### 📦 {title}")

    st.markdown("#### 🔌 الكيابل")
    for c in CABLES:
        st.write(f"كيبل {c}: {total['cables'][c]['count']} عدد / {total['cables'][c]['meter']} متر")

    st.markdown("#### 🔩 S/J")
    for s in SJ_TYPES:
        st.write(f"S/J {s}: {total['sj'][s]} عدد")

    st.markdown("#### 🔧 T/J")
    for t in TJ_TYPES:
        st.write(f"T/J {t}: {total['tj'][t]} عدد")

    st.markdown("#### 🧩 Boot End / الفحص")
    st.write(f"Boot End 300: {total['boot']} عدد")
    st.write(f"عدد الفحص: {total['inspection']}")

data = load_data()

tab1, tab2, tab3 = st.tabs(["➕ إضافة تقرير", "📁 التقارير اليومية", "📊 التقارير الشهرية"])

# ================= إضافة تقرير =================
with tab1:
    st.subheader("➕ إضافة تقرير جديد")

    with st.form("add_report_form", clear_on_submit=True):
        st.markdown("### 📍 الموقع")
        location = st.text_input("الموقع")

        st.markdown("### ⚡ بيانات المحطة")
        station = st.text_input("بيانات المحطة")

        st.markdown("### 🛠️ الأعمال المنجزة")
        work = st.text_area("الأعمال المنجزة")

        st.markdown("### 📝 ملاحظات")
        notes = st.text_area("ملاحظات")

        st.markdown("### 📦 المواد المستخدمة")

        st.write("🔌 الكيابل")
        cable_cols = st.columns(4)
        cables = {}

        for i, c in enumerate(CABLES):
            with cable_cols[i]:
                count = st.number_input(f"كيبل {c} - عدد", min_value=0, step=1, key=f"add_c_count_{c}")
                meter = st.number_input(f"كيبل {c} - متر", min_value=0, step=1, key=f"add_c_meter_{c}")
                cables[c] = {"count": int(count), "meter": int(meter)}

        st.write("🔩 S/J")
        sj_cols = st.columns(5)
        sj = {}

        for i, s in enumerate(SJ_TYPES):
            with sj_cols[i]:
                qty = st.number_input(f"S/J {s}", min_value=0, step=1, key=f"add_sj_{s}")
                sj[s] = int(qty)

        st.write("🔧 T/J")
        tj_cols = st.columns(3)
        tj = {}

        for i, t in enumerate(TJ_TYPES):
            with tj_cols[i]:
                qty = st.number_input(f"T/J {t}", min_value=0, step=1, key=f"add_tj_{t}")
                tj[t] = int(qty)

        st.write("🧩 Boot End / الفحص")
        col1, col2 = st.columns(2)
        with col1:
            boot = st.number_input("Boot End 300", min_value=0, step=1)
        with col2:
            inspection = st.number_input("عدد الفحص", min_value=0, step=1)

        submitted = st.form_submit_button("💾 حفظ التقرير")

    if submitted:
        now = datetime.now()

        report = {
            "id": str(uuid.uuid4()),
            "no": len(data) + 1,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "datetime": now.strftime("%Y-%m-%d %H:%M"),
            "location": location,
            "station": station,
            "work": work,
            "notes": notes,
            "materials": {
                "cables": cables,
                "sj": sj,
                "tj": tj,
                "boot": int(boot),
                "inspection": int(inspection)
            }
        }

        data.append(report)
        save_data(data)
        st.success("تم حفظ التقرير ✅")

# ================= التقارير اليومية =================
with tab2:
    st.subheader("📁 التقارير اليومية")

    if not data:
        st.info("لا توجد تقارير محفوظة")
    else:
        days = sorted(set(r.get("date", "") for r in data), reverse=True)

        for day in days:
            st.markdown(f"## 📅 {day}")

            for r in [x for x in data if x.get("date") == day]:
                title = f"تقرير رقم {r.get('no', '?')} - {r.get('time', '')}"

                with st.expander(title):
                    st.write("📍 الموقع:")
                    st.write(r.get("location", ""))

                    st.write("⚡ بيانات المحطة:")
                    st.write(r.get("station", ""))

                    st.write("🛠️ الأعمال المنجزة:")
                    st.write(r.get("work", ""))

                    st.write("📝 ملاحظات:")
                    st.write(r.get("notes", ""))

                    st.write("📦 المواد:")
                    render_materials(r.get("materials", {}))

                    st.markdown("---")
                    st.markdown("### ✏️ تعديل التقرير")

                    with st.form(f"edit_form_{r['id']}"):
                        new_location = st.text_input("الموقع", r.get("location", ""), key=f"edit_loc_{r['id']}")
                        new_station = st.text_input("بيانات المحطة", r.get("station", ""), key=f"edit_station_{r['id']}")
                        new_work = st.text_area("الأعمال المنجزة", r.get("work", ""), key=f"edit_work_{r['id']}")
                        new_notes = st.text_area("ملاحظات", r.get("notes", ""), key=f"edit_notes_{r['id']}")

                        old_m = normalize_materials(r.get("materials", {}))

                        st.write("🔌 الكيابل")
                        edit_cable_cols = st.columns(4)
                        edit_cables = {}

                        for i, c in enumerate(CABLES):
                            with edit_cable_cols[i]:
                                count = st.number_input(
                                    f"كيبل {c} - عدد",
                                    min_value=0,
                                    value=int(old_m["cables"][c]["count"]),
                                    step=1,
                                    key=f"edit_c_count_{r['id']}_{c}"
                                )
                                meter = st.number_input(
                                    f"كيبل {c} - متر",
                                    min_value=0,
                                    value=int(old_m["cables"][c]["meter"]),
                                    step=1,
                                    key=f"edit_c_meter_{r['id']}_{c}"
                                )
                                edit_cables[c] = {"count": int(count), "meter": int(meter)}

                        st.write("🔩 S/J")
                        edit_sj_cols = st.columns(5)
                        edit_sj = {}

                        for i, s in enumerate(SJ_TYPES):
                            with edit_sj_cols[i]:
                                qty = st.number_input(
                                    f"S/J {s}",
                                    min_value=0,
                                    value=int(old_m["sj"][s]),
                                    step=1,
                                    key=f"edit_sj_{r['id']}_{s}"
                                )
                                edit_sj[s] = int(qty)

                        st.write("🔧 T/J")
                        edit_tj_cols = st.columns(3)
                        edit_tj = {}

                        for i, t in enumerate(TJ_TYPES):
                            with edit_tj_cols[i]:
                                qty = st.number_input(
                                    f"T/J {t}",
                                    min_value=0,
                                    value=int(old_m["tj"][t]),
                                    step=1,
                                    key=f"edit_tj_{r['id']}_{t}"
                                )
                                edit_tj[t] = int(qty)

                        col1, col2 = st.columns(2)
                        with col1:
                            new_boot = st.number_input(
                                "Boot End 300",
                                min_value=0,
                                value=int(old_m["boot"]),
                                step=1,
                                key=f"edit_boot_{r['id']}"
                            )
                        with col2:
                            new_inspection = st.number_input(
                                "عدد الفحص",
                                min_value=0,
                                value=int(old_m["inspection"]),
                                step=1,
                                key=f"edit_inspection_{r['id']}"
                            )

                        save_edit = st.form_submit_button("💾 حفظ التعديل")

                    if save_edit:
                        for idx, item in enumerate(data):
                            if item["id"] == r["id"]:
                                data[idx]["location"] = new_location
                                data[idx]["station"] = new_station
                                data[idx]["work"] = new_work
                                data[idx]["notes"] = new_notes
                                data[idx]["materials"] = {
                                    "cables": edit_cables,
                                    "sj": edit_sj,
                                    "tj": edit_tj,
                                    "boot": int(new_boot),
                                    "inspection": int(new_inspection)
                                }

                        save_data(data)
                        st.success("تم تعديل التقرير ✅")
                        st.rerun()

                    if st.button(f"🗑️ حذف تقرير رقم {r.get('no', '?')}", key=f"delete_{r['id']}"):
                        data = [x for x in data if x["id"] != r["id"]]
                        save_data(data)
                        st.success("تم حذف التقرير ✅")
                        st.rerun()

# ================= التقارير الشهرية =================
with tab3:
    st.subheader("📊 التقارير الشهرية")

    year_total = empty_total()

    for month_num, month_name in MONTHS.items():
        month_reports = [r for r in data if f"-{month_num}-" in r.get("date", "")]

        if not month_reports:
            continue

        month_total = empty_total()

        for r in month_reports:
            add_to_total(month_total, r.get("materials", {}))
            add_to_total(year_total, r.get("materials", {}))

        with st.expander(f"📅 تقارير شهر {month_name}"):
            render_total(month_total, f"مواد شهر {month_name}")

            st.markdown("---")
            st.markdown("### 📋 تقارير الشهر")

            for r in month_reports:
                with st.expander(f"تقرير رقم {r.get('no', '?')} - {r.get('time', '')}"):
                    st.write("📍 الموقع:")
                    st.write(r.get("location", ""))

                    st.write("⚡ بيانات المحطة:")
                    st.write(r.get("station", ""))

                    st.write("🛠️ الأعمال المنجزة:")
                    st.write(r.get("work", ""))

                    st.write("📝 ملاحظات:")
                    st.write(r.get("notes", ""))

                    st.write("📦 المواد:")
                    render_materials(r.get("materials", {}))

    st.markdown("---")
    render_total(year_total, "مجموع المواد خلال السنة")
