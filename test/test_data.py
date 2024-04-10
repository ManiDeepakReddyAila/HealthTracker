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

    pd.testing.assert_frame_equal(actual_df, expected_df)

    import os
    os.remove(expected_file)


if __name__ == '__main__':
    unittest.main()
