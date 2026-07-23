import streamlit as st
from src.ui.base_layout import style_base_layout , style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.database.db import create_teacher , check_teacher_exists , teacher_login


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data"  in st.session_state :
        teacher_dashboard()


    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif  st.session_state.teacher_login_type=="register":
        teacher_screen_register()

def  teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f"""Welcome, {teacher_data['name']}""")     



def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data =teacher
        st.session_state.is_logged_in = True

        return True

    return False
    
def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type ='secondary', key = 'loginbackbtn', shortcut="control+backspace"):
            st.session_state['login-type'] = None
            st.rerun()    


    st.header('Login using password', text_alignment='center')
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username: ", placeholder='Bidisha')

    teacher_password = st.text_input("Enter password:", type = 'password', placeholder='Enter password')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button("Login", icon=':material/passkey:', shortcut='ctrl+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_password):
                st.toast("welcome Back!", icon = "👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")    

    with btnc2:
        if st.button("Register Instead", type='primary', icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type='register'



    footer_dashboard()






def register_teacher(teacher_username,teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name )
        return True, "Successfully created, login now!"
    except Exception as e:
        import traceback

        traceback.print_exc()   # prints the full error in the terminal
        return False, str(e)



def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type ='secondary', key = 'loginbackbtn', shortcut="control+backspace"):
            st.session_state['login-type'] = None
            st.rerun()     


    st.header('Register your teacher profile')

    
    

    teacher_username = st.text_input("Enter username: ", placeholder='Bidisha')

    teacher_name = st.text_input("Enter your name: ", placeholder='Bidisha Das')

    teacher_pass = st.text_input("Enter password:", type = 'password', placeholder='Enter password')

    teacher_pass_confirm = st.text_input("Confirm your password:", type = 'password', placeholder='Confirm password')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button("Register now", icon=':material/passkey:', shortcut='ctrl+enter', width='stretch'):
            success, message = register_teacher(teacher_username,teacher_name, teacher_pass, teacher_pass_confirm )
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type ="login"
                st.rerun()
            else:
                st.error(message)    



    with btnc2:
        if st.button("Login Instead", type='primary', icon=':material/passkey:', width='stretch') :  
            st.session_state.teacher_login_type= 'login'


    footer_dashboard()