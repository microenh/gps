from serial_base import SerialBase

from event import NotifyGUI
from settings import settings

# Sending from FlexControl to host:
# All commands terminate with ';' (no returns or line feeds)
# U; - knob CW (single tick) -- U02; U03; U04; etc - multiticks
# D; - knob CCW (single tick) -- D02; D03; D04; etc - multiticks
# S; - short press, main knob
# L; - long press, main knob
# C; - fast double click, main knob

# The fast knob codes reflect multiple encoder ticks between USB polling times,
# so the knob should be able to keep track of fast spinning.

# XnS; - normal press, key n=1,2,3
# XnL; - long press
# XnC; - fast double click
# e.g. 
#    U; (frequency up one tick)
#    X2S; (normal press, button 2)

# Sending from host to FlexControl:
# Ixyz;  where x,y,z = 1 or 0 for LED 0, 1, 2 on or off
# e.g.
#    I001; set right hand LED on
#    I000; set all LEDs off
#    I111; set all LEDs on

class FlexControl(SerialBase):
    def __init__(self):
        super().__init__(settings.flex_port, 9600, b';')

    def report_serial_open(self):
        self.push(NotifyGUI.FC_OPEN)        

    def report_serial_close(self):
        self.push(NotifyGUI.FC_CLOSE)        

    def process(self, data):
        if data == 'S':
            self.push(NotifyGUI.QUIT)
        else:
            self.push(NotifyGUI.FC_ROTATE, data)

