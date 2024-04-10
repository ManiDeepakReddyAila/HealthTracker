import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import pytest
import time
import os
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import AgentType, Tool, initialize_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.callbacks import StreamlitCallbackHandler

load_dotenv()

@pytest.fixture
def setup_assistant():
    HEALTH_WORKOUT_FILE = "data/workouts_data.csv"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo-0613"

    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        openai_api_key=OPENAI_API_KEY,
        streaming=True,
        temperature=0,
    )
    assistant = create_csv_agent(
        llm,
        HEALTH_WORKOUT_FILE,
        verbose=False,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
    )
    return assistant
def test_chatbot_answers_workout_question(setup_assistant):
    """
        Requirement: The system's chatbot assistant shall answer question related to workout data of the user.

        Pre-condition:
        Ensure that the chatbot assistant is set up properly with appropriate configurations.

        Steps to be followed:
        1. Set up the chatbot assistant with necessary configurations.
        2. Send a workout-related question to the chatbot assistant.
        3. Receive a response from the chatbot assistant.
        4. Assert that the response is not None.

        Expected Behavior:
        Upon receiving a workout-related question, the chatbot assistant should provide a meaningful response based on the data it has access to.

        Actual Behavior:
        The chatbot assistant's response to the workout-related question.

        Test Result:
        The test will pass if the chatbot assistant answers the question related to workout data of the user, else fails.
        """
    assistant = setup_assistant
    user_input = "What was my workout yesterday?"

    response = assistant.run(user_input)
    assert response is not None

def test_chatbot_answers_within_30_seconds(setup_assistant):
    """
    Requirement: The chatbot assistant shall respond to the questions asked by the user within 30 seconds.
    Pre-condition: Ensure that the chatbot assistant is set up properly with appropriate configurations.
    Steps to be followed:
    1. Set up the chatbot assistant with necessary configurations.
    2. Send a question to the chatbot assistant.
    3. Measure the time taken for the chatbot assistant to respond.
    4. Assert that the response time is less than or equal to 30 seconds.

    Expected Behavior:
    The chatbot assistant should respond to user questions within 30 seconds.

    Actual Behavior:
    The time taken by the chatbot assistant to respond to the user question.

    Test Result:
    The test will pass if the chatbot assistant responds to the question within 30 seconds. Otherwise, it will fail.
    """
    assistant = setup_assistant

    question = "What was my workout yesterday?"

    start_time = time.time()
    response = assistant.run(question)
    end_time = time.time()
    response_time = end_time - start_time

    assert response_time <= 30
    assert response is not None

def test_data_matching():
    """
        Requirement: The system shall be able to read the health data of the user.
        Pre-condition: Ensure that the CSV file contains expected data.
        Steps to be followed:
            1. Define the expected data.
            2. Write the data into a CSV file.
            3. Read the data from the CSV file using the function `read_csv`.
            4. Load the data into a pandas DataFrame.
            5. Perform assertions to check if the data from the file matches the data in the DataFrame.
    """

    expected_data = [
        {'type': 'AppleStandHour', 'unit': '', 'creationDate': '2023-01-01 10:09:38+10:00',
         'startDate': '2023-01-01 10:00:00+10:00', 'endDate': '2023-01-01 11:00:00+10:00', 'value': ''},
        {'type': 'StepCount', 'unit': 'count', 'creationDate': '2023-01-01 10:00:29+10:00',
         'startDate': '2023-01-01 10:00:04+10:00', 'endDate': '2023-01-01 10:00:27+10:00', 'value': 23.0},
        {'type': 'DistanceWalkingRunning', 'unit': 'km', 'creationDate': '2023-01-01 10:00:29+10:00',
         'startDate': '2023-01-01 10:00:04+10:00', 'endDate': '2023-01-01 10:00:27+10:00',
         'value': 0.0180393},
        {'type': 'ActiveEnergyBurned', 'unit': 'kJ', 'creationDate': '2023-01-01 10:02:25+10:00',
         'startDate': '2023-01-01 10:00:34+10:00', 'endDate': '2023-01-01 10:01:35+10:00', 'value': 1.70707},
        {'type': 'DistanceWalkingRunning', 'unit': 'km', 'creationDate': '2023-01-01 10:10:50+10:00',
         'startDate': '2023-01-01 10:00:42+10:00', 'endDate': '2023-01-01 10:00:44+10:00', 'value': 0.0148289}
    ]

    expected_file = '/Users/manideepakreddyaila/Desktop/projects/HealthTracker/data/test/expected_data.csv'
    expected_df = pd.DataFrame(expected_data)
    expected_df.to_csv(expected_file, index=False)

    file_path = '/Users/manideepakreddyaila/Desktop/projects/HealthTracker/data/test/test_records_data.csv'

    actual_df = pd.read_csv(file_path)

    expected_df.replace('', np.nan, inplace=True)
    print(actual_df)
    print(expected_df)

    # Test results (pass/fail):
    pd.testing.assert_frame_equal(actual_df, expected_df)

    import os
    os.remove(expected_file)


if __name__ == '__main__':
    unittest.main()
