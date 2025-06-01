import streamlit as st
from datetime import datetime
import json

# Set page configuration
st.set_page_config(
    page_title="سجل حضور مجموعة القرآن",
    layout="wide"
)

# Custom CSS for Arabic text and styling
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 40px !important;
        min-width: 40px !important;
        margin-top: 0 !important;
        display: inline-block !important;
        position: relative !important;
        top: 0 !important;
    }
    .main .block-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        max-width: 150px !important;
    }
    h1 {
        font-size: 1.5rem !important;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1f77b4;
        padding-top: 0.5rem !important;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(2) {
        margin-top: 1.5rem;
    }
    .section-divider {
        border-top: 1px solid #e0e0e0;
        margin: 2rem 0;
    }
    [data-testid="column"] {
        padding: 0 0.25rem !important;
    }
    .button-container {
        display: inline-flex !important;
        flex-direction: row !important;
        gap: 0.25rem !important;
        margin-top: 0 !important;
        align-items: center !important;
        position: relative !important;
        top: 0 !important;
    }
    .student-container {
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        margin-bottom: 0.25rem !important;
        padding-top: 0.25rem !important;
    }
    .stTextInput {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Center the title
st.title("سجل حضور مجموعة القرآن")

# Load data from JSON file
def load_data():
    try:
        with open('store.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"selected_date": None, "students": []}

# Save data to JSON file
def save_data(data):
    with open('store.json', 'w') as file:
        json.dump(data, file, indent=4)

# Load initial data
data = load_data()
selected_date = datetime.strptime(data['selected_date'], '%Y-%m-%d') if data['selected_date'] else datetime.now()
st.session_state.students = data['students']  # Initialize session state with loaded students

# Section 1: Date Selection
st.markdown('<div class="section-header">التاريخ</div>', unsafe_allow_html=True)
selected_date = st.date_input(
    "",
    value=selected_date,
    format="DD/MM/YYYY"
)

# Update the JSON file with the selected date
data['selected_date'] = selected_date.strftime('%Y-%m-%d')
save_data(data)

# Add divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Section 2: Add New Student
st.markdown('<div class="section-header">إضافة طالب</div>', unsafe_allow_html=True)
st.markdown('<div class="student-container">', unsafe_allow_html=True)
new_student = st.text_input("", key="new_student")
if st.button("➕", key="add_button"):
    if new_student:
        st.session_state.students.append(new_student)
        data['students'] = st.session_state.students
        save_data(data)  # Save the updated data to the JSON file
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Add divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Function to remove a student
def remove_student(index):
    st.session_state.students.pop(index)
    data['students'] = st.session_state.students
    save_data(data)

# Section 3: Students List
st.markdown('<div class="section-header">قائمة الطلاب</div>', unsafe_allow_html=True)
if st.session_state.students:
    st.info(f"يوجد {len(st.session_state.students)} طلاب مسجلين")

    for i, student in enumerate(st.session_state.students):
        st.markdown('<div class="student-container">', unsafe_allow_html=True)
        st.session_state.students[i] = st.text_input(
            "",
            value=student,
            key=f"student_{i}"
        )
        if st.button("➖", key=f"delete_{i}"):
            remove_student(i)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("لا يوجد طلاب مسجلين")
