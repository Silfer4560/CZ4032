import numpy as np
import math
from sklearn.tree import DecisionTreeRegressor
import pickle

admit_data = np.genfromtxt('cleanRegressionData.csv', delimiter= ',')

print("Data imported")

X_data, Y_data = admit_data[1:,1:46], admit_data[1:,-1]
Y_data = Y_data.reshape(Y_data.shape[0], 1)

idx = np.arange(X_data.shape[0])
np.random.shuffle(idx)
X_data, Y_data = X_data[idx], Y_data[idx]

realmean = np.mean(X_data, axis=0)
realstd = np.std(X_data, axis=0)

X_data = (X_data- np.mean(X_data, axis=0))/ np.std(X_data, axis=0)
mean = np.mean(Y_data)
std = np.std(Y_data)
Y_data = (Y_data - mean)/ std

#split into train and test
cutoff = math.floor(0.7 * len(X_data))

trainX = np.copy(X_data[:cutoff])
trainY = np.copy(Y_data[:cutoff])

testX = np.copy(X_data[cutoff:])
testY = np.copy(Y_data[cutoff:])

print("Creating model...")
# Create model
regr1 = DecisionTreeRegressor(max_depth=14)
regr1.fit(trainX, trainY)

print("Saving model...")
# Save model
f = open("decisiontree.pkl", 'wb')
pickle.dump(regr1, f)
pickle.dump(realmean, f)
pickle.dump(realstd, f)
pickle.dump(mean, f)
pickle.dump(std, f)
f.close()

print("Model saved")