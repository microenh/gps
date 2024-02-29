#! C:\Users\mark\Developer\Python\gps\.venv\scripts\pythonw.exe
import os
import tkinter as tk
from tkinter import scrolledtext, ttk

from darkdetect import isDark
from PIL import Image, ImageTk
from settings import settings

from event import NotifyGUI
from manager import manager

class Gui(tk.Tk):
    """Main class more"""
    LOGO = os.path.join(os.path.dirname(__file__), "Logo.png")
    ICON = os.path.join(os.path.dirname(__file__), "Icon.ico")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screenName = ':0.0'
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.bind((n := '<<gui>>'), self.do_notify)
        manager.event_generate = lambda: self.event_generate(n, when="tail")
        self.setup_variables()
        self.setup_theme()
        self.layout()
        self.hb = True

    def setup_variables(self):
        self.fix = tk.StringVar()
        self.grid = tk.StringVar()
        self.time = tk.StringVar()
        self.sats = tk.StringVar()
        self.flex = tk.StringVar()
        

    def setup_theme(self):
        self.style = ttk.Style(self)
        self.last_dark = None
        # Import the tcl files
        self.tk.call('source', 'forest-dark.tcl')
        self.tk.call('source', 'forest-light.tcl')
        # Set the theme with the theme to match the system theme
        self.check_dark()

    def layout(self):
        self.resizable(False, False)
        self.title('GPS')
        self.image = ImageTk.PhotoImage(Image.open(self.LOGO))
        self.icon = ImageTk.PhotoImage(Image.open(self.ICON))
        self.iconphoto(False, self.icon)
        
        # self.after_idle(lambda: self.eval('tk::PlaceWindow . center'))
        
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='y')
        ttk.Label(main_frame, image=self.image).pack()

        self.gps_button = ttk.Button(main_frame, command=self.startGPS)
        self.gps_button.pack(padx=10)
        
        bg = ttk.Frame(main_frame)
        bg.pack(padx=10, fill='x')
        ttk.Label(bg, text='FIX:').pack(side='left')
        ttk.Label(bg, textvariable=self.fix).pack(side='left', padx=(10,0))
        
        bg = ttk.Frame(main_frame)
        bg.pack(padx=10, fill='x')
        ttk.Label(bg, text='GRID:').pack(side='left')
        ttk.Label(bg, textvariable=self.grid).pack(side='left', padx=(10,0))

        bg = ttk.Frame(main_frame)
        bg.pack(padx=10, fill='x')
        ttk.Label(bg, text='TIME:').pack(side='left')
        ttk.Label(bg, textvariable=self.time).pack(side='left', padx=(10,0))

        bg = ttk.Frame(main_frame)
        bg.pack(padx=10, fill='x')
        ttk.Label(bg, text='SATS:').pack(side='left')
        ttk.Label(bg, textvariable=self.sats).pack(side='left', padx=(10,0))

        bg = ttk.Frame(main_frame)
        bg.pack(padx=10, pady=(0,10), fill='x')
        ttk.Label(bg, text='FlexControl:').pack(side='left')
        ttk.Label(bg, textvariable=self.flex).pack(side='left', padx=(10,0))
        
    def do_notify(self, _):
        while (data := manager.pop()) is not None:
            id_, d = data
            match id_:
                case NotifyGUI.QUIT:
                    self.quit()
                case NotifyGUI.GPS_OPEN:
                    self.gps_button.config(state='disabled')
                case NotifyGUI.GPS_CLOSE:
                    self.gps_button.config(state='normal', text='OPEN GPS')
                    self.fix.set('')
                    self.grid.set('')
                    self.time.set('')
                    self.sats.set('')
                case NotifyGUI.GPGGA:
                    self.gps_button.config(text = 'GPS' if self.hb else '')
                    self.hb = not self.hb
                    self.fix.set(d.get('fix', ''))
                    self.grid.set(d.get('grid',''))
                    self.time.set(d.get('time',''))
                    self.sats.set(d.get('sats',''))
                case NotifyGUI.FC_ROTATE:
                    self.flex.set(d)

    def startGPS(self):
        if self.gps is not None:
            self.gps.start()
            
    def check_dark(self):
        cur_dark = isDark()
        if cur_dark != self.last_dark:
            self.last_dark = cur_dark
            self.style.theme_use("forest-" + ("dark" if cur_dark else "light"))
        self.after(10, self.check_dark)

    def start(self, gps, flex):
        self.gps = gps
        self.flex_control = flex
        self.mainloop()
        manager.running = False
        self.destroy()

if __name__ == '__main__':
    Gui().start(None)
