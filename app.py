
import streamlit as st
import csv
import io

st.set_page_config(
    page_title="Student Marksheet Automation",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eaf5ff, #f5edff, #fff5fb);
        color: #24345b;
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.85);
    }

    h1 {
        color: #5b4bdb !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #7138c8 !important;
    }

    label, [data-testid="stWidgetLabel"] p {
        color: #34466e !important;
        font-weight: 600 !important;
    }

    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.92);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #dce4ff;
        box-shadow: 0 8px 25px rgba(91, 75, 219, 0.08);
    }

    input, textarea {
        background-color: #f2f6ff !important;
        color: #24345b !important;
        border: 1px solid #d5dfff !important;
        border-radius: 10px !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-testid="stNumberInput"] button {
        background-color: #edf3ff !important;
        color: #24345b !important;
        border-color: #d5dfff !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff, #f0edff);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #ded8ff;
        box-shadow: 0 5px 16px rgba(91, 75, 219, 0.08);
    }

    [data-testid="stMetricValue"] {
        color: #5b4bdb !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #6688ff, #9b4de0) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 8px 18px !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(90deg, #4f6ee8, #8134c6) !important;
        color: white !important;
        transform: translateY(-1px);
    }

    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 14px;
        border: 1px solid #dce4ff;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)



if "students" not in st.session_state:
    st.session_state.students = []

def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 40:
        return "E"
    return "F"

st.title("🎓 Student Marksheet Automation")
st.write("Create customized marksheets with different subjects and maximum marks.")

st.header("Generate Student Marksheet")

# Choose how many subjects this student has
subject_count = st.number_input(
    "Number of subjects for this student",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

with st.form("marksheet_form"):
    name = st.text_input("Student Name")
    roll_no = st.text_input("Roll Number")

    st.subheader("Subjects and Marks")
    student_subjects = {}

    for i in range(int(subject_count)):
        st.markdown(f"**Subject {i + 1}**")
        col1, col2, col3 = st.columns(3)

        with col1:
            subject_name = st.text_input(
                "Subject Name",
                value=f"Subject {i + 1}",
                key=f"subject_name_{i}"
            )

        with col2:
            max_marks = st.number_input(
                "Maximum Marks",
                min_value=1,
                max_value=1000,
                value=100,
                step=1,
                key=f"max_marks_{i}"
            )

        with col3:
            marks_obtained = st.number_input(
                "Marks Obtained",
                min_value=0,
                max_value=1000,
                value=0,
                step=1,
                key=f"obtained_marks_{i}"
            )

        student_subjects[subject_name.strip()] = {
            "marks": marks_obtained,
            "max_marks": max_marks
        }

    submitted = st.form_submit_button("Generate Marksheet")

if submitted:
    if not name.strip() or not roll_no.strip():
        st.error("Please enter the student name and roll number.")
    elif any(
        s["roll_no"].lower() == roll_no.strip().lower()
        for s in st.session_state.students
    ):
        st.error("This roll number already exists in this session.")
    elif any(not subject.strip() for subject in student_subjects):
        st.error("Please enter every subject name.")
    elif len(student_subjects) != int(subject_count):
        st.error("Subject names must be unique. Please check duplicates.")
    elif any(
        data["marks"] > data["max_marks"]
        for data in student_subjects.values()
    ):
        st.error("Marks obtained cannot exceed maximum marks.")
    else:
        total = sum(s["marks"] for s in student_subjects.values())
        maximum = sum(s["max_marks"] for s in student_subjects.values())
        percentage = (total / maximum) * 100

        passed = all(
            (s["marks"] / s["max_marks"]) * 100 >= 35
            for s in student_subjects.values()
        )

        st.session_state.students.append({
            "name": name.strip(),
            "roll_no": roll_no.strip(),
            "subjects": student_subjects.copy(),
            "total": total,
            "maximum": maximum,
            "percentage": percentage,
            "grade": calculate_grade(percentage),
            "result": "PASS" if passed else "FAIL"
        })

        st.success("Marksheet generated successfully!")

students = sorted(
    st.session_state.students,
    key=lambda s: s["percentage"],
    reverse=True
)

for i, student in enumerate(students):
    student["rank"] = i + 1

if students:
    st.divider()
    st.header("Class Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(students))
    col2.metric(
        "Passed",
        sum(s["result"] == "PASS" for s in students)
    )
    col3.metric(
        "Failed",
        sum(s["result"] == "FAIL" for s in students)
    )

    st.header("Ranking Summary")

    st.dataframe([
        {
            "Rank": s["rank"],
            "Name": s["name"],
            "Roll Number": s["roll_no"],
            "Total": f'{s["total"]} / {s["maximum"]}',
            "Percentage": f'{s["percentage"]:.2f}%',
            "Grade": s["grade"],
            "Result": s["result"]
        }
        for s in students
    ], use_container_width=True, hide_index=True)

    st.header("Search Student")
    search_roll = st.text_input("Search by Roll Number")

    if search_roll.strip():
        matches = [
            s for s in students
            if s["roll_no"].lower() == search_roll.strip().lower()
        ]

        if matches:
            s = matches[0]
            st.subheader(f'Marksheet: {s["name"]}')
            st.write(f'Roll Number: {s["roll_no"]}')

            st.dataframe([
                {
                    "Subject": subject,
                    "Marks Obtained": data["marks"],
                    "Maximum Marks": data["max_marks"],
                    "Percentage": (
                        f'{data["marks"] / data["max_marks"] * 100:.2f}%'
                    )
                }
                for subject, data in s["subjects"].items()
            ], use_container_width=True, hide_index=True)

            st.write(f'Total: {s["total"]} / {s["maximum"]}')
            st.write(f'Percentage: {s["percentage"]:.2f}%')
            st.write(f'Grade: {s["grade"]}')
            st.write(f'Result: {s["result"]}')
            st.write(f'Rank: {s["rank"]}')
        else:
            st.warning("Student not found.")

    # CSV export supports different subjects for different students
    all_subjects = list(dict.fromkeys(
        subject
        for s in students
        for subject in s["subjects"]
    ))

    output = io.StringIO()
    writer = csv.writer(output)

    headers = ["Rank", "Name", "Roll Number"]
    for subject in all_subjects:
        headers.extend([f"{subject} Marks", f"{subject} Maximum"])

    headers.extend(["Total", "Maximum Total", "Percentage", "Grade", "Result"])
    writer.writerow(headers)

    for s in students:
        row = [s["rank"], s["name"], s["roll_no"]]

        for subject in all_subjects:
            data = s["subjects"].get(subject)
            if data:
                row.extend([data["marks"], data["max_marks"]])
            else:
                row.extend(["", ""])

        row.extend([
            s["total"],
            s["maximum"],
            round(s["percentage"], 2),
            s["grade"],
            s["result"]
        ])
        writer.writerow(row)

    st.download_button(
        "Download Marksheets CSV",
        data=output.getvalue(),
        file_name="marksheets.csv",
        mime="text/csv"
    )

else:
    st.info("Enter the first student's details above to get started.")
