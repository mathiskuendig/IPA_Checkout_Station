 ###############################################################################
# io16.py
#
# Contacts: Mathis Kündig
# DATE: April 2020
###############################################################################


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_io16_v2 import BrickletIO16V2

class Io16:

    button_pressed_time = 500

    def __init__ (self, UID_IO16, ipcon: IPConnection, cb_button_pressed):
        self.button = BrickletIO16V2(UID_IO16, ipcon)
        self.cb_button_pressed = cb_button_pressed
        self.button.register_callback(self.button.CALLBACK_INPUT_VALUE, cb_button_pressed)
        self.button.set_input_value_callback_configuration(8, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(9, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(10, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(11, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(12, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(13, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(14, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(15, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(1, self.button_pressed_time, False)
        self.button.set_input_value_callback_configuration(2, self.button_pressed_time, False)
        self.button_pressed_time


    #def cb_input_value(channel, changed, value):
