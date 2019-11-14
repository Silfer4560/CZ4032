CZ4032 Data Mining Project
--------------------------
Groupmates:
Alvin
Andy
ChinWei
Leroy
QiYuan
TeeYang
--------------------------
PREREQUISITES
--------------------------
Python 3.6 or above
Scikit-learn library (pip install scikit-learn)
Tensorflow 1.15 (only for tensorflow model) (pip install tensorflow==1.15)
TQDM (for loading bar) (pip install tqdm)
Seaborn (For correlation matrix) (pip install seaborn)
Numpy
Pandas
Matplotlib
Pylab

----------------------------
Key files to be unzipped and locations to unzip to:
----------------------------
Raw data: 
Original Data/*.csv

Geographical coordinate data:
Original Data/coord_mapping.csv

Cleaned Data (Fixed columns): 
Original Data/Master File/MasterA.csv

Cleaned Data + dropped columns:
cleanRegressionData.csv <<< This is the only important file you need to run our models and clustering
----------------------------

Each of the above files are successively generated from the previous files, in our data cleaning process.
Eg.
createMaster.py <path to raw csvs> : Converts original data to MasterA.csv
find_coord.py <masterA.csv>: Queries all google maps coordinates and appends all coordinates into MasterA.csv
createColumn.py: Removes duplicate columns from MasterA.csv
regressionModelCleaner.py: Removes unnecessary columns from MasterA.csv, and makes a new file, cleanRegressionData.csv


NOTE: **You only need the final file cleanRegressionData.csv to run the next few scripts.**
----------------------------

To test any of the regression models, use the following files:
RegressionEnsemble.py   - Ensemble learning models
RegressionK-NN.py - K-Nearest Neighbours models
RegressionNN-sklearn.py - Neural Network models (Sklearn)
RegressionModel.py - Neural Network Model (Tensorflow)
RegressionSVM.py - Support Vector Regression models
RegressionTree.py - Decision Tree Model

To create the correlation matrix, use the following file:
Correlation Matrix.py

To perform K-means clustering, use the following file:
kmeanscluster.py

To perform DBSCAN clustering, use the following file:
clusteringDBSCAN.py