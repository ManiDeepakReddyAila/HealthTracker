# HealthTracker

## Application Link: http://localhost:8501

[![FastAPI Unit Tests](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml/badge.svg)](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml)

# Code Coverage - CodeCov
Integrated our repository with the CodeCov to get the code coverage with the tests written. <br>
Below is the codecoverage showing different files of the fastapi module of Stock Analysis Summarizer.<br>
<img src="https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/branch/main/graphs/sunburst.svg?token=NGU9K01WWF" alt="Code Coverage" width="200" height="200">

[![Code Coverage](https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/branch/main/graph/badge.svg?token=NGU9K01WWF)](https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer)

# Overview

This project highlights the focus on advanced medical devices developed by  following the software engineering principles as laid down by IEC 62304. The aim of this project is to collect user’s workout information from their Apple Health application and enhance their health and fitness goals. Personalized Health Coach is an application that provides insights into user’s health data and enables to do a question-answering about their workout activities


# Problem Statement
- Lack of personalized guidance - difficulty in tracking daily health goals and progress according to their personal needs.
- Monitoring progress - Without right tools and insights, it is not easy to monitor if you are reaching your daily targets.
- Complexity in accessing data - It is hectic to always go back to your past data and search for any information you want.


# Solution  🎯

 - 💡 The system collects data from Apple Health application and converts to easily readable format for further analysis.
 - 💡 By creating right visualisations, it is easy for the users to view their progress and set targets for various activities such as running and swimming.
 - 💡 Users can track their daily progress against set targets, providing feedback on their performance and motivation to achieve their goals.
 - 💡 A chatbot interface allows users to query their health data, providing instant access to information.

# Technologies Used
![Python](https://img.shields.io/badge/python-grey?style=for-the-badge&logo=python&logoColor=orange)
![](https://img.shields.io/badge/GitHub_Actions-green?style=for-the-badge&logo=github-actions&logoColor=white)
![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![](https://img.shields.io/badge/Apple%20Health-blue?style=for-the-badge&logo=apple&logoColor=white)

# Architecture
![Architecture_diagram](https://github.com/ManiDeepakReddyAila/HealthTracker/blob/main/data/personalised_health_tracker.png)

# Application Workflow
- User enters basic details like name, age and gender in the Streamlit web interface.
- User can chat with the QA Assistant to get informatin about their health data.
- User can set targets for Running metrics like Ground Contact Time, Maximum Heart Rate, Maximum Pace and Stride Length.
- User can click on the points on line graph which is an interactive chart.
- User can ask get AI recommendations based on the selected day's workouts for both Running and Step Counts.
- The dashboards are displayed in the Streamlit web interface.

# Directory Structure
```
Health Tracker/
┣ .github/
┃ ┗ workflows/
┃   ┗ pytest.yml
┣ data/
┃ ┣ test/
┃ ┃ ┗ test_records_data.csv
┃ ┣ image2.jpg
┃ ┣ process_data.ipynb
┃ ┣ records_data.csv
┃ ┗ workouts_data.csv
┣ test/
┃ ┣ __init__.py 
┃ ┣ test_chatbot.py
┃ ┣ test_data.py
┃ ┣ test_home.py
┃ ┣ test_running.py
┃ ┗ test_ui_requirements.py
┣ src/
┃ ┣ pages/
┃ ┃ ┣ 1_Assistant.py
┃ ┃ ┣ 2_Running.py
┃ ┃ ┗ 3_Step_Count.py
┃ ┣ Home.py
┃ ┗ requirements.txt
┣ .venv/
┣ .env
┣ .gitignore
┣ README.md
┣ architecture.py
┗ personalised_health_tracker.png
```


# Local Installation 
## Streamlit & FastAPI

Step 1 -  Clone the repository on your local system using the below command and Change the directory to streamlit:
```bash
git clone https://github.com/ManiDeepakReddyAila/HealthTracker.git
cd HealthTracker/src
```

Step 2 - Create Virtual Environment and activate
```bash
python -m venv .venv
source .venv/bin/activate
```

Step 3 - Install all the requirements by navigating to the streamlit folder and enter the command:
```bash
pip install -r requirements.txt
```

Step 4 - Run the streamlit application using the below command
```bash
streamlit run Home.py
```
