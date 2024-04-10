import os
import pandas as pd
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
import plotly.express as px
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from streamlit_plotly_events import plotly_events

load_dotenv()
AGE = st.session_state['age']
GENDER = st.session_state['gender']
STEP_TARGET = 3000
HEALTH_RECORD_FILE = 'data/records_data.csv'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Step Count", page_icon="🚶")

st.sidebar.header("Step Count")
st.sidebar.write(
    """
    Keeping track of your daily steps can help you maintain an active lifestyle and 
    achieve your fitness goals. Aim for at least 3,000 steps per day!
    """
)

def get_recommendations(step_count, age, gender):
    coach_says = st.empty()

    SYSTEM_MESSAGE = """
        You are a professional running coach with expertise in step count analysis.
        Your task is to analyze the step count data provided by the user and provide recommendations.
        """

    HUMAN_MESSAGE = f"""
        Today's step count: {step_count}
        Age: {age}
        Gender: {gender}
        """

    st_callback = StreamlitCallbackHandler(parent_container = coach_says)

    chat = ChatOpenAI(
        model_name="gpt-4-0613",
        streaming=True,
        callbacks=[st_callback],
        temperature=0.5,
        openai_api_key=OPENAI_API_KEY,
    )

    recommendation = chat([
        SystemMessage(content=SYSTEM_MESSAGE),
        HumanMessage(content=HUMAN_MESSAGE),
    ])

    return recommendation.content

st.header("Step Count 🚶", divider=True)

# Load data
records = pd.read_csv(HEALTH_RECORD_FILE)
records['date'] = pd.to_datetime(records['startDate']).dt.date

# Daily mean step count
mean_step_count = records.groupby('date')['value'].mean().reset_index(name='mean_steps')
daily_step_count = records.groupby('date')['value'].count().reset_index(name='daily_steps')

# Dashboard
st.subheader("Dashboard")
# with st.expander('Plot'):
fig = px.line(daily_step_count, x='date', y='daily_steps', title='Daily Step Count')
fig.update_xaxes(title="Date")
fig.update_yaxes(title="Daily Step Count")
fig.update_traces(mode='markers+lines', marker=dict(size=8))
fig.add_hline(y=STEP_TARGET, line_dash="dot", line_color="red", annotation_text=f'Target: {STEP_TARGET}',
                annotation_position="bottom right")
selected_points = plotly_events(fig)

# st.write(selected_points)
if selected_points:
    st.success(f''' 
            Selected Date: {selected_points[0]["x"]} 
            Step Count: {selected_points[0]["y"]}
    ''')
    button = st.button('Ask Coach')
    st.subheader('Recommendation')
    coach_says = st.empty()
    if button:

        SYSTEM_MESSAGE = """
                You are a professional running coach with expertise in step count analysis.
                Your task is to analyze the step count data provided by the user and provide recommendations.
                """

        HUMAN_MESSAGE = f"""
                Today's step count: {selected_points[0]['y']}
                Age: {AGE}
                Gender: {GENDER}
                Target step count: {STEP_TARGET}
                """

        st_callback = StreamlitCallbackHandler(parent_container=coach_says)

        chat = ChatOpenAI(
            model_name="gpt-4-0613",
            streaming=True,
            callbacks=[st_callback],
            temperature=0.5,
            openai_api_key=OPENAI_API_KEY,
        )

        recommendation = chat([
            SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessage(content=HUMAN_MESSAGE),
        ])
        coach_says.write(recommendation.content)
