 ###############################################################################
# rfidreader.py
#
# Contacts: Mathis Kündig
# DATE: April 2020
###############################################################################

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc import BrickletNFC

class RFIDReader:

    def __init__ (self,UID_RFID,ipcon: IPConnection, cb_tag_scan_done):
        self.reader = BrickletNFC(UID_RFID, ipcon)
        self.cb_tag_scan_done = cb_tag_scan_done
        self.reader.register_callback(self.reader.CALLBACK_READER_STATE_CHANGED,
                              lambda x, y: self.cb_reader_state_changed(x, y, self.reader))

    def cb_reader_state_changed(self, state, idle, nfc):
        if state == nfc.READER_STATE_IDLE:
            nfc.reader_request_tag_id()
        elif state == nfc.READER_STATE_REQUEST_TAG_ID_READY:
            ret = nfc.reader_get_tag_id()
            self.cb_tag_scan_done('tag found',str(ret.tag_id))
        elif state == nfc.READER_STATE_REQUEST_TAG_ID_ERROR:
            self.cb_tag_scan_done('tag error', 0)

    def start_scan(self):
        print('scan started')
        self.reader.set_mode(self.reader.MODE_READER)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HOST = "localhost"
# PORT = 4223
# UID = "LB7" # Change XYZ to the UID of your NFC Bricklet
#
# from tinkerforge.ip_connection import IPConnection
# from tinkerforge.bricklet_nfc import BrickletNFC
#
# # Callback function for reader state changed callback
# def cb_reader_state_changed(state, idle, nfc):
#     if state == nfc.READER_STATE_IDLE:
#         nfc.reader_request_tag_id()
#     elif state == nfc.READER_STATE_REQUEST_TAG_ID_READY:
#         ret = nfc.reader_get_tag_id()
#
#         print("Found tag of type " +
#               str(ret.tag_type) +
#               " with ID [" +
#               " ".join(map(str, map(hex, ret.tag_id))) +
#               "]")
#
#     elif state == nfc.READER_STATE_REQUEST_TAG_ID_ERROR:
#         print("Request tag ID error")
#
# if __name__ == "__main__":
#     ipcon = IPConnection() # Create IP connection
#     nfc = BrickletNFC(UID, ipcon) # Create device object
#
#     ipcon.connect(HOST, PORT) # Connect to brickd
#     # Don't use device before ipcon is connected
#
#     # Register reader state changed callback to function cb_reader_state_changed
#     nfc.register_callback(nfc.CALLBACK_READER_STATE_CHANGED,
#                           lambda x, y: cb_reader_state_changed(x, y, nfc))
#
#     # Enable reader mode
#     nfc.set_mode(nfc.MODE_READER)
#
#     input("Press key to exit\n") # Use raw_input() in Python 2
#     ipcon.disconnect()
