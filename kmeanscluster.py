print(__doc__)

import time
import numpy as np
import itertools as it
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale

#constants
cluster_size=[3,4]
max_cluster = 50
filepath = "kmeans_image/"
#import dataframes
data = pd.read_csv("Original Data/Master File/kmeansA.csv")
#data1 = pd.read_csv("Original Data/Master File/kmeansB.csv")

dataset_array = data.values
sse ={}
columns = []
#print (data.columns)
for x in data.columns:
    columns.append(x)
#print (columns)
for i in cluster_size:
    km = KMeans(n_clusters=i)
    km.fit(data.values)
    for a,b in it.combinations(columns,2):
        print(a,b)
        plt.scatter(x=data[a], y=data[b], c=km.labels_.astype(float), s=10)
        plt.ylabel(b)
        plt.xlabel(a)
        plt.title('{} against {}, k{}'.format(b, a, i))
        plt.savefig('{}_against_{}_k{}'.format(b, a, i))
        plt.clf()

#iterate thru axes
# for x in cluster_size:


#iterate thru k for optimal K
# for x in range(max_cluster-1):
#     start = time.time()
#     n = x+1
#     print(n)
#     km = KMeans(n_clusters=n)
#     km.fit(data.values)
#     sse[n] = km.inertia_
#     end = time.time()
#     print(end-start)
    # plt.scatter(x=data.floor_area_sqm, y=data.resale_price,c=km.labels_.astype(float),s=10)
    # plt.ylabel('Resale Price')
    # plt.xlabel('Floor Area')
    # plt.title(titleA.format(n))
    # plt.savefig(filepath + nameA.format(n))
    # plt.clf()
    # plt.scatter(x=data.s_months, y=data.resale_price, c=km.labels_.astype(float), s=10)
    # plt.ylabel('Resale Price')
    # plt.xlabel('Time')
    # plt.title(titleB.format(n))
    # plt.savefig(filepath + nameB.format(n))

# plt.plot(list(sse.keys()),list(sse.values()))
# plt.xlabel("Number of cluster")
# plt.ylabel("SSE")
# plt.show()
# plt.savefig('kmeans_sseplot.png')
# km = KMeans(n_clusters=5)
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
