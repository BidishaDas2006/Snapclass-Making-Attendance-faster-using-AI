import streamlit as st


@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher to enroll")
    join_code = st.text_input('subject_code', placeholder = 'e.g.CS101' )
    
