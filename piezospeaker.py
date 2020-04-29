###############################################################################
# piezospeaker.py
#
# Contacts: Mathis Kündig
# DATE: Juni 2019
###############################################################################


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2


class PiezoSpeaker:

    def __init__(self, UID_PIEZO, ipcon: IPConnection):
        self.display = BrickletPiezoSpeakerV2(UID_PIEZO, ipcon)


    def errorsound(self):
        self.sound.set_beep(100, 5, 1000)
        self.sound.set_beep(100, 5, 1000)

    def successsound(self):
        self.sound.set_beep(500, 5, 1000)