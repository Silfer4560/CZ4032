import numpy as np
import math
from sklearn.tree import DecisionTreeRegressor
import pickle

admit_data = np.genfromtxt('cleanRegressionData.csv', delimiter= ',')

print("Data imported")

X_data, Y_data = admit_data[1:,1:32], admit_data[1:,-1]
Y_data = Y_data.reshape(Y_data.shape[0], 1)

idx = np.arange(X_data.shape[0])
np.random.shuffle(idx)
X_data, Y_data = X_data[idx], Y_data[idx]

#split into train and test
cutoff = math.floor(0.7 * len(X_data))

trainX = np.copy(X_data[:cutoff])
trainY = np.copy(Y_data[:cutoff])

testX = np.copy(X_data[cutoff:])
testY = np.copy(Y_data[cutoff:])

print("Creating model...")
# Create model
regr1 = DecisionTreeRegressor(max_depth=19)
regr1.fit(trainX, trainY)

print("Saving model...")
# Save model
f = open("decisiontree.pkl", 'wb')
pickle.dump(regr1, f)

f.close()

print("Model saved")