import sys
import time

import pandas as pd


def importDframe():
    data = pd.read_csv("Original Data/Master File/masterA_nd.csv")
    data1 = pd.read_csv("Original Data/Master File/masterB_nd.csv")
    list = [data, data1]
    return list

def drop_rows(dataframes):
    temp = []
    for x in dataframes:
        data = x.drop(["month", "town", "flat_type","block","street_name","storey_range","flat_model", "blk_street", "latitude","longitude"],axis =1)
        temp.append(data)
    return temp

if __name__ == '__main__':
    dfList = importDframe()
    final = drop_rows(dfList)

    f1 = open("Original Data/Master File/kmeansA.csv", "w")
    f2 = open("Original Data/Master File/kmeansB.csv", "w")

    final[0].to_csv(f1, index=False)
    final[1].to_csv(f2, index=False)
    f1.close()
    f2.close()