import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout , style_bachground_home
from src.components.footer import footer_home



def home_screen():
    

    header_home()
    style_bachground_home()

    style_base_layout()


    col1, col2 = st.columns(2, gap = "large")

    with col1:
        st.header("I'm student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width = 120)
        if st.button('student portal', type = 'primary',icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login-type'] = 'student'
            st.rerun()
        

    with col2:
        st.header("I'm teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width = 145)
        if st.button('Teacher portal', type = 'primary', icon=':material/arrow_outward:', icon_position='right' ):

            st.session_state['login-type'] = 'teacher'
            st.rerun()
        
    footer_home()