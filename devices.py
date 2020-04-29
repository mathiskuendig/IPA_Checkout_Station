###############################################################################
# devices.py
#
# Contacts: Manuel Weber
# DATE: 24.02.2020
###############################################################################

import csv,os
from datetime import datetime
from myDatabase import MyDatabase
#from logger import Logger


nameOfDatabase = 'devices'  # Specify name of database file
nameOfTable = 'devices'  # Specify name of table
deviceCharacteristics = ('inventoryNumber', 'type', 'manufacturer', 'model','tagId')


class Devices(MyDatabase):
    """ A class implementing a measurement device database with the following attributes:
        - Inventory Number
        - Type
        - Manufacturer
        - Model
        """
    def __init__(self):
        #self.loggerInstance = Logger(__name__)
        super().__init__(nameOfDatabase)  # call parent's init function
        super().createTable(nameOfTable)  # create table in database
        
    def doesDeviceExist(self, userKey, userValue):
        """Returns true if device exists otherwise false."""
        deviceExists = False
        if (super().doesEntryExistInTable(nameOfTable, userKey, userValue) == True):
            deviceExists = True
        return deviceExists

    def addDeviceAsDict(self, deviceAsDict):
        """Add device and return true if successful otherwise false."""
        deviceCreated = False
        # check if device already exists
        if (self.doesDeviceExist('inventoryNumber',deviceAsDict['inventoryNumber']) == False):
            # create new device
            super().addEntryToTable(nameOfTable, deviceAsDict)
            deviceCreated = True
        return deviceCreated

    def removeDevice(self, inventoryNumber):
        """Remove device and return true if successful otherwise false."""
        deviceRemoved = False
        # check if device exists
        if (self.doesDeviceExist('inventoryNumber',inventoryNumber) == True):
            # remove device
            super().removeEntryFromTable(nameOfTable, deviceCharacteristics[0], inventoryNumber)
        return deviceRemoved

    def getDevice(self, deviceKey="", deviceValue=""):
        """ Returns device as dict."""
        device = {}
        if deviceKey != "":
            # check if device exists
            if (self.doesDeviceExist(deviceKey, deviceValue) == True):
                # return only first element of entry because we expect that every device just exists once
                device = super().getEntryFromTable(nameOfTable, deviceKey, deviceValue)[0]
        else:
            device = super().getEntireTable(nameOfTable)
        return device

    def importDevicesFromCSVFile(self, file, overwriteIfDeviceExists):
        """
        Load users from csv file
        Format: 'surname;firstname;shortname;tagId
        File must contain the following header: inventoryNumber type manufacturer model
        :param file: csv file
        :param overwriteIfDeviceExists: if true existing devices are overwritten with new values from csv file
        """
        with open(file) as csvfile:
            numberOfDevicesInFile = 0
            numberOfDevicesImported = 0
            reader = csv.DictReader(csvfile, delimiter=';')

            for device in reader:
                numberOfDevicesInFile += 1
                if (overwriteIfDeviceExists == True):
                    numberOfDevicesImported += 1
                    self.removeDevice(device[deviceCharacteristics[0]])
                    self.addDeviceAsDict(device)
                else:
                    if(self.doesDeviceExist('inventoryNumber',device['inventoryNumber']) == False):
                        numberOfDevicesImported += 1
                        self.addDeviceAsDict(device)
        print(str(numberOfDevicesImported) +  ' of ' + str(numberOfDevicesInFile) + ' devices from file imported (' + str(numberOfDevicesInFile-numberOfDevicesImported) + ' already existed)')

    def exportDevicesToCSVFile(self):
        """Export devices to a csv file."""
        filename = os.path.join('export/','devicesExport_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=deviceCharacteristics, delimiter=';')
            headers = dict((n, n) for n in deviceCharacteristics)
            writer.writerow(headers)
            allDevices = self.getEntireTable(nameOfTable)
            for i in range(len(allDevices)):
                writer.writerow(allDevices[i])
        print('Devices exported to: ' + filename)
