from streamlit.testing.v1 import AppTest

def test_show_health_tracker():
    at = AppTest.from_file("/Users/manideepakreddyaila/Desktop/projects/HealthTracker/src/Home.py", default_timeout=30)
    at.run()
    assert at.markdown[0].value == "# Health Tracker"

def test_initial_session_state():
    at = AppTest.from_file("/Users/manideepakreddyaila/Desktop/projects/HealthTracker/src/Home.py", default_timeout=30)
    at.run()
    assert at.session_state['name'] == None
    assert at.session_state['age'] == None
    assert at.session_state['gender'] == None
    assert "Enter all the details"  in at.error[0].value

def test_set_variables():
    at = AppTest.from_file("/Users/manideepakreddyaila/Desktop/projects/HealthTracker/src/Home.py", default_timeout=30)
    at.run()
    at.text_input[0].set_value("Mani Deepak").run()
    at.selectbox[0].set_value("Male").run()
    at.number_input[0].set_value(25).run()
    at.button[0].click().run()
    assert at.session_state['name'] == "Mani Deepak"
    assert not at.session_state['age'] == 26
    assert at.session_state['age'] == 25
    assert at.session_state['gender'] == "Male"