###############################################################################
# myDatabase.py
#
# Contacts: Manuel Weber
# DATE: 24.02.2020
###############################################################################

from tinydb import TinyDB, Query

class MyDatabase:

    def __init__(self, dbName):
        # create database object
        self.db = TinyDB(dbName + '.tinyDB')

    def createTable(self,*tableName):
        # get list of existing tables
        existingTables = self.db.tables()

        # iterate over tableName and create table if it does not exists yet
        for i in range(len(tableName)):
            if tableName[i] in existingTables:
                print('Table already exists:', tableName[i])
            else:
                print('Table created:', tableName[i])
                # create table
                self.db.table(tableName[i])

    def clearTablesContent(self, *tableName):
        # get list of existing tables
        existingTables = self.db.tables()

        # iterate over tableName and clear table if it exists
        for i in range(len(tableName)):
            if (tableName[i] in existingTables):
                self.db.purge_table(tableName[i])
                self.db.table(tableName[i])
                print('Table cleared:', tableName[i])
            else:
                print('Clear table failed - table does not exist:', tableName[i])

    def removeTables(self, *tableName):
        # get list of existing tables
        existingTables = self.db.tables()

        # iterate over tableName and remove table if it exists
        for i in range(len(tableName)):
            if (tableName[i] in existingTables):
                self.db.purge_table(tableName[i])
                print('Table removed:', tableName[i])
            else:
                print('Remove table failed - table does not exist:', tableName[i])

    def removeAllTables(self):
        self.db.purge_tables()
        print("All tables removed")

    def addEntryToTable(self, tableName, entry):

        # get list of existing tables
        existingTables = self.db.tables()

        if tableName in existingTables:
            self.db.table(tableName).insert(entry)
        else:
            print("Add entry failed - table does not exist")

    def removeEntryFromTable(self, tableName, keyName, keyValue):
        query = Query()
        return self.db.table(tableName).remove(query[keyName] == keyValue)

    def getEntryFromTable(self, tableName, key, value):
        query = Query()
        return self.db.table(tableName).search(query[key] == value)

    def doesEntryExistInTable(self, tableName, key, value):
        query = Query()
        return self.db.table(tableName).contains(query[key] == value)

    def updateValueOfKey(self, tableName, keyFilter, valueFiler, keyUpdate, valueUpdate):
        query = Query()
        return self.db.table(tableName).update({keyUpdate: valueUpdate}, query[keyFilter] == valueFiler)

    def getEntireTable(self, tableName):
        return self.db.table(tableName).all()
