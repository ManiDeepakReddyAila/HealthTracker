import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home", page_icon="🏠")

if "name" not in st.session_state:
    st.session_state['name'] = None

if "gender" not in st.session_state:
    st.session_state['gender'] = None

if "age" not in st.session_state:
    st.session_state['age'] = None


def show_health_tracker():
    st.write("# Health Tracker")
    image_url = "/Users/manideepakreddyaila/Desktop/projects/HealthTracker/data/image2.jpg"
    st.image(image_url, use_column_width=True)

def set_variables():
    if not st.session_state['name'] or not st.session_state['gender'] or not st.session_state['age']:
        name = st.text_input('Enter your name')
        gender = st.selectbox('Select Gender', ['Male', 'Female', 'Other'], index = None, placeholder = "Choose an Option",)
        age = st.number_input(label = "Enter age", min_value = 0, max_value = 100, value = 25)
        if not name or not gender or not age:
            st.error("Enter all the details")

        if st.button('Submit'):
            st.session_state['name'] = name
            st.session_state['gender'] = gender
            st.session_state['age'] = age
            st.experimental_rerun()

        show_health_tracker()
    else:
        show_health_tracker()

if __name__=="__main__":
    set_variables()

