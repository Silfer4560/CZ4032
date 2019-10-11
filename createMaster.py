import os
import sys
import time
import csv


def createMasterA(handleA, fileList):
    for x in fileList:
        with open(x,"w") as f:
            reader = csv.reader(f)


def show_help():
    print("Meant to create both Masterfile A and B")
    print("Usage: createMaster.py [directory path]")


def createMasterB(f1, fileList):
    pass


if __name__ == " __main__":
    if len(sys.argv) != 1:
        show_help()
        sys.exit(0)
    #file handle for two master files
    f = open("masterA.csv", "w")
    f1 = open("masterB.csv","w")
    #iterate through directory to find all files to merge
    fileList = os.listdir(sys.argv[1])
    if (len(fileList)):
        print("Directory found: "+ len(fileList)+ "files found")
        for x in fileList:
            print(x)
    else:
        print("Directory not found")
        time.sleep(2)
        sys.exit(0)
    createMasterA(f, fileList)
    createMasterB(f1, fileList)
   # sys.exit(0)










# if __name__ == '__main__':
#     if "-c" in sys.argv:
#         print "True"
#         if len(sys.argv) != 4:
#             show_help()
#         compareSum(sys.argv[2],sys.argv[3])
#     else:
#         if len(sys.argv) != 3:
#             show_help()
#             sys.exit(0)
#         f = open(sys.argv[2], "w")
#         fullSet = set()
#         progThread =[]
#         summary(sys.argv[1])
#         #print progThread