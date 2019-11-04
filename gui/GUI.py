from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QWidget, QInputDialog, QLineEdit, QCompleter
from PyQt5.QtCore import QStringListModel
from mydesign import *
import sys
import ReadModel
import googlemaps
import json
 
data = ['PyQt5','Is','Awesome']

#all flat types 
flat_Type_List =['1 ROOM','2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM',  'EXECUTIVE', 'MULTI GENERATION']
flat_Type_Binary = [0 for i in range(len(flat_Type_List))]

#all flat models 
flat_Model_List = ["IMPROVED","NEW GENERATION","MODEL A","STANDARD","SIMPLIFIED","MODEL A-MAISONETTE","APARTMENT","MAISONETTE","TERRACE","IMPROVED-MAISONETTE","PREMIUM APARTMENT","Adjoined flat","Premium Maisonette","Model A2","Type S1","Type S2","DBSS","Premium Apartment Loft"]
flat_Model_Binary = [0 for i in range(len(flat_Model_List))]
 
class mywindow(QtWidgets.QMainWindow):
 
        def __init__(self):
            super().__init__() 
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            #Fill comboBox
            self.ui.flat_Type_List.addItems(flat_Type_List)
            self.ui.flat_Model_List.addItems(flat_Model_List)
            
            #Linking button signals and actions
            self.ui.predictButton.clicked.connect(self.printAll)

        def printAll(self):
            (flatType,flatModel,storeyRange,lease,addr,floorArea,months) = self.getAll()
            final_array = []
            print (flatType,flatModel,storeyRange,lease,addr,floorArea,months)

            flat_Type_Binary_copy = flat_Type_Binary.copy()
            flat_Model_Binary_copy = flat_Model_Binary.copy()

            for i, word in enumerate(flat_Type_List):
                if word == flatType:
                    flat_Type_Binary_copy[i] = 1
                    #print (flat_Type_Binary_copy)
                    #print (word)

            for i, word in enumerate(flat_Model_List):
                if word == flatModel:
                    flat_Model_Binary_copy[i] = 1
                    #print (flat_Model_Binary_copy)
                    #print (word)

            print (addr)
            (lat,lng) = self.find_longlang(addr)


            final_array = [floorArea,lease]
            final_array.extend(flat_Type_Binary_copy)
            final_array.extend(flat_Model_Binary_copy)
            final_array.append(months)
            final_array.append(storeyRange)
            final_array.append(lat)
            final_array.append(lng)



            prediction = ReadModel.predict(final_array)
            #prediction_str = "SGD " + format(prediction[0], '.2f')
            prediction_str = "SGD " + str(prediction[0])
            self.ui.prediction_Label.setText(prediction_str)
            print (prediction)
            print (final_array)


        def getAll(self):
            flatType = self.ui.flat_Type_List.currentText()
            flatModel = self.ui.flat_Model_List.currentText()
            storeyRange = self.ui.storey_Range_Box.value()
            lease = self.ui.lease_Box.value()
            addr = self.ui.address_Box.text()
            addr = addr + " Singapore"
            floorArea = self.ui.horizontalSlider.value()
            months = self.ui.months_Box.value()
            return (flatType,flatModel,storeyRange,lease,addr,floorArea,months)

        def find_longlang(self, addr):
            filename = 'apikey'
            api_key = self.get_file_contents(filename)

            gmaps = googlemaps.Client(key=api_key)
            geocode_result = gmaps.geocode(addr)
            data = json.dumps(geocode_result)
            latitude = geocode_result[0]["geometry"]["location"]["lat"]
            longitude = geocode_result[0]["geometry"]["location"]["lng"]

            return latitude,longitude

        def get_file_contents(self, filename):
            """ Given a filename,
                return the contents of that file
            """
            try:
                with open(filename, 'r') as f:
                    # It's assumed our file contains a single line,
                    # with our API key
                    return f.read().strip()
            except FileNotFoundError:
                print("'%s' file not found" % filename)
            

 
app = QtWidgets.QApplication([])
#app.setStyle('Fusion')
win = mywindow()
win.show()
sys.exit(app.exec())
