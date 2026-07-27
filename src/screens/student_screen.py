import streamlit as st

from src.ui.base_layout import style_base_layout , style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embedding, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student
import time


show_registration = False
def student_dashboard():
      student_data = st.session_state.student_data
              
      c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
          
      with c1:
            header_dashboard()
      with c2:
            st.subheader(f"""Welcome, {student_data['name']}""")
            if st.button("Logout", type ='secondary', key = 'loginbackbtn', shortcut="control+backspace"):
                  st.session_state['is_logged_in'] = False
                  del st.session_state.student_data
                  st.rerun()    
          
      
      st.space()

      c1, c2 = st.columns(2)
      with c1:
            st.header("Youe Enrolled Subjects")
      with c2:
            if st.button('Enroll in subject', type = 'primary', width='stretch'):
                  enroll_dialog()

      st.divider()                 

      footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    show_registration = False

    if "student_data" in st.session_state:
          student_dashboard()
          return



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
          img = np.array(Image.open(photo_source))

          with st.spinner('AI is scanning...'):
                detected , all_ids, num_faces = predict_attendance(img)

                if num_faces == 0:
                      st.warning('face not found..') 
                if num_faces > 1:
                      st.warning('numtiple faces found')  
                else:
                      if detected:
                            student_id = list(detected.keys())[0]
                            all_students = get_all_students()
                            student = next((s for s in all_students if s['student_id'] == student_id), None)

                            if student:
                                  st.session_state.is_logged_in = True
                                  st.session_state.user_role = 'student'
                                  st.session_state.student_data = student
                                  st.toast(f'Welcome Back!{student['name']}')
                                  time.sleep(1)
                                  st.rerun()

                                  
                      else:
                           st.info('Face not recogtnized! , you might be a new student!') 
                           show_registration = True

    if show_registration:
          with st.container(border = True) : 
                st.header("Register new profile!") 
                new_name =st.text_input("Enter your name", placeholder='e.g. Bidisha Das')


                st.subheader('Optional : voice enrollment')
                st.info("Enroll for voice only attendance")

                audio_data = None

                try:
                        audio_data = st.audio_input('Record a short phase like I am present, My name is Bidisha.')
                except Exception:
                        st.error('Audio  data failed !')

                if st.button('Create Account', type = 'primary'):
                      if new_name:
                            with st.spinner("Creating profile..."):
                                  img = np.array(Image.open(photo_source))
                                  encodings = get_face_embedding(img)
                                  if encodings:
                                        face_emb = encodings[0].tolist()

                                  voice_emb = None
                                  if audio_data:
                                        voice_emb = get_voice_embedding(audio_data.read())

                                  response_data = create_student(new_name, face_embedding = face_emb, voice_embedding = voice_emb) 
                                    
                                  if response_data:
                                        train_classifier()
                                        st.session_state.is_logged_in = True
                                        st.session_state.user_role = 'student'
                                        st.session_state.student_data = response_data[0]
                                        st.toast(f'Profile created, Hi! {new_name}!')
                                        time.sleep(1)
                                        st.rerun()

                                  else:
                                        st.error('Couldnt capture your facial features for registration')      


                                        
                      else:
                        st.warning('please enter your name!')            



    footer_dashboard()
