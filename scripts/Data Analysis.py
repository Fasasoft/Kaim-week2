# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data into a DataFrame
def load_aggregated_data(query, connection):
    return pd.read_sql(query, connection)

# Handle missing values and outliers
def clean_data(df):
    # Replace missing values with the mean
    for col in ['avg_tcp_retransmission', 'avg_rtt', 'avg_throughput']:
        df[col].fillna(df[col].mean(), inplace=True)
    return df

# Compute Top, Bottom, and Most Frequent Values
def compute_top_bottom_frequent(df, column):
    top_10 = df.nlargest(10, column)
    bottom_10 = df.nsmallest(10, column)
    most_frequent = df[column].value_counts().head(10)
    return top_10, bottom_10, most_frequent

# Plot distribution of throughput per handset type
def plot_throughput_distribution(df):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='handset_type', y='avg_throughput')
    plt.xticks(rotation=90)
    plt.title("Distribution of Average Throughput per Handset Type")
    plt.show()

# Plot average TCP retransmission view per handset type
def plot_tcp_retransmission(df):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='handset_type', y='avg_tcp_retransmission')
    plt.xticks(rotation=90)
    plt.title("Average TCP Retransmission per Handset Type")
    plt.show()

# Main Script
if __name__ == "__main__":
    # Database connection setup
    import mysql.connector
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="telecom"
    )

    # SQL Query
    query = """
    SELECT
        customer_id AS MSISDN,
        AVG(TCP_retransmission) AS avg_tcp_retransmission,
        AVG(RTT) AS avg_rtt,
        handset_type,
        AVG(throughput) AS avg_throughput
    FROM
        user_network_data
    GROUP BY
        customer_id, handset_type;
    """

    # Load data
    aggregated_data = load_aggregated_data(query, conn)

    # Close connection
    conn.close()

    # Clean data
    cleaned_data = clean_data(aggregated_data)

    # Compute top, bottom, and most frequent values
    top_tcp, bottom_tcp, freq_tcp = compute_top_bottom_frequent(cleaned_data, 'avg_tcp_retransmission')
    top_rtt, bottom_rtt, freq_rtt = compute_top_bottom_frequent(cleaned_data, 'avg_rtt')
    top_throughput, bottom_throughput, freq_throughput = compute_top_bottom_frequent(cleaned_data, 'avg_throughput')

    # Print results
    print("Top 10 TCP Retransmission:\n", top_tcp)
    print("Bottom 10 TCP Retransmission:\n", bottom_tcp)
    print("Most Frequent TCP Retransmission:\n", freq_tcp)

    print("\nTop 10 RTT:\n", top_rtt)
    print("Bottom 10 RTT:\n", bottom_rtt)
    print("Most Frequent RTT:\n", freq_rtt)

    print("\nTop 10 Throughput:\n", top_throughput)
    print("Bottom 10 Throughput:\n", bottom_throughput)
    print("Most Frequent Throughput:\n", freq_throughput)

    # Plot throughput distribution per handset type
    plot_throughput_distribution(cleaned_data)

    # Plot TCP retransmission view per handset type
    plot_tcp_retransmission(cleaned_data)
