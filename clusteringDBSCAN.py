from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
def scale(data):
    scaled_data = (data- np.mean(data, axis=0))/ np.std(data, axis=0)
    return scaled_data

def create_data(col1,col2):
    unscaled_data = np.vstack((col1,col2))
    unscaled_data = np.transpose(unscaled_data)
    
    col1 = scale(col1)
    col2 = scale(col2)

    data = np.vstack((col1,col2))
    data = np.transpose(data)
    return data,unscaled_data

def cluster_dbscan(data,unscaled_data,title):
    # compute dbscan
    db = DBSCAN(eps=0.1, min_samples=50).fit(data)

    # Extract a mask of core cluster members
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    
    # Extract labels (-1 is used for outliers)
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)

    # Plot up the results!
    min_x = np.min(unscaled_data[:,0])
    max_x = np.max(unscaled_data[:,0])
    min_y = np.min(unscaled_data[:,1])
    max_y = np.max(unscaled_data[:,1])

    fig = plt.figure(figsize=(12,6))
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = unscaled_data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                markeredgecolor='k', markersize=7)

        xy = unscaled_data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                markeredgecolor='k', markersize=3)
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.title('DBSCAN: %d clusters found' % n_clusters, fontsize = 20)
    plt.title(title)
    fig.tight_layout()
    plt.savefig(title)
    return




# Get the dataset to be used for clustering
housing_data = np.genfromtxt("Original Data/Master File/cleanRegressionData.csv",delimiter=",")

# #shuffle data
idx = np.arange(housing_data.shape[0])
np.random.shuffle(idx)
housing_data = housing_data[idx]

# first column is nan so we drop it
square_area = housing_data[1:10000,1]
resale_price = housing_data[1:10000,-1]
num_months = housing_data[1:10000,-5]


# DBScan clustering
area_price,unscaled_area_price = create_data(square_area,resale_price)
cluster_dbscan(area_price,unscaled_area_price,"Floor area against price")
months_price,unscaled_months_price = create_data(num_months,resale_price)
cluster_dbscan(months_price,unscaled_months_price,"Months against price")

#lat long 
lat_long_price = housing_data[1:10000,-3:]
scaled_lat_long_price = scale(lat_long_price)
# compute dbscan
db = DBSCAN(eps=0.1, min_samples=50).fit(scaled_lat_long_price)

# Extract a mask of core cluster members
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True

# Extract labels (-1 is used for outliers)
labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = set(labels)
# Plot up the results!
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(lat_long_price[:,1], lat_long_price[:,0], lat_long_price[:,2])

ax.set_xlabel('Long')
ax.set_ylabel('Lat')
ax.set_zlabel('Price')
plt.savefig("latlong vs price")