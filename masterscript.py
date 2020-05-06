###############################################################################
# Temp_Measure.py
#
# Contacts: Mathis Kündig
# DATE: April 2020
###############################################################################
######initialize files & packages#############
from devices import Devices
from loans import Loans
from users import Users
import io16
import rfidreader
import lcddisplay
import time
from tinkerforge.ip_connection import IPConnection
from enum import Enum, unique
##############################################

@unique
class ProgramState(Enum):
    STATE_START = 0  # auto()
    STATE_CHECKIN = 1  # auto()
    STATE_CHECKOUT = 2  # auto()
    STATE_WAITFORDEVICE = 3
    STATE_WAITFORUSER = 4
    STATE_ASSIGNID = 5
    STATE_SCANASSIGNID = 6
    STATE_ASSIGNUSERID = 7
    STATE_ERROR = 8
    STATE_SUCCESS = 9


##########variable declaration################
scroll = 0
loan_device = ''
loan_user = ''
errortype = ''
successtype = ''
user_id = ''
device_id = ''
scandone_status = ''
scandone_id = ''
new_ID = ''
button_pushed = ''
state = ProgramState.STATE_START
###############################################


HOST = 'localhost'
PORT = 4223

ipcon = IPConnection()  # Create IP connection
ipcon.connect(HOST, PORT)  # Connect to brick

UID_RFID = 'LB7'
UID_IO16 = '2p8Rx4'
UID_LCD = 'MWz'
UID_PIEZO = '284og6'

device = Devices()
user = Users()
loan = Loans(user, device)


##########callback functions###################
def button_pressed(channel, changed, value):
    global button_pushed
    output8 = 0
    if channel == 13 and value == True:
        button_pushed = 'Enter'
    if channel == 8 and value == True and changed == True:
        print('D')
    if channel == 2 and value == True and changed == True:
        button_pushed = 'Delete'


def scan_done(result, id):
    global scandone_status
    global scandone_id
    scandone_status = result
    scandone_id = id
    if result == 'tag found':
        print('tag found: ' + id)
        scandone_id = id
    elif result == 'tag error':
        print('tag not found')
        RFID_reader.start_scan()
###############################################

LCD_display = lcddisplay.LCDDisplay(UID_LCD, UID_PIEZO, ipcon)  # Create device object
io16 = io16.Io16(UID_IO16, ipcon, button_pressed)  # Create device object
RFID_reader = rfidreader.RFIDReader(UID_RFID, ipcon, scan_done)  # Create device object

user.importUsersFromCSVFile('usersImport.csv', False)  # import Userlist
device.importDevicesFromCSVFile('devicesImport.csv', False)  # import Deviceslist

LCD_display.cleardisplay()  # clear display
LCD_display.displaystart()  # display home screen

