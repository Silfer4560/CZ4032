from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
def scale(data):
    scaled_data = (data- np.mean(data, axis=0))/ np.std(data, axis=0)
    return scaled_data
# Get the dataset to be used for clustering
housing_data = np.genfromtxt("Original Data/Master File/masterA.csv",delimiter=",")


# #shuffle data
idx = np.arange(housing_data.shape[0])
np.random.shuffle(idx)
housing_data = housing_data[idx]

# first column is nan so we drop it
square_area = housing_data[1:10000,6]
resale_price = housing_data[1:10000,9]

scaled_square_area = scale(square_area)
scaled_resale_price = scale(resale_price)

area_price = np.vstack((scaled_square_area,scaled_resale_price))
area_price = np.transpose(area_price)

unscaled_area_price = np.vstack((square_area,resale_price))
unscaled_area_price = np.transpose(unscaled_area_price)

# COMPUTE DBSCAN
db = DBSCAN(eps=0.1, min_samples=50).fit(area_price)

# Extract a mask of core cluster members
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
# Extract labels (-1 is used for outliers)
labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = set(labels)

# Plot up the results!
min_x = np.min(square_area)
max_x = np.max(square_area)
min_y = np.min(resale_price)
max_y = np.max(resale_price)

fig = plt.figure(figsize=(12,6))
plt.subplot(121)
plt.plot(unscaled_area_price[:,0], unscaled_area_price[:,1], 'ko')
plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y)
plt.title('Original Data', fontsize = 20)

plt.subplot(122)

colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = unscaled_area_price[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=7)

    xy = unscaled_area_price[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=3)
plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y)
plt.title('DBSCAN: %d clusters found' % n_clusters, fontsize = 20)
fig.tight_layout()
plt.xlabel("Floor area in Square Meters")
plt.ylabel("Resale price in SGD")
plt.subplots_adjust(left=0.03, right=0.98, top=0.9, bottom=0.05)
plt.show()
