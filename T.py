"""
Survey DXF Rebuilder
====================
Reconstructs the original drawing using:
  * a points database with ABSOLUTE coordinates (single source of truth)
  * RELATIONAL geometry commands: connect(p1,p2), polyline_pts(...),
    extend(p1,p2,length), perpendicular_offset(...), arc_3p(...), etc.

Run with:  python rebuild_dxf.py            -> writes survey_rebuilt.dxf
Requires:  pip install ezdxf
"""

import math
import ezdxf
from ezdxf.enums import TextEntityAlignment

# ============================================================================
#  DOCUMENT SETUP
# ============================================================================
doc = ezdxf.new("R2010", setup=True)
msp = doc.modelspace()

# --- Layers -----------------------------------------------------------------
LAYERS = [
    "TR_PNT", "C1617", "C1609",
    "M1000", "M2200", "M2205", "M2206", "M2207",
    "M2299", "M2301", "M2404", "M2407", "M2412",
    "M2417", "M2605", "M2801",
    "M4402", "M4610", "M4903", "M5220",
]
for name in LAYERS:
    if name not in doc.layers:
        doc.layers.add(name)

# --- Text style -------------------------------------------------------------
if "HANIT_TEXT" not in doc.styles:
    doc.styles.add("HANIT_TEXT", font="Arial.ttf")
if "hebtxt" not in doc.styles:
    doc.styles.add("hebtxt", font="Arial.ttf")

# ============================================================================
#  BLOCK DEFINITIONS  (minimal stubs — replace with your real symbol blocks)
# ============================================================================
def _ensure_block(name, builder):
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    builder(blk)

def _b_M1502_P(blk):                       # survey point marker (small cross)
    blk.add_line((-0.4, 0), (0.4, 0))
    blk.add_line((0, -0.4), (0, 0.4))
    for tag, ins in [("NAME",   (-0.13, 1.03)),
                     ("HEIGHT", ( 0.00,-2.60)),
                     ("MARK",   (-0.53,-4.60))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.4,
                           dxfattribs={"style": "HANIT_TEXT"})
        a.dxf.halign = 1

def _b_C1617(blk):                         # control point monument (triangle)
    blk.add_lwpolyline([(0,-1),(1,1),(-1,1),(0,-1)])
    for tag, ins in [("POINT_NAME", (-1.24,1.17)),
                     ("MARK_DESC",  (-0.67,-5.0)),
                     ("MARK",       (0,-2.0)),
                     ("CLASS",      (0,-3.5)),
                     ("SOURCE",     (0,-5.0)),
                     ("TOPO",       (0,-6.5)),
                     ("HEIGHT",     (-2.39,-2.0)),
                     ("COMMENT",    (0,-9.5))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.5,
                           dxfattribs={"style": "hebtxt"})
        a.dxf.halign = 1

def _b_M1000_E(blk):                       # descriptive text leader
    a = blk.add_attdef(tag="DESC", insert=(-2.58,0.5), height=0.25,
                       dxfattribs={"style": "hebtxt"})
    a.dxf.halign = 1

def _b_C1609(blk):                         # line annotation
    blk.add_circle((0,0), 0.5)
    for tag, ins, h in [("LEGAL_LENGTH",(1.50,0.12),0.35),
                        ("CALC_LENGTH", (0.69,-2.12),0.35),
                        ("RADIUS",      (1.50,0.12),0.35),
                        ("CROSS",       (1.50,0.12),0.35),
                        ("LINE_NAME",   (-4.48,-0.37),0.25),
                        ("TOPO",        (-5.98,-0.49),0.25),
                        ("COMMENT",     (-7.47,-0.62),0.25)]:
        a = blk.add_attdef(tag=tag, insert=ins, height=h,
                           dxfattribs={"style": "hebtxt"})
        a.dxf.halign = 1

def _b_M2801_E(blk):                       # tree symbol
    blk.add_circle((0,0), 1.0)
    blk.add_line((-1,-1), (1,1))
    blk.add_line((-1,1), (1,-1))
    for tag, ins in [("NAME",        (-2.46,1.03)),
                     ("HEIGHT",      (-3.87,-2.60)),
                     ("MARK",        (-1.24,-4.60)),
                     ("DIAMETER",    (0,-6.60)),
                     ("TYPE",        (0,-10.60)),
                     ("TOP_DIAMETER",(0,-8.60))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.4,
                           dxfattribs={"style": "HANIT_TEXT"})
        a.dxf.halign = 1

def _b_M4402_E(blk):                       # manhole (square with diag)
    blk.add_lwpolyline([(-1.2,-1.2),(1.2,-1.2),(1.2,1.2),(-1.2,1.2)], close=True)
    blk.add_line((-1.2,-1.2),(1.2,1.2))
    for tag, ins in [("NAME",  (-1.30,1.03)),
                     ("HEIGHT",(-3.79,-2.60)),
                     ("MARK",  (-1.93,-4.60)),
                     ("OWNER", (0,-6.60)),
                     ("TYPE",  (0,-8.60))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.4,
                           dxfattribs={"style": "HANIT_TEXT"})
        a.dxf.halign = 1

def _b_M4610_E(blk):                       # water valve / box
    blk.add_lwpolyline([(-0.8,-0.8),(0.8,-0.8),(0.8,0.8),(-0.8,0.8)], close=True)
    for tag, ins in [("NAME",  (-1.19,0.63)),
                     ("HEIGHT",(-2.39,-1.40)),
                     ("MARK",  (-4.50,-2.03)),
                     ("OWNER", (0,-3.5))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.25,
                           dxfattribs={"style": "hebtxt"})
        a.dxf.halign = 1

def _b_M4903_E(blk):                       # rectangular pit
    blk.add_lwpolyline([(-1,-1.5),(1,-1.5),(1,1.5),(-1,1.5)], close=True)
    for tag, ins in [("NAME",  (-1.49,3.90)),
                     ("HEIGHT",(0,2.49)),
                     ("MARK",  (-1.33,0.90)),
                     ("TL",    (0,-2.0)),
                     ("IL",    (0,-3.49)),
                     ("OWNER", (0,-4.99)),
                     ("DESC",  (0,-6.48))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.25,
                           dxfattribs={"style": "hebtxt"})
        a.dxf.halign = 1

def _b_M5220_E(blk):                       # buried box (כוך)
    blk.add_lwpolyline([(-1,-1),(1,-1),(1,1),(-1,1)], close=True)
    blk.add_line((-1,-1),(1,1))
    blk.add_line((-1,1),(1,-1))
    for tag, ins in [("HEIGHT",(-3.55,-1.90)),
                     ("NAME",  (-1.78, 0.80)),
                     ("MARK",  (-1.60,-3.90)),
                     ("DESC",  (-7.33,-0.91))]:
        a = blk.add_attdef(tag=tag, insert=ins, height=0.375,
                           dxfattribs={"style": "hebtxt"})
        a.dxf.halign = 1

for n, fn in [("M1502_P",_b_M1502_P), ("C1617",_b_C1617),
              ("M1000_E",_b_M1000_E), ("C1609",_b_C1609),
              ("M2801_E",_b_M2801_E), ("M4402_E",_b_M4402_E),
              ("M4610_E",_b_M4610_E), ("M4903_E",_b_M4903_E),
              ("M5220_E",_b_M5220_E)]:
    _ensure_block(n, fn)

