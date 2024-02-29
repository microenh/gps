from enum import Enum, auto

class NotifyGUI(Enum):
    QUIT=auto()
    
    GPS_OPEN=auto()
    GPS_CLOSE=auto()
    GPGGA=auto()
    
    FC_OPEN=auto()
    FC_CLOSE=auto()
    FC_ROTATE=auto()

