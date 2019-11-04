import numpy as np
import math
from sklearn.tree import DecisionTreeRegressor
import pickle

f = open("decisiontree.pkl", 'rb')
model = pickle.load(f)

def predict(features):
    
    features = np.array([features])
    predictions = model.predict(features)

    return predictions


