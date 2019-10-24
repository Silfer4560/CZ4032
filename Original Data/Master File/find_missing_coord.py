import googlemaps
from datetime import datetime
import json
import pandas as pd
import numpy as np

gmaps = googlemaps.Client(key='AIzaSyBoEiWBbGP-k-1JyODIHbkfY5aUnafEq5w')



def find_longlang(addr):


    geocode_result = gmaps.geocode(addr)
    data = json.dumps(geocode_result)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]


    return latitude,longitude

def main():

    asd = find_longlang("311138")

    print (asd)

if __name__ == "__main__":
    main()