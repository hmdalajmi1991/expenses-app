import streamlit as st

st.set_page_config(page_title="مصاريفي", page_icon="💰")

st.title("💰 مصاريفي")
st.write("سجل مصاريفك وشوف وضع ميزانيتك")

budget = st.number_input("💵 كم ميزانيتك؟", min_value=0.0)
expense = st.number_input("🧾 كم صرفت؟", min_value=0.0)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ إضافة"):
        file = open("expenses.txt", "a")
        file.write(str(expense) + "\n")
        file.close()
        st.success("تمت الإضافة ✅")

with col2:
    show = st.button("📊 عرض")

with col3:
    if st.button("🗑️ مسح الكل"):
        file = open("expenses.txt", "w")
        file.close()
        st.warning("تم مسح المصاريف")

try:
    file = open("expenses.txt", "r")
    numbers = file.readlines()
    file.close()

    expenses_list = []

    for n in numbers:
        if n.strip() != "":
            expenses_list.append(float(n.strip()))

except:
    expenses_list = []

if len(expenses_list) > 0:
    st.subheader("📋 المصاريف المسجلة")

    for index, value in enumerate(expenses_list):
        st.write(index + 1, "-", value)

    delete_number = st.number_input(
        "اكتب رقم المصروف اللي تبي تحذفه",
        min_value=1,
        max_value=len(expenses_list),
        step=1
    )

    if st.button("❌ حذف مصروف"):
        expenses_list.pop(delete_number - 1)

        file = open("expenses.txt", "w")
        for item in expenses_list:
            file.write(str(item) + "\n")
        file.close()

        st.success("تم حذف المصروف ✅")
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
