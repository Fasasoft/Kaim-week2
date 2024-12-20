import pandas as pd
import numpy as np

# Group by MSISDN/Number (unique user identifier) and aggregate
user_behavior = df.groupby('MSISDN/Number').agg({
    'Bearer Id': 'count',  # Number of sessions
    'Dur. (ms)': 'sum',    # Total duration
    'Total DL (Bytes)': 'sum',
    'Total UL (Bytes)': 'sum',
    'Social Media DL (Bytes)': 'sum',
    'Social Media UL (Bytes)': 'sum',
    'Google DL (Bytes)': 'sum',
    'Google UL (Bytes)': 'sum',
    'Email DL (Bytes)': 'sum',
    'Email UL (Bytes)': 'sum',
    'Youtube DL (Bytes)': 'sum',
    'Youtube UL (Bytes)': 'sum',
    'Netflix DL (Bytes)': 'sum',
    'Netflix UL (Bytes)': 'sum',
    'Gaming DL (Bytes)': 'sum',
    'Gaming UL (Bytes)': 'sum',
    'Other DL (Bytes)': 'sum',
    'Other UL (Bytes)': 'sum'
}).reset_index()

# Rename columns for clarity
user_behavior = user_behavior.rename(columns={
    'Bearer Id': 'Number_of_Sessions',
    'Dur. (ms)': 'Total_Duration_ms'
})

# Convert bytes to MB for better readability
bytes_columns = [col for col in user_behavior.columns if 'Bytes' in col]
for col in bytes_columns:
    user_behavior[col.replace('Bytes', 'MB')] = user_behavior[col] / (1024 * 1024)
    user_behavior = user_behavior.drop(col, axis=1)

# Display first few rows and basic statistics
print("User Behavior Analysis Summary:")
print("\
First few users:")
print(user_behavior.head())

print("\
Overall Statistics:")
print(user_behavior.describe())