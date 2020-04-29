###############################################################################
# users.py
#
# Contacts: Manuel Weber
# DATE: 24.02.2020
###############################################################################

import csv
import os
from datetime import datetime
#from logger import Logger
from myDatabase import MyDatabase

nameOfDatabase = 'user'  # Specify name of database file
nameOfTable = 'user'  # Specify name of table
userCharacteristics = ('surname', 'firstname', 'shortname', 'tagId')


class Users(MyDatabase):
    """ A class implementing a user database with the following attributes:
        - Surname
        - Firstname
        - Shortname
        - TagId
        """

    def __init__(self):

        super().__init__(nameOfDatabase)  # call parent's init function
        super().createTable(nameOfTable)  # create table in database

        #self.loggerInstance = Logger(__name__)

    def doesUserExist(self, userKey, userValue):
        """Returns true if user exists otherwise false."""
        userExists = False
        if super().doesEntryExistInTable(nameOfTable, userKey, userValue):
            userExists = True
        return userExists

    def addUser(self, surname, firstname, shortname, tagId):
        """Add user and return true if successful otherwise false."""
        userCreated = False
        # check if user already exists
        if self.doesUserExist('shortname', shortname):
            # user already exists
            print('AddUser failed: ' + shortname)
        else:
            # create new user
            super().addEntryToTable(nameOfTable,
                                    {userCharacteristics[0]: surname,
                                     userCharacteristics[1]: firstname,
                                     userCharacteristics[2]: shortname,
                                     userCharacteristics[3]: tagId})
            userCreated = True
            print('AddUser done: ' + shortname)

        return userCreated

    def addUserAsDict(self, userAsDict):
        """Add user and return true if successful otherwise false."""
        userCreated = False
        # check if user already exists
        if (self.doesUserExist('shortname', userAsDict['shortname']) == False):
            # create new user
            super().addEntryToTable(nameOfTable, userAsDict)
            userCreated = True
        return userCreated

    def removeUser(self, shortname):
        """Remove user and return true if successful otherwise false."""
        userRemoved = False
        # check if user exists
        if (self.doesUserExist('shortname', shortname) == True):
            # remove user
            super().removeEntryFromTable(nameOfTable, userCharacteristics[2], shortname)
        return userRemoved

    def getUser(self, userKey="", userValue=""):
        """Returns user as dict."""
        user = {}
        if (userKey != ""):
            # check if user exists
            if (self.doesUserExist(userKey, userValue) == True):
                # return only first element of entry because we expect that every user just exists once
                user = super().getEntryFromTable(nameOfTable, userKey, userValue)[0]
        else:
            user = super().getEntireTable(nameOfTable)
        return user

    def changeValueTagIdOfUser(self, shortname, tadId):
        """Change tagId of user and return true if successful otherwise false."""
        if (super().updateValueOfKey(nameOfTable, userCharacteristics[2], shortname, userCharacteristics[3], tadId)):
            # change tag of user
            print('UpdateTagId done: ' + shortname)
        else:
            # user does not exist
            print('UpdateTagId failed: ' + shortname)

    def importUsersFromCSVFile(self, file, overwriteIfUserExists):
        """
        Load users from csv file
        Format: 'surname;firstname;shortname;tagId
        File must contain the following header: surname firstname shortname tagId
        :param file: csv file
        :param overwriteIfUserExists: if true existing users are overwritten with new values from csv file
        """

        with open(file) as csvfile:
            numberOfUsersInFile = 0
            numberOfUsersImported = 0
            reader = csv.DictReader(csvfile, delimiter=';')

            for user in reader:
                numberOfUsersInFile += 1
                if (overwriteIfUserExists == True):
                    numberOfUsersImported += 1
                    self.removeUser(user[userCharacteristics[2]])
                    self.addUserAsDict(user)
                else:
                    if (self.doesUserExist('shortname', user['shortname']) == False):
                        numberOfUsersImported += 1
                        self.addUserAsDict(user)
        print(str(numberOfUsersImported) + ' of ' + str(numberOfUsersInFile) + ' users from file imported (' + str(
            numberOfUsersInFile - numberOfUsersImported) + ' already existed)')

    def exportUsersToCSVFile(self):
        """Export users to a csv file."""
        filename = os.path.join('export/', 'usersExport_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=userCharacteristics, delimiter=';')
            headers = dict((n, n) for n in userCharacteristics)
            writer.writerow(headers)
            allUsers = self.getEntireTable(nameOfTable)
            for i in range(len(allUsers)):
                writer.writerow(allUsers[i])
        print('Users exported to: ' + filename)
