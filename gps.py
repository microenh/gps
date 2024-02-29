from serial_base import SerialBase
from utility import grid_square, timefromgps, todec
from event import NotifyGUI
from settings import settings

class GPS(SerialBase):
    def __init__(self):
        super().__init__(settings.gps_port, 9600)

    def report_serial_open(self):
        self.push(NotifyGUI.GPS_OPEN)        

    def report_serial_close(self):
        self.push(NotifyGUI.GPS_CLOSE)        

    def process(self, data):
        a = data.strip().split(',')
        match a[0]:
            case '$GPGGA':
                time = timefromgps(a[1]).__str__()
                lat = todec(a[2],a[3])
                lon = todec(a[4],a[5])
                grid = grid_square(lon, lat)[:6]
                fix = int(a[6])
                sats = int(a[7])
                self.push(NotifyGUI.GPGGA, {'time': time,
                                            'grid': grid,
                                            'fix':  fix,
                                            'sats': sats})

if __name__ == '__main__':
    from main import main
    main()
