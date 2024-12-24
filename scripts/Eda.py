import pandas as pd
import numpy as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Check missing values
missing_values = df.isnull().sum()
missing_percentages = (missing_values / len(df)) * 100

print("Missing Values Analysis:")
print(missing_values[missing_values > 0])
print("\
Missing Percentages:")
print(missing_percentages[missing_percentages > 0])

# Basic statistics for numerical columns
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
basic_stats = df[numeric_cols].describe()
print("\
Basic Statistics for Key Metrics:")
print(basic_stats)