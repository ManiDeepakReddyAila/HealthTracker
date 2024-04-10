import os
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import streamlit as st
import time
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()
AGE = 25
GENDER = "Female"
HEIGHT = 120
WEIGHT = 47
PACE_TARGET = 6.30
HEART_RATE_TARGET = 160
STRIDE_LENGTH_TARGET = 1.00
GROUND_CONTACT_TIME_TARGET = 250
HEALTH_RECORD_FILE = 'data/records_data.csv'
HEALTH_WORKOUT_FILE = 'data/workouts_data.csv'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Running", page_icon="🏃")

st.sidebar.header("Running")
st.sidebar.write(
    """
Running should be a lifelong activity. 
Approach it patiently and intelligently, and it will reward you for a long, long time.
"""
)

st.header("Running 🏃", divider=True)



def load_records(file):
    records_data = pd.read_csv(file)
    return records_data

def load_workouts(file):
    workouts_data = pd.read_csv(file)
    return workouts_data

def get_records_for_workout(all_records, record_type, workout_startdate, workout_enddate):
    records = all_records.loc[all_records["type"] == record_type]
    records = records.loc[
        (records["startDate"] >= workout_startdate)
        & (records["endDate"] <= workout_enddate)
    ]
    if not records.empty:
        records.reset_index(drop=True, inplace=True)
        unit = records["unit"].iloc[0]
        if record_type in [
            "HeartRate",
            "RunningStrideLength",
            "RunningPower",
            "RunningVerticalOscillation",
            "RunningGroundContactTime",
            "RunningSpeed",
        ]:
            return {
                f"max {record_type} ({unit})": records["value"].max(),
                f"min {record_type} ({unit})": records["value"].min(),
                f"mean {record_type} ({unit})": records["value"].mean(),
            }
        if record_type in ["ActiveEnergyBurned", "BasalEnergyBurned"]:
            return {f"{record_type} ({unit})": records["value"].sum()}
    return {}

def get_workout_statistics(all_workouts, workout_type, all_records, record_types):
    workouts = all_workouts.loc[all_workouts["workoutActivityType"] == workout_type]
    statistics = []
    for index, row in workouts.iterrows():
        statistic = {}
        statistic["type"] = workout_type
        statistic[f'duration ({row["durationUnit"]})'] = row["duration"]
        statistic["time"] = row["startDate"]
        statistic["date"] = row["startDate"][:10]
        for record_type in record_types:
            statistic.update(
                get_records_for_workout(
                    all_records, record_type, row["startDate"], row["endDate"]
                )
            )
        if len(statistic) == 24:
            pace = 1000 / 60 / statistic["mean RunningSpeed (m/s)"]
            statistic["pace (min/km)"] = f"{pace:.2f}"
            statistic["distance (km)"] = f'{(statistic["duration (min)"] / pace):.2f}'
            if float(statistic["distance (km)"]) >= 0.1:
                statistics.append(statistic)
    return statistics


def show_status(reach_target):
    if reach_target:
        return st.success("You have reached the target!", icon="😊")
    return st.error("You are doing fine... Just keep running!", icon="😢")


if 'maximum_heart_rate' not in st.session_state:
    st.session_state['maximum_heart_rate'] = 160

if 'slider_value' not in st.session_state:
    st.session_state['slider_value'] = None

