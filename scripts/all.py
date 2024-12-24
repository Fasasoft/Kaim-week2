import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import mysql.connector

# Load your cleaned data into a DataFrame
def load_data(filepath):
    return pd.read_csv(filepath)

# Compute Euclidean Distance
def compute_euclidean_distance(df, centroid, columns):
    return np.sqrt(((df[columns] - centroid) ** 2).sum(axis=1))

# K-means clustering
def perform_kmeans(df, columns, k):
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df[columns])
    kmeans = KMeans(n_clusters=k, random_state=42)
    df['Cluster'] = kmeans.fit_predict(normalized_data)
    return df, kmeans, scaler

# Calculate engagement and experience scores
def calculate_scores(df, engagement_centroid, experience_centroid, columns):
    df['Engagement_Score'] = compute_euclidean_distance(df, engagement_centroid, columns)
    df['Experience_Score'] = compute_euclidean_distance(df, experience_centroid, columns)
    df['Satisfaction_Score'] = (df['Engagement_Score'] + df['Experience_Score']) / 2
    return df

# Build regression model
def build_regression_model(df, feature_columns, target_column):
    X = df[feature_columns]
    y = df[target_column]
    model = LinearRegression()
    model.fit(X, y)
    return model

# Export to MySQL database
def export_to_mysql(df, table_name, connection):
    cursor = connection.cursor()
    df.to_sql(table_name, con=connection, if_exists='replace', index=False)
    connection.commit()

# Main Script
if __name__ == "__main__":
    # Load data
    data_filepath = "user_data.csv"  # Replace with your data file path
    data = load_data(data_filepath)

    # Columns used for clustering
    engagement_columns = ['sessions_frequency', 'session_duration', 'session_total_traffic']
    experience_columns = ['avg_tcp_retransmission', 'avg_rtt', 'avg_throughput']

    # Perform K-means clustering for engagement (Task 4.1)
    engagement_data, engagement_kmeans, engagement_scaler = perform_kmeans(data, engagement_columns, k=3)
    less_engaged_centroid = engagement_kmeans.cluster_centers_[np.argmin(engagement_kmeans.cluster_centers_.sum(axis=1))]

    # Perform K-means clustering for experience
    experience_data, experience_kmeans, experience_scaler = perform_kmeans(data, experience_columns, k=3)
    worst_experience_centroid = experience_kmeans.cluster_centers_[np.argmax(experience_kmeans.cluster_centers_.sum(axis=1))]

    # Calculate engagement, experience, and satisfaction scores
    scored_data = calculate_scores(data, less_engaged_centroid, worst_experience_centroid, engagement_columns + experience_columns)

    # Task 4.2: Report the top 10 satisfied customers
    top_10_satisfied = scored_data.nlargest(10, 'Satisfaction_Score')
    print("Top 10 Satisfied Customers:")
    print(top_10_satisfied[['user_id', 'Satisfaction_Score']])

    # Task 4.3: Build regression model to predict satisfaction scores
    regression_model = build_regression_model(scored_data, engagement_columns + experience_columns, 'Satisfaction_Score')
    print("Regression Model Coefficients:", regression_model.coef_)

    # Task 4.4: Run K-means on engagement and experience scores
    scored_data, satisfaction_kmeans, _ = perform_kmeans(scored_data, ['Engagement_Score', 'Experience_Score'], k=2)

    # Task 4.5: Aggregate satisfaction and experience scores per cluster
    cluster_aggregates = scored_data.groupby('Cluster').agg({
        'Engagement_Score': 'mean',
        'Experience_Score': 'mean',
        'Satisfaction_Score': 'mean'
    }).reset_index()
    print("Cluster Aggregates:")
    print(cluster_aggregates)

    # Task 4.6: Export to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="telecom"
    )
    export_to_mysql(scored_data, 'user_scores', db_connection)

    # Verification: Query the exported table
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM user_scores LIMIT 10;")
    for row in cursor.fetchall():
        print(row)

    # Close database connection
    db_connection.close()
