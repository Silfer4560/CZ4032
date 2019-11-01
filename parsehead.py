import pandas as pd

def extract(dataframes):
    for x in dataframes:
        print("headers: " + str(x.columns) + '\n')



if __name__ == "__main__":
    data = pd.read_csv("Original Data/Master File/masterA_nd.csv")
    data1 = pd.read_csv("Original Data/Master File/masterB_nd.csv")
    list = [data, data1]
    extract(list)