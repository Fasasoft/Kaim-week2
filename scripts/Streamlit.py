import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Database connection setup
@st.cache(allow_output_mutation=True)
def get_db_connection():
    db_engine = create_engine("mysql+pymysql://username:password@localhost/telecom_db")
    return db_engine

# Fetch data from SQL database
@st.cache
def fetch_data(query):
    engine = get_db_connection()
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

# Sidebar navigation
def sidebar_menu():
    st.sidebar.title("Navigation")
    return st.sidebar.radio(
        "Go to:",
        ["User Overview Analysis", "User Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"]
    )

# User Overview Analysis
def user_overview_analysis():
    st.title("User Overview Analysis")
    st.write("Analyze user behavior across sessions and applications.")
    
    query = """
        SELECT user_id, COUNT(session_id) AS num_sessions, 
               SUM(session_duration) AS total_duration,
               SUM(download_data + upload_data) AS total_data
        FROM sessions
        GROUP BY user_id
    """
    data = fetch_data(query)
    
    # Example plot
    fig = px.histogram(data, x='total_duration', nbins=20, title="Total Duration Distribution")
    st.plotly_chart(fig)
    
    total_users = data['user_id'].nunique()
    st.metric(label="Total Users", value=total_users)

# User Engagement Analysis
def user_engagement_analysis():
    st.title("User Engagement Analysis")
    st.write("Analyze user engagement using frequency, duration, and traffic.")
    
    query = """
        SELECT user_id, COUNT(session_id) AS session_frequency,
               SUM(session_duration) AS total_duration,
               SUM(download_data + upload_data) AS total_traffic
        FROM sessions
        GROUP BY user_id
    """
    data = fetch_data(query)

    # Example scatter plot
    fig = px.scatter(data, x='session_frequency', y='total_traffic',
                     color='total_duration', title="User Engagement Scatter Plot")
    st.plotly_chart(fig)

    top_users = data.nlargest(10, 'total_traffic')
    st.write("Top 10 Users by Total Traffic")
    st.dataframe(top_users[['user_id', 'total_traffic']])

# Experience Analysis
def experience_analysis():
    st.title("Experience Analysis")
    st.write("Analyze user experience based on network parameters.")
    
    query = """
        SELECT user_id, AVG(tcp_retransmission) AS avg_tcp_retransmission,
               AVG(rtt) AS avg_rtt, AVG(throughput) AS avg_throughput, handset_type
        FROM network_metrics
        GROUP BY user_id, handset_type
    """
    data = fetch_data(query)

    # Example bar chart
    avg_throughput = data.groupby('handset_type')['avg_throughput'].mean().reset_index()
    fig = px.bar(avg_throughput, x='handset_type', y='avg_throughput', title="Average Throughput per Handset Type")
    st.plotly_chart(fig)

# Satisfaction Analysis
def satisfaction_analysis():
    st.title("Satisfaction Analysis")
    st.write("Analyze user satisfaction based on engagement and experience.")
    
    query = """
        SELECT user_id, engagement_score, experience_score,
               (engagement_score + experience_score) / 2 AS satisfaction_score
        FROM satisfaction_metrics
    """
    data = fetch_data(query)

    # Example scatter plot
    fig = px.scatter(data, x='engagement_score', y='experience_score', color='satisfaction_score',
                     title="Engagement vs Experience Scatter Plot")
    st.plotly_chart(fig)

    top_satisfied = data.nlargest(10, 'satisfaction_score')
    st.write("Top 10 Satisfied Users")
    st.dataframe(top_satisfied[['user_id', 'satisfaction_score']])

# Main function
def main():
    st.set_page_config(layout="wide")
    st.sidebar.header("Telecom Dashboard")
    
    # Sidebar menu
    page = sidebar_menu()

    # Page selection
    if page == "User Overview Analysis":
        user_overview_analysis()
    elif page == "User Engagement Analysis":
        user_engagement_analysis()
    elif page == "Experience Analysis":
        experience_analysis()
    elif page == "Satisfaction Analysis":
        satisfaction_analysis()

if __name__ == "__main__":
    main()
