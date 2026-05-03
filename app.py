import streamlit as st
from datetime import datetime
import json
import uuid

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")
st.title("⚡ نظام تقارير الأعطال والمواد")

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

def empty_materials():
    return {
        "cables": {c: {"count": 0, "meter": 0} for c in CABLES},
        "sj": {s: 0 for s in SJ_TYPES},
        "tj": {t: 0 for t in TJ_TYPES},
        "boot_300": 0,
        "inspection_count": 0
    }

def get_materials_total():
    return {
        "cables": {c: {"count": 0, "meter": 0} for c in CABLES},
        "sj": {s: 0 for s in SJ_TYPES},
        "tj": {t: 0 for t in TJ_TYPES},
        "boot_300": 0,
        "inspection_count": 0
    }

def add_to_total(total, materials):
    for c in CABLES:
        total["cables"][c]["count"] += materials["cables"][c]["count"]
        total["cables"][c]["meter"] += materials["cables"][c]["meter"]

    for s in SJ_TYPES:
        total["sj"][s] += materials["sj"][s]

    for t in TJ_TYPES:
        total["tj"][t] += materials["tj"][t]

    total["boot_300"] += materials["boot_300"]
    total["inspection_count"] += materials["inspection_count"]

data = load_data()

tab1, tab2, tab3 = st.tabs(["➕ إضافة تقرير", "📁 التقارير اليومية", "📊 مجموع الشهر"])

# ================= إضافة تقرير =================
with tab1:
    st.subheader("➕ إضافة تقرير جديد")

    with st.form("add_report_form", clear_on_submit=True):

        st.markdown("### 📍 الموقع")
        location = st.text_input("الموقع")

        st.markdown("### ⚡ بيانات المحطة")
        station_info = st.text_input("بيانات المحطة")

        st.markdown("### 🛠️ الأعمال المنجزة")
        work_done = st.text_area("الأعمال المنجزة", height=120)

        st.markdown("### 📝 ملاحظات")
        notes = st.text_area("ملاحظات", height=100)

        st.markdown("### 📦 المواد المستخدمة")

        st.write("🔌 الكيابل")
        c_cols = st.columns(4)
        cable_inputs = {}

        for i, c in enumerate(CABLES):
            with c_cols[i]:
                count = st.number_input(f"كيبل {c} - عدد", min_value=0, step=1, key=f"add_c_count_{c}")
                meter = st.number_input(f"كيبل {c} - متر", min_value=0, step=1, key=f"add_c_meter_{c}")
                cable_inputs[c] = {"count": int(count), "meter": int(meter)}

        st.write("🔩 S/J")
        sj_cols = st.columns(5)
        sj_inputs = {}

        for i, s in enumerate(SJ_TYPES):
            with sj_cols[i]:
                qty = st.number_input(f"S/J {s}", min_value=0, step=1, key=f"add_sj_{s}")
                sj_inputs[s] = int(qty)

        st.write("🔧 T/J")
        tj_cols = st.columns(3)
        tj_inputs = {}

        for i, t in enumerate(TJ_TYPES):
            with tj_cols[i]:
                qty = st.number_input(f"T/J {t}", min_value=0, step=1, key=f"add_tj_{t}")
                tj_inputs[t] = int(qty)

        st.write("🧩 Boot End / الفحص")
        col_boot, col_inspect = st.columns(2)

        with col_boot:
            boot_300 = st.number_input("Boot End 300", min_value=0, step=1)

        with col_inspect:
            inspection_count = st.number_input("عدد الفحص", min_value=0, step=1)

        submitted = st.form_submit_button("💾 حفظ التقرير")

    if submitted:
        now = datetime.now()

        report = {
            "id": str(uuid.uuid4()),
            "report_no": len(data) + 1,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "datetime": now.strftime("%Y-%m-%d %H:%M"),
            "location": location,
            "station_info": station_info,
            "work_done": work_done,
            "notes": notes,
            "materials": {
                "cables": cable_inputs,
                "sj": sj_inputs,
                "tj": tj_inputs,
                "boot_300": int(boot_300),
                "inspection_count": int(inspection_count)
            }
        }

        data.append(report)
        save_data(data)
        st.success("تم حفظ التقرير ✅")

