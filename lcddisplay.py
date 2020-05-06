###############################################################################
# Temp_Measure.py
#
# Contacts: Mathis Kündig
# DATE: April 2020
###############################################################################

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from users import Users
user = Users()
userlist = user.getUser()



class LCDDisplay:

    def __init__(self, UID_LCD, UID_PIEZO, ipcon: IPConnection):  # init function
        self.display = BrickletLCD128x64(UID_LCD, ipcon)
        self.sound = BrickletPiezoSpeakerV2(UID_PIEZO, ipcon)

    def getbuttonpressed(self, index):  # function to get if button is pressed
        index = self.display.get_gui_button_pressed(index)
        return index

    def displaystart(self):  # function to display home screen
        self.display.write_line(0, 0, "Check-out Station")
        self.display.set_gui_button(1, 0, 12, 64, 26, "Check-out")
        self.display.set_gui_button(0, 64, 12, 64, 26, "Check-in")
        self.display.set_gui_button(2, 0, 38, 64, 26, "assign ID")

    def displayerror(self, errortype):  # function to display error screen
        self.display.write_line(2, 1, "error: ")
        self.display.write_line(4, 1, errortype)
        self.sound.set_beep(100, 3, 500)


    def displaysuccess(self, successtype):  # function to display success screen
        self.display.write_line(2, 1, "success: ")
        self.display.write_line(4, 1, successtype)
        self.sound.set_beep(500, 3, 500)

    def displayscan(self):  # function to display scan screen
        self.display.write_line(2, 2, "scan ID...")


    def cleardisplay(self):  # function to clear display
        self.display.clear_display()
        self.display.remove_gui_button(255)

    def displayassign(self):  # function to display assign screen
        self.display.write_line(0, 0, "Assign ID to...")
        self.display.set_gui_button(4, 0, 12, 64, 26, "user")

    def displayshortnamelist(self, scroll):  # function to display shortname list
        userlist[0]['shortname']
        self.display.set_gui_button(5, 110, 0, 18, 32, 'u')
        self.display.set_gui_button(6, 110, 32, 18, 32, 'd')
        self.display.write_line(0, 0, 'choose your short')
        self.display.write_line((2), 0, userlist[scroll]['shortname'] + '   choose this')
        if scroll <= (len(user.getUser())-2):
            self.display.write_line((3), 0, userlist[scroll + 1]['shortname'])
        if scroll <= (len(user.getUser())-3):
            self.display.write_line((4), 0, userlist[scroll + 2]['shortname'])
        if scroll <= (len(user.getUser())-4):
            self.display.write_line((5), 0, userlist[scroll + 3]['shortname'])
        if scroll <= (len(user.getUser())-5):
            self.display.write_line((6), 0, userlist[scroll + 4]['shortname'])
        if scroll <= (len(user.getUser())-6):
            self.display.write_line((7), 0, userlist[scroll + 5]['shortname'])

        return userlist[scroll]['shortname']


