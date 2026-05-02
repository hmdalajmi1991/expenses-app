st.subheader("➕ إضافة بلاغ")

raw_text = st.text_area("📋 الصق رسالة الواتساب")

if "materials" not in st.session_state:
    st.session_state.materials = []

# زر التحليل
if st.button("🔍 تحليل الرسالة"):
    st.session_state.materials = extract_materials(raw_text)

materials = st.session_state.materials

edited_materials = []

if materials:
    st.write("🔍 المواد المقترحة (عدلها إذا فيها خطأ):")

    for i, m in enumerate(materials):
        col1, col2, col3 = st.columns(3)

        with col1:
            t = st.text_input(f"نوع {i}", m["type"], key=f"type{i}")
        with col2:
            s = st.text_input(f"حجم {i}", m["size"], key=f"size{i}")
        with col3:
            q = st.number_input(f"كمية {i}", value=m["qty"], key=f"qty{i}")

        edited_materials.append({"type": t, "size": s, "qty": q})
