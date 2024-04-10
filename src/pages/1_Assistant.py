import os
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
import time
from dotenv import load_dotenv
from langchain.agents import AgentType, Tool, initialize_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI

load_dotenv()
st.set_page_config(page_title="Assistant", page_icon="💬")
NAME = st.session_state['name']
HEALTH_RECORD_FILE = "data/records_data.csv"
HEALTH_WORKOUT_FILE = "data/workouts_data.csv"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not st.session_state['name'] or not st.session_state['age'] or not st.session_state:
    st.error("Enter the details in Home Page")
    time.sleep(2)
    switch_page('Home')

st.sidebar.header("Assistant")


MODEL_NAME = "gpt-3.5-turbo-0613"

llm = ChatOpenAI(
    model_name=MODEL_NAME,
    openai_api_key=OPENAI_API_KEY,
    streaming=True,
    temperature=0,
)

tools = [
    Tool(
        name="Workout",
        func=create_csv_agent(
            llm,
            HEALTH_WORKOUT_FILE,
            verbose=False,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True,
        ).run,
        description="useful for when you need to answer questions about workout history.",
    )
]
assistant = create_csv_agent(
    llm,
    HEALTH_WORKOUT_FILE,
    verbose=False,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": f"Hi {NAME}! I hope you're having a great day. How can I help you?",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input(placeholder=""):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    response = assistant.run(prompt, callbacks=[st_cb])
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write(response)
