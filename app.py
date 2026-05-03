import streamlit as st
from datetime import datetime
import json
import uuid

st.set_page_config(page_title="نظام الأعطال", page_icon="⚡")
st.title("⚡ نظام تقارير الأعطال والمواد")

DATA_FILE = "data.json"

CABLES = ["300", "240", "150", "35"]
SJ_TYPES = ["300-300", "300-150", "150-150", "150-35", "35-35"]

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

def empty_totals():
    return {
        "cables": {c: {"count": 0, "meter": 0} for c in CABLES},
        "sj": {s: 0 for s in SJ_TYPES},
        "boot_300": 0
    }

def add_to_totals(total, materials):
    for c in CABLES:
        total["cables"][c]["count"] += materials["cables"][c]["count"]
        total["cables"][c]["meter"] += materials["cables"][c]["meter"]

    for s in SJ_TYPES:
        total["sj"][s] += materials["sj"][s]

    total["boot_300"] += materials["boot_300"]

def materials_is_empty(materials):
    for c in CABLES:
        if materials["cables"][c]["count"] > 0 or materials["cables"][c]["meter"] > 0:
            return False
    for s in SJ_TYPES:
        if materials["sj"][s] > 0:
            return False
    if materials["boot_300"] > 0:
        return False
    return True

data = load_data()

tab1, tab2, tab3 = st.tabs(["➕ إضافة تقرير", "📁 التقارير اليومية", "📊 مجموع الشهر"])

# ================= إضافة تقرير =================
with tab1:
    st.subheader("➕ إضافة تقرير جديد")

    with st.form("add_report_form", clear_on_submit=True):
        whatsapp_text = st.text_area("📋 الاعمال المنجزه ", height=140)

        st.write("📦 الكيابل")
        c_cols = st.columns(4)

        cable_inputs = {}
        for i, c in enumerate(CABLES):
            with c_cols[i]:
                count = st.number_input(f"كيبل {c} - عدد", min_value=0, step=1, key=f"c_count_{c}")
                meter = st.number_input(f"كيبل {c} - متر", min_value=0, step=1, key=f"c_meter_{c}")
                cable_inputs[c] = {"count": int(count), "meter": int(meter)}

        st.write("🔩 S/J")
        sj_cols = st.columns(5)

        sj_inputs = {}
        for i, s in enumerate(SJ_TYPES):
            with sj_cols[i]:
                qty = st.number_input(f"S/J {s}", min_value=0, step=1, key=f"sj_{s}")
                sj_inputs[s] = int(qty)

        st.write("🧩 Boot End")
        boot_300 = st.number_input("Boot End 300", min_value=0, step=1)

        submitted = st.form_submit_button("💾 حفظ التقرير")

    if submitted:
        materials = {
            "cables": cable_inputs,
            "sj": sj_inputs,
            "boot_300": int(boot_300)
        }

        if whatsapp_text.strip() == "" and materials_is_empty(materials):
            st.warning("ما يصير تحفظ تقرير فاضي")
        else:
            now = datetime.now()
            report = {
                "id": str(uuid.uuid4()),
                "report_no": len(data) + 1,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M"),
                "datetime": now.strftime("%Y-%m-%d %H:%M"),
                "text": whatsapp_text,
                "materials": materials
            }

            # منع تكرار نفس الحفظ مباشرة
            if data:
                last = data[-1]
                if last.get("text") == report["text"] and last.get("materials") == report["materials"]:
                    st.warning("هذا نفس آخر تقرير محفوظ، ما تم تكراره")
                else:
                    data.append(report)
                    save_data(data)
                    st.success("تم حفظ التقرير ✅")
            else:
                data.append(report)
                save_data(data)
                st.success("تم حفظ التقرير ✅")

# ================= التقارير اليومية =================
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
                title = f"تقرير رقم {r.get('report_no', '?')} - {r.get('time', '')}"

                with st.expander(title):
                    st.write("📋 رسالة القروب:")
                    st.write(r.get("text", ""))

                    st.write("📦 المواد المصروفة لهذا التقرير:")

                    materials = r["materials"]

                    st.markdown("### 🔌 الكيابل")
                    for c in CABLES:
                        count = materials["cables"][c]["count"]
                        meter = materials["cables"][c]["meter"]
                        if count > 0 or meter > 0:
                            st.write(f"كيبل {c}: {count} عدد / {meter} متر")

                    st.markdown("### 🔩 S/J")
                    for s in SJ_TYPES:
                        qty = materials["sj"][s]
                        if qty > 0:
                            st.write(f"S/J {s}: {qty} عدد")

                    st.markdown("### 🧩 Boot End")
                    if materials["boot_300"] > 0:
                        st.write(f"Boot End 300: {materials['boot_300']} عدد")

                    if st.button(f"🗑️ حذف تقرير رقم {r.get('report_no', '?')}", key=r["id"]):
                        data = [x for x in data if x["id"] != r["id"]]
                        save_data(data)
                        st.success("تم حذف التقرير")
                        st.rerun()

# ================= تقرير شهري =================
with tab3:
    st.subheader("📊 مجموع المواد المستهلكة خلال الشهر")

    month = st.text_input("اكتب رقم الشهر مثال: 05")

    if st.button("📈 عرض مجموع الشهر"):
        if month.strip() == "":
            st.warning("اكتب رقم الشهر")
        else:
            total = empty_totals()
            month_reports = []

            for r in data:
                if f"-{month}-" in r["date"]:
                    month_reports.append(r)
                    add_to_totals(total, r["materials"])

            st.write(f"عدد التقارير في الشهر: {len(month_reports)}")

            st.markdown("## 🔌 إجمالي الكيابل")
            for c in CABLES:
                st.write(
                    f"كيبل {c}: "
                    f"{total['cables'][c]['count']} عدد / "
                    f"{total['cables'][c]['meter']} متر"
                )

            st.markdown("## 🔩 إجمالي S/J")
            for s in SJ_TYPES:
                st.write(f"S/J {s}: {total['sj'][s]} عدد")

            st.markdown("## 🧩 إجمالي Boot End")
            st.write(f"Boot End 300: {total['boot_300']} عدد")

            st.markdown("## 📋 تقارير هذا الشهر")
            for r in month_reports:
                st.write(f"- تقرير رقم {r.get('report_no', '?')} | {r['datetime']}")
