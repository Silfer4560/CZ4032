import numpy as np
import math
from sklearn.tree import DecisionTreeRegressor
import pickle

f = open("decisiontree.pkl", 'rb')
model = pickle.load(f)
mean = pickle.load(f)
std = pickle.load(f)
meanY = pickle.load(f)
stdY = pickle.load(f)

def predict(features):
    
    features = np.array([features])
    features = (features- mean/ std)
    predictions = model.predict(features)

    predictions = predictions * meanY + stdY
    return predictions

