###############################################################################
# Temp_Measure.py
#
# Contacts: Mathis Kündig
# DATE: Juni 2019
###############################################################################

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2




class LCDDisplay:

    def __init__(self, UID_LCD, UID_PIEZO, ipcon: IPConnection):
        self.display = BrickletLCD128x64(UID_LCD, ipcon)
        self.sound = BrickletPiezoSpeakerV2(UID_PIEZO, ipcon)

    def WriteTextToPosition(self, line, position, text):
        self.display.write_line(line, position, text)

    def ClearDisplay(self):
        self.display.clear_display()
        self.display.remove_gui_button(255)

    def gettouch(self):
        print(self.display.get_touch_gesture())

    def setbutton(self, index, position_x, position_y, width, height, text):
        self.display.set_gui_button(index, position_x, position_y, width, height, text)

    def getbuttonpressed(self, index):
        self.display.get_gui_button_pressed(index)
        print(self.display.get_gui_button_pressed(index)())

    def getbutton(self, index):
        self.display.get_gui_button(index)

    def removebutton(self, index):
        self.display.remove_gui_button(index)

    def displaystart(self):
        self.display.clear_display()
        self.display.remove_gui_button(255)
        self.display.write_line(0, 0, "Check-out Station")
        self.display.set_gui_button(0, 0, 12, 64, 26, "Check-in")
        self.display.set_gui_button(1, 64, 12, 64, 26, "Check-out")
        self.display.set_gui_button(2, 0, 38, 64, 26, "assign ID")
        self.display.set_gui_button(3, 64, 38, 64, 26, "loan state")

    def displayerror(self, errortype):
        self.display.write_line(2, 3, "error: " + errortype)
        #self.sound.set_beep(100, 5, 500)


    def displaysuccess(self):
        self.display.write_line(2, 3, "success")
        #self.sound.set_beep(500, 5, 500)

    def displayscan(self):
        self.display.write_line(2, 3, "scan ID")


    def cleardisplay(self):
        self.display.clear_display()
        self.display.remove_gui_button(255)