# ================= التقارير اليومية + تعديل =================
with tab2:
    st.subheader("📁 التقارير اليومية")

    if not data:
        st.info("لا توجد تقارير محفوظة")
    else:
        dates = sorted(set(r["date"] for r in data), reverse=True)

        for day in dates:
            st.markdown(f"## 📅 {day}")
            day_reports = [r for r in data if r["date"] == day]

            for r in day_reports:
                with st.expander(f"تقرير رقم {r.get('report_no', '?')} - {r.get('time', '')}"):

                    st.write("📍 الموقع:")
                    st.write(r.get("location", ""))

                    st.write("⚡ بيانات المحطة:")
                    st.write(r.get("station_info", ""))

                    st.write("🛠️ الأعمال المنجزة:")
                    st.write(r.get("work_done", ""))

                    st.write("📝 ملاحظات:")
                    st.write(r.get("notes", ""))

                    st.write("📦 المواد المصروفة:")
                    materials = r["materials"]

                    for c in CABLES:
                        cdata = materials["cables"][c]
                        if cdata["count"] > 0 or cdata["meter"] > 0:
                            st.write(f"كيبل {c}: {cdata['count']} عدد / {cdata['meter']} متر")

                    for s in SJ_TYPES:
                        if materials["sj"][s] > 0:
                            st.write(f"S/J {s}: {materials['sj'][s]} عدد")

                    for t in TJ_TYPES:
                        if materials["tj"][t] > 0:
                            st.write(f"T/J {t}: {materials['tj'][t]} عدد")

                    if materials["boot_300"] > 0:
                        st.write(f"Boot End 300: {materials['boot_300']} عدد")

                    if materials["inspection_count"] > 0:
                        st.write(f"عدد الفحص: {materials['inspection_count']}")

                    st.markdown("---")
                    st.markdown("### ✏️ تعديل التقرير")

                    with st.form(f"edit_form_{r['id']}"):

                        new_location = st.text_input("الموقع", r.get("location", ""), key=f"loc_{r['id']}")
                        new_station = st.text_input("بيانات المحطة", r.get("station_info", ""), key=f"station_{r['id']}")
                        new_work = st.text_area("الأعمال المنجزة", r.get("work_done", ""), key=f"work_{r['id']}")
                        new_notes = st.text_area("ملاحظات", r.get("notes", ""), key=f"notes_{r['id']}")

                        st.write("🔌 الكيابل")
                        edit_cables = {}
                        edit_c_cols = st.columns(4)

                        for i, c in enumerate(CABLES):
                            with edit_c_cols[i]:
                                old = materials["cables"][c]
                                count = st.number_input(f"كيبل {c} عدد", min_value=0, value=int(old["count"]), step=1, key=f"edit_c_count_{r['id']}_{c}")
                                meter = st.number_input(f"كيبل {c} متر", min_value=0, value=int(old["meter"]), step=1, key=f"edit_c_meter_{r['id']}_{c}")
                                edit_cables[c] = {"count": int(count), "meter": int(meter)}

                        st.write("🔩 S/J")
                        edit_sj = {}
                        edit_sj_cols = st.columns(5)

                        for i, s in enumerate(SJ_TYPES):
                            with edit_sj_cols[i]:
                                qty = st.number_input(f"S/J {s}", min_value=0, value=int(materials["sj"][s]), step=1, key=f"edit_sj_{r['id']}_{s}")
                                edit_sj[s] = int(qty)

                        st.write("🔧 T/J")
                        edit_tj = {}
                        edit_tj_cols = st.columns(3)

                        for i, t in enumerate(TJ_TYPES):
                            with edit_tj_cols[i]:
                                qty = st.number_input(f"T/J {t}", min_value=0, value=int(materials["tj"].get(t, 0)), step=1, key=f"edit_tj_{r['id']}_{t}")
                                edit_tj[t] = int(qty)

                        col_boot, col_inspect = st.columns(2)

                        with col_boot:
                            new_boot = st.number_input("Boot End 300", min_value=0, value=int(materials.get("boot_300", 0)), step=1, key=f"edit_boot_{r['id']}")

                        with col_inspect:
                            new_inspection = st.number_input("عدد الفحص", min_value=0, value=int(materials.get("inspection_count", 0)), step=1, key=f"edit_inspection_{r['id']}")

                        save_edit = st.form_submit_button("💾 حفظ التعديل")

                    if save_edit:
                        for idx, item in enumerate(data):
                            if item["id"] == r["id"]:
                                data[idx]["location"] = new_location
                                data[idx]["station_info"] = new_station
                                data[idx]["work_done"] = new_work
                                data[idx]["notes"] = new_notes
                                data[idx]["materials"] = {
                                    "cables": edit_cables,
                                    "sj": edit_sj,
                                    "tj": edit_tj,
                                    "boot_300": int(new_boot),
                                    "inspection_count": int(new_inspection)
                                }
                                save_data(data)
                                st.success("تم تعديل التقرير ✅")
                                st.rerun()

                    if st.button(f"🗑️ حذف تقرير رقم {r.get('report_no', '?')}", key=f"delete_{r['id']}"):
                        data = [x for x in data if x["id"] != r["id"]]
                        save_data(data)
                        st.success("تم حذف التقرير")
                        st.rerun()

# ================= تقرير شهري =================
with tab3:
    st.subheader("📊 مجموع المواد المستهلكة خلال الشهر")

    month = st.text_input("اكتب رقم الشهر مثال: 05")

    if st.button("📈 عرض مجموع الشهر"):
        total = get_materials_total()
        month_reports = []

        for r in data:
            if f"-{month}-" in r["date"]:
                month_reports.append(r)
                add_to_total(total, r["materials"])

        st.write(f"عدد التقارير في الشهر: {len(month_reports)}")

        st.markdown("## 🔌 إجمالي الكيابل")
        for c in CABLES:
            st.write(f"كيبل {c}: {total['cables'][c]['count']} عدد / {total['cables'][c]['meter']} متر")

        st.markdown("## 🔩 إجمالي S/J")
        for s in SJ_TYPES:
            st.write(f"S/J {s}: {total['sj'][s]} عدد")

        st.markdown("## 🔧 إجمالي T/J")
        for t in TJ_TYPES:
            st.write(f"T/J {t}: {total['tj'][t]} عدد")

        st.markdown("## 🧩 Boot End / الفحص")
        st.write(f"Boot End 300: {total['boot_300']} عدد")
        st.write(f"عدد الفحص: {total['inspection_count']}")
