 ###############################################################################
# rfidreader.py
#
# Contacts: Mathis Kündig
# DATE: April 2020
###############################################################################

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc import BrickletNFC

class RFIDReader:

    def __init__ (self,UID_RFID,ipcon: IPConnection, cb_tag_scan_done):  # init function with callback for ID
        self.reader = BrickletNFC(UID_RFID, ipcon)
        self.cb_tag_scan_done = cb_tag_scan_done
        self.reader.register_callback(self.reader.CALLBACK_READER_STATE_CHANGED,
                              lambda x, y: self.cb_reader_state_changed(x, y, self.reader))

    def cb_reader_state_changed(self, state, idle, nfc):  # callback function if a tag was found
        if state == nfc.READER_STATE_IDLE:
            nfc.reader_request_tag_id()
        elif state == nfc.READER_STATE_REQUEST_TAG_ID_READY:
            ret = nfc.reader_get_tag_id()
            self.cb_tag_scan_done('tag found',str(ret.tag_id))
        elif state == nfc.READER_STATE_REQUEST_TAG_ID_ERROR:
            self.cb_tag_scan_done('tag error', 0)

    def start_scan(self):  # function that starts scan
        print('scan started')
        self.reader.set_mode(self.reader.MODE_READER)
