import time
import threading
import win32com.client
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError, ElementAmbiguousError

from pywinauto import Desktop

def handle_trupdapt_dialog(timeout=15):
    """Wait for the TRUPDAPT dialog, toggle 'Visible', click OK."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # NOTE: adjust title_re to match the real dialog title.
            # Use Inspect.exe or `python -m pywinauto.inspect` to confirm.
            return True

        except (ElementNotFoundError, ElementAmbiguousError):
            time.sleep(0.25)
    print("Dialog not found within timeout.")
    return False


def main():
    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = True
    doc = acad.ActiveDocument

    # Start watcher BEFORE sending the command, since the dialog
    # appears synchronously and would otherwise block us.
    watcher = threading.Thread(target=handle_trupdapt_dialog, daemon=True)
    watcher.start()
    time.sleep(0.3)  # let the watcher get into its polling loop

    doc.SendCommand("TRUPDAPT\n")
    dlg = Desktop(backend="uia").window(title_re=".*")  # whatever matches
    dlg.print_control_identifiers()
    watcher.join(timeout=20)
    print("Done.")


if __name__ == "__main__":
    main()