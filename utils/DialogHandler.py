from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError
import threading, time

def dismiss_dialog(title_regex, button="OK", timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        try:
            dlg = Desktop(backend="uia").window(title_re=title_regex)
            dlg.wait("visible", timeout=1)
            dlg.child_window(title=button, control_type="Button").click()
            return True
        except ElementNotFoundError:
            time.sleep(0.2)
    return False

# Run the watcher in parallel with the AutoCAD action
t = threading.Thread(target=dismiss_dialog, args=("Save Drawing As", "Yes"))
t.start()
doc.SendCommand('_.SAVEAS\n...\n')
t.join()