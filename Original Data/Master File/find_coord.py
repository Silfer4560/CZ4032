# importing the requests library 
import requests 
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import time
from multiprocessing import  Pool
import sys

def find_longlat(addr):
    # api-endpoint 
    URL = "https://developers.onemap.sg/commonapi/search"

    # defining a params dict for the parameters to be sent to the API 
    
    PARAMS = {'searchVal':addr, 'returnGeom': "Y", 'getAddrDetails': 'Y'} 

    # Fetch request from oneMap api with retries
    try:
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=1.0)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        r = session.get(url = URL, params = PARAMS)
        print(r.url)
    except Exception as e:
        print (e)
        return 8,8

    # extracting data in json format 
    data = r.json() 


    # extracting latitude, longitude
    if data['found']==0:
        print ("No address found")
        return 0,0
    else:
        latitude = data['results'][0]['LATITUDE']
        longitude = data['results'][0]['LONGITUDE']

        # printing the output 
        #print("Latitude:%s\nLongitude:%s\n" %(latitude, longitude))
        # return function
        return latitude,longitude

def write_longlang(df):
    df["latitude"], df["longitude"] = zip(*df["blk_street"].apply(find_longlat))
    return df

def parallelize_dataframe(df, func, n_cores=8):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def main():

    if len(sys.argv)==1:
        print ("Please input csv data file as argument.")

    elif len(sys.argv)>2:
        print ("File used unclear, please try again.")

    else:

        if sys.argv[1][-4:] == ".csv":

            #read in masterA dataset
            df = pd.read_csv(sys.argv[1])

            #append blk and street name into blk_street
            #df['blk_street'] = df.block.astype(str).str.cat(df.street_name.astype(str), sep=' ')

            # Make a copy of the original dataframe
            df_1000=df.copy()
            #df_1000=df.tail(123)

            # Timer for benchmarking
            start = time.time()
			
			# Remove repeated address
            #df_1000.drop_duplicates(subset = "blk_street" , keep = 'first', inplace = True)
			
			# Run multicore function
            df_1000 = parallelize_dataframe(df_1000, write_longlang)

            # End of timer
            end = time.time()

            # Write dataframe to new csv
            new_csv_name="new_" + sys.argv[1]
            df_1000.to_csv(new_csv_name, index=False)

            print(end - start)

        else:
            print ("Please input a csv file")

if __name__ == "__main__":
    main()






 
