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

    STATE_ERROR = 6
    STATE_SUCCESS = 7


##########variable declaration################
loan_device = ''
loan_user = ''
errortype = ''
successtype = ''
user_id = ''
device_id = ''
scandone_status = ''
scandone_id = ''
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
    output8 = 0
    if channel == 13 and value == True:
        print('Enter')
    if channel == 8 and value == True and changed == True:
        print('D')


def scan_done(result, id):
    global scandone_status
    global scandone_id
    scandone_status = result
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

user.importUsersFromCSVFile('usersImport.csv', False) # import Userlist
device.importDevicesFromCSVFile('devicesImport.csv', False) # import Deviceslist

LCD_display.cleardisplay()
LCD_display.displaystart()

while (1):
    if state == ProgramState.STATE_START:
        scandone_id = ''
        scandone_status = ''
        if LCD_display.getbuttonpressed(0) == True:
            state = ProgramState.STATE_CHECKIN
            LCD_display.cleardisplay()
            LCD_display.displayscan()
            RFID_reader.start_scan()

        if LCD_display.getbuttonpressed(1) == True:
            state = ProgramState.STATE_CHECKOUT
            LCD_display.cleardisplay()
            LCD_display.displayscan()
            RFID_reader.start_scan()

    elif state == ProgramState.STATE_CHECKIN:
        if scandone_status == 'tag found':
            scandone_status = ''

            if loan.isDeviceCheckedOut(device.getDevice('tagId', scandone_id)['inventoryNumber']) == True:
                if user.doesUserExist('tagId', scandone_id) == True:
                    errortype = 'scan device not user'
                elif user.doesUserExist('tagId', scandone_id) == False and device.doesDeviceExist('tagId',
                                                                                                  scandone_id) == False:
                    errortype = 'unknown ID'
                else:
                    errortype = 'already checked in'

                state = ProgramState.STATE_ERROR


            else:
                #current_loan = loan.getLoan('inventoryNumber', device.getDevice('tagId', scandone_id)['inventoryNumber'])
                loan_user = user.getUser('shortname', loan.getLoan('inventoryNumber', device.getDevice('tagId', scandone_id)['inventoryNumber'])['shortname'])
                loan_device = device.getDevice('inventoryNumber', loan.getLoan('inventoryNumber', device.getDevice('tagId', scandone_id)['inventoryNumber'])[
                    'inventoryNumber'])
                loan.checkInOrCheckOutDevice(loan_device, loan_user)
                loan_device = ''
                loan_user = ''
                successtype = 'checked in'
                state = ProgramState.STATE_SUCCESS

    elif state == ProgramState.STATE_CHECKOUT:
        if scandone_status == 'tag found':
            scandone_status = ''
            if device.doesDeviceExist('tagId', scandone_id) == True:
                device_id = scandone_id
                print('deviceid: ' + device_id)
                LCD_display.cleardisplay()
                time.sleep(2)
                LCD_display.displayscan()
                RFID_reader.start_scan()
                state = ProgramState.STATE_WAITFORUSER

            elif user.doesUserExist('tagId', scandone_id) == True:
                user_id = scandone_id
                print('userid: ' + user_id)
                LCD_display.cleardisplay()
                time.sleep(2)
                LCD_display.displayscan()
                RFID_reader.start_scan()
                state = ProgramState.STATE_WAITFORDEVICE

            else:
                errortype = 'unknown ID'
                state = ProgramState.STATE_ERROR

    elif state == ProgramState.STATE_WAITFORDEVICE:
        if scandone_status == 'tag found':
            if loan.isDeviceCheckedOut(device.getDevice('tagId', scandone_id)) == True:
                errortype = 'already checked out'
                state = ProgramState.STATE_ERROR
            elif device.doesDeviceExist('tagId', scandone_id) == True:
                device_loan = device.getDevice('tagId', scandone_id)
                user_loan = user.getUser('tagId', user_id)
                loan.checkInOrCheckOutDevice(device_loan, user_loan)
                device_loan = ''
                user_loan = ''
                scandone_id = ''
                successtype = 'checked out'
                state = ProgramState.STATE_SUCCESS
            elif user.doesUserExist('tagId', scandone_id) == True:
                errortype = 'two user IDs'
                state = ProgramState.STATE_ERROR
            else:
                errortype = 'device does not exist'
                state = ProgramState.STATE_ERROR


    elif state == ProgramState.STATE_WAITFORUSER:
        if scandone_status == 'tag found':
            if loan.isDeviceCheckedOut(device.getDevice('tagId', device_id)) == True:
                errortype = 'already checked out'
                state = ProgramState.STATE_ERROR
            elif user.doesUserExist('tagId', scandone_id) == True:
                device_loan = device.getDevice('tagId', device_id)
                user_loan = user.getUser('tagId', scandone_id)
                loan.checkInOrCheckOutDevice(device_loan, user_loan)
                device_loan = ''
                user_loan = ''
                scandone_id = ''
                successtype = 'checked out'
                state = ProgramState.STATE_SUCCESS
            elif device.doesDeviceExist('tagId', scandone_id) == True:
                errortype = 'two device IDs'
                state = ProgramState.STATE_ERROR
            else:
                errortype = 'user does not exist'
                state = ProgramState.STATE_ERROR

    elif state == ProgramState.STATE_ERROR:
        LCD_display.cleardisplay()
        LCD_display.displayerror(errortype)
        errortype = ''
        time.sleep(2)
        LCD_display.cleardisplay()
        LCD_display.displaystart()
        state = ProgramState.STATE_START

    elif state == ProgramState.STATE_SUCCESS:
        LCD_display.cleardisplay()
        LCD_display.displaysuccess(successtype)
        successtype = ''
        time.sleep(2)
        LCD_display.cleardisplay()
        LCD_display.displaystart()
        state = ProgramState.STATE_START
