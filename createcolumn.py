import sys
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
            x.at[index,temp1] = 1
            # print(row[temp])
        finalframes.append(x)
    return finalframes


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if len(sys.argv) > 1:
        show_help()
        sys.exit(0)
    print (len(constants.FLAT_LOCATION))
    # dfList = importDframe()
    # modelList = constants.FLAT_M
    # typeList = constants.FLAT_T
    # addType(dfList, typeList)
    # addModel(dfList, modelList)
    # final = assertCol(dfList)
    # f1 = open("Original Data/Master File/masterA.csv", "w")
    # f2 = open("Original Data/Master File/masterB.csv", "w")
    # final[0].to_csv(f1, index=False, encoding='utf-8-sig')
    # final[1].to_csv(f2, index=False, encoding='utf-8-sig')
    # f1.close()
    # f2.close()
    # print("masterA headers: " + str(final[0].columns) + '\n')
    # print("Length: " + str(len(final[0].columns)) + '\n')
    # print("masterB headers: " + str(final[1].columns) + '\n')
    # print("Length: " + str(len(final[1].columns)) + '\n')
    # print("FILES WRITTEN")