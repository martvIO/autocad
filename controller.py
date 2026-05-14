import win32com.client

acad = win32com.client.Dispatch("AutoCAD.Application")
acad.Visible = True
doc = acad.ActiveDocument
ms = doc.ModelSpace

import pythoncom
def pt(x, y, z=0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))

ms.AddLine(pt(0,0), pt(100,100))
doc.SendCommand("ZOOM\nE\n")
