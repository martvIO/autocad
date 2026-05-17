import ezdxf

def decode_text(s):
    """Replace common AutoCAD control codes with readable characters."""
    return (s.replace("%%C", "Ø").replace("%%c", "Ø")
             .replace("%%D", "°").replace("%%d", "°")
             .replace("%%P", "±").replace("%%p", "±")
             .replace("%%U", "").replace("%%O", ""))

def dump_all_attribs(e, f, indent="  "):
    """Write every DXF attribute that exists on the entity."""
    for key, value in e.dxfattribs().items():
        f.write(f"{indent}{key} = {value}\n")

def run():
    
    input_path = r"26357.dxf"
    output_path = r"26357_entities.txt"
    inputs = {
        "Points",
        "Lines",
        "Arcs",
        "Texts",
        "InsertedTexts",
        "MTexts",

    }
    doc = ezdxf.readfile(input_path)
    msp = doc.modelspace()

    with open(output_path, "w", encoding="utf-8") as f:
        for e in msp:
            etype = e.dxftype()
            f.write(f"=== {etype} (handle {e.dxf.handle}) ===\n")

            if etype == "TEXT":
                f.write(f"  text:         {decode_text(e.dxf.text)!r}\n")
                f.write(f"  raw_text:     {e.dxf.text!r}\n")
                f.write(f"  position:     {e.dxf.insert}\n")
                f.write(f"  height:       {e.dxf.height}\n")
                f.write(f"  rotation:     {e.dxf.get('rotation', 0)}\n")
                f.write(f"  width_factor: {e.dxf.get('width', 1.0)}\n")
                f.write(f"  oblique:      {e.dxf.get('oblique', 0)}\n")
                f.write(f"  style:        {e.dxf.get('style', 'Standard')}\n")
                f.write(f"  halign:       {e.dxf.get('halign', 0)}\n")
                f.write(f"  valign:       {e.dxf.get('valign', 0)}\n")
                f.write(f"  align_point:  {e.dxf.get('align_point', None)}\n")
                f.write(f"  layer:        {e.dxf.layer}\n")
                f.write(f"  -- all attribs --\n")
                dump_all_attribs(e, f, indent="    ")
                data = {
                    'text': e.dxf.text!r,
                    'position': [e.dxf.insert[0],e.dxf.insert[1]],
                    'height': e.dxf.height,
                    'rotation': e.dxf.get('rotation', 0),
                    'layer': e.dxf.layer
                }
                inputs["Texts"].add(data)

            elif etype == "INSERT":
                f.write(f"  block_name:   {e.dxf.name}\n")
                f.write(f"  position:     {e.dxf.insert}\n")
                f.write(f"  xscale:       {e.dxf.get('xscale', 1.0)}\n")
                f.write(f"  yscale:       {e.dxf.get('yscale', 1.0)}\n")
                f.write(f"  zscale:       {e.dxf.get('zscale', 1.0)}\n")
                f.write(f"  rotation:     {e.dxf.get('rotation', 0)}\n")
                f.write(f"  row_count:    {e.dxf.get('row_count', 1)}\n")
                f.write(f"  column_count: {e.dxf.get('column_count', 1)}\n")
                f.write(f"  layer:        {e.dxf.layer}\n")
                # ATTRIB sub-entities (the visible labels attached to the block)
                attribs = list(e.attribs)
                if attribs:
                    f.write(f"  -- attached ATTRIBs ({len(attribs)}) --\n")
                    for a in attribs:
                        f.write(f"    ATTRIB tag={a.dxf.tag!r}\n")
                        f.write(f"      text:     {decode_text(a.dxf.text)!r}\n")
                        f.write(f"      position: {a.dxf.insert}\n")
                        f.write(f"      height:   {a.dxf.height}\n")
                        f.write(f"      rotation: {a.dxf.get('rotation', 0)}\n")
                        f.write(f"      layer:    {a.dxf.layer}\n")
                        f.write(f"      -- all attrib attribs --\n")
                        print(a.dxf.tag!r)
                        if e.dxf.name is 'M1000_E' and a.dxf.tag == 'DESC':
                            data = {
                                'text': a.dxf.text!r,
                                'position': [a.dxf.insert[0],a.dxf.insert[1]],
                                'height': a.dxf.height,
                                'rotation': a.dxf.get('rotation', 0),
                                'layer': e.dxf.layer
                            }
                            for key, value in e.dxfattribs().items():
                                if key in ["insert", "align_point"]:
                                    data[key] = [value[0], value[1]]
                                elif key in ["style"]:
                                    data[key] = value
                            inputs["InsertedTexts"].add(data)
                        dump_all_attribs(a, f, indent="        ")
                f.write(f"  -- all insert attribs --\n")
                dump_all_attribs(e, f, indent="    ")

            elif etype == "LWPOLYLINE":
                f.write(f"=== LWPOLYLINE (handle {e.dxf.handle}) ===\n")
                f.write(f"  Layer:     {e.dxf.layer}\n")
                f.write(f"  Elevation: {e.dxf.get('elevation', 0)}\n")
                f.write(f"  Closed:    {e.closed}\n")

                for i, sub in enumerate(e.virtual_entities()):
                    stype = sub.dxftype()
                    if stype == "LINE":
                        s, end = sub.dxf.start, sub.dxf.end
                        length = ((end.x - s.x) ** 2 + (end.y - s.y) ** 2) ** 0.5
                        f.write(f"  [{i}] LINE\n")
                        f.write(f"        start:  ({s.x:.4f}, {s.y:.4f}, {s.z:.4f})\n")
                        f.write(f"        end:    ({end.x:.4f}, {end.y:.4f}, {end.z:.4f})\n")
                        f.write(f"        length: {length:.4f}\n")
                    elif stype == "ARC":
                        c = sub.dxf.center
                        f.write(f"  [{i}] ARC\n")
                        f.write(f"        center:      ({c.x:.4f}, {c.y:.4f}, {c.z:.4f})\n")
                        f.write(f"        radius:      {sub.dxf.radius:.4f}\n")
                        f.write(f"        start_angle: {sub.dxf.start_angle:.4f}°\n")
                        f.write(f"        end_angle:   {sub.dxf.end_angle:.4f}°\n")
                        # Compute the actual start/end points of the arc
                        import math
                        sa = math.radians(sub.dxf.start_angle)
                        ea = math.radians(sub.dxf.end_angle)
                        r = sub.dxf.radius
                        sp = (c.x + r * math.cos(sa), c.y + r * math.sin(sa))
                        ep = (c.x + r * math.cos(ea), c.y + r * math.sin(ea))
                        f.write(f"        start_pt:    ({sp[0]:.4f}, {sp[1]:.4f})\n")
                        f.write(f"        end_pt:      ({ep[0]:.4f}, {ep[1]:.4f})\n")
                    else:
                        f.write(f"  [{i}] {stype}: {sub.dxfattribs()}\n")

            elif etype == "LINE":
                f.write(f"  start: {e.dxf.start}\n")
                f.write(f"  end:   {e.dxf.end}\n")
                f.write(f"  layer: {e.dxf.layer}\n")
                dump_all_attribs(e, f, indent="    ")

            elif etype == "CIRCLE":
                f.write(f"  center: {e.dxf.center}\n")
                f.write(f"  radius: {e.dxf.radius}\n")
                f.write(f"  layer:  {e.dxf.layer}\n")
                dump_all_attribs(e, f, indent="    ")

            elif etype == "ARC":
                f.write(f"  center:      {e.dxf.center}\n")
                f.write(f"  radius:      {e.dxf.radius}\n")
                f.write(f"  start_angle: {e.dxf.start_angle}\n")
                f.write(f"  end_angle:   {e.dxf.end_angle}\n")
                f.write(f"  layer:       {e.dxf.layer}\n")
                dump_all_attribs(e, f, indent="    ")

            else:
                # Fallback: dump everything we can find
                dump_all_attribs(e, f, indent="  ")

            f.write("\n")

    print(f"Done. Wrote entities to {output_path}")

if __name__ == "__main__":
    run()