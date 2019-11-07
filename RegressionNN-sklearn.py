import numpy as np
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import math
from tqdm import tqdm

num_sample_data = 100
models = [0]

def unnormalise(data, mean, std):
    return data * std + mean

def calculateloss(d, y):
    d = np.reshape(d, -1)    
    difference = d-y
    mse = np.square(difference)
    return np.mean(mse)

admit_data = np.genfromtxt('cleanRegressionData.csv', delimiter= ',')

print("Data imported")

X_data, Y_data = admit_data[1:,1:32], admit_data[1:,-1]
Y_data = Y_data.reshape(Y_data.shape[0], 1)

idx = np.arange(X_data.shape[0])
np.random.shuffle(idx)
X_data, Y_data = X_data[idx], Y_data[idx]

X_data = (X_data- np.mean(X_data, axis=0))/ np.std(X_data, axis=0)
mean = np.mean(Y_data)
std = np.std(Y_data)
Y_data = (Y_data - mean)/ std

#X_data = X_data[:100000]
#Y_data = Y_data[:100000]

#split into train and test
cutoff = math.floor(0.7 * len(X_data))

trainX = np.copy(X_data[:cutoff])
trainY = np.copy(Y_data[:cutoff])

testX = np.copy(X_data[cutoff:])
testY = np.copy(Y_data[cutoff:])

# prepare test set of 100 samples 
idxtest = np.arange(testX.shape[0])
np.random.shuffle(idxtest)
testX, testY = testX[idxtest], testY[idxtest]
sub_testX = testX[:num_sample_data]
sub_testY = testY[:num_sample_data]

# Sort the samples for visual aesthetic sake
idxsort = np.argsort([i[0] for i in sub_testY])
sub_testX, sub_testY = sub_testX[idxsort], sub_testY[idxsort]
sub_testY2 = [i[0] for i in sub_testY]
sub_testY = unnormalise(np.array(sub_testY2), mean, std)

predictions = []
loss = []
print("creating models")
for i in tqdm(models):
    # Create model

    #print("Creating model")
    nn=MLPRegressor(hidden_layer_sizes=(15,))
    trainX = trainX.astype('float')
    trainY = trainY.astype('float')
    nn.fit(trainX, trainY)

    #print("Model fitted")

    # Predict
    
    testYpredict = nn.predict(testX)
    loss.append(calculateloss(testY, testYpredict))

    predictY = nn.predict(sub_testX)
    predictY = unnormalise(np.array(predictY), mean, std)
    predictions.append(predictY)
    
print(loss)
# f1 = plt.figure(0)
# plt.plot(models, loss, label = "MSE")
# plt.title('Mean Square Errors of predictions vs K neighbours')
# plt.xlabel('Depth of tree')
# plt.ylabel('Loss')
# plt.legend()


for prediction, depth in zip(predictions, models):
    f1 = plt.figure(depth)
    plt.scatter(range(num_sample_data), prediction, label = "Neural Network")
    plt.scatter(range(num_sample_data), sub_testY, label = "Actual values")
    plt.title('Scatterplot of Predicted vs Target values')
    plt.xlabel('100 random data samples, sorted')
    plt.ylabel('Housing Prices')
    plt.legend()

plt.show()

