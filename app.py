
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Record Management System")
st.write("Manage student records using CRUD operations.")

# Initialize student data
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course", "Marks"]
    )

df = st.session_state.students

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("➕ Add New Student")

    with st.form("add_form"):
        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        marks = st.number_input("Marks", min_value=0, max_value=100)

        submit = st.form_submit_button("Add Student")

        if submit:
            if name and course:
                if roll not in df["Roll No"].values:
                    new_student = pd.DataFrame([{
                        "Roll No": roll,
                        "Name": name,
                        "Age": age,
                        "Course": course,
                        "Marks": marks
                    }])

                    st.session_state.students = pd.concat(
                        [df, new_student], ignore_index=True
                    )
                    st.success("Student added successfully!")
                else:
                    st.error("Roll Number already exists!")
            else:
                st.warning("Please enter Name and Course.")

# READ
elif menu == "View Students":
    st.subheader("📋 Student Records")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.write("Total Students:", len(df))
    else:
        st.info("No student records found.")

# UPDATE
elif menu == "Update Student":
    st.subheader("✏️ Update Student Details")

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"].tolist())

        student = df[df["Roll No"] == roll].iloc[0]

        with st.form("update_form"):
            name = st.text_input("Name", value=student["Name"])
            age = st.number_input(
                "Age", min_value=1, max_value=100,
                value=int(student["Age"])
            )
            course = st.text_input("Course", value=student["Course"])
            marks = st.number_input(
                "Marks", min_value=0, max_value=100,
                value=int(student["Marks"])
            )

            update = st.form_submit_button("Update Student")

            if update:
                idx = df.index[df["Roll No"] == roll][0]

                st.session_state.students.loc[idx, "Name"] = name
                st.session_state.students.loc[idx, "Age"] = age
                st.session_state.students.loc[idx, "Course"] = course
                st.session_state.students.loc[idx, "Marks"] = marks

                st.success("Student record updated successfully!")
    else:
        st.info("No records available to update.")

# DELETE
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student Record")

    if not df.empty:
        roll = st.selectbox("Select Roll Number to Delete",
                            df["Roll No"].tolist())

        if st.button("Delete Student", type="primary"):
            st.session_state.students = df[
                df["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student deleted successfully!")
    else:
        st.info("No records available to delete.")

st.sidebar.markdown("---")
st.sidebar.info("Student Management System | Python + Streamlit")
