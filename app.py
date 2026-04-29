import streamlit as st
import pandas as pd

st.set_page_config(page_title="مصاريفي", page_icon="💰")

st.title("💰 مصاريفي")
st.write("سجل مصاريفك وشوف وضع ميزانيتك")

# إدخال البيانات
budget = st.number_input("💵 كم ميزانيتك؟", min_value=0.0)
expense = st.number_input("🧾 كم صرفت؟", min_value=0.0)

category = st.selectbox(
    "📂 اختر التصنيف",
    ["🍔 أكل", "☕ قهوة", "⛽ بنزين", "🛍️ تسوق", "🎮 ترفيه"]
)

# قراءة البيانات من الملف
expenses_list = []
categories_list = []

try:
    file = open("expenses.txt", "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2:
            categories_list.append(parts[0])
            expenses_list.append(float(parts[1]))
except:
    pass

# الأزرار
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ إضافة"):
        file = open("expenses.txt", "a")
        file.write(f"{category},{expense}\n")
        file.close()
        st.success("تمت الإضافة ✅")
        st.rerun()

with col2:
    show = st.button("📊 عرض")

with col3:
    if st.button("🗑️ مسح الكل"):
        file = open("expenses.txt", "w")
        file.close()
        st.warning("تم مسح كل المصاريف ❌")
        st.rerun()

# عرض النتائج
if show:
    total = sum(expenses_list)
    remaining = budget - total

    # الرسم البياني
    data = {}

    for i in range(len(expenses_list)):
        cat = categories_list[i]
        val = expenses_list[i]

        if cat in data:
            data[cat] += val
        else:
            data[cat] = val

    df = pd.DataFrame(list(data.items()), columns=["Category", "Amount"])

    st.subheader("📊 توزيع المصاريف")
    st.bar_chart(df.set_index("Category"))

    # النتائج
    st.subheader("📌 النتائج")
    st.metric("مجموع المصاريف", total)
    st.metric("الباقي", remaining)

    if budget > 0:
        percent = (total / budget) * 100
        st.progress(min(percent / 100, 1.0))
        st.write("نسبة الصرف:", int(percent), "%")

        if percent > 100:
            st.error("❌ تعديت الميزانية!")
        elif percent > 80:
            st.warning("⚠️ قربت تخلص الميزانية")
        else:
            st.success("✅ وضعك ممتاز")
