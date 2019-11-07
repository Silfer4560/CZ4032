import googlemaps
from datetime import datetime
import json
import pandas as pd
import numpy as np





def find_longlang(addr):
    filename = 'apikey'
    api_key = get_file_contents(filename)
    print("Our API key is: %s" % (api_key))
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(addr)
    data = json.dumps(geocode_result)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]


    return latitude,longitude
	
def get_file_contents(filename):
    """ Given a filename,
		return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
			# It's assumed our file contains a single line,
			# with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

def main():

    asd = find_longlang("311138")

    print (asd)

if __name__ == "__main__":
    main()