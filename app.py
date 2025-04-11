
import streamlit as st
import os
from datetime import datetime
from database import init_db, insert_record, get_all_records
from utils import save_uploaded_images, export_excel

st.set_page_config(page_title="保研坞小卫星计划", layout="wide")
st.title("🚀 保研坞 · 小卫星计划")

init_db()

# 表单输入
with st.form("record_form"):
    school = st.text_input("🎓 保研院校名称")
    interview_date = st.date_input("🗓️ 面试时间")
    process = st.text_area("🧪 考核流程")
    lesson = st.text_area("📌 经验教训")

    images = st.file_uploader("📷 上传图片（可多选）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    descriptions = []
    for i in range(len(images)):
        descriptions.append(st.text_input(f"备注 - 图片{i+1}"))

    submitted = st.form_submit_button("✅ 提交记录")

if submitted:
    record_id = insert_record(school, str(interview_date), process, lesson)
    save_uploaded_images(record_id, images, descriptions)
    st.success("记录已保存！")

st.markdown("---")
st.subheader("📚 我的记录")
if st.button("📥 导出为 Excel"):
    export_excel()

records = get_all_records()
for r in records:
    with st.expander(f"📌 {r['school_name']} - {r['interview_date']}"):
        st.markdown(f"**考核流程：** {r['assessment_process']}")
        st.markdown(f"**经验教训：** {r['lessons_learned']}")
        image_dir = f"uploads/{r['id']}"
        if os.path.exists(image_dir):
            for file in os.listdir(image_dir):
                filepath = f"{image_dir}/{file}"
                if file.endswith(".txt"):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        st.caption(f"备注：{f.read()}")
                else:
                    st.image(filepath, width=300)
