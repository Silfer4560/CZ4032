print(__doc__)

import time
import numpy as np
import itertools as it
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale

#constants
cluster_size=[3]
max_cluster = 10
filepath = "kmeans_image/"
#import dataframes
data = pd.read_csv("Original Data/Master File/cleanRegressionData.csv")
#create new data frame with only needed columns
newdf = data[['floor_area_sqm', 'resale_price', 's_months']]
#sample data from dataframe
testdf = newdf.sample(n=1000, random_state= 5)

dataset_array = testdf.values
sse ={}
columns = []
alist = ['floor_area_sqm', 'resale_price', 's_months']
blist = ['floor_area_sqm', 'resale_price', 's_months']
#print (data.columns)
for x in testdf.columns:
    columns.append(x)
#print (columns)
for i in cluster_size:
    km = KMeans(n_clusters=i)
    km.fit(testdf.values)
    for a in alist:
        for b in blist:
            if a != b:
                print(a,b)
                plt.scatter(x=testdf[a], y=testdf[b], c=km.labels_.astype(float), s=10)
                plt.ylabel(b)
                plt.xlabel(a)
                plt.title('{} against {}, k{}'.format(b, a, i))
                plt.savefig('{}_against_{}_k{}'.format(b, a, i))
                plt.clf()

#iterate thru axes
# for x in cluster_size:


#iterate thru k for optimal K
# for x in range(max_cluster-1):
# #     start = time.time()
#     n = x+1
#     print(n)
#     km = KMeans(n_clusters=n)
#     km.fit(newdf.values)
#     sse[n] = km.inertia_
# #     end = time.time()
# #     print(end-start)
#
#
# plt.plot(list(sse.keys()),list(sse.values()))
# plt.xlabel("Number of cluster")
# plt.ylabel("SSE")
# plt.show()
# plt.savefig('kmeansnew_sseplot.png')
# # km = KMeans(n_clusters=5)
# km.fit(data.values)
# labels = km.labels_
# # Format results as a DataFrame
# # results = pd.DataFrame([data.index,labels]).T
# # f = open("Original Data/Master File/results.csv", "w")
# # results.to_csv(f, index=False)
#
# plt.scatter(x=data.floor_area_sqm,c=km.labels_.astype(float), y=data.resale_price, s=10)
# plt.title("price against area")
# plt.savefig('1.png')
# plt.clf()
# plt.scatter(x=data.s_months,c=km.labels_.astype(float), y=data.resale_price, s=10)
# plt.title("price against area")
# plt.savefig('2.png')
