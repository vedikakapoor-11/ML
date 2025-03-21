import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from scipy.stats import zscore

# 1. Data Cleaning
file_path = r'C:\Users\vedik\Downloads\archive\Diabetes.csv'
data = pd.read_csv(file_path)

# Remove duplicates and handle missing values
data.drop_duplicates(inplace=True)
data.dropna(inplace=True)

# Identify numerical columns
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns

# 2. Box Plotting Graphs
plt.figure(figsize=(12, 6))
sns.boxplot(data=data[numerical_columns], palette='Set2')
plt.title('Box Plot for Numerical Columns')
plt.show()
# line graph
plt.figure(figsize=(12, 6))
for column in numerical_columns:
    plt.plot(data.index, data[column], label=column)

plt.title("Line Graph for Numerical Features")
plt.xlabel("Index")
plt.ylabel("Values")
plt.legend()
plt.grid(True)
plt.show()



# 3. Outlier Detection using IQR 
# Plot Before Outlier Removal
plt.figure(figsize=(12, 6))
sns.boxplot(data=data[numerical_columns], palette='Set2')
plt.title('Before Outlier Removal (IQR)')
plt.xticks(rotation=45)
plt.show()

# Outlier Capping using IQR
for column in numerical_columns:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data[column] = np.where(data[column] < lower_bound, lower_bound, data[column])
    data[column] = np.where(data[column] > upper_bound, upper_bound, data[column])

# Plot After Outlier Removal
plt.figure(figsize=(12, 6))
sns.boxplot(data=data[numerical_columns], palette='Set2')
plt.title('After Outlier Removal (IQR)')
plt.xticks(rotation=45)
plt.show()


# 3. Outlier Detection using Z-Score
# 3. Outlier Detection using Z-Score

# Copy original data
data_zscore = data.copy()

# Box Plot Before Outlier Removal
plt.figure(figsize=(12, 6))
sns.boxplot(data=data_zscore[numerical_columns], palette='coolwarm')
plt.title('Box Plot Before Outlier Removal (Z-Score)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Outlier Removal using Z-Score
z_scores = np.abs(zscore(data_zscore[numerical_columns]))
data_zscore[numerical_columns] = np.where(z_scores > 3, np.nan, data_zscore[numerical_columns])
data_zscore.dropna(inplace=True)

# Box Plot After Outlier Removal
plt.figure(figsize=(12, 6))
sns.boxplot(data=data_zscore[numerical_columns], palette='coolwarm')
plt.title('Box Plot After Outlier Removal (Z-Score)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# 4. Encoding
categorical_columns = data.select_dtypes(include=['object']).columns
label_encoders = {}
for column in categorical_columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le


target_column = 'diabetes'  
X = data.drop(columns=[target_column])
y = data[target_column]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 5. KNN using Scikit-learn
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
sklearn_accuracy = knn.score(X_test, y_test)
print(f'Scikit-learn KNN Accuracy: {sklearn_accuracy:.2f}')


plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], X_test[:, 1], c=knn.predict(X_test), cmap='coolwarm', edgecolors='k', alpha=0.7)
plt.title('KNN Classification (Scikit-learn)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(label='Class')
plt.show()


#KNN manual implementation 
import numpy as np
from collections import Counter

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def knn_manual(X_train, y_train, X_test, k=5):
    predictions = []
    for test_point in X_test:
        distances = [euclidean_distance(test_point, train_point) for train_point in X_train]
        k_indices = np.argsort(distances)[:k]  # Get k nearest neighbors
        k_labels = [y_train[i] for i in k_indices]  # Get labels of k nearest
        most_common_label = Counter(k_labels).most_common(1)[0][0]  # Most frequent class
        predictions.append(most_common_label)
    return np.array(predictions)

# Call the manual KNN function on  dataset
y_pred_manual_knn = knn_manual(X_train, y_train.to_numpy(), X_test, k=5)

# Calculate accuracy
accuracy_manual_knn = np.sum(y_pred_manual_knn == y_test.to_numpy()) / len(y_test)
print(f'Manual KNN Accuracy: {accuracy_manual_knn:.2f}')

#decision tree 
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Initialize the Decision Tree Classifier
dt = DecisionTreeClassifier(criterion='gini', max_depth=5, random_state=42)

# Train the model
dt.fit(X_train, y_train)

# Predictions
y_pred_dt = dt.predict(X_test)

# Accuracy
dt_accuracy = accuracy_score(y_test, y_pred_dt)
print(f'Decision Tree Accuracy: {dt_accuracy:.2f}')

# Visualizing the Decision Tree
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 8))
plot_tree(dt, feature_names=X.columns, class_names=['No Diabetes', 'Diabetes'], filled=True)
plt.title("Decision Tree Visualization")
plt.show()

#k-means clusterring using library
from sklearn.cluster import KMeans

# Choosing the number of clusters (Elbow Method)
inertia = []
K_range = range(1, 11)  # Checking for 1 to 10 clusters

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Graph
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, marker='o', linestyle='-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (Within-Cluster Sum of Squares)')
plt.title('Elbow Method for Optimal K')
plt.grid(True)
plt.show()

# Applying K-Means with the chosen K (assume K=3, modify if needed)
optimal_k = 3  
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Adding cluster labels to data
data['Cluster'] = clusters

# Plotting Clusters
plt.figure(figsize=(10, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis', edgecolors='k', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', marker='X', label="Centroids")
plt.title('K-Means Clustering Visualization')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True)
plt.show()

#Kmeans manual
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Function to compute Euclidean distance
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

# Manual K-Means function
def k_means_manual(X, k, max_iters=100, tol=1e-4):
    np.random.seed(42)  # Ensure reproducibility
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    
    for _ in range(max_iters):
        clusters = [[] for _ in range(k)]
        for point in X:
            distances = [euclidean_distance(point, centroid) for centroid in centroids]
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(point)

        new_centroids = np.array([np.mean(cluster, axis=0) if len(cluster) > 0 else centroids[i] 
                                  for i, cluster in enumerate(clusters)])
        if np.all(np.abs(new_centroids - centroids) < tol):
            break
        centroids = new_centroids
    
    return centroids, clusters

# Load the dataset
file_path = r'C:\Users\vedik\Downloads\archive\Diabetes.csv'
df = pd.read_csv(file_path)

# Extract relevant features (BMI, Glucose)
X = df[['bmi', 'glucose']].values

# Run Manual K-Means
k = 3
centroids_manual, clusters_manual = k_means_manual(X, k)

# Plot Clusters for Manual K-Means
plt.figure(figsize=(8, 6))
for i, cluster in enumerate(clusters_manual):
    cluster = np.array(cluster)
    plt.scatter(cluster[:, 0], cluster[:, 1], label=f'Manual Cluster {i+1}')
plt.scatter(centroids_manual[:, 0], centroids_manual[:, 1], s=200, c='red', marker='X', label="Manual Centroids")
plt.title("Manual K-Means Clustering on BMI and Glucose")
plt.xlabel("BMI")
plt.ylabel("Glucose")
plt.legend()
plt.show()

# Run Sklearn K-Means
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_
centroids_sklearn = kmeans.cluster_centers_

# Plot Clusters for Sklearn K-Means
plt.figure(figsize=(8, 6))
for i in range(k):
    plt.scatter(X[labels == i, 0], X[labels == i, 1], label=f'Sklearn Cluster {i+1}')
plt.scatter(centroids_sklearn[:, 0], centroids_sklearn[:, 1], s=200, c='red', marker='X', label="Sklearn Centroids")
plt.title("Sklearn K-Means Clustering on BMI and Glucose")
plt.xlabel("BMI")
plt.ylabel("Glucose")
plt.legend()
plt.show()

plt.ylabel("Glucose")
plt.legend()
plt.show()

# Run Sklearn K-Means
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_
centroids_sklearn = kmeans.cluster_centers_

# Plot Clusters for Sklearn K-Means
plt.figure(figsize=(8, 6))
for i in range(k):
    plt.scatter(X[labels == i, 0], X[labels == i, 1], label=f'Sklearn Cluster {i+1}')
plt.scatter(centroids_sklearn[:, 0], centroids_sklearn[:, 1], s=200, c='red', marker='X', label="Sklearn Centroids")
plt.title("Sklearn K-Means Clustering on BMI, Glucose, and Blood Pressure")
plt.xlabel("BMI")
plt.ylabel("Glucose")
plt.legend()
plt.show()










