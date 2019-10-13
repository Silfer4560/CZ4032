import os
import sys
import time
import csv
import glob
import pandas as pd


def createMasterA(handleA, fileList,alen):
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
    #write to masterfileA
    combined_csv.to_csv(handleA, index=False, encoding='utf-8-sig', chunksize=10000)
    print("combined all to master A")


def show_help():
    print("Meant to create both Masterfile A and B")
    print("Usage: createMaster.py [directory path]")


def createMasterB(handleB, fileList,blen):
    print("merging B list")
    combined_csv = pd.concat([pd.read_csv(f) for f in fileList], ignore_index=True)
    #printout to check correctness
    print("COMBINED CSV COLUMNS")
    print(combined_csv.columns)
    print("number of rows = " + str(len(combined_csv.index)))
    print("blen = " + str(blen))
    # write to masterfileB
    combined_csv.to_csv(handleB, index=False, encoding='utf-8-sig')
    print("combined all to master B")


if __name__ == "__main__":
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    if len(sys.argv) != 2:
        show_help()
        sys.exit(0)
    # declare directory
    os.chdir(sys.argv[1])


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
        time.sleep(2)
        sys.exit(0)


    #variables for theoretical rows in table for checking
    alen=0
    blen=0


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
        if (len(data.columns) == 10):
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
