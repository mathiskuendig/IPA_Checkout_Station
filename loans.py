###############################################################################
# loans.py
#
# Contacts: Manuel Weber
# DATE: 27.02.2020
###############################################################################

from datetime import datetime
from myDatabase import MyDatabase
#from logger import Logger

nameOfDatabase = 'loans'  # Specify name of database file
nameOfTable = 'loans'  # Specify name of table
userCharacteristics = ('shortname', 'inventoryNumber', 'status', 'timestamp')  # 'checked out' or 'available'


class Loans(MyDatabase):
    """ A class implementing a loan database with the following attributes:
        - Shortname
        - InventoryNumber
        - Status
        - Timestamp
        """
    def __init__(self, users, devices):
        #self.loggerInstance = Logger(__name__)
        super().__init__(nameOfDatabase)  # call parent's init function
        super().createTable(nameOfTable)  # create table in database

    def doesLoanExist(self, loanKey, loanValue):
        """Returns true if loan exists otherwise false."""
        loanExists = False
        if super().doesEntryExistInTable(nameOfTable, loanKey, str(loanValue)) == True:
            loanExists = True
        return loanExists

    def checkInOrCheckOutDevice(self, device, user):
        if not super().doesEntryExistInTable(nameOfTable, 'inventoryNumber', device['inventoryNumber']):
            # device does not yet exist in table, check out device
            super().addEntryToTable(nameOfTable,
                                    {'inventoryNumber': device['inventoryNumber'], 'shortname': user['shortname'],
                                     'status': 'checked out',
                                     'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S')})
            return 'DEVICE CHECKED OUT'
        else:
            loan = super().getEntryFromTable(nameOfTable, 'inventoryNumber', device['inventoryNumber'])[0]
            if loan['status'] == 'checked out':
                super().removeEntryFromTable(nameOfTable, 'inventoryNumber', device['inventoryNumber'])
                super().addEntryToTable(nameOfTable,
                                        {'inventoryNumber': device['inventoryNumber'], 'shortname': user['shortname'],
                                         'status': 'available',
                                         'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S')})
                return 'DEVICE CHECKED IN'
            else:
                super().removeEntryFromTable(nameOfTable, 'inventoryNumber', device['inventoryNumber'])
                super().addEntryToTable(nameOfTable,
                                        {'inventoryNumber': device['inventoryNumber'], 'shortname': user['shortname'],
                                         'status': 'checked out',
                                         'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S')})
                return 'DEVICE CHECKED OUT'

    def getLoan(self, loanKey="", loanValue=""):
        loan = {}
        if loanKey != "":
            # check if loan exists
            if self.doesLoanExist(loanKey, str(loanValue)):
                # return only first element of entry because we expect that every loan just exists once
                loan = super().getEntryFromTable(nameOfTable, loanKey, str(loanValue))[0]
        else:
            loan = super().getEntireTable(nameOfTable)

        return loan

    def isDeviceCheckedOut(self, inventoryNumber):
        device_is_checked_out = False
        if self.doesLoanExist('inventoryNumber', inventoryNumber):
            loan = self.getLoan('inventoryNumber', inventoryNumber)
            print(loan)
            if loan['status'] == 'checked out':
                device_is_checked_out = True
        return device_is_checked_out
