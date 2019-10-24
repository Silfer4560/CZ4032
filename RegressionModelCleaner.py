import pandas as pd
import numpy as np
import math

EPOCH_TIME = '1990-01'

masterWithoutLatLong = pd.read_csv("Original Data\\Master File\\Master File\\masterA.csv")
latlong = pd.read_csv("Original Data\\Master File\\Coordinates_mapping.csv")

# merge table with latlong table
masterWithoutLatLong['blk_street'] = masterWithoutLatLong['block'] + ' ' + masterWithoutLatLong['street_name']
master = pd.merge(masterWithoutLatLong, latlong, left_on='blk_street', right_on='blk_street', how='left')

# convert storey into a integer
master['storey'] = master['storey_range'].str.split(' ').str[0]

# convert month
formattedMonth = pd.to_datetime(master['month'], format='%Y-%m')
epochMonth = pd.to_datetime(EPOCH_TIME, format='%Y-%m')
master['monthFromStart'] = round((formattedMonth - epochMonth)/np.timedelta64(1, 'M'))

resale_price = master.pop('resale_price')
master['resale_price'] = resale_price

# drop all columns that are not integer
masterdropped = master.drop(columns=['month', 'town', 'storey_range', 'flat_type', 'block', 'street_name', 'flat_model', 'blk_street']) 

masterdropped.to_csv("cleanRegressionData.csv")