from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User

with Diagram("Personalised Health Tracker", show=False, direction="LR"):
    apple_health = Custom("", "/Users/pranitha/Desktop/AlgoDM/HealthTracker/assets/apple_health.png")
    xml_data = Custom("", "/Users/pranitha/Desktop/AlgoDM/HealthTracker/assets/xml.jpeg")
    csv_data = Custom("", "/Users/pranitha/Desktop/AlgoDM/HealthTracker/assets/csv.jpeg")
    openai = Custom("", "/Users/pranitha/Desktop/AlgoDM/HealthTracker/assets/openai.webp")
    pandas_df = Python("Pandas DataFrame")
    dashboard = Custom("", "/Users/pranitha/Desktop/AlgoDM/HealthTracker/assets/dashboard.png")

    streamlit = Custom("Streamlit", "/Users/pranitha/Desktop/AlgoDM/HealthTracker/assets/streamlit.jpeg")

    user = User("User")

    user >> Edge(label="") >> apple_health
    apple_health >> Edge(label="extract data from Apple Health application") >> xml_data
    xml_data >> Edge(label="transformation") >> csv_data
    csv_data >> Edge(label="transformation") >> pandas_df
    pandas_df >> Edge(label="knowledge base for LLM") >> openai
    openai >> Edge(label="Q&A retrieval using chatbot") >> streamlit
    pandas_df >> Edge(label="visualisations for workout activities") >> dashboard
    dashboard >> Edge(label="") >> streamlit

    # streamlit >> Edge(label="Conversational Retrieval for Q&A") >> openai
    # streamlit >> Edge(label="Data Visualization") >> pandas_df
    # streamlit >> Edge(label="Data Input") >> [apple_health, xml_data, csv_data