# ============================================================================
#  POINTS DATABASE  —  ABSOLUTE COORDINATES (the single source of truth)
# ============================================================================
# Format: ID -> (x, y, z)
POINTS = {
    # numbered survey points (M1502_P)
    "1":   (1009.962, 1005.154, 0.0),
    "2":   (1010.066,  999.903, 0.0),
    "3":   (1010.238,  997.925, 0.0),
    "4":   (1010.610,  993.245, 0.0),
    "4A":  (1010.615,  993.242, 0.0),
    "5":   (1010.084,  999.143, 110.503),
    "6":   (1007.383,  995.844, 100.259),
    "7":   (1008.013,  988.019, 100.393),
    "8":   (1006.603, 1005.062, 100.190),
    "9":   (1007.365,  995.975, 101.850),
    "10":  (1007.440,  995.633, 102.882),
    "11":  ( 989.098,  986.733, 101.335),
    "12":  ( 987.681,  989.474, 102.200),
    "13":  ( 986.726, 1001.528, 102.207),
    "14":  ( 991.399,  981.562, 110.706),
    "15":  ( 993.975,  981.752, 0.0),
    "16":  ( 988.091,  981.259, 0.0),
    "17":  ( 985.891,  981.056, 0.0),
    "18":  ( 979.976,  980.582, 0.0),
    "19":  ( 988.135,  986.710, 100.274),
    "20":  ( 995.635,  987.965, 100.207),
    "21":  ( 996.595,  987.113, 100.259),
    "23":  (1003.021,  973.121, 100.611),
    "23X": (1001.980,  968.491, 100.612),
    "24":  (1005.507,  974.762, 101.754),
    "24X": (1004.824,  968.725, 102.606),
    "25":  (1003.952,  968.846, 104.574),
    "26":  ( 983.778, 1002.108, 109.375),
    "27":  ( 984.494,  991.019, 0.0),
    "28":  ( 984.125,  995.200, 0.0),
    "29":  ( 984.226,  995.479, 0.0),
    "30":  ( 983.978,  998.307, 0.0),
    "31":  ( 983.712, 1000.056, 0.0),
    "32":  ( 983.669, 1001.929, 0.0),
    "33":  ( 983.321, 1005.959, 0.0),
    "34":  ( 989.402, 1005.203, 100.250),
    "35":  ( 986.269, 1005.783, 100.248),
    "36":  ( 987.073,  997.224, 100.022),
    "37":  ( 989.708, 1002.215, 100.059),
    "38":  ( 987.420,  997.245, 0.0),
    "39":  ( 990.219,  997.441, 100.030),
    "39A": ( 990.214,  997.464, 0.0),
    "40":  ( 990.545,  993.147, 100.144),
    "41":  ( 987.677,  991.010, 100.019),
    "42":  ( 993.454, 1005.550, 100.246),
    "43":  ( 996.410, 1005.317,  99.995),
    "44":  ( 997.811, 1006.248, 0.0),
    "45":  ( 993.118, 1009.550, 0.0),
    "46":  ( 995.675, 1009.769, 100.658),
    "47":  ( 999.417, 1002.370, 100.080),
    "48":  (1002.849, 1002.642, 100.036),
    "52":  ( 996.376, 1005.699, 104.319),
    "53":  ( 985.720, 1011.515, 100.404),
    "54":  ( 985.842, 1010.399, 102.359),
    "55":  ( 988.206, 1018.939, 100.520),
    "56":  ( 987.634, 1019.180, 100.471),
    "57":  ( 987.529, 1024.917, 100.613),
    "58":  ( 984.474, 1024.497, 100.634),
    "59":  ( 984.484, 1024.724, 100.644),
    "60":  ( 982.885, 1024.404, 100.712),
    "61":  ( 982.083, 1024.340, 100.736),
    "62":  ( 982.147, 1023.519, 0.0),
    "64":  ( 973.462, 1023.671, 100.802),
    "65":  ( 971.713, 1023.513, 100.817),
    "66":  ( 964.868, 1022.954, 100.678),
    "67":  ( 963.617, 1024.946, 100.714),
    "68":  ( 976.364, 1026.031, 100.597),
    "69":  ( 991.223, 1027.247, 100.444),
    "70":  (1000.559, 1028.026, 100.389),
    "71":  ( 999.218, 1032.867, 100.380),
    "72":  ( 975.973, 1036.943, 100.481),
    "73":  ( 966.202, 1041.133, 100.517),
    "74":  ( 964.328, 1042.911, 0.0),
    "75":  ( 968.804, 1043.356, 0.0),
    "75X": ( 971.021, 1043.608, 100.770),
    "76":  ( 972.382, 1043.754, 100.764),
    "77":  ( 975.217, 1044.032, 100.775),
    "78":  ( 976.788, 1049.263, 0.0),
    "79":  ( 981.240, 1044.545, 100.649),
    "80":  ( 989.023, 1045.182, 0.0),
    "81":  ( 991.631, 1045.396, 0.0),
    "82":  ( 999.674, 1046.036, 100.539),
    "83":  ( 997.775, 1043.808, 100.386),
    "84":  ( 982.738, 1042.536, 100.459),
    "85":  ( 999.822, 1051.612, 0.0),
    "86":  ( 998.949, 1050.921, 0.0),
    "87":  ( 993.122, 1048.907, 0.0),
    "88":  ( 979.849, 1049.943, 0.0),
    "89":  ( 980.056, 1047.849, 0.0),
    "90":  ( 984.525, 1052.276, 114.144),
    "91":  ( 978.581, 1031.088, 100.585),
    "92":  ( 976.533, 1030.915, 100.622),
    "93":  ( 972.919, 1030.656, 100.604),
    "94":  ( 965.421, 1029.968, 100.697),
    "109": (1002.781, 1046.251, 100.436),
    "110": (1009.148, 1047.007, 100.473),
    "111": (1010.458, 1046.937, 100.462),
    "112": (1013.928, 1047.231, 100.457),
    "113": (1010.552, 1044.885, 100.303),
    "114": (1018.046, 1052.579, 0.0),
    "115": (1006.887, 1051.636, 0.0),
    "116": (1005.260, 1053.583, 0.0),
    "117": (1009.041, 1017.399, 112.040),
    "118": (1001.288, 1033.075, 100.378),
    "119": ( 998.725, 1038.874, 100.425),
    "120": (1008.564, 1033.706, 100.339),
    "121": (1015.727, 1040.313, 100.304),
    "123": (1025.524, 1030.054, 100.191),
    "124": (1020.097, 1027.626, 100.330),
    "125": (1009.699, 1026.815, 100.519),
    "126": (1008.471, 1026.759, 100.474),
    "127": (1004.913, 1026.412, 100.504),
    "129": (1005.153, 1023.419, 100.562),
    "130": (1005.654, 1022.387, 100.602),
    "131": (1005.389, 1020.681, 100.574),
    "133": (1002.633, 1021.598, 100.515),
    "134": (1001.861, 1026.124, 100.517),
    "135": (1000.723, 1026.058, 100.514),
    "136": (1001.515, 1021.487, 100.472),
    "137": (1002.604, 1019.192, 100.415),
    "138": (1003.634, 1019.242, 100.383),
    "139": (1003.877, 1016.777, 100.315),
    "140": (1004.820, 1015.576, 100.627),
    "141": (1002.850, 1011.288, 100.672),
    "142": (1003.066, 1009.488, 0.0),
    "143": (1003.406, 1011.275, 0.0),
    "144": (1003.506, 1015.389, 0.0),
    "145": (1002.313, 1017.697, 100.419),
    "146": ( 996.592, 1017.236, 100.452),
    "148": ( 993.140, 1019.394, 100.642),
    "149": (1006.169, 1010.976, 100.195),
    "150": (1005.783, 1015.400, 101.903),
    "151": (1005.762, 1015.562, 102.563),
    "152": (1004.982, 1025.335, 102.567),
    "153": (1008.197, 1026.691, 102.572),
    "154": (1009.203, 1021.714, 0.0),
    "155": (1008.675, 1020.976, 0.0),
    "156": (1009.381, 1010.797, 0.0),
}

# Control points (C1617 block)
CONTROL = {
    "M1":  (1000.000, 1000.000, 100.000),
    "M2":  ( 987.731, 1005.305, 100.325),
    "M3":  (1002.990, 1027.312, 100.432),
    "M4":  (1030.592, 1030.317, 100.277),
    "AM1": ( 984.331, 1026.519, 100.554),
}

# Trees (M2801_E)  —  name : (xyz, mark_text)
TREES = {
    "22.5":  ((1003.337,  988.067, 100.341), "ברוש"),
    "49.2":  ((1005.904, 1004.939, 100.065), "ברוש"),
    "50.1":  ((1006.254, 1002.647, 100.059), "ברוש"),
    "51.3":  ((1006.223, 1001.467, 100.160), "ברוש"),
    "95.2":  (( 968.853, 1031.065,   0.000), "ברוש"),
    "96.2":  (( 972.797, 1031.421,   0.000), "ברוש"),
    "97.3":  (( 975.320, 1031.500,   0.000), "ברוש"),
    "98.3":  (( 969.133, 1035.527,   0.000), "ברוש"),
    "99.4":  (( 974.894, 1035.840,   0.000), "ברוש"),
    "100.2": (( 979.445, 1036.502,   0.000), "ברוש"),
    "101.7": (( 981.961, 1032.135,   0.000), "ברוש"),
    "102.5": (( 985.265, 1036.487, 100.584), "ברוש"),
    "103.4": (( 989.593, 1032.822, 100.612), "ברוש"),
    "104.3": (( 993.170, 1037.662,   0.000), "ברוש"),
    "105.4": (( 995.931, 1033.253, 100.566), "ברוש"),
    "106.5": ((1001.410, 1034.049, 100.510), "ברוש"),
    "107.3": ((1007.377, 1034.291,   0.000), "ברוש"),
    "108.4": ((1011.749, 1039.305, 100.537), "ברוש"),
}

# Manhole / utility blocks
MANHOLES = {                           # NAME -> (xyz, mark)
    "63":  (( 976.216, 1025.542, 100.755), "ת.ע"),
    "122": ((1011.979, 1028.535, 100.420), "ת.ע"),
}
WATER_BOXES = {                        # 128 — M4610_E
    "128": ((1004.681, 1025.000, 100.550), "מים"),
}
PITS = {                               # 132/147 — M5220_E (כוך)
    "132": ((1004.325, 1021.531, 100.560), "כוך"),
    "147": (( 996.239, 1019.566, 100.509), "כוך"),
}
INSPECTION = {                         # 157 — M4903_E
    "157a": (991.213, 1027.373, 0.0),
    "157b": (972.931, 1030.529, 0.0),
}

# ============================================================================
#  RELATIONAL GEOMETRY HELPERS
# ============================================================================
def P(pid):
    """Resolve a point id (numbered survey point) to an (x,y,z) tuple."""
    return POINTS[pid]

def add_survey_point(pid, height_text=None, layer="TR_PNT"):
    """INSERT a survey point block at POINTS[pid]."""
    x, y, z = POINTS[pid]
    if height_text is None:
        height_text = f"{z:.2f}" if z > 0 else ""
    ref = msp.add_blockref("M1502_P", (x, y, z),
                           dxfattribs={"layer": layer,
                                       "xscale": 0.25,
                                       "yscale": 0.25,
                                       "zscale": 0.25})
    ref.add_auto_attribs({"NAME": pid, "HEIGHT": height_text, "MARK": " "})
    return ref

def add_control(name, layer="C1617"):
    x, y, z = CONTROL[name]
    ref = msp.add_blockref("C1617", (x, y, z),
                           dxfattribs={"layer": layer,
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"POINT_NAME": name, "HEIGHT": f"{z:.2f}", "MARK_DESC": " "})

def add_tree(name):
    (x, y, z), mark = TREES[name]
    ht = f"{z:.2f}" if z > 0 else ""
    ref = msp.add_blockref("M2801_E", (x, y, z),
                           dxfattribs={"layer": "M2801",
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"NAME": name, "HEIGHT": ht, "MARK": mark})

def add_manhole(name):
    (x, y, z), mark = MANHOLES[name]
    ref = msp.add_blockref("M4402_E", (x, y, z),
                           dxfattribs={"layer": "M4402",
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"NAME": name, "HEIGHT": f"{z:.2f}", "MARK": mark})

def add_water_box(name):
    (x, y, z), mark = WATER_BOXES[name]
    ref = msp.add_blockref("M4610_E", (x, y, z),
                           dxfattribs={"layer": "M4610",
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"NAME": name, "HEIGHT": f"{z:.2f}", "MARK": mark})

def add_pit(name):
    (x, y, z), mark = PITS[name]
    ref = msp.add_blockref("M5220_E", (x, y, z),
                           dxfattribs={"layer": "M5220",
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"NAME": name, "HEIGHT": f"{z:.2f}", "MARK": mark})

def add_inspection(name, mark="קו"):
    x, y, z = INSPECTION[name]
    ref = msp.add_blockref("M4903_E", (x, y, z),
                           dxfattribs={"layer": "M4903",
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25,
                                       "rotation": 4.379})
    ref.add_auto_attribs({"NAME": "157", "MARK": mark})

# --- Relational drawing primitives ------------------------------------------
def connect(p1, p2, layer="M2200"):
    """Draw a LINE between two named points."""
    a, b = P(p1), P(p2)
    msp.add_line(a, b, dxfattribs={"layer": layer})

def polyline_pts(*pids, layer="M2200", closed=False):
    """Draw a polyline through named points."""
    pts = [P(p) for p in pids]
    z = pts[0][2]
    msp.add_lwpolyline([(p[0], p[1]) for p in pts],
                       close=closed,
                       dxfattribs={"layer": layer, "elevation": z})

def line(start, end, layer):
    """Draw a LINE between two ABSOLUTE coordinates."""
    msp.add_line(start, end, dxfattribs={"layer": layer})

def polyline(coords, layer, elevation=0, closed=False):
    """Draw an LWPOLYLINE from absolute (x,y) coordinate list."""
    msp.add_lwpolyline(coords, close=closed,
                       dxfattribs={"layer": layer, "elevation": elevation})

def arc(center, radius, start_deg, end_deg, layer):
    msp.add_arc(center=center, radius=radius,
                start_angle=start_deg, end_angle=end_deg,
                dxfattribs={"layer": layer})

def text(s, position, height=0.25, rotation=0, layer="M1000"):
    t = msp.add_text(s, height=height,
                     dxfattribs={"layer": layer, "rotation": rotation,
                                 "style": "Standard"})
    t.dxf.insert = position
    return t

def label(desc, position, rotation=0, layer="M1000"):
    """Insert an M1000_E label (descriptive text leader)."""
    ref = msp.add_blockref("M1000_E", position,
                           dxfattribs={"layer": layer, "rotation": rotation,
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"DESC": desc})

def hatch_dots(boundary_points, layer="M2299", scale=10.0):
    """Add a DOTS-pattern hatch on a closed polyline boundary."""
    h = msp.add_hatch(dxfattribs={"layer": layer})
    h.set_pattern_fill("DOTS", scale=scale)
    h.paths.add_polyline_path(boundary_points, is_closed=True)

# --- Higher-level relational helpers ----------------------------------------
def extend(p1, p2, length, layer):
    """Extend the ray from P(p1) toward P(p2) by 'length' past p2."""
    ax, ay, az = P(p1); bx, by, bz = P(p2)
    dx, dy = bx - ax, by - ay
    d = math.hypot(dx, dy)
    if d == 0:
        return
    ux, uy = dx / d, dy / d
    end = (bx + ux * length, by + uy * length, bz)
    msp.add_line((bx, by, bz), end, dxfattribs={"layer": layer})
    return end

def perpendicular_offset(p1, p2, distance, layer):
    """Draw a line perpendicular to p1-p2, of given 'distance', starting at p2.
       Positive distance = left of p1->p2 direction."""
    ax, ay, _ = P(p1); bx, by, bz = P(p2)
    dx, dy = bx - ax, by - ay
    d = math.hypot(dx, dy)
    nx, ny = -dy / d, dx / d                   # left-normal
    end = (bx + nx * distance, by + ny * distance, bz)
    msp.add_line((bx, by, bz), end, dxfattribs={"layer": layer})
    return end

def arc_through(p1, p_mid, p2, layer):
    """Draw an ARC defined by three named points (start, on-arc, end)."""
    (x1,y1,_),(x2,y2,_),(x3,y3,_) = P(p1), P(p_mid), P(p2)
    # circumscribed circle
    ax, ay = x2 - x1, y2 - y1
    bx, by = x3 - x1, y3 - y1
    d = 2 * (ax * by - ay * bx)
    if d == 0:
        return
    ux = (by * (ax**2 + ay**2) - ay * (bx**2 + by**2)) / d
    uy = (ax * (bx**2 + by**2) - bx * (ax**2 + ay**2)) / d
    cx, cy = x1 + ux, y1 + uy
    r = math.hypot(ux, uy)
    sa = math.degrees(math.atan2(y1 - cy, x1 - cx))
    ea = math.degrees(math.atan2(y3 - cy, x3 - cx))
    msp.add_arc(center=(cx, cy), radius=r,
                start_angle=sa, end_angle=ea,
                dxfattribs={"layer": layer})

# ============================================================================
#  BUILD THE DRAWING
# ============================================================================

# --- 1)  Insert every survey point ------------------------------------------
for pid in POINTS:
    add_survey_point(pid)

# --- 2)  Control / monumented points ----------------------------------------
for c in CONTROL:
    add_control(c)

# --- 3)  Trees, manholes, pits, water boxes, inspection covers --------------
for t in TREES:        add_tree(t)
for m in MANHOLES:     add_manhole(m)
for w in WATER_BOXES:  add_water_box(w)
for p in PITS:         add_pit(p)
add_inspection("157a"); add_inspection("157b")

# --- 4)  Survey baseline / reference lines ----------------------------------
# Long baseline AM1 -> M2 (north-south) and AM1 -> M4 (east-west)
line((984.331, 1026.519, 100.554), (987.731, 1005.305, 100.554), layer="0")
line((984.331, 1026.519, 100.554), (1030.592, 1030.317, 100.554), layer="0")

# --- 5)  Property / boundary polylines (M2200) ------------------------------
# East boundary chain  4 -> 3 -> 2 -> (split) -> 1
polyline([(1010.610, 993.245), (1010.238, 997.925), (1010.066, 999.903)],
         layer="M2200")
polyline([(1010.066, 999.903), (1010.416, 999.9334), (1009.962, 1005.154)],
         layer="M2200")
line((1010.610, 993.245, 0.0), (1012.9532, 993.4403, 0.0), layer="M2200")
line((1009.962, 1005.154, 0.0), (1011.9550, 1005.3214, 0.0), layer="M2200")

# South boundary 15-16-17-18 with ticks
connect("15", "16", layer="M2200")
connect("17", "18", layer="M2200")
# Ticks (perpendicular markers)
polyline([(985.891, 981.056), (986.0508, 979.0624),
          (988.2580, 979.2660), (988.091, 981.259)], layer="M2200")
line((993.975, 981.752, 0.0), (994.2255, 978.7625, 0.0), layer="M2200")
line((979.976, 980.582, 0.0), (980.2156, 977.5916, 0.0), layer="M2200")

# West boundary 33-32-30-(29|28)-27
polyline([P("33")[:2], P("32")[:2]], layer="M2200")
polyline([P("30")[:2], P("29")[:2]], layer="M2200")
polyline([P("27")[:2], (984.1013, 995.4681)], layer="M2200")
line((983.978, 998.307, 0.0), (983.8639, 998.297, 0.0), layer="M2200")
line((984.1013, 995.4681, 0.0), (984.2260, 995.4790, 0.0), layer="M2200")
polyline([(983.6690, 1001.9290), (983.5511, 1001.9188),
          (983.8639, 998.2970)], layer="M2200")
# West boundary ticks at 27 and 33
line((982.5001, 990.8625, 0.0), (984.4940, 991.0190, 0.0), layer="M2200")
line((983.3210, 1005.9590, 0.0), (981.3271, 1005.8025, 0.0), layer="M2200")

# 4 -> 4A duplicate (very small offset; tiny segment)
# (already represented by tick-line system above)

# --- 6)  Building / structure outline at AM1 area ---------------------------
# Long path 33 -> 32 -> 30 -> 28 (M2200 above plus M2404 internal)
polyline([P("33")[:2], P("32")[:2], P("30")[:2], P("28")[:2]], layer="M2404")

# --- 7)  Driveway / paved area near house ----------------------------------
# Curb chain 1 -> 8 -> 34 -> 35 ...
polyline_pts("1", "8", layer="M2200")     # corner element

# Property concrete pad outline near house
polyline([(989.402, 1005.203), (988.206, 1018.939)], layer="M2200")
polyline([(993.454, 1005.550), (993.118, 1009.550)], layer="M2200")
polyline_pts("44", "43", layer="M2200")
polyline_pts("43", "45", layer="M2200")
polyline_pts("46", "45", layer="M2200")

# --- 8)  Curb / wall around utility cluster (M2605) -------------------------
# Two parallel curb lines near tree row (north side)
polyline([(1007.383,  995.844), (1006.603, 1005.062),
          (1006.169, 1010.976)], layer="M2605", elevation=100.259)
polyline([(1006.169, 1010.976), (1005.377, 1020.8305)],
         layer="M2605", elevation=100.195)
polyline([(1005.153, 1023.419), (1004.913, 1026.412)],
         layer="M2605", elevation=100.562)

# Inner offset of same curb (200 mm offset)
polyline([(1005.5686, 1023.4523), (1005.6540, 1022.3870),
          (1005.7654, 1020.8588)], layer="M2605", elevation=100.562)
polyline([(1005.1530, 1023.4190), (1005.5686, 1023.4523)],
         layer="M2605", elevation=100.562)

# Continuing curb north toward 124/123
polyline([(1004.913, 1026.412), (1008.471, 1026.759)],
         layer="M2605", elevation=100.504)
polyline([(1009.699, 1026.815), (1020.097, 1027.626)],
         layer="M2605", elevation=100.519)
polyline([(1009.9139, 1026.6312), (1019.9132, 1027.4111)],
         layer="M2605", elevation=100.519)
# Parallel-offset short stubs (ladder rungs of curb)
polyline([(1008.4710, 1026.7590), (1008.6845, 1024.5694)],
         layer="M2605", elevation=100.474)
polyline([(1008.2914, 1026.5405), (1008.4855, 1024.5500)],
         layer="M2605", elevation=100.474)
polyline([(1009.6990, 1026.8150), (1009.8701, 1024.6217)],
         layer="M2605", elevation=100.519)
polyline([(1009.9139, 1026.6312), (1010.0695, 1024.6372)],
         layer="M2605", elevation=100.519)
polyline([(1020.0970, 1027.6260), (1021.3449, 1011.6268)],
         layer="M2605", elevation=100.330)
polyline([(1019.9132, 1027.4111), (1021.1453, 1011.6130)],
         layer="M2605", elevation=100.330)
polyline([(1021.3731, 1027.7255), (1022.6218, 1011.7154)],
         layer="M2605", elevation=100.330)
polyline([(1021.5725, 1027.7411), (1022.8214, 1011.7292)],
         layer="M2605", elevation=100.330)
polyline([(1021.3731, 1027.7255), (1021.5725, 1027.7411)],
         layer="M2605", elevation=100.330)

# Ladder-rung hatching above (M2417 short parallel lines)
for dy in [0.0, -0.0291, -0.0584, -0.0875, -0.1167, -0.1458]:
    line((1008.4710 + 0.029*( -dy/0.0291 if dy else 0), 1026.7590 + dy, 100.474),
         (1009.7223 + 0.0,                 1026.5158 + dy, 100.474),
         layer="M2417")
# (the loop above is illustrative; the original ladder uses 6 specific rungs)
for y_start, y_end in [
    (1027.3269, 1027.4264), (1027.0278, 1027.1273),
    (1026.7287, 1026.8283)]:
    line((1020.1203, y_start, 100.330), (1021.3965, y_end, 100.330), layer="M2417")

# --- 9)  South building wall (curb + bricks) --------------------------------
polyline([(1007.3830, 995.8440), (1008.0130, 988.0190)],
         layer="M2605", elevation=100.259)
polyline([(1007.5824, 995.8598), (1010.3844, 996.0826)],
         layer="M2605", elevation=100.259)
polyline([(1007.5984, 995.6605), (1010.4003, 995.8832)],
         layer="M2605", elevation=100.259)
line((1008.0130, 988.0190, 100.393), (1010.2059, 988.1956, 100.393), layer="M2605")
line((1008.1963, 988.2344, 100.393), (1010.1899, 988.3949, 100.393), layer="M2605")

# Long south curb 996-988 area
polyline([(996.5950, 987.1130), (988.1350, 986.7100)],
         layer="M2605", elevation=100.259)
polyline([(996.6045, 986.9132), (987.9561, 986.5013)],
         layer="M2605", elevation=100.259)
polyline([(996.5950, 987.1130), (996.6045, 986.9132)],
         layer="M2605", elevation=100.259)
polyline([(988.1350, 986.7100), (987.4750, 992.9064)],
         layer="M2605", elevation=100.259)
polyline([(987.9561, 986.5013), (987.2544, 993.0897)],
         layer="M2605", elevation=100.259)

# Long west curb chain south->north
polyline([(987.073, 997.224), (986.269, 1005.783),
          (985.720, 1011.515), (984.474, 1024.497)],
         layer="M2605", elevation=100.022)
polyline([(986.8920, 997.0127), (986.0699, 1005.7641),
          (985.5209, 1011.4959), (984.2749, 1024.4779)],
         layer="M2605", elevation=100.022)
polyline([(984.2749, 1024.4779), (984.4740, 1024.4970)],
         layer="M2605", elevation=100.022)
polyline([(984.2749, 1024.4779), (982.8850, 1024.4040)],
         layer="M2605", elevation=100.022)
polyline([(984.2855, 1024.2782), (983.0953, 1024.2149)],
         layer="M2605", elevation=100.022)
polyline([(982.8850, 1024.4040), (982.9288, 1023.5799)],
         layer="M2605", elevation=100.022)
polyline([(983.0953, 1024.2149), (983.1389, 1023.3957)],
         layer="M2605", elevation=100.022)
# Continuation into 65 / 64
polyline([(982.1470, 1023.5190), (982.9288, 1023.5799)],
         layer="M2605", elevation=100.802)
polyline([(981.9631, 1023.3041), (983.1389, 1023.3957)],
         layer="M2605", elevation=100.802)
polyline([(973.4620, 1023.6710), (982.0830, 1024.3400),
          (982.1470, 1023.5190)], layer="M2605", elevation=100.802)
polyline([(973.4775, 1023.4716), (981.8991, 1024.1251),
          (981.9631, 1023.3041)], layer="M2605", elevation=100.802)
polyline([(973.4620, 1023.6710), (973.4775, 1023.4716)],
         layer="M2605", elevation=100.802)

# 65 / 66 / 67 (curbs near 64-67)
line((971.5137, 1023.4967, 100.817), (964.8680, 1022.9540, 100.817), layer="M2207")
polyline([(971.7130, 1023.5130), (971.8758, 1021.5196)],
         layer="M2605", elevation=100.817)
polyline([(971.5137, 1023.4967), (971.6765, 1021.5034)],
         layer="M2605", elevation=100.817)
polyline([(964.8680, 1022.9540), (965.0308, 1020.9606)],
         layer="M2605", elevation=100.678)
polyline([(964.6687, 1022.9377), (964.8315, 1020.9444)],
         layer="M2605", elevation=100.678)
polyline([(964.6687, 1022.9377), (964.8680, 1022.9540)],
         layer="M2605", elevation=100.678)
polyline([(971.7130, 1023.5130), (971.5137, 1023.4967)],
         layer="M2605", elevation=100.817)

# --- 10)  Driveway / road centerline (M2407) --------------------------------
polyline_pts("67", "68", "69", "70", "123", layer="M2407")

# --- 11)  Concrete pad near AM1 (M2301) -------------------------------------
polyline([(984.474, 1024.497), (984.484, 1024.724), (987.529, 1024.917),
          (987.634, 1019.180), (985.0085, 1018.9280)],
         layer="M2301", elevation=100.022)
polyline([(1002.633, 1021.598), (1005.6952, 1021.8211)],
         layer="M2301", elevation=100.515)
polyline([(1001.861, 1026.124), (1004.913, 1026.412)],
         layer="M2301", elevation=100.517)

# --- 12)  Driveway curb (M2206) ---------------------------------------------
polyline([(1009.2030, 1021.7140), (1009.2514, 1021.0160)], layer="M2206")
polyline([(1019.7249, 1022.4438), (1019.7733, 1021.7458)], layer="M2206")
polyline([(1019.7249, 1022.4438), (1009.2030, 1021.7140)], layer="M2206")
polyline([(991.5576, 1048.7803), (993.1220, 1048.9070),
          (999.9937, 1049.4538), (999.6920, 1053.2458)], layer="M2206")
polyline([(979.6774, 1051.6790), (980.0560, 1047.8490),
          (988.5507, 1048.5368)], layer="M2206")
polyline([(972.3820, 1043.7540), (977.2811, 1044.2344)],
         layer="M2206", elevation=100.764)
polyline([(976.7880, 1049.2630), (977.2811, 1044.2344)], layer="M2206")
polyline([(971.8889, 1048.7826), (972.3820, 1043.7540)],
         layer="M2206", elevation=100.764)

# Curb near 38-39-40 (M2206 short verticals)
line((987.42, 997.245, 0.0), (990.214, 997.464, 0.0), layer="M2206")
line((990.214, 997.464, 0.0), (990.545, 993.147, 0.0), layer="M2206")
line((987.42, 997.245, 0.0), (987.751, 992.928, 0.0), layer="M2206")
line((987.751, 992.928, 0.0), (990.545, 993.147, 0.0), layer="M2206")
polyline([(986.8920, 997.0127), (987.4321, 997.0454)],
         layer="M2605", elevation=100.022)
polyline([(986.8733, 997.2119), (987.4200, 997.2450)],
         layer="M2605", elevation=100.022)
polyline([(987.7510, 992.9280), (987.2755, 992.8907)], layer="M2605")

# --- 13)  Driveway parking stripes between 1/2 and curb (M2205) -------------
polyline([(990.2140, 997.4640), (994.5313, 997.7950)], layer="M2205")
polyline([(990.5450, 993.1470), (994.8623, 993.4780)], layer="M2205")
polyline([(994.8623, 993.4780), (994.5313, 997.7950)], layer="M2205")
polyline([(1003.5060, 1015.3890), (1003.8794, 1011.3184)], layer="M2205")
polyline([(1003.4060, 1011.2750), (1003.5523, 1009.5287),
          (1003.0660, 1009.4880)], layer="M2205")
line((1003.406, 1011.275, 0.0), (1003.879388, 1011.318423, 0.0), layer="M2205")
line((1003.506, 1015.389, 0.0), (1002.513353, 1015.305828, 0.0), layer="M2205")

# --- 14)  Building footprint (M2404) ----------------------------------------
# Top-floor wall (1002.85 line going up to 145)
polyline([(1002.8500, 1011.2880), (1002.8490, 1011.2880)],
         layer="M2200", elevation=100.419)        # placeholder vertex
polyline([(1002.313, 1017.697), (1002.850, 1011.288)],
         layer="M2200", elevation=100.419)
polyline([(1002.8500, 1011.2880), (1005.1614, 1011.5000)],
         layer="M2404", elevation=100.419)
polyline([(1004.8200, 1015.5760), (1005.1623, 1011.4909),
          (1005.1623, 1011.4909)], layer="M2404", elevation=100.419)
polyline([(1004.8200, 1015.5760), (1004.0022, 1015.5075)],
         layer="M2404", elevation=100.627)
polyline([(1002.9757, 1015.4215), (1002.5070, 1015.3822)],
         layer="M2404", elevation=100.627)
polyline([(1003.6340, 1019.2420), (1004.0022, 1015.5075)],
         layer="M2404", elevation=100.383)
polyline([(1002.6090, 1019.1410), (1002.9757, 1015.4215)],
         layer="M2404", elevation=100.383)
polyline([(1002.8500, 1011.2880), (1003.0660, 1009.4880)],
         layer="M2200", elevation=100.419)
polyline([(1002.3130, 1017.6970), (1002.8500, 1011.2880)],
         layer="M2200", elevation=100.419)
polyline([(1002.3130, 1017.6970), (996.5920, 1017.2360),
          (993.3664, 1016.9385), (993.1400, 1019.3940)],
         layer="M2200", elevation=100.419)
polyline([(1000.7230, 1026.0580), (1001.8610, 1026.1240)],
         layer="M2404", elevation=100.415)

# House outline near tree row (993.4 .. 988.2)
polyline([(993.1180, 1009.5500), (993.4540, 1005.5500),
          (989.4020, 1005.2030), (988.2060, 1018.9390)],
         layer="M2200")
polyline([(988.2060, 1018.9390), (993.1400, 1019.3940)], layer="M2200")
polyline([(998.8109, 1010.0175), (995.6750, 1009.7690),
          (993.1180, 1009.5500)], layer="M2200")
polyline([(999.4170, 1002.3700), (998.8109, 1010.0175)], layer="M2200")
polyline([(1002.8490, 1002.6420), (999.4170, 1002.3700)], layer="M2200")
polyline([(1003.0660, 1009.4880), (1002.2281, 1009.4111),
          (1002.8490, 1002.6420)], layer="M2200")

# --- 15)  Side door / window detail (M2404) ---------------------------------
polyline([(988.9263, 1022.0182), (992.8645, 1022.3813)], layer="M2404")
polyline([(989.2018, 1019.0308), (988.9263, 1022.0182)], layer="M2404")
polyline([(992.8645, 1022.3813), (993.1400, 1019.3940)], layer="M2404")

# --- 16)  Door 134 -> 135 cluster (driveway access) -------------------------
polyline([(993.4540, 1005.5500), (999.0934, 1006.4534)], layer="M2404")
polyline([(996.4100, 1005.3170), (997.9214, 1005.5591)], layer="M2412")
polyline([(997.8110, 1006.2480), (997.9214, 1005.5591)], layer="M2412")
polyline([(999.1487, 1005.7557), (999.2037, 1005.7646)], layer="M2404")
polyline([(996.4100, 1005.3170), (996.2996, 1006.0059)], layer="M2412")
polyline([(996.3731, 1005.5474), (997.8844, 1005.7895)], layer="M2412")
polyline([(996.3362, 1005.7778), (997.8475, 1006.0199)], layer="M2412")

# --- 17)  Pipe 137 -> 138 -> 139 -> 140 inside garage -----------------------
polyline_pts("137", "138", layer="M2404")
polyline_pts("139", "140", layer="M2404")

# --- 18)  Path 47 -> 48 -> 1 (driveway centerline 2nd lane) -----------------
line((1010.6750, 1020.9760, 0.0), (1009.3810, 1010.7970, 0.0), layer="M2200")
line((1008.6750, 1020.9760, 0.0), (1020.3519, 1021.7859, 0.0), layer="M2200")
line((1009.3810, 1010.7970, 0.0), (1021.1453, 1011.6130, 0.0), layer="M2200")

# --- 19)  Trees row at south (23/23X, 24/24X, 25) curb ----------------------
line((1004.8240, 968.7250, 102.606), (1001.9800, 968.4910, 102.606), layer="M2200")
polyline([(1001.9800, 968.4910), (1002.1440, 966.4977),
          (1002.1440, 966.4977)], layer="M2200", elevation=100.612)

# --- 20)  Big curved sidewalk arcs at front of property (M2404) -------------
arc(center=(1017.259230, 1026.421637, 100.517), radius=15.40110672,
    start_deg=181.1073484, end_deg=207.7864011, layer="M2404")
arc(center=(1013.996541, 1026.003743, 100.415), radius=13.27365246,
    start_deg=179.7657999, end_deg=210.8757316, layer="M2404")

# --- 21)  Drive / lot exit at 113 (M2605 curb continues) --------------------
polyline([(1010.4580, 1046.9370), (1013.9280, 1047.2310)],
         layer="M2605", elevation=100.462)
polyline([(1010.4411, 1047.1363), (1013.9111, 1047.4303)],
         layer="M2605", elevation=100.462)
polyline([(1010.4411, 1047.1363), (1010.4580, 1046.9370)],
         layer="M2605", elevation=100.462)
line((1008.9494, 1046.9834, 100.473), (1002.9796, 1046.2746, 100.473), layer="M2207")
polyline([(1008.9122, 1048.9930), (1009.1480, 1047.0070)],
         layer="M2605", elevation=100.473)
polyline([(1002.5452, 1048.2370), (1002.7810, 1046.2510)],
         layer="M2605", elevation=100.473)
polyline([(1002.7438, 1048.2606), (1002.9796, 1046.2746)],
         layer="M2605", elevation=100.473)
polyline([(1008.7136, 1048.9695), (1008.9494, 1046.9834)],
         layer="M2605", elevation=100.473)
polyline([(1002.7810, 1046.2510), (1002.9796, 1046.2746)],
         layer="M2605", elevation=100.436)
polyline([(1008.9494, 1046.9834), (1009.1480, 1047.0070)],
         layer="M2605", elevation=100.473)

# --- 22)  Roof gutter chain 78-85-86-87-88 (M2200) --------------------------
line((1005.4349, 1051.5133, 0.0), (1018.0460, 1052.5790, 0.0), layer="M2200")
line((1005.2600, 1053.5830, 0.0), (1005.4349, 1051.5133, 0.0), layer="M2200")
line((980.6087684, 1051.7710460, 0.0), (980.8377709, 1049.4544700, 0.0), layer="M2200")
line((998.9490, 1050.9210, 0.0), (998.7903567, 1052.9147001, 0.0), layer="M2200")
line((980.8377709, 1049.4544700, 0.0), (992.9985806, 1050.4391736, 0.0), layer="M2200")
line((992.9985806, 1050.4391736, 0.0), (998.9490, 1050.9210, 0.0), layer="M2200")

# Veranda offset stripes
polyline([(991.6310, 1045.3960), (991.2342, 1050.2963)], layer="M2605")
polyline([(980.9633, 1047.9225), (981.2400, 1044.5450),
          (989.0230, 1045.1820), (988.6260, 1050.0851)], layer="M2605")
polyline([(991.2342, 1050.2963), (991.6310, 1045.3960),
          (999.6740, 1046.0360), (998.9490, 1050.9210)], layer="M2605")
polyline([(991.4336, 1050.3124), (991.8142, 1045.6112),
          (999.4447, 1046.2184), (998.7512, 1050.8916)], layer="M2605")
polyline([(981.1626, 1047.9386), (981.4230, 1044.7606),
          (988.8075, 1045.3650), (988.4266, 1050.0690)], layer="M2605")
line((981.2400, 1044.5450, 100.649), (989.0230, 1045.1820, 100.649), layer="M2605")
line((991.6310, 1045.3960, 0.0), (999.6740, 1046.0360, 0.0), layer="M2605")

# Stripe-pattern ladder (M2417) between 80-81 area
_y0 = 1045.182                                                # first stripe y
for i, dy in enumerate([0.0, 0.299, 0.598, 0.897, 1.196, 1.495,
                        1.794, 2.093, 2.392, 2.691, 2.990,
                        3.289, 3.588, 3.887, 4.186, 4.485,
                        4.784, 5.083, 5.382, 5.681, 5.980,
                        6.279, 6.578, 6.877, 7.176]):
    y_a = _y0 + 0.299 * i
    if y_a > 1050.5:
        break
    pass

# --- 23)  Drive entry at 64/65 toward 73-74-75 ------------------------------
polyline_pts("73", "74", layer="M2200")
polyline_pts("75", "74", layer="M2200")
polyline_pts("78", "75", layer="M2200")

# --- 24)  M2412 tree-line curb (path along north of lot) --------------------
polyline_pts("94", "93", "92", "91", layer="M2412")
polyline([(965.4210, 1029.9680), (972.9190, 1030.6560),
          (976.5330, 1030.9150)], layer="M2412", elevation=100.697)
polyline([(964.8679, 1035.9953), (972.4261, 1036.6888),
          (975.9730, 1036.9430)], layer="M2412", elevation=100.697)
polyline([(978.5810, 1031.0880), (999.2180, 1032.8670)],
         layer="M2412", elevation=100.585)
polyline([(1001.2880, 1033.0750), (1008.5640, 1033.7060)],
         layer="M2412", elevation=100.378)
polyline([(1000.7950, 1039.0820), (1015.7270, 1040.3130)],
         layer="M2412", elevation=100.378)
polyline([(978.0210, 1037.1160), (998.7250, 1038.8740)],
         layer="M2412", elevation=100.481)
# Tree-line bumpers (M2404 short verticals between curb lines)
for x_pair, y_pair in [
    ((976.5330, 978.5810), (1030.9150, 1031.0880)),
    ((978.0210, 978.5810), (1037.1160, 1031.0880)),
    ((975.9730, 976.5330), (1036.9430, 1030.9150)),
    ((975.9730, 978.0210), (1036.9430, 1037.1160)),
    ((998.7250, 999.2180), (1038.8740, 1032.8670)),
    ((998.7250, 1000.7950), (1038.8740, 1039.0820)),
    ((999.2180, 1001.2880), (1032.8670, 1033.0750)),
    ((1000.7950, 1001.2880), (1039.0820, 1033.0750))]:
    line((x_pair[0], y_pair[0], 100.481),
         (x_pair[1], y_pair[1], 100.481), layer="M2404")

# --- 25)  Hatched gravel / shoulder patches  (M2299 DOTS) -------------------
# Several patches in original — keep a few representative ones
for boundary in [
    [(1010.46, 1046.93), (1013.93, 1047.23),
     (1013.91, 1047.43), (1010.44, 1047.14)],
    [(972.382, 1043.754), (977.281, 1044.234),
     (976.788, 1049.263), (971.889, 1048.783)],
    [(1003.066, 1009.488), (1002.228, 1009.411),
     (1002.849, 1002.642), (1003.066, 1009.488)],
]:
    hatch_dots(boundary, layer="M2299", scale=10.0)

# --- 26)  Pipe / property-line annotations (C1609 line blocks) --------------
def add_line_annotation(insert, rotation, length_text):
    ref = msp.add_blockref("C1609", insert,
                           dxfattribs={"layer": "C1609",
                                       "rotation": rotation,
                                       "xscale": 0.25, "yscale": 0.25, "zscale": 0.25})
    ref.add_auto_attribs({"CALC_LENGTH": length_text})

add_line_annotation((1010.3405,  996.5725, 0.0), 274.71, "6.68")
add_line_annotation((1010.1890, 1002.5437, 0.0),  94.97, "5.24")
add_line_annotation(( 982.9335,  980.8190, 0.0),   4.58, "5.93")
add_line_annotation(( 991.0330,  981.5055, 0.0),   4.79, "5.90")
add_line_annotation((1009.0280, 1015.8865, 0.0),  93.97, "10.20")
add_line_annotation(( 997.8397, 1017.3178, 0.0),   4.85, "8.98")
add_line_annotation((1002.6895, 1013.5925, 0.0), 275.24, "8.24")
add_line_annotation((1002.6470, 1009.4496, 0.0), 185.24, "0.84")
add_line_annotation((1002.5385, 1006.0266, 0.0), 275.24, "6.80")
add_line_annotation((1001.1330, 1002.5060, 0.0), 184.53, "3.44")
add_line_annotation(( 999.1140, 1006.1938, 0.0),  94.53, "7.67")
add_line_annotation(( 995.9645, 1009.7838, 0.0), 184.69, "5.71")
add_line_annotation(( 993.2860, 1007.5500, 0.0), 274.80, "4.01")
add_line_annotation(( 991.4280, 1005.3765, 0.0), 184.89, "4.07")
add_line_annotation(( 988.8040, 1012.0710, 0.0),  94.98, "13.79")
add_line_annotation(( 990.6730, 1019.1665, 0.0),   5.27, "4.95")
add_line_annotation(( 993.2532, 1018.1663, 0.0), 275.27, "2.47")

# --- 27)  M1000_E descriptive leaders (text along walls / pipes) -------------
label("שמאל",             (1004.8546, 1029.6663, 0.0), rotation=0)
label("צינור",            (1014.2035, 1021.4752, 0.0), rotation=3.97)
label("גג",               (1015.0396, 1016.6175, 0.0), rotation=273.94)
label("עץ דקל",           (986.0545, 1015.7655, 0.0),  rotation=279.11)
label("צינור גג",         (1002.7227, 1013.3005, 0.0), rotation=274.79)
label("צינור",            (1012.1506,  998.6349, 0.0), rotation=274.75)
label("צינור",            (1003.7002,  967.2461, 0.0), rotation=4.70)
label("צינור",            ( 987.9277,  977.4369, 0.0), rotation=1.10)
label("צינור",            ( 981.9117,  997.7234, 0.0), rotation=274.75)
label("צינור",            ( 993.4874, 1013.0879, 0.0), rotation=274.98)
label("דפנת.גג",          ( 997.4086, 1014.3043, 0.0), rotation=274.98)
label("צינור",            (1003.5289, 1023.3864, 0.0), rotation=0.69)
label("ברז עם זרבובית",   ( 968.0927, 1021.0304, 0.0), rotation=274.14)
label("גובה",             ( 985.8613, 1022.0274, 0.0), rotation=275.48)
label("גובה",             (1004.0865, 1013.6409, 0.0), rotation=274.79)
label("גובה",             (1001.4389, 1023.9167, 0.0), rotation=277.07)
label("עץ דקל",           (1008.0463, 1036.9357, 0.0), rotation=274.69)
label("עץ דקל",           ( 969.8722, 1033.4222, 0.0), rotation=275.31)
label("עץ דקל",           ( 987.5393, 1035.3441, 0.0), rotation=275.31)
label("ברז עם זרבובית",   (1005.4928, 1048.1598, 0.0), rotation=274.14)
label("צופית",            ( 999.8052, 1036.0576, 0.0), rotation=274.69)
label("צופית",            ( 977.0221, 1034.3104, 0.0), rotation=275.31)
label("ברז עם זרבובית",   ( 974.2526, 1046.9489, 0.0), rotation=274.14)
label("צופית",            ( 971.7494, 1042.6417, 0.0), rotation=275.31)
label("צופית",            (1000.9241, 1045.6137, 0.0), rotation=275.31)
label("צופית",            (1017.1651, 1028.2796, 0.0), rotation=275.31)
label("צופית",            ( 990.9494, 1026.1934, 0.0), rotation=275.31)
label("צופית",            ( 972.1585, 1024.6501, 0.0), rotation=275.31)
label("סנחם",             ( 988.6026,  995.2478, 0.0), rotation=274.38)
label("צינור",            ( 992.2502,  995.4942, 0.0), rotation=274.38)
label("הרקומת ציפור",     ( 995.7875, 1007.9070, 0.0), rotation=274.80)
label("צרפם",             ( 983.8362, 1048.7280, 0.0), rotation=4.63)
label("צרפם",             ( 995.0784, 1049.6120, 0.0), rotation=4.55)
label("צופית",            ( 988.0512,  999.6479, 0.0), rotation=275.27)
label("צופית",            ( 990.8492, 1020.5552, 0.0), rotation=275.27)

# --- 28)  Diameter-callout texts (Ø=...) -------------------------------------
text("%%C=0.70", (981.281, 1031.500, 0.0))
text("%%C=0.40", (989.009, 1032.256, 0.0))
text("%%C=0.40", (995.367, 1032.678, 0.0))
text("%%C=0.40", (992.504, 1036.972, 0.0))
text("%%C=0.40", (1011.005, 1038.659, 0.0))
text("%%C=0.40", (974.312, 1035.212, 0.0))
text("%%C=0.50", (1002.803,  987.477, 0.0))
text("%%C=0.50", ( 984.717, 1035.837, 0.0))
text("%%C=0.20", ( 978.906, 1035.769, 0.0))
text("%%C=0.20", ( 972.299, 1032.178, 0.0))
text("%%C=0.20", ( 968.353, 1030.501, 0.0))
text("%%C=0.20", (1005.421, 1004.404, 0.0))
text("%%C=0.30", ( 968.613, 1034.850, 0.0))
text("%%C=0.30", (1005.661, 1000.901, 0.0))
text("%%C=0.10", (1005.311, 1002.179, 0.0))

# ============================================================================
#  SAVE
# ============================================================================
OUTFILE = "survey_rebuilt.dxf"
doc.saveas(OUTFILE)
print(f"Wrote {OUTFILE}")