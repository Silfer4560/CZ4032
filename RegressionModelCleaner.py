import pandas as pd
import numpy as np
import math

EPOCH_TIME = '1990-01'

master = pd.read_csv("masterA_nd.csv")

resale_price = master.pop('resale_price')
master['resale_price'] = resale_price

# drop all columns that are not integer
masterdropped = master.drop(columns=['month', 'town', 'storey_range', 'flat_type', 'block', 'street_name', 'flat_model', 'blk_street']) 

# Realign 2 room to be in the right column
realigned = masterdropped[['floor_area_sqm', 'lease_commence_date', '1 ROOM', '2-ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI GENERATION', 'IMPROVED', 'NEW GENERATION', 'MODEL A', 'STANDARD', 'SIMPLIFIED', 'MODEL A-MAISONETTE', 'APARTMENT', 'MAISONETTE', 'TERRACE', 'IMPROVED-MAISONETTE', 'PREMIUM APARTMENT', 'Adjoined flat', 'Premium Maisonette', 'Model A2', 'Type S1', 'Type S2', 'DBSS', 'Premium Apartment Loft', 's_months', 'storyUpper', 'latitude', 'longitude', 'resale_price']]

realigned.to_csv("cleanRegressionData.csv")