while (1):
    if state == ProgramState.STATE_START:
        scandone_id = ''
        scandone_status = ''
        if LCD_display.getbuttonpressed(0) == True:
            state = ProgramState.STATE_CHECKIN
            LCD_display.cleardisplay()  # clear display
            LCD_display.displayscan()
            RFID_reader.start_scan()

        if LCD_display.getbuttonpressed(1) == True:
            state = ProgramState.STATE_CHECKOUT
            LCD_display.cleardisplay()  # clear display
            LCD_display.displayscan()
            RFID_reader.start_scan()

        if LCD_display.getbuttonpressed(2) == True:
            state = ProgramState.STATE_ASSIGNID
            LCD_display.cleardisplay()  # clear display
            LCD_display.displayassign()


    elif state == ProgramState.STATE_CHECKIN:
        if scandone_status == 'tag found':
            scandone_status = ''  # reset variable
            if user.doesUserExist('tagId', scandone_id) == False and device.doesDeviceExist('tagId', scandone_id) == False:
                errortype = 'unknown ID'
                state = ProgramState.STATE_ERROR
            elif user.doesUserExist('tagId', scandone_id) == True:
                errortype = 'scan device not user'
                state = ProgramState.STATE_ERROR
            elif loan.isDeviceCheckedOut(device.getDevice('tagId', scandone_id)['inventoryNumber']) == False:
                errortype = 'already checked in'
                state = ProgramState.STATE_ERROR
            else:
                current_loan = loan.getLoan('inventoryNumber',
                                            device.getDevice('tagId', scandone_id)['inventoryNumber'])
                loan_user = user.getUser('shortname', loan.getLoan('inventoryNumber', (
                device.getDevice('tagId', scandone_id)['inventoryNumber']))['shortname'])
                loan_device = device.getDevice('inventoryNumber', loan.getLoan('inventoryNumber', device.getDevice('tagId', scandone_id)['inventoryNumber'])[
                    'inventoryNumber'])
                loan.checkInOrCheckOutDevice(loan_device, loan_user)
                loan_device = ''  # reset variable
                loan_user = ''  # reset variable
                scandone_id = ''
                successtype = 'checked in'
                state = ProgramState.STATE_SUCCESS

    elif state == ProgramState.STATE_CHECKOUT:
        if scandone_status == 'tag found':
            scandone_status = ''
            print('scandone_id:' + scandone_id)
            if scandone_id == '':
                x = 1
            elif user.doesUserExist('tagId', scandone_id) == False and device.doesDeviceExist('tagId', scandone_id) == False:
                errortype = 'unknown ID'
                state = ProgramState.STATE_ERROR
            elif user.doesUserExist('tagId', scandone_id) == True:
                user_id = scandone_id
                scandone_id = ''  # reset variable
                LCD_display.cleardisplay()
                time.sleep(2)
                LCD_display.displayscan()
                RFID_reader.start_scan()
                state = ProgramState.STATE_WAITFORDEVICE
            elif device.doesDeviceExist('tagId', scandone_id) == True:
                device_id = scandone_id
                scandone_id = ''  # reset variable
                LCD_display.cleardisplay()
                time.sleep(2)
                LCD_display.displayscan()
                RFID_reader.start_scan()
                state = ProgramState.STATE_WAITFORUSER
            else:
                errortype = 'unknown ID'
                state = ProgramState.STATE_ERROR

    elif state == ProgramState.STATE_WAITFORDEVICE:
        if scandone_status == 'tag found':
            scandone_status = ''
            print(str(device.getDevice('tagId', scandone_id)))
            if user.doesUserExist('tagId', scandone_id) == True:
                errortype = 'two user IDs'
                state = ProgramState.STATE_ERROR
            elif device.doesDeviceExist('tagId', scandone_id) == False:
                errortype = 'unknown ID'
                state = ProgramState.STATE_ERROR
            elif loan.isDeviceCheckedOut(device.getDevice('tagId', scandone_id)['inventoryNumber']) == True:
                errortype = 'already checked out'
                state = ProgramState.STATE_ERROR
            elif device.doesDeviceExist('tagId', scandone_id) == True:
                device_loan = device.getDevice('tagId', scandone_id)
                user_loan = user.getUser('tagId', user_id)
                loan.checkInOrCheckOutDevice(device_loan, user_loan)
                device_loan = ''  # reset variable
                user_loan = ''  # reset variable
                user_id = ''
                scandone_id = ''  # reset variable
                successtype = 'checked out'
                state = ProgramState.STATE_SUCCESS
            else:
                errortype = 'device does not exist'
                state = ProgramState.STATE_ERROR


    elif state == ProgramState.STATE_WAITFORUSER:
        if scandone_status == 'tag found':
            scandone_status = ''
            if device.doesDeviceExist('tagId', scandone_id) == True:
                errortype = 'two device IDs'
                state = ProgramState.STATE_ERROR
            elif user.doesUserExist('tagId', scandone_id) == False:
                errortype = 'unknown ID'
                state = ProgramState.STATE_ERROR
            elif loan.isDeviceCheckedOut(device.getDevice('tagId', device_id)['inventoryNumber']) == True:
                errortype = 'already checked out'
                state = ProgramState.STATE_ERROR
            elif user.doesUserExist('tagId', scandone_id) == True:
                device_loan = device.getDevice('tagId', device_id)
                user_loan = user.getUser('tagId', scandone_id)
                loan.checkInOrCheckOutDevice(device_loan, user_loan)
                device_loan = ''  # reset variable
                user_loan = ''  # reset variable
                device_id = ''
                scandone_id = ''  # reset variable
                successtype = 'checked out'
                state = ProgramState.STATE_SUCCESS
            else:
                errortype = 'user does not exist'
                state = ProgramState.STATE_ERROR

    elif state == ProgramState.STATE_ASSIGNID:
        if LCD_display.getbuttonpressed(4) == True:
            state = ProgramState.STATE_SCANASSIGNID
            LCD_display.cleardisplay()
            LCD_display.displayscan()
            RFID_reader.start_scan()

    elif state == ProgramState.STATE_SCANASSIGNID:
        #scandone_id = ''
        if scandone_status == 'tag found':
            scandone_status = ''
            new_ID = scandone_id
            scandone_id = ''  # reset variable
            if user.doesUserExist('tagId', new_ID) == True or device.doesDeviceExist('tagId', new_ID) == True:
                errortype = 'ID already used'
                state = ProgramState.STATE_ERROR
            else:
                LCD_display.cleardisplay()
                LCD_display.displayshortnamelist(0)
                button_pushed = ''  # reset variable
                state = ProgramState.STATE_ASSIGNUSERID

    elif state == ProgramState.STATE_ASSIGNUSERID:
        if LCD_display.getbuttonpressed(5):
            if scroll >= 1:
                scroll -= 1
                LCD_display.cleardisplay()
                LCD_display.displayshortnamelist(scroll)
                time.sleep(0.5)
        elif LCD_display.getbuttonpressed(6):
            if scroll <= (len(user.getUser())-2):
                scroll += 1
                LCD_display.cleardisplay()
                LCD_display.displayshortnamelist(scroll)
                time.sleep(0.5)
        elif button_pushed == 'Enter':
            user_chosen = LCD_display.displayshortnamelist(scroll)
            successtype = 'ID assigned to ' + str(LCD_display.displayshortnamelist(scroll))
            user.changeValueTagIdOfUser(LCD_display.displayshortnamelist(scroll), new_ID)
            new_ID = ''  # reset variable
            scroll = ''  # reset variable
            state = ProgramState.STATE_SUCCESS
        elif button_pushed == 'Delete':
            errortype = 'exited'
            state = ProgramState.STATE_ERROR

    elif state == ProgramState.STATE_ERROR:
        LCD_display.cleardisplay()
        LCD_display.displayerror(errortype)
        errortype = ''  # reset variable
        scandone_id = ''
        time.sleep(2)
        LCD_display.cleardisplay()
        LCD_display.displaystart()
        state = ProgramState.STATE_START

    elif state == ProgramState.STATE_SUCCESS:
        LCD_display.cleardisplay()
        LCD_display.displaysuccess(successtype)
        successtype = ''  # reset variable
        scandone_id = ''
        time.sleep(2)
        LCD_display.cleardisplay()
        LCD_display.displaystart()
        state = ProgramState.STATE_START
