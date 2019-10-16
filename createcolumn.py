import sys
import constants
import pandas as pd



def show_help():
    print("Usage: python createcolumn.py to run\n")
    print("Be in the same directory as masterA ane masterB")


def importDframe():
    data = pd.read_csv("Original Data/Master File/masterA.csv")
    data1 = pd.read_csv("Original Data/Master File/masterB.csv")
    lista = [data, data1]
    return lista


def addModel(dataframes, models):
    for x in dataframes:
        for y in models:
            x[y] = 0


def addType(dataframes, types):
    for x in dataframes:
        for y in types:
            x[y] = 0


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if len(sys.argv) > 1:
        show_help()
        sys.exit(0)

    dfList = importDframe()
    modelList = constants.FLAT_M
    typeList = constants.FLAT_T
    addType(dfList, typeList)
    addModel(dfList, modelList)
    f1 = open("Original Data/Master File/masterA.csv", "w")
    f2 = open("Original Data/Master File/masterB.csv", "w")
    dfList[0].to_csv(f1, index=False, encoding='utf-8-sig')
    dfList[1].to_csv(f2, index=False, encoding='utf-8-sig')
    f1.close()
    f2.close()
    print("masterA headers: " + str(dfList[0].columns) + '\n')
    print("Length: " + str(len(dfList[0].columns)) + '\n')
    print("masterB headers: " + str(dfList[1].columns) + '\n')
    print("Length: " + str(len(dfList[1].columns)) + '\n')
    print("FILES WRITTEN")