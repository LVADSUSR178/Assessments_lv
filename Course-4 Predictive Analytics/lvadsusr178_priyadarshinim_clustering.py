# -*- coding: utf-8 -*-
"""LVADSUSR178_PriyadarshiniM_Clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EN5SFYm2sjn3A4HQhpfllZ0pZtqYvsVA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns

d=pd.read_csv('/content/customer_segmentation.csv')

d.head()

#data cleaning
d.isnull().sum()

d['Income']=d['Income'].fillna(d['Income'].mean())

d.isnull().sum()

d.duplicated().sum()

d.info()

#Encoding
from sklearn.preprocessing import LabelEncoder
len=LabelEncoder()
for column in d.select_dtypes(include=['object']):
  d[column]=len.fit_transform(d[column])

d.info()

from sklearn.preprocessing import StandardScaler
ss=StandardScaler()
scaled_data=ss.fit_transform(d)

#EDA
d.hist(figsize=(10,10))
plt.tight_layout()

plt.figure(figsize=(10, 10))
plt.title('Correlation Heatmap')
sns.heatmap(d.corr(), annot=True, cmap='rainbow', fmt='.2f')

# sns.pairplot(df, diag_kind='kde')

import warnings
warnings.filterwarnings('ignore')

#Find optimal number of clusters
inertia_values = []
silhouette_scores = []
k_values = range(2, 10)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia_values.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_data, kmeans.labels_))

#Elbow plot
plt.plot(k_values, inertia_values, marker='*',color='blue')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Curve for determining Optimal k value')
plt.xticks(k_values)

#silhoutte score plot
plt.plot(k_values, silhouette_scores, marker='o',color='red')
plt.xticks(k_values)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Scores for Optimal k')

optimal_k = 7
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(scaled_data)

cluster_labels = kmeans.predict(scaled_data)

silhouette_avg = silhouette_score(scaled_data, cluster_labels)
print("Ave silhouetter score: ",silhouette_avg)

#cluster profiling
d['Cluster'] = kmeans.labels_
clusters = d.groupby('Cluster').mean()
print(clusters)

#D.Cluster Analysis
import seaborn as sns
x=scaled_data[:0]
y=scaled_data[:1]
plt.figure(figsize=(10,5))
sns.scatterplot(x=y ,y =y, hue='Cluster',palette=['green','red','blue','black','yellow','orange','pink'],legend=True,data=d)
plt.title("Visualization of clusters")
plt.show()