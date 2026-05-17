from Points import Point
import time
import threading
import win32com.client
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError, ElementAmbiguousError
import win32com.client as comctl
from pywinauto import Desktop

def send_keys_to_window(wsh, key, times: int = 1):
    for _ in range(times):
        wsh.SendKeys(key)
        time.sleep(0.5)  # small delay between key presses
    
def update_point_symbol(point: Point, new_symbol: int, new_mark: str = None):

if __name__ == "__main__":
    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = True
    doc = acad.ActiveDocument

    doc.SendCommand("TRUPDAPT\n")
    wsh = win32com.client.Dispatch("WScript.Shell")
    # Google Chrome window title
    wsh.AppActivate("AutoCAD.Application")
    temp = {
        "TAB": 2,
        'SPACE': 1,
        'TAB': 1,
        "ARROW_UP": 1,
        "TAB": 3,
        "SPACE": 1,
        "TAB": 2,
        'SYMBOL_CODE': NONE,
        'TAB': 2,
        'SPACE': 1,
        'TAB': 1,
        'ARROW_UP': 2,
        'TAB': 5,
        'SPACE': 1,
        'TAB': 3,
        'SPACE': 1,
        
    }