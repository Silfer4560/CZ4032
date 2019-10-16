import os
import sys
import time
import csv
import glob
import pandas as pd
import constants


def createMasterA(handleA, fileList, alen):
    print("merging A list")
    # list of all dataframes
    dfList = []
    for f in fileList:
        data = pd.read_csv(f)
        if len(data.columns) == 11:
            print("dropping column in file " + f)
            data = data.drop('remaining_lease', axis=1)
        dfList.append(data)
    combined_csv = pd.concat(dfList, ignore_index=True)
    # printout to check correctness
    print("COMBINED CSV COLUMNS")
    print(combined_csv.columns)
    print("number of rows = " + str(len(combined_csv.index)))
    print("alen = " + str(alen))
    # write to masterfileA
    combined_csv.to_csv(handleA, index=False, encoding='utf-8-sig', chunksize=10000)
    print("combined all to master A")


def show_help():
    print("Usage: createMaster.py [csv directory path] to create master files")
    print("Usage: createMaster.py [directory path to masterfiles] -i to isolate address for lat long calculation")


def createMasterB(handleB, fileList, blen):
    print("merging B list")
    combined_csv = pd.concat([pd.read_csv(f) for f in fileList], ignore_index=True)
    # printout to check correctness
    print("COMBINED CSV COLUMNS")
    print(combined_csv.columns)
    print("number of rows = " + str(len(combined_csv.index)))
    print("blen = " + str(blen))
    # write to masterfileB
    combined_csv.to_csv(handleB, index=False, encoding='utf-8-sig')
    print("combined all to master B")


def isolate(fileHandle, dataframe):
    location = []
    flat_m = []
    flat_t = []
    count = 0

    for index, row in dataframe.iterrows():
        count += 1
        if (count % 1000 == 0):
            print("Iterated {} times".format(count))
        locString = row["block"] + "," + row["street_name"]
    # identify all flat_model in dataset
        if row["flat_model"] not in flat_m:
            flat_m.append(row["flat_model"])
        # identify all flat type in dataset
        if row["flat_type"] not in flat_t:
            flat_t.append(row["flat_type"])
        # identify all different locations
        if locString not in location:
            location.append(locString)


    print("extraction complete: printing to file")
    fileHandle.write("#all flat types \n")
    fileHandle.write("FLAT_T =")
    fileHandle.write(str(flat_t))
    fileHandle.write("\n\n")
    fileHandle.write("#all flat models \n")
    fileHandle.write("FLAT_M =")
    fileHandle.write(str(flat_m))
    fileHandle.write("\n\n")
    fileHandle.write("#all locations \n")
    fileHandle.write("FLAT_LOCATION =")
    fileHandle.write(str(location))
    fileHandle.write("\n\n")
    fileHandle.close()
    print("File written")

if __name__ == "__main__":
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    # declare directory

    os.chdir(sys.argv[1])

    if (len(sys.argv) == 2):
        # get all file names
        print ("changed dir")
        extension = 'csv'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

        # check if files are found and print
        if (len(all_filenames)):
            print("Directory found: " + str(len(all_filenames)) + "files found")
            for x in all_filenames:
                print(x)
        else:
            print("Directory not found")
            show_help()
            sys.exit(0)

        # variables for theoretical rows in table for checking
        alen = 0
        blen = 0

        # file handle for two master files
        f1 = open("Master File\masterA.csv", "w")  # no remaining months(all files)
        f2 = open("Master File\masterB.csv", "w")  # remaining months, files without will be excluded

        # split files accordingly
        masterAList = []
        masterBList = []
        for f in all_filenames:
            print ("reading " + f)
            data = pd.read_csv(f)
            print(data.columns)
            if (len(data.columns) == 11):
                masterBList.append(f)
                blen = blen + len(data.index)
            masterAList.append(f)
            alen = alen + len(data.index)
        print("Sorted all files")
        print("Master A files: ")
        for f in masterAList:
            print(f + ",")
        print("Master b files: ")
        for f in masterBList:
            print(f + ",")

        # call functions to merge files
        createMasterA(f1, masterAList, alen)
        createMasterB(f2, masterBList, blen)
    elif "-i" in sys.argv:
        # extract data
        # open master file A
        try:
            masterDf = pd.read_csv('masterA.csv')
        except:
            print("masterA.csv not found")

        f3 = open("constants.py", "w")
        isolate(f3, masterDf)

    elif "-t" in sys.argv:
        print (constants.FLAT_T)
        print(constants.FLAT_M)
        print(constants.FLAT_LOCATION)
