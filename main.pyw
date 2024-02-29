#! .venv/scripts/pythonw.exe
from gui import Gui
from gps import GPS
from flexcontrol import FlexControl

def main():
    gps = GPS()
    flex = FlexControl()
    
    gps.start()
    flex.start()
    Gui().start(gps, flex)
    
    gps.stop()
    flex.stop()
        
if __name__ == '__main__':
    main()
 
