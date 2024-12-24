import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare features for clustering
features_for_clustering = [
    'Total DL (MB)', 'Total UL (MB)',
    'Number_of_Sessions', 'Total_Duration_ms',
    'Social Media DL (MB)', 'Youtube DL (MB)',
    'Netflix DL (MB)', 'Gaming DL (MB)',
    'Google DL (MB)', 'Email DL (MB)'
]

# Get the data ready
X = user_behavior[features_for_clustering].copy()

# Handle any remaining missing values
X = X.fillna(0)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal number of clusters using elbow method
inertias = []
silhouette_scores = []
K = range(2, 8)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

# Plot elbow curve
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(K, inertias, 'bx-')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')

plt.subplot(1, 2, 2)
plt.plot(K, silhouette_scores, 'rx-')
plt.xlabel('k')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score for Optimal k')
plt.tight_layout()
plt.show()


kmeans = KMeans(n_clusters=optimal_k, random_state=42)
user_behavior['Cluster'] = kmeans.fit_predict(X_scaled)

# Calculate cluster centers
cluster_centers = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=features_for_clustering
)

# Print cluster sizes
print("\
Cluster Sizes:")
print(user_behavior['Cluster'].value_counts())

# Calculate mean values for each cluster
cluster_means = user_behavior.groupby('Cluster')[features_for_clustering].mean()
print("\
Cluster Centers (Mean Values):")
print(cluster_means)
