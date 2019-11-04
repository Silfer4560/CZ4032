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


#print (predict([100, 1999, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1.352083, 103.819836]))