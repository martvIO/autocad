from asyncio import log

from pyautocad import Autocad

acad = Autocad()
doc = acad.doc
def save_as_dxf(path: str = '/output.dxf', ac_version: str = "2010"):
    """
    path: the path to save the dxf file
    ac_version: on of the following versions:
        2000
        2004
        2007
        2010
        2013
        2018 
    """
    dxf_type = {
        "2000": 13,
        "2004": 21,
        "2007": 25,
        "2010": 29,
        "2013": 37,
        "2018": 61
    }

    if ac_version not in dxf_type.keys():
        raise RuntimeWarning("the Autocad version of the dxf file you entered wasn't correct")

    doc.SaveAs(path, dxf_type[ac_version])
    print("the dxf file has been saved")