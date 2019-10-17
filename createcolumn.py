import sys
import time

import constants
import pandas as pd


def show_help():
    print("Usage: python createcolumn.py to run\n")
    print("Be in the same directory as masterA ane masterB")


def importDframe():
    data = pd.read_csv("Original Data/Master File/masterA.csv")
    data1 = pd.read_csv("Original Data/Master File/masterB.csv")
    list = [data, data1]
    return list


def addModel(dataframes, models):
    for x in dataframes:
        for y in models:
            x[y] = 0


def addType(dataframes, types):
    for x in dataframes:
        for y in types:
            x[y] = 0


def assertCol(dataframes):
    finalframes = []
    for x in dataframes:
        count = 0
        for index, row in x.iterrows():
            count += 1
            if (count % 1000 == 0):
                print("Iterated {} times".format(count))
            temp = row['flat_model']
            temp1 = row['flat_type']
            # print(row[temp])
            x.at[index, temp] = 1
            # print(row[temp])
            # print(row[temp1])
            x.at[index, temp1] = 1
            # print(row[temp])
        finalframes.append(x)
    return finalframes


def assertDupe(dataframes):
    temp = []
    for x in dataframes:
        count = 0
        for index, row in x.iterrows():
            count += 1
            if (count % 1000 == 0):
                print("Iterated {} times".format(count))
            if (row["2 ROOM"] == 1) or (row["2-ROOM"] == 1) or (row["2-room"] == 1):
                x.at[index, '2-ROOM'] = 1
            if (row["APARTMENT"] == 1) or (row["Apartment"] == 1):
                x.at[index, 'APARTMENT'] = 1
            if (row["IMPROVED"] == 1) or (row["Improved"] == 1):
                x.at[index, 'IMPROVED'] = 1
            if (row["Maisonette"] == 1) or (row["MAISONETTE"] == 1):
                x.at[index, "MAISONETTE"] = 1
            if (row["MODEL A"] == 1) or (row["Model A"] == 1):
                x.at[index, "MODEL A"] = 1
            if (row["MULTI GENERATION"] == 1) or (row["MULTI-GENERATION"] == 1) or (row["Multi Generation"] == 1):
                x.at[index, 'MULTI GENERATION'] = 1
            if (row["NEW GENERATION"] == 1) or (row["New Generation"] == 1):
                x.at[index, 'NEW GENERATION'] = 1
            if (row["PREMIUM APARTMENT"] == 1) or (row["Premium Apartment"] == 1):
                x.at[index, 'PREMIUM APARTMENT'] = 1
            if (row["SIMPLIFIED"] == 1) or (row["Simplified"] == 1):
                x.at[index, 'SIMPLIFIED'] = 1
            if (row["STANDARD"] == 1) or (row["Standard"] == 1):
                x.at[index, 'STANDARD'] = 1
            if (row["Terrace"] == 1) or (row["TERRACE"] == 1):
                x.at[index, 'TERRACE'] = 1
            if (row["Model A-Maisonette"]==1) or (row["MODEL A-MAISONETTE"] ==1):
                x.at[index,"MODEL A-MAISONETTE"] = 1
        temp.append(x)
    return temp


def dropDupe(dataframes):
    temp = []
    for x in dataframes:
        data = x.drop(["2 ROOM","2-room","Apartment","Model A-Maisonette","Improved","Maisonette","Model A","MULTI-GENERATION","Multi Generation","New Generation","Premium Apartment","Simplified","Standard","Terrace"],axis=1)
        temp.append(data)
    return temp


def convertMonths(dataframes):
    monthlist =[]
    for x in dataframes:
        flag = False
        count = 1
        x['s_months'] = 0
        if 'remaining_lease' in x.columns:
            x['lease_months'] = 0
            flag = True
        for index, row in x.iterrows():
            if (count % 1000 == 0):
                print("Iterated {} times".format(count))
            if flag:
                rString = row['remaining_lease']
                if "year" in str(rString):
                    #formatted as x years y months
                    myArr = rString.split(" ")
                    if len(myArr) == 2:
                        #only years
                        months = int(myArr[0]) * 12
                    else:
                        #both months and years
                        months = (int(myArr[0]) * 12) + int(myArr[2])
                else:
                    #only years
                    months = int(rString) * 12
                x.at[index, 'lease_months'] = months
            mString = row['month'] #formatted as year-month
            #MONTH 1 IS 1990-01
            myArr1 = mString.split('-')
            mYear = int(myArr1[0])
            mMonth = int(myArr1[1])
            var = ((mYear - 1990) *12) + mMonth
            x.at[index,'s_months'] = var
        monthlist.append(x)
    return monthlist

def storyRange(dataframes):
    temp = []
    for x in dataframes:
        x['storyUpper'] = 0
        for index, row in x.iterrows():
            myString = row['storey_range']
            myArr = myString.split(" ")
            x.at[index, 'storyUpper'] = myArr[2]
        temp.append(x)
    return temp


if __name__ == "__main__":
    start = time.time()
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    mylist = constants.stuff
    mylist.sort()
    print(mylist)
    if len(sys.argv) > 1:
        show_help()
        sys.exit(0)
    print(len(constants.FLAT_LOCATION))
    dfList = importDframe()
    modelList = constants.FLAT_M
    typeList = constants.FLAT_T
    addType(dfList, typeList)
    addModel(dfList, modelList)
    temp = assertCol(dfList)
    temp1 = assertDupe(temp)
    temp2 = dropDupe(temp1)
    temp3 = convertMonths(temp2)
    final = storyRange(temp3)
    #final should be the final array of dataframes
    f1 = open("Original Data/Master File/masterA.csv", "w")
    f2 = open("Original Data/Master File/masterB.csv", "w")
    final[0].to_csv(f1, index=False, encoding='utf-8-sig')
    final[1].to_csv(f2, index=False, encoding='utf-8-sig')
    f1.close()
    f2.close()
    print("masterA headers: " + str(final[0].columns) + '\n')
    print("Length: " + str(len(final[0].columns)) + '\n')
    print("masterB headers: " + str(final[1].columns) + '\n')
    print("Length: " + str(len(final[1].columns)) + '\n')
    print("Extra headers: ")
    print(len(constants.FLAT_T) + len(constants.FLAT_M))
    print("FILES WRITTEN")
    end = time.time()
    print (end-start)
