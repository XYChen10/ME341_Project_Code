# Imports for K-fold cross-validation
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load your datasets
data1 = pd.read_csv('optimization_data_60_x1.csv')
data2 = pd.read_csv('optimization_data_60_x2.csv')
data3 = pd.read_csv('optimization_data_60_x3.csv')

# Extract columns as float arrays
max_stress1 = data1["MaxStress"].astype(float).values.reshape(-1, 1)
max_stress2 = data2["MaxStress"].astype(float).values.reshape(-1, 1)
max_stress3 = data3["MaxStress"].astype(float).values.reshape(-1, 1)

mass_without_penalty1 = data1["MassWithoutPenalty"].astype(float).values.reshape(-1, 1)
mass_without_penalty2 = data2["MassWithoutPenalty"].astype(float).values.reshape(-1, 1)
mass_without_penalty3 = data3["MassWithoutPenalty"].astype(float).values.reshape(-1, 1)

# Set up K-Fold cross-validation
kfold = KFold(n_splits=10, shuffle=True, random_state=1) # (# of folds, shuffled data, reproducibility)
kmeans = KMeans(n_clusters=3, random_state=1)  # (# of clusters, reproducibility)

silhouette_scores = []  # List to store silhouette scores for each fold

# Perform K-Fold cross-validation
for train_index, test_index in kfold.split(mass_without_penalty1):
    X_train, X_test = mass_without_penalty1[train_index], max_stress1[test_index]

    kmeans.fit(X_train)  # Train the model on the training data
    labels = kmeans.predict(X_test)  # Predict clusters for the test data

    # Check if there are at least 2 clusters in the test data
    unique_labels = np.unique(labels)
    if len(unique_labels) > 1:  # Only calculate silhouette score if there are 2 or more clusters
        score = silhouette_score(X_test, labels)
        silhouette_scores.append(score)
    else:
        print(f"Skipping fold: Only one cluster found in test data.")

# Print the average silhouette score across all valid folds
if silhouette_scores:
    print(f"Mean Silhouette Score: {np.mean(silhouette_scores)}")
else:
    print("No valid folds with multiple clusters were found.")