def display_dashboard():
    st.divider()
    records = load_records(HEALTH_RECORD_FILE)
    workouts = load_workouts(HEALTH_WORKOUT_FILE)
    runnings = get_workout_statistics(
        workouts,
        "Running",
        records,
        [
            "HeartRate",
            "RunningStrideLength",
            "RunningPower",
            "RunningVerticalOscillation",
            "RunningGroundContactTime",
            "RunningSpeed",
            "ActiveEnergyBurned",
            "BasalEnergyBurned",
        ],
    )
    runnings_pd = pd.DataFrame(runnings)
    runnings_pd["distance (km)"] = runnings_pd["distance (km)"].astype("float")
    runnings_pd["pace (min/km)"] = runnings_pd["pace (min/km)"].astype("float")

    running_dates = [x["time"] for x in runnings]
    default_msg = "Overview"
    running_dates.insert(0, default_msg)
    st.subheader("Dashboard")
    running_date = st.selectbox("Running history", running_dates)
    st.write(running_date)
    if running_date != default_msg:
        running_statistics = [x for x in runnings if x["time"] == running_date][0]

        running_statistics_pd = pd.DataFrame(running_statistics, index=[0])
        running_statistics_pd["distance (km)"] = running_statistics_pd[
            "distance (km)"
        ].astype("float")
        running_statistics_pd["pace (min/km)"] = running_statistics_pd[
            "pace (min/km)"
        ].astype("float")
    analysis = st.empty()
    if running_date == default_msg:
        with analysis.container():
            total_runnings = len(runnings)
            overall = runnings_pd[["date", "distance (km)", "duration (min)"]]
            st.pyplot(
                overall[-total_runnings:]
                .plot(title="Distance and Duration", x="date", kind="bar")
                .figure
            )
            st.pyplot(
                runnings_pd[-total_runnings:]
                .plot(title="Pace", x="date", y="pace (min/km)", kind='line')
                .axhline(y=float(PACE_TARGET), color="red")
                .figure
            )
            st.pyplot(
                runnings_pd[-total_runnings:]
                .plot(
                    title="Heart Rate",
                    x="date",
                    y="mean HeartRate (count/min)",
                    kind='line',
                )
                .axhline(y=int(st.session_state['maximum_heart_rate']), color="red")
                .figure
            )
            st.pyplot(
                runnings_pd[-total_runnings:]
                .plot(
                    title="Stride Length",
                    x="date",
                    y="mean RunningStrideLength (m)",
                    kind='line',
                )
                .axhline(y=float(STRIDE_LENGTH_TARGET), color="red")
                .figure
            )
            st.pyplot(
                runnings_pd[-total_runnings:]
                .plot(
                    title="Ground Contact Time",
                    x="date",
                    y="mean RunningGroundContactTime (ms)",
                    kind='line',
                )
                .axhline(y=float(GROUND_CONTACT_TIME_TARGET), color="red")
                .figure
            )
    else:
        analysis.empty()

        st.pyplot(
            running_statistics_pd.plot(
                title="Pace", x="date", y="pace (min/km)", kind="scatter"
            )
            .axhline(y=float(PACE_TARGET), color="red")
            .figure
        )

        st.pyplot(
            running_statistics_pd.plot(
                title="Heart Rate",
                x="date",
                y="mean HeartRate (count/min)",
                kind="scatter",
            )
            .axhline(y=int(st.session_state['maximum_heart_rate']), color="red")
            .figure
        )

        st.pyplot(
            running_statistics_pd.plot(
                title="Stride Length",
                x="date",
                y="mean RunningStrideLength (m)",
                kind="scatter",
            )
            .axhline(y=float(STRIDE_LENGTH_TARGET), color="red")
            .figure
        )

        st.pyplot(
            running_statistics_pd.plot(
                title="Ground Contact Time",
                x="date",
                y="mean RunningGroundContactTime (ms)",
                kind="scatter",
            )
            .axhline(y=float(GROUND_CONTACT_TIME_TARGET), color="red")
            .figure
        )




    ask_coach = st.button(
        "Ask coach", type="primary", disabled=(running_date == default_msg)
    )

    st.subheader("Recommendation")


    coach_says = st.empty()
    if running_date in st.session_state:
        coach_says.write(st.session_state[running_date])
    if ask_coach:
        coach_says.empty()
        SYSTEM_MESSAGE = """
            You are a very professional running coach with a passion for helping your coachee to achieve his or her running goals.
            You have a deep understanding of all running performance metrics. Your task is to analyze the running data,
            then provide insightful recommendations in data driven manner to help the coachee to improve his or her running performance.
            """

        HUMAN_MESSAGE = f"""
            I am your coachee.
            I am a {AGE} years old {GENDER}.
            I am {HEIGHT} cm tall and weigh {WEIGHT} kg.

            When I run, my target is to
            keep heart rate less than {st.session_state['maximum_heart_rate']} count/min,
            keep stride length greater than {STRIDE_LENGTH_TARGET} m,
            keep ground contact time less than {GROUND_CONTACT_TIME_TARGET} ms,
            keep running pace less than {PACE_TARGET} min/km.

            Here is my running data in json format:\n {running_statistics}\n
            Please analyze my running data and make recommendations.
            Please suggest the running techniques that I can adopt to improve performance.

            Optionally, please provide links to some learning resources.

            The response should be in bullet format.
            """
        st_callback = StreamlitCallbackHandler(coach_says)

        chat = ChatOpenAI(
            model_name="gpt-4-0613",
            streaming=True,
            callbacks=[st_callback],
            temperature=0.5,
            openai_api_key=OPENAI_API_KEY,
        )

        recommendation = chat(
            [
                SystemMessage(content=SYSTEM_MESSAGE),
                HumanMessage(content=HUMAN_MESSAGE),
            ]
        )

        coach_says.empty().write(recommendation.content)
        st.session_state[running_date] = recommendation.content

with st.form("target_values_form"):
    st.subheader("Set Target Values")
    max_pace = st.number_input("Pace Target (min/km)", value=6.30)
    heart_rate_target = st.number_input("Maximum Heart Rate", value=160)
    stride_length_target = st.number_input("Stride Length Target (m)", value=1.00)
    ground_contact_time_target = st.number_input("Ground Contact Time Target (ms)", value=250)
    if st.form_submit_button("Submit"):
        if heart_rate_target < 0 or heart_rate_target > 220:
            st.error(f"Please enter a number between 0 and 220.")
        else:
            PACE_TARGET = max_pace
            st.session_state['maximum_heart_rate'] = heart_rate_target
            HEART_RATE_TARGET = heart_rate_target
            STRIDE_LENGTH_TARGET = stride_length_target
            GROUND_CONTACT_TIME_TARGET = ground_contact_time_target
display_dashboard()

