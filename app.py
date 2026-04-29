import streamlit as st

st.set_page_config(page_title="مصاريفي", page_icon="💰")

st.title("💰 مصاريفي")
st.write("سجل مصاريفك وشوف وضع ميزانيتك")

budget = st.number_input("💵 كم ميزانيتك؟", min_value=0.0)

expense = st.number_input("🧾 كم صرفت؟", min_value=0.0)

category = st.selectbox(
    "📂 اختر التصنيف",
    ["🍔 أكل", "☕ قهوة", "⛽ بنزين", "🛍️ تسوق", "🎮 ترفيه", "📦 أخرى"]
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ إضافة"):
        file = open("expenses.txt", "a")
        file.write(f"{category},{expense}\n")
        file.close()
        st.success("تمت الإضافة ✅")

with col2:
    show = st.button("📊 عرض")

with col3:
    if st.button("🗑️ مسح الكل"):
        file = open("expenses.txt", "w")
        file.close()
        st.warning("تم مسح المصاريف")

expenses_list = []
categories_list = []

try:
    file = open("expenses.txt", "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        if line.strip() != "":
            cat, val = line.strip().split(",")
            categories_list.append(cat)
            expenses_list.append(float(val))
except:
    pass

if len(expenses_list) > 0:
    st.subheader("📋 المصاريف")

    for i in range(len(expenses_list)):
        st.write(i + 1, "-", categories_list[i], ":", expenses_list[i])

    delete_number = st.number_input(
        "اكتب رقم المصروف للحذف",
        min_value=1,
        max_value=len(expenses_list),
        step=1
    )

    if st.button("❌ حذف مصروف"):
        expenses_list.pop(delete_number - 1)
        categories_list.pop(delete_number - 1)

        file = open("expenses.txt", "w")
        for i in range(len(expenses_list)):
            file.write(f"{categories_list[i]},{expenses_list[i]}\n")
        file.close()

        st.success("تم الحذف ✅")
        st.rerun()

if show:
    total = sum(expenses_list)
    remaining = budget - total

    st.subheader("📌 النتائج")
    st.metric("مجموع المصاريف", total)
    st.metric("الباقي", remaining)

    if budget > 0:
        percent = (total / budget) * 100
        st.progress(min(percent / 100, 1.0))
        st.write("نسبة الصرف:", int(percent), "%")

        if percent > 100:
            st.error("❌ تعدّيت الميزانية!")
        elif percent > 80:
            st.warning("⚠️ قربت تخلص الميزانية")
        else:
            st.success("👍 وضعك ممتاز")
