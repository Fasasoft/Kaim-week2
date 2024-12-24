import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Calculate engagement scores based on different metrics
def calculate_engagement_score(row):
    # Initialize base score
    score = 0
    
    # Session frequency score (0-25 points)
    session_score = min(row['Number_of_Sessions'] * 5, 25)
    
    # Duration score (0-25 points)
    duration_score = min((row['Total_Duration_ms'] / 3600000) * 10, 25)  # Convert ms to hours
    
    # Data usage score (0-25 points)
    total_data = row['Total DL (MB)'] + row['Total UL (MB)']
    data_score = min(total_data / 100, 25)
    
    # Service diversity score (0-25 points)
    services = ['Social Media DL (MB)', 'Youtube DL (MB)', 'Netflix DL (MB)', 
                'Gaming DL (MB)', 'Google DL (MB)', 'Email DL (MB)']
    used_services = sum([1 for service in services if row[service] > 0])
    diversity_score = (used_services / len(services)) * 25
    
    # Calculate total score
    score = session_score + duration_score + data_score + diversity_score
    
    return score

# Calculate engagement scores
user_behavior['Engagement_Score'] = user_behavior.apply(calculate_engagement_score, axis=1)

# Create engagement categories
user_behavior['Engagement_Level'] = pd.qcut(user_behavior['Engagement_Score'], 
                                          q=5, 
                                          labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

# Display basic statistics of engagement scores
print("Engagement Score Statistics:")
print(user_behavior['Engagement_Score'].describe())

# Display distribution of engagement levels
print("\
Engagement Level Distribution:")
print(user_behavior['Engagement_Level'].value_counts())

# Create visualization of engagement score distribution
plt.figure(figsize=(12, 6))

# Histogram of engagement scores
plt.subplot(1, 2, 1)
sns.histplot(data=user_behavior, x='Engagement_Score', bins=50)
plt.title('Distribution of Engagement Scores')
plt.xlabel('Engagement Score')
plt.ylabel('Count')

# Box plot of engagement scores by level
plt.subplot(1, 2, 2)
sns.boxplot(data=user_behavior, x='Engagement_Level', y='Engagement_Score')
plt.title('Engagement Scores by Level')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate average metrics for each engagement level
engagement_metrics = ['Number_of_Sessions', 'Total_Duration_ms', 'Total DL (MB)', 'Total UL (MB)']
avg_metrics = user_behavior.groupby('Engagement_Level')[engagement_metrics].mean()

print("\
Average Metrics by Engagement Level:")
print(avg_metrics)

# Reload the dataset to ensure the dataframe is available
import pandas as pd

# Assuming the dataset is named 'Week2_challenge_data_source.xlsx'
file_path = 'Week2_challenge_data_source.xlsx'

# Load the dataset
user_behavior = pd.read_excel(file_path, sheet_name=0)

# Display the first few rows to confirm successful loading
print(user_behavior.head())


