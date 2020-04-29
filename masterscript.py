from devices import Devices
from loans import Loans
from users import Users
import io16
import rfidreader
import lcddisplay
import time
from tinkerforge.ip_connection import IPConnection
from enum import Enum, unique


@unique
class ProgramState(Enum):
    STATE_START = 0  # auto()
    STATE_CHECKINSCAN = 1  # auto()
    STATE_CHECKEDINSCANNED = 2  # auto()


##########variable declaratiobn################


state = ProgramState.STATE_START
###############################################


HOST = 'localhost'
PORT = 4223

ipcon = IPConnection()  # Create IP connection
ipcon.connect(HOST, PORT)  # Connect to brick

UID_RFID = 'LB7'
UID_IO16 = '2p8Rx4'
UID_LCD = 'MXY'
UID_PIEZO = '284og6'

device = Devices()
user = Users()
loan = Loans(user, device)


def button_pressed(channel, changed, value):
    output8 = 0
    if channel == 13 and value == True:
        print("Enter")
    if channel == 8 and value == True and changed == True:
        print("D")


def scan_done(result, id):
    if result == 'tag found':
        print('tag found: ' + id)
    elif result == 'tag error':
        print('tag not found')
        RFID_reader.start_scan()


LCD_display = lcddisplay.LCDDisplay(UID_LCD, UID_PIEZO, ipcon)  # Create device object
io16 = io16.Io16(UID_IO16, ipcon, button_pressed)  # Create device object
RFID_reader = rfidreader.RFIDReader(UID_RFID, ipcon, scan_done)  # Create device object

# RFID_reader.start_scan()

# user.importUsersFromCSVFile('usersImport.csv', False)
# userforloan = (user.getUser('shortname', 'kuma'))
# strshortname = str(userforloan['shortname'])

# LCD_display.displaystart()
# time.sleep(1)
# LCD_display.displayerror("errortype")
# time.sleep(1)
# LCD_display.displaysuccess()

LCD_display.cleardisplay()
LCD_display.displaystart()
while (1):
    if state == ProgramState.STATE_START:
        #LCD_display.displaystart()
        x = 1


