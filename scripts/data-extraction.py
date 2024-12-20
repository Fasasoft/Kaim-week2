import matplotlib.pyplot as plt
import seaborn as sns

# Calculate average data usage per application
app_usage = user_behavior[[
    'Social Media DL (MB)', 'Social Media UL (MB)',
    'Google DL (MB)', 'Google UL (MB)',
    'Email DL (MB)', 'Email UL (MB)',
    'Youtube DL (MB)', 'Youtube UL (MB)',
    'Netflix DL (MB)', 'Netflix UL (MB)',
    'Gaming DL (MB)', 'Gaming UL (MB)',
    'Other DL (MB)', 'Other UL (MB)'
]].mean()

# Create a bar plot
plt.figure(figsize=(12, 6))
app_usage.plot(kind='bar')
plt.title('Average Data Usage per Application (MB)')
plt.xticks(rotation=45, ha='right')
plt.ylabel('MB')
plt.tight_layout()
plt.show()

# Calculate total data consumption per user
user_behavior['Total_Data_MB'] = user_behavior['Total DL (MB)'] + user_behavior['Total UL (MB)']

# Basic statistics of user engagement
print("\
User Engagement Metrics:")
print(f"Average sessions per user: {user_behavior['Number_of_Sessions'].mean():.2f}")
print(f"Average duration per user (hours): {(user_behavior['Total_Duration_ms'].mean() / (1000 * 3600)):.2f}")
print(f"Average total data per user (MB): {user_behavior['Total_Data_MB'].mean():.2f}")