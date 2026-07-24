import streamlit as st

from src.ui.base_layout import style_base_layout , style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np

def student_screen():
    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    
    with c1:
            header_dashboard()
    with c2:
            if st.button("Go back to home", type ='secondary', key = 'loginbackbtn', shortcut="control+backspace"):
                st.session_state['login-type'] = None
                st.rerun()    
    
    
    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()

    

    photo_source = st.camera_input("position your face in the center")

    if photo_source:
          np.array(Image.open(photo_source))

    footer_dashboard()
