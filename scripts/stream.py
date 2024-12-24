import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data(filepath):
    return pd.read_csv(filepath)

# Sidebar navigation
def sidebar_menu():
    st.sidebar.title("Navigation")
    return st.sidebar.radio(
        "Go to:",
        ["User Overview Analysis", "User Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"]
    )

# User Overview Analysis
def user_overview_analysis(data):
    st.title("User Overview Analysis")
    st.write("Analyze user behavior across sessions and applications.")
    
    # Example plot
    fig = px.histogram(data, x='session_duration', nbins=20, title="Session Duration Distribution")
    st.plotly_chart(fig)
    
    total_users = data['user_id'].nunique()
    st.metric(label="Total Users", value=total_users)

# User Engagement Analysis
def user_engagement_analysis(data):
    st.title("User Engagement Analysis")
    st.write("Analyze user engagement using frequency, duration, and traffic.")

    # Example scatter plot
    fig = px.scatter(data, x='sessions_frequency', y='session_total_traffic',
                     color='session_duration', title="User Engagement Scatter Plot")
    st.plotly_chart(fig)

    top_users = data.nlargest(10, 'session_total_traffic')
    st.write("Top 10 Users by Total Traffic")
    st.dataframe(top_users[['user_id', 'session_total_traffic']])

# Experience Analysis
def experience_analysis(data):
    st.title("Experience Analysis")
    st.write("Analyze user experience based on network parameters.")

    # Example bar chart
    avg_throughput = data.groupby('handset_type')['avg_throughput'].mean().reset_index()
    fig = px.bar(avg_throughput, x='handset_type', y='avg_throughput', title="Average Throughput per Handset Type")
    st.plotly_chart(fig)

# Satisfaction Analysis
def satisfaction_analysis(data):
    st.title("Satisfaction Analysis")
    st.write("Analyze user satisfaction based on engagement and experience.")

    # Example heatmap
    fig = px.scatter(data, x='Engagement_Score', y='Experience_Score', color='Satisfaction_Score',
                     title="Engagement vs Experience Scatter Plot")
    st.plotly_chart(fig)

    top_satisfied = data.nlargest(10, 'Satisfaction_Score')
    st.write("Top 10 Satisfied Users")
    st.dataframe(top_satisfied[['user_id', 'Satisfaction_Score']])

# Main function
def main():
    st.set_page_config(layout="wide")
    data_filepath = "processed_data.csv"  # Replace with your cleaned dataset path
    data = load_data(data_filepath)

    # Sidebar menu
    page = sidebar_menu()

    # Page selection
    if page == "User Overview Analysis":
        user_overview_analysis(data)
    elif page == "User Engagement Analysis":
        user_engagement_analysis(data)
    elif page == "Experience Analysis":
        experience_analysis(data)
    elif page == "Satisfaction Analysis":
        satisfaction_analysis(data)

if __name__ == "__main__":
    main()
