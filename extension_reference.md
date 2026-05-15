# MapPit 2025 — Complete Extension Reference

> Generated from source-code analysis of `C:\MapPit2025\`
> Date: 2026-05-14

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Startup Chain](#startup-chain)
3. [Binary Components](#binary-components)
4. [LISP Modules](#lisp-modules)
5. [DCL Dialogs](#dcl-dialogs)
6. [Menu Files](#menu-files)
7. [Configuration System](#configuration-system)
8. [Data Files](#data-files)
9. [Global State Variables](#global-state-variables)
10. [ARX-Exposed Functions](#arx-exposed-functions)
11. [Call Graph Summary](#call-graph-summary)

---

## Architecture Overview

MapPit is a five-layer system:

| Layer | Technology | Location |
|---|---|---|
| 1 | C++ ARX/BRX compiled extension | Root: `pit20xx_x64.ARX` / `.BRX` |
| 2 | .NET / COM components | Root: `TR_DotnetGui.dll`, `Pit2000COM.dll`, etc. |
| 3 | AutoLISP | `USR\`, `TRA_LSP\`, `tra_flex\`, `BricsCAD\` |
| 4 | DCL dialogs | `tra_dcl\`, `tra_flex\arf_dcl\` |
| 5 | Menu definitions | Root: `.mnu` / `.cuix` files |

---

## Startup Chain

### AutoCAD Path
```
USR\acad.mnl
  └─ (findfile "MAPIT-START.LSP") → loads USR\mapit-start.lsp
       ├─ Detects ACADVER / architecture
       ├─ arxload  pit20xx_x64.ARX  (version table below)
       ├─ load "TRA_ARX.LSP"
       ├─ load "TRA_LSP.LSP"
       │    ├─ tra_lsp\tra_kitz.lsp
       │    ├─ tra_lsp\tra_shrt.lsp
       │    ├─ tra_lsp\tra_utls.lsp
       │    ├─ tra_lsp\tra_rish.lsp
       │    ├─ tra_lsp\tra_tbl.lsp
       │    ├─ tra_lsp\tra_tool.lsp
       │    ├─ tra_lsp\tra_s2l.lsp
       │    ├─ tra_lsp\tra_utl.lsp
       │    ├─ tra_lsp\tra_ddt.lsp
       │    ├─ tra_lsp\tra_seld.lsp
       │    ├─ tra_lsp\tra_init.lsp
       │    ├─ tra_lsp\tra_ps.lsp
       │    ├─ tra_lsp\tra_idan.lsp
       │    ├─ tra_lsp\tra_epol.lsp
       │    ├─ tra_lsp\tr_taba.lsp
       │    ├─ tra_lsp\tr_pschg.lsp
       │    ├─ tra_lsp\demo.lsp
       │    ├─ tra_lsp\Image_helmert.lsp
       │    ├─ tra_lsp\tr_lyout.lsp  (if tr_flag2000)
       │    ├─ tra_flex\Tra_flex.lsp (flexible toolbar)
       │    ├─ tra_flex\flex_mnu.lsp
       │    └─ PitronimMnu.lsp
       └─ (tr_startup)  → calls _pitmenu
```

### BricsCAD Path
```
BricsCAD\on_start.lsp
  ├─ Detects ACADVER (20.1 through 25.0) → arxload pit20xx_x64.brx
  └─ load "Tra_brx.lsp"  (defines c:PitBrxMenu, c:HebBrxMenu)

BricsCAD\on_doc_load.lsp
  └─ load "Tra_lsp.lsp"  (then silent load)
```

### ARX Version Selection Table

| ACADVER string | AutoCAD release | Binary loaded |
|---|---|---|
| < "20" | 2014 and earlier | `pit2013_x64.ARX` |
| "20" | 2015/2016 | `pit2015_x64.ARX` |
| "21" | 2017/2018 | `pit2017_x64.ARX` |
| "22" | 2018 | `pit2018_x64.ARX` |
| "23" | 2019/2020 | `pit2019_x64.ARX` |
| "24" | 2021–2024 | `pit2021_x64.ARX` |
| "25" | 2025 | `pit2025_x64.ARX` |

### BRX Version Selection Table

| ACADVER | BricsCAD release | Binary loaded |
|---|---|---|
| "20.1" | BC 17 | `pit2017_x64.brx` |
| "21.0" | BC 18 | `pit2018_x64.brx` |
| "21.1" | BC 19 | `pit2019_x64.brx` |
| "22.0" | BC 20 | `pit2020_x64.brx` |
| "22.1" | BC 21 | `pit2021_x64.brx` |
| "22.2" | BC 22 | `pit2022_x64.brx` |
| "23.0" | BC 23 | `pit2023_x64.brx` |
| "24.0" | BC 24 | `pit2024_x64.brx` |
| "25.0" | BC 25 | `pit2025_x64.brx` |

---

## Binary Components

### ARX / BRX Extension DLLs (C++ compiled, content not readable)

| File | Purpose |
|---|---|
| `pit2013_x64.ARX` | AutoCAD 2014 and earlier core engine |
| `pit2015_x64.ARX` | AutoCAD 2015/2016 core engine |
| `pit2017_x64.ARX` | AutoCAD 2017/2018 core engine |
| `pit2018_x64.ARX` | AutoCAD 2018 variant core engine |
| `pit2019_x64.ARX` | AutoCAD 2019/2020 core engine |
| `pit2021_x64.ARX` | AutoCAD 2021–2024 core engine |
| `pit2025_x64.ARX` | AutoCAD 2025 core engine |
| `pit2017_x64.BRX` | BricsCAD 17 core engine |
| `pit2018_x64.BRX` | BricsCAD 18 core engine |
| `pit2019_x64.BRX` | BricsCAD 19 core engine |
| `pit2020_x64.BRX` | BricsCAD 20 core engine |
| `pit2021_x64.BRX` | BricsCAD 21 core engine |
| `pit2022_x64.BRX` | BricsCAD 22 core engine |
| `pit2023_x64.BRX` | BricsCAD 23 core engine |
| `pit2024_x64.BRX` | BricsCAD 24 core engine |
| `pit2025_x64.BRX` | BricsCAD 25 core engine |

### .NET / COM Components

| File | Purpose |
|---|---|
| `Pit2000COM.dll` | COM automation server; registered via `MapPit_REG_DLL_64BIT.bat` |
| `TR_DotnetGui.dll` | .NET GUI dialogs host |
| `DTM2.dll` | Digital Terrain Model (contour) engine |
| `GeneticAlgorithm.dll` | Parcel area optimization |
| `RnzPdfLib.dll` | PDF export wrapper |
| `itext.*.dll` | iTextSharp PDF generation library |
| `JsonIniDll.dll` | JSON/INI parsing helper |

---

## LISP Modules

### File: `USR\acad.mnl`
**Purpose:** AutoCAD MNL auto-loaded with every menu. Conditionally loads the MapPit startup chain.

No `(defun C:...)` commands defined. Executes inline:
- Loads `TEKENPLUS.LSP` if both `.lsp` and `.cuix` found
- Loads `VEGA.LSP` if both found
- Loads `TEAMCAD-START.LSP` if found
- Loads `MAPIT-START.LSP` if found (main entry point)

---

### File: `USR\mapit-start.lsp`
**Purpose:** Version detection, ARX binary selection, primary load sequencer.

**Side effects:**
- Sets `(setvar "ATTREQ" 0)` at startup
- arxloads the correct `.ARX` binary
- Loads `TRA_ARX.LSP` and `TRA_LSP.LSP`
- Calls `(_pitmenu)` to load the default menu

No `(defun C:...)` commands defined (commands come from loaded modules).

---

### File: `TRA_ARX.LSP`
**Purpose:** Defines menu-loading user commands. Sets `(setvar "plinetype" 2)` at load time.

| Command | Description | Parameters | Side Effects |
|---|---|---|---|
| `c:pitmenu` | Load English Pitronim main menu | none | Loads `pit_sub.mnu`; sets menubar=1 for acver≥17.2; activates pop20–pop23 |
| `c:hebmenu` | Load Hebrew Pitronim main menu | none | Loads `pit_heb.mnu`; activates pop20–pop23 |
| `c:tabamenu` | Load TABA land-use menu | none | Loads `tr_taba.mnu`; activates pop24 |
| `c:mamimenu` | Load MAMI menu | none | Loads `mami_heb.mnu` |
| `c:pit` | Legacy load command | none | Loads `tra_lsp` if not loaded; arxloads `pit14.arx` or `pit95.arx` |

---

### File: `TRA_LSP.LSP`
**Purpose:** Sequential loader for all utility modules. Defines `tr_load_lsp` helper.

| Function | Description |
|---|---|
| `tr_load_lsp(fname)` | Secure file loader: calls `findfile` to verify before `load`; prints error if not found |

No `(defun C:...)` commands; ends with `(tr_startup)`.

---

### File: `TRA_LSP\TRA_INIT.LSP`
**Purpose:** Initializes all global constants and extended-data app names.

**Global variables initialized:**

| Variable | Value | Description |
|---|---|---|
| `TRAppName` | `"TR_DXF"` | Extended data app name for MapPit entities |
| `NOTRAppName` | `"NOTR_DXF"` | App name for non-MapPit entities |
| `TRPname` | `"TR_PNAME"` | Point name xdata tag |
| `TRFname` | `"TR_FRONT"` | Front measurement block name |
| `TRAname` | `"TR_AREA"` | Area annotation block name |
| `TRLname` | `"TR_LOT"` | Lot name block name |
| `TRHname` | `"TR_HIGHT"` | Height annotation block name |
| `TRArcDT` | `"TR_ARCD"` | Arc data block name |
| `TRWrngLay` | list | Invalid layer name prefixes |
| `TRerrsDESC` | list | Error layer descriptions |
| `TRfilt0` | filter | Entity selection filter |
| `is_icad_ver` | bool | True if running IntelliCAD |
| `tr_flag2000` | bool | True if AutoCAD 2000+ (supports layouts) |
| `TRsel_T` | `1` | Selection type default |

| Function | Description |
|---|---|
| `tr_startup` | Sets `GRIPBLOCK=0`, initializes `STYLE_CMD` global |

---

### File: `TRA_LSP\TRA_UTLS.LSP`
**Purpose:** Core utility functions — filter constants, entity helpers, error management, text drawing.

| Function | Description | Parameters |
|---|---|---|
| `TRsetCONSTANTS` | Define selection filter atoms `<a`, `a>`, `<o`, `o>`, `<n`, `n>` | none |
| `TRgetDEFAULT` | Get value with default using supplied getter function | `getter`, `prompt`, `default` |
| `TRgetstringDEFAULT` | Get string with default | `prompt`, `default` |
| `TRgetSCALE` | Read current drawing scale from config | none; returns scale real |
| `TRfirstEPT` | Get first endpoint of entity | `ent` (entget list) |
| `TRsecEPT` | Get second endpoint of entity | `ent` |
| `TRputPOINT` | Insert a point entity | `pt`, `layer` |
| `TRsetERROR` | Install MapPit error handler | none |
| `TRunsetERROR` | Restore previous error handler | none |
| `TRsetERRORsnp` | Install error handler with snap save | `flag` |
| `TRunsetERRORsnp` | Restore error handler and snap | `flag` |
| `TRsetERRlay` | Set current layer and save state for error recovery | `style`, `layer` |
| `TRunsetERRlay` | Restore layer from saved state | none |
| `TRlineTXT` | Draw text centered along a line | `p1`, `p2`, `height`, `text` |

---

### File: `TRA_LSP\TRA_TOOL.LSP`
**Purpose:** Miscellaneous internal utilities — debugging, layer operations, geometry helpers, string tools.

| Function | Description | Parameters |
|---|---|---|
| `tr_brk(prom)` | Interactive breakpoint debugger | `prom` — prompt string |
| `tr_getblist(tbl_name)` | Get all items from a symbol table as list | `tbl_name` — e.g. "layer" |
| `tr_getLtbl()` | Get all layer table items | none |
| `tr_lviz(item)` | Check if layer item is visible (not frozen, color≥0) | `item` — layer tblnext entry |
| `tr_getvizl()` | Get list of all visible (non-locked) layers | none |
| `tr_getlockl()` | Get list of all locked layers | none |
| `tr_selviz(filtlst)` | `ssget "x"` filtered to visible layers | `filtlst` — additional filter |
| `tr_vizdxf()` | Write DXF of all visible-layer entities to temp file | none |
| `tr_fsubstr(str,subs)` | Find position of substring in string | `str`, `subs` |
| `tr_delsubs(str,subs)` | Delete first occurrence of substring | `str`, `subs` |
| `tr_remspace(s)` | Strip leading spaces | `s` |
| `tr_parses(str,cl)` | Parse string by column-spec list | `str`, `cl` — `((key (col len))...)` |
| `tr_vlname(name,goodl)` | Validate layer name against `TRWrngLay` | `name`, `goodl` — allowed exceptions |
| `tr_entget(ename)` | `entget` with TR_DXF xdata | `ename` |
| `tr_entsget()` | Interactive entity select with TR_DXF xdata | none |
| `notr_entsget()` | Interactive entity select with NOTR_DXF xdata | none |
| `notr_gil_str_last(gilnum,usestr,locstr)` | Attach NOTR_DXF xdata to last entity | `gilnum`, `usestr`, `locstr` |
| `notr_move(e)` | Move entity to NOTR_DXF app | `e` — entget list |
| `notr_do()` | Interactive: select entity and NOTR_move it | none |
| `notr_last()` | NOTR_move last entity | none |
| `notr_set()` | Interactive: select set and NOTR_move all | none |
| `tr_getatt(iname)` | Get first attribute after INSERT ename | `iname` |
| `tr_getmaine(name)` | Get main entity ename from sub-entity ename | `name` — ATTRIB or VERTEX ename |
| `tr_entselp(pt)` | Get main entity at point (handles nested) | `pt` — pick point |
| `tr_setcurr(lname)` | Create layer if needed and set current | `lname` |
| `tr_veriflay(lname)` | Create layer if not exists; return name | `lname` |
| `tr_docomm(com)` | Execute command allowing arbitrary user input | `com` — command string |
| `scale_size(x)` | Multiply by global `scale` variable | `x` — real |
| `tr_direc(pnt,size)` | Move point in global `dirc` direction | `pnt`, `size` |
| `tr_up(pnt,size)` | Move point up (90°) | `pnt`, `size` |
| `tr_down(pnt,size)` | Move point down (270°) | `pnt`, `size` |
| `tr_right(pnt,size)` | Move point right (0°) | `pnt`, `size` |
| `tr_left(pnt,size)` | Move point left (180°) | `pnt`, `size` |
| `tr_mid(p1,p2)` | Midpoint of two points | `p1`, `p2` |
| `tra_open(bdir,fname,mode)` | Open file using full path via `TRFULP_A` | `bdir`, `fname`, `mode` |
| `tredit(fname)` | Edit file using configured editor | `fname` |

---

### File: `TRA_LSP\TRA_S2L.LSP`
**Purpose:** String/list parsing utilities and selection-set iteration helpers. No C: commands.

| Function | Description | Parameters |
|---|---|---|
| `tr_str2list(str)` | Parse space-separated string into list | `str` |
| `tr_fpref(path)` | Extract filename prefix (basename without extension) | `path` |
| `TR_matchar(charlist,str)` | Find first char from list in string; return position | `charlist`, `str` |
| `tr_princ(item)` | Print item including lists (overrides normal princ) | `item` |
| `TRdoSETfp(fn,ss,fp)` | Iterate selection set calling fn with ename, index, file pointer | `fn`, `ss`, `fp` |
| `TRdoSET(fn,ss)` | Iterate selection set calling fn with ename, index | `fn`, `ss` |
| `TRgetPTstr` | Point-get string keyword placeholder | — |
| `TRgetPTkw(getter,prompt,kwlist)` | Get point or keyword | `getter`, `prompt`, `kwlist` |

---

### File: `TRA_LSP\TRA_KITZ.LSP`
**Purpose:** Short-name command aliases (AutoCAD shortcuts and Pitronim shortcuts).

#### AutoCAD Shortcut Commands

| Command | Delegates to | Description |
|---|---|---|
| `c:zw` | `command "_.zoom" "w"` | Zoom window |
| `c:zp` | `command "_.zoom" "p"` | Zoom previous |
| `c:zd` | `command "_.zoom" "d"` | Zoom dynamic |
| `c:zv` | `command "_.zoom" "vmax"` | Zoom vmax |
| `c:ze` | `command "_.zoom" "e"` | Zoom extents |
| `c:ch` | `command "_.change"` | Change entity properties |
| `c:li` | `command "_.list"` | List entity |
| `c:ex` | `command "_.extend"` | Extend |
| `c:x` | `command "_.explode"` | Explode |
| `c:of` | `command "_.offset"` | Offset |
| `c:tr` | `command "_.trim"` | Trim |
| `c:f` | `command "_.fillet"` | Fillet (current radius) |
| `c:fr` | `command "_.fillet" "r"` | Fillet — set radius |
| `c:laa` | `command "_.layer"` | Layer command |

#### Pitronim Shortcut Commands

| Command | Delegates to | Description |
|---|---|---|
| `c:con` | `c:trlincon` | Auto-connect survey points into lines |
| `` c:` `` | `c:trqmove` | Quick move (pick and move) |
| `c:1` | `c:trqmany` | Quick many (repeat insert/move) |
| `c:2` | `c:trqed` | Quick edit text/attribute |
| `c:3` | `c:trqhetz` | Draw survey boundary marker (hetz) |
| `c:33` | `c:trqhetzHANIT` | Draw survey boundary marker (HANIT variant) |
| `c:4` | `c:tranots` | Annotate single entity |
| `c:5` | `c:trqsum` | Sum front measurements with error calc |
| `c:6` | `c:trpvalh` | Show/hide point value heights |
| `c:d1` | `c:dist1` | Show distance label on one line |
| `c:d2` | `c:trqdist` | Show distance between two picked points |
| `c:er1` | error command 1 | Unknown; delegates to specific error layer command |
| `c:er2` | error command 2 | Unknown |
| `c:er3` | error command 3 | Unknown |
| `c:er4` | error command 4 | Unknown |
| `c:er5` | error command 5 | Unknown |
| `c:er6` | error command 6 | Unknown |
| `c:er7` | error command 7 | Unknown |
| `c:er8` | error command 8 | Unknown |
| `c:lpl` | `labelsplacer_a` (ARX) | Run labels placement optimizer |

---

### File: `TRA_LSP\TRA_SHRT.LSP`
**Purpose:** Layer management, quick operations, boundary and measurement commands.

| Command | Description | Parameters / Interaction |
|---|---|---|
| `c:trsle` | Set current layer by picking entity | Pick entity → sets its layer current |
| `c:trstol` | Move entities to another layer | Pick entities; prompts for target layer |
| `c:trn2l` | Set points by name wildcard to layer | Prompts for name wildcard and layer |
| `c:trdle` | Delete all entities on a layer | Prompts for layer name |
| `c:trfle` | Freeze a layer | Prompts for layer name |
| `c:trl2l` | Move all entities from one layer to another | Prompts for source and target layer |
| `c:trshl1` | Show only one layer (freeze all others) | Prompts for layer name |
| `c:trshls` | Show multiple named layers | Prompts for list of layer names |
| `c:trrestl` | Restore layer visibility state | Restores previously saved state |
| `c:trqmove` | Quick move: pick entity then pick new location | Interactive; calls `mmove` |
| `c:trqrot` | Quick rotate: pick entity then rotation center + angle | Interactive |
| `c:trqmany` | Repeat quick move multiple times | Loops until Enter; calls `mmove` |
| `c:trqhetz` | Draw survey boundary marker (TRA_SYS hetz block) | Pick insertion point, enter attributes |
| `c:trqhetzHANIT` | Draw boundary marker (HANIT hetz block) | Pick point; HANIT code system |
| `c:trqsum` | Sum front lengths with error calculation | Select fronts; shows total + closure error |
| `c:trqsumhanit` | Sum fronts (HANIT variant) | HANIT code system variant |
| `c:trqed` | Interactive text/attribute editor with duplicate check | Pick text/attrib; edit value; checks for duplicates |
| `c:trqdim` | Draw dimensioned text along line | Pick line; insert dimension annotation |
| `c:trqdist` | Show distance between two picked points | Pick two points; inserts TR_FRONT block |

---

### File: `TRA_LSP\TRA_UTL.LSP`
**Purpose:** Primary utility module — point import, connection, insert, error, layer, configuration.

#### Lot Naming

| Command | Description |
|---|---|
| `c:TRAnameLOTS` | Interactive lot naming: pick inside polygon, assign sequential number |
| `c:TRAnameLOTS_CDCD` | HANIT variant lot naming |

#### Point File Import / Conversion

| Command | Description |
|---|---|
| `c:trxcnv` | Import/convert XYZ survey points from file |
| `c:trlotcnv` | Import lot points from file |
| `c:trdigicnv` | Import digitizer points |
| `c:trpcnv` | Import P-format points |
| `c:trgcnv` | Import G-format points |
| `c:trpreadcsv` | Import points from CSV file |

#### Connection Commands

| Command | Description |
|---|---|
| `c:trxcon` | Auto-connect XYZ points into lines |
| `c:trlotcon` | Connect lot points |
| `c:trpcon` | Connect P-format points |
| `c:trpconcsv` | Connect CSV points |
| `c:trgcon` | Connect G-format points |

#### Insert Commands

| Command | Description |
|---|---|
| `c:trgpnt` | Insert survey points from G-file |
| `c:trgfro` | Insert front measurements |
| `c:trglot` | Insert lot data |
| `c:trgare` | Insert area data |
| `c:trgarc` | Insert arc data |
| `c:trgall` | Insert all: points, fronts, lots, areas |
| `c:trghigh` | Insert height annotations |
| `c:trgobj` | Insert lines/arcs from data |
| `c:trgbrd` | Insert border/boundary |
| `c:trdrawpoly` | Draw polylines from point data |
| `c:trdrawpoly_CDCD` | Draw polylines (HANIT/CDCD variant) |

#### Error Handling

| Command | Description |
|---|---|
| `c:trgerr` | Read and display DXF error file |
| `c:trsherr` | Show error entities |
| `c:trerr1` | Show error layers only (hide all others) |
| `c:trrsterrl` | Restore layer state after error display |
| `c:trsherrl` | Show error layer |
| `c:trhiderrl` | Hide error layer |
| `c:trnoterr` | Mark entity as not an error |
| `c:trclrerr` | Clear error markers |

#### Snap Shots

| Command | Description |
|---|---|
| `c:spa` | Add current view/layer state as snapshot |
| `c:spd` | Delete snapshot |
| `c:sps` | Show (restore) snapshot |
| `c:trsnp` | Open snap shots DCL dialog |

#### Block / Entity Inspection

| Command | Description |
|---|---|
| `c:trecods` | Entity codes DCL dialog — inspect entity's codes |
| `c:trlcods` | Layer codes DCL dialog — inspect layer's codes |
| `c:pitconf` | Configuration DCL dialog — edit TR_CFG.INI parameters |

#### Layer Visualization

| Command | Description |
|---|---|
| `c:SHOWlayers` | Show standard MapPit layers |
| `c:SHOWlayersCADCAD` | Show HANIT (CADCAD) layers |

#### Layer Preparation

| Command | Description |
|---|---|
| `c:TRprepTZR` | Prepare TZR (parcel) layers |
| `c:TRprepGUSH` | Prepare GUSH (block) layers |
| `c:TRprepGUSH2` | Prepare GUSH2 layers |
| `c:TRprepGUSH_Hanit` | Prepare GUSH layers (HANIT) |
| `c:TRprepTZR_CDCD` | Prepare TZR layers (CDCD) |
| `c:TRprepGUSH_CDCD` | Prepare GUSH layers (CDCD) |

#### Gush Operations

| Command | Description |
|---|---|
| `c:MARKgush` | Mark gush (cadastral block) boundaries |
| `c:SELECTgush` | Select entities in a gush |

#### Coordinate / Transformation

| Command | Description |
|---|---|
| `c:trtrns` | Coordinate transformation (up to 7 points) using DCL `tr_trans` |
| `c:trtrns25` | Coordinate transformation (up to 25 control points) |

#### Legend / Annotation

| Command | Description |
|---|---|
| `c:trlgnd` | Insert symbol legend block |
| `c:tranots` | Annotate single entity (insert annotation block) |
| `c:trsect` | Define and manage sectors for map sheets |
| `c:trcoords` | Insert coordinate annotation at picked point |

#### HANIT-Specific

| Command | Description |
|---|---|
| `c:tr_CorBldCalc` | Area correlation build calculation |
| `c:tr_CreateHanitFronts` | Create HANIT front measurement entities |
| `c:tr_CreateHanitHekFronts` | Create HANIT HEK front entities |
| `c:tr_CreateHanitHekPolygons` | Create HANIT HEK polygon entities |

---

### File: `TRA_LSP\TRA_TBL.LSP`
**Purpose:** Table insertion commands for gush, TZR parcel, transfer, HEK, TTG, area, and coordinate tables.

| Command | Description |
|---|---|
| `c:KRinsGUSH` | Insert GUSH area table (right-to-left, auto-select) |
| `c:TRinsGUSH` | Insert GUSH area table (left-to-right, auto-select) |
| `c:KRinsGUSH2` | Insert GUSH2 table (user-selection variant) |
| `c:TRinsGUSH2` | Insert GUSH2 table (user-selection, left-to-right) |
| `c:TRinsTZR` | Insert TZR parcel summary table |
| `c:TRinsTZR_CDCD` | Insert TZR table (CDCD/HANIT variant) |
| `c:TRinsTZR_HANIT_old` | Insert TZR table (old HANIT format) |
| `c:trinstzr_hanit` | Insert TZR table (new HANIT; calls `TRTAZARTABLE_A`) |
| `c:TRinsTRNS` | Insert transfer (TRNS) table |
| `c:TRinsTRNS_CDCD` | Insert transfer table (CDCD variant) |
| `c:TRinsTRNS_HANIT` | Insert transfer table (HANIT variant) |
| `c:TRinsHEK_HANIT` | Insert HEK table (HANIT) |
| `c:TRinsTTG_HANIT` | Insert TTG (Taba-Tatag) table (HANIT) |
| `c:TRinsHanitAreasTable` | Insert lot areas table (HANIT) |
| `c:TRinsCOORD` | Insert coordinate table |
| `c:trtranslots` | Transfer lots between records |

---

### File: `TRA_LSP\TRA_DDT.LSP`
**Purpose:** Primary dialog-driven survey data operations and 3D Cadastre (TAMAR) commands.

**Global state at load:**
```lisp
(setq trchk_p 1   ; check-points flag
      trplc_l 1   ; place-lines flag
      trstp_n 3   ; stop number
      trlay_c ""  ; current layer code
      tra_ss nil  ; selection set
      trch_cf nil ; config-changed flag
)
```

#### Main Survey Dialog Commands

| Command | DCL dialog | Description |
|---|---|---|
| `c:tr_points` | `tra_ddt.dcl / tr_points` | Add/modify POINTS: check pts, place pts, snap, scale, layer |
| `c:tr_linarc` | `tra_ddt.dcl / tr_linarc` | Modify LINES AND ARCS: break long lines, replace existing |
| `c:tr_parc` | `tra_ddt.dcl / tr_parc_def` | PARCELS DEFINITION: lot code, correlation steps |
| `c:tr_topo` | `tra_ddt.dcl / tr_topo_dlg` | Auto Topology: build topological relationships |
| `c:tr_cor_build` | `tra_ddt.dcl / tr_areas_cor` | Areas Correlation build dialog |
| `c:tr_set_gush` | `tra_ddt.dcl / tr_set_gush` | Set Block to Lots dialog |
| `c:TRoutFILES` | `tra_ddt.dcl / tr_outfiles` | Output ASCII FILES dialog |
| `c:tr_parts` | `tra_ddt.dcl / tr_parts_cor` | Parts correlation dialog |
| `c:tr_plan` | `tra_ddt.dcl / tr_plan_cor` | Plan correlation dialog |
| `c:tr_plans` | `tra_ddt.dcl / tr_plans_cor` | Multiple plans correlation dialog |

#### 3D Cadastre (TAMAR) Commands
All delegate to `(trtmrcommand_a "keyword")`:

| Command | Keyword | Description |
|---|---|---|
| `c:BuildSolid` | `"BuildSolid"` | Build 3D solid from parcel |
| `c:Extrude2Solid` | `"Extrude2Solid"` | Extrude parcel to solid |
| `c:UnifySolid` | `"UnifySolid"` | Unify adjacent solids |
| `c:SubtractSolid` | `"SubtractSolid"` | Subtract solid from another |
| `c:Add3dParcel` | `"Add3dParcel"` | Add new 3D parcel definition |
| `c:ParcelsDeduction` | `"ParcelsDeduction"` | Parcel area deduction |
| `c:Ins_parcel_table` | `"Ins_parcel_table"` | Insert parcel table |
| `c:Ins_Subtract_table` | `"Ins_Subtract_table"` | Insert subtraction table |
| `c:splitparcels` | `"splitparcels"` | Split parcel interactively |
| `c:Ins_Divide_parcel_table` | `"Ins_Divide_parcel_table"` | Insert parcel division table |
| `c:Unify_parcels` | `"Unify_parcels"` | Unify parcels |
| `c:UnifyLoop_parcels` | `"UnifyLoop_parcels"` | Loop unify parcels |
| `c:Ins_Unify_parcel_Table` | `"Ins_Unify_parcel_Table"` | Insert unification table |
| `c:Parcels_Gush_Transfer` | `"Parcels_Gush_Transfer"` | Transfer parcels between gush blocks |
| `c:Ins_Gush_Transfer_table` | `"Ins_Gush_Transfer_table"` | Insert gush transfer table |
| `c:Difine_Section` | `"Difine_Section"` | Define cross-section plane |
| `c:Cross_Section` | `"Cross_Section"` | Generate cross-section view |
| `c:splitparcels_prompt` | `"splitparcels_prompt"` | Split parcel with prompt |
| `c:POINTS_SURFACE` | `"POINTS_SURFACE"` | Create surface from points |
| `c:POLYS_SURFACE` | `"POLYS_SURFACE"` | Create surface from polygons |

#### 2024 Special Commands

| Command | ARX function | Description |
|---|---|---|
| `c:raznizav` | `TRraznizav_A` | Raznizav (difference) calculation |
| `c:RESTOREraznizav` | `TRRNZRESTORE_A` | Restore raznizav state |
| `c:trLotTreeView` | `TR_SHOWLOTTREE_A` | Show lot tree view (.NET UI) |
| `c:trtazarmenu` | `TR_SHOWTAZARUI_A` | Show TAZAR UI (.NET) |

---

### File: `TRA_LSP\TRA_PS.LSP`
**Purpose:** Paper-space / layout management, gilyon (map sheet) operations.

| Command | Description |
|---|---|
| `c:gildiv` | Main gilyon division command: prompts "Grouped/<Separated>:", dispatches to grouping or single mode |
| `c:gilkey` | Create sheets location plan with hatch in paper space (requires TILEMODE=0) |
| `c:clean_gil` | Delete UCS, block, and layer for a given gilyon number |
| `c:cut_gil_ps` | Cut gilyon from paper space to external DWG file |
| `c:cut_gil_ms` | Cut gilyon from model space using polyline boundary + trim |
| `c:tr_chvp_s` | Start viewport change mode |
| `c:tr_chvp_f` | Finish viewport change mode |
| `c:tr_show_vp` | Show viewport layer |
| `c:tr_hide_vp` | Hide viewport layer |
| `c:gilon` | Thaw all `tr_gil*` layers |
| `c:giloff` | Freeze all `tr_gil*` layers |
| `c:tops` | Switch to paper space (set TILEMODE=0) |
| `c:toms` | Switch to model space (set TILEMODE=1) |
| `c:tr_pschg` | Change/create paper space sheet for a given gilyon number |
| `c:zzz` | Debug/test hatch command |

---

### File: `TRA_LSP\TRA_RISH.LSP`
**Purpose:** Map sheet (gilyon) frame insertion.

| Command | Description |
|---|---|
| `c:TRinsgil` | Insert gilyon frame block; calls ARX `trgetgil`; sets ATTREQ=1, ATTDIA=0 before insert |

---

### File: `TRA_LSP\TRA_IDAN.LSP`
**Purpose:** DTM (Digital Terrain Model) / contour interface. All commands delegate to ARX functions.

| Command | ARX function | Description |
|---|---|---|
| `c:tridnprj` | `tridnprj_a` | Change DTM project |
| `c:trruncnt` | `trruncnt_a` | Create/run contour calculation |
| `c:trgetcnt` | `trgetcnt_a` | Draw contours from DTM |
| `c:trwreg` | `trwreg_a` | Write REG file for DTM |
| `c:trwdis` | `trwdis_a` | Write DIS (distance) file |
| `c:trreadis` | `trreadis_a` | Read DIS file |
| `c:trwbou` | `trwbou_a` | Write BOU (boundary) file |
| `c:triremod` | `triremod_a` | Change elevation mode |
| `c:trice` | `trice_a` | Run ICE (interpolation) |
| `c:trice3d` | `trice3d_a` | Run ICE 3D |

---

### File: `TRA_LSP\TR_TABA.LSP`
**Purpose:** Land-use (TABA) polygon and hatch operations.

| Command | Description |
|---|---|
| `c:trhp` | Set polygon layers and annotate land-use |
| `c:trhh` | Draw hatches for land-use polygons |
| `c:trhl` | Insert area usage legend |
| `c:trhupdt` | Update lot area usage values |
| `c:trdbsel` | Select lot database |
| `c:trlotdat` | Edit lot data interactively |
| `c:tri2db` | Copy annotations to database |
| `c:trl2db_flag` | Set auto-lots-to-DB flag |
| `c:trh_on` | Show hatch layer |
| `c:trh_off` | Hide hatch layer |
| `c:trh_del` | Delete hatch entities |
| `c:trhsld` | Create slide libraries for TABA |
| `c:trhdon` | Show land usage description labels |
| `c:trhdoff` | Hide land usage description labels |
| `c:trgushon` | Show gush description labels |
| `c:trgushoff` | Hide gush description labels |
| `c:trhcola` | Color areas by land-usage code |
| `c:tabamenu` | Load `tr_taba.mnu` menu |
| `c:tr_topo` | Auto topology dialog (also in TRA_DDT) |
| `c:tr_parts` | Parts definition dialog |
| `c:tr_plan` | Plan correlation dialog |
| `c:tr_plans` | Multiple plans correlation dialog |

---

### File: `TRA_LSP\TRA_EPOL.LSP`
**Purpose:** Clip/erase entities inside or outside a polyline boundary.

| Command | Description | Options |
|---|---|---|
| `c:epol` | Erase entities inside or outside a polyline | Prompts: select polyline; Inside/Outside; Cut crossing lines Y/N; Window/Crossing selection |

---

### File: `TRA_LSP\TRA_SELD.LSP`
**Purpose:** Generic selection-set choice dialog. No C: commands.

| Function | Description | Parameters |
|---|---|---|
| `tr_select_dlg(fn)` | Show All/Visible/Select radio dialog; calls `fn` with resulting selection set | `fn` — function to call with ss |

---

### File: `TRA_LSP\Image_helmert.lsp`
**Purpose:** Graphical Helmert (conformal) coordinate transformation for raster image geo-registration.

| Command | Description |
|---|---|
| `c:tr_Image_Helmrt_trans` | Interactive: collect ≥2 source/target point pairs, compute least-squares translation (dx,dy), rotation (w), scale (q), apply conformal transform to selected entities |

**Algorithm:** Least-squares conformal (4-parameter Helmert): dx, dy, w (rotation), q (scale). Requires minimum 2 control point pairs.

---

### File: `TRA_LSP\tr_lyout.lsp`
**Purpose:** VLA-based layout (paper space tab) management. Requires `(vl-load-com)`.

| Function | Description | Parameters |
|---|---|---|
| `trcreate_layout(name,template)` | Create named layout from `.dwt` template file | `name`, `template` |
| `tr-acad-obj()` | Get VLA AutoCAD application object | none |
| `tr-act-doc()` | Get active document VLA object | none |
| `tr-layouts()` | Get layouts collection | none |
| `tr-actlay()` | Get active layout | none |
| `tr-layname(lay)` | Get layout name string | `lay` — VLA layout object |
| `tr-tmplt-path()` | Get template directory path | none |
| `tr-tmplt-full(name)` | Get full template file path | `name` |
| `tr-mak-tmplt(name)` | Create template from current layout | `name` |

---

### File: `TRA_LSP\tr_pschg.lsp`
**Purpose:** Change/create paper-space sheet for gilyon.

| Command | Description |
|---|---|
| `c:tr_pschg` | Interactive: enter gilyon number; if UCS exists, creates layout rectangle, text label, and calls `tr_pspace` to build full paper-space layout including viewports |

---

### File: `TRA_LSP\tr_symbol.lsp`
**Purpose:** Point symbol management — update point block references and xdata.

| Command | Description |
|---|---|
| `c:tr_update_symbols` | Interactive: display symbol list, user picks number, select points, update block/layer/xdata |
| `c:tr_query_symbol` | Query and display symbol info stored in entity xdata |
| `c:tr_list_symbols` | Display all available symbols in console |
| `c:tr_batch_update_by_layer` | Batch update all points on a named layer to a symbol |

**Symbol library (13 entries):** SURVEY_POINT, CONTROL_POINT, BENCHMARK, BOUNDARY_MARKER, UTILITY_POLE, BUILDING_CORNER, TREE, MONUMENT, PROPERTY_LINE_START, PROPERTY_LINE_END, SETBACK_POINT, EASEMENT_POINT, REFERENCE_POINT.

---

### File: `TRA_LSP\tr_updcode.lsp`
**Purpose:** Update a MapPit point's symbol code and layer without interactive dialog. Three-tier point-finding strategy.

| Command | Description |
|---|---|
| `c:TRUPDCODE` | Update point symbol code: prompts for point name and new code; finds entity via (1) scanning all INSERTs for TAG=NAME match, (2) launching `c:trmfindp` ARX finder, (3) manual entsel; reads Hanit_Pcod.INI for block/layer info; updates INSERT block reference + layer + MARK attribute via entmod |

**Internal functions:**

| Function | Description |
|---|---|
| `tr_updcode_ini_val(fpath,section,key)` | Read key from INI section |
| `tr_updcode_get_paths()` | Resolve TR_CFG.INI → system INI → pcod path + dwg dir |
| `tr_updcode_lookup_code(code)` | Return `(block-name layer-name)` from Hanit_Pcod.INI |
| `tr_updcode_ensure_block(blk,dir)` | Insert+delete to load block definition if not in drawing |
| `tr_updcode_apply(ins-en,code,mark)` | Apply block name, layer, and mark changes via entmod |
| `tr_updcode_find_entity(pname)` | Walk all INSERT-with-attribs to find TAG=NAME=pname |

---

### File: `TRA_LSP\tr_thin.lsp`
**Purpose:** Elevation label thinning — hides redundant height ATTRIBs inside M1502_P blocks.

| Command | Description |
|---|---|
| `c:THINHEIGHTS` | Thin elevation labels: select area (rectangle or polyline), set radius and tolerance; greedy spatial sweep sorted by elevation descending; hides redundant nearby ATTRIBs via DXF code-70 invisible flag; saves original flags in XDATA "TRTHIN" |
| `c:RESTOREHEIGHTS` | Restore all ATTRIBs hidden by THINHEIGHTS; finds by XDATA "TRTHIN"; restores original flags |

---

### File: `TRA_LSP\DEMO.LSP`
**Purpose:** Miscellaneous utility commands (distance labeling, attribute elevation, text oblique angle fix).

| Command | Description |
|---|---|
| `c:fff` | Interactive polyline join: pick starting object, repeatedly join next objects into a fitted polyline |
| `c:dist1` | Show distance label for one picked line; inserts TR_FRONT block at midpoint |
| `c:dist2` | Show distance label between two picked points |
| `c:ddd` | Simple distance measurement (no height factor); prints distance to console |
| `c:att2pt` | Elevate attribute positions to block Z height for selected INSERTs |
| `c:ob_chg` | Set oblique angle of selected text entities to 0 (fixes IntelliCAD issue) |

---

### File: `TRA_LSP\trh_tbl.lsp`
**Purpose:** TABA land-use table drawing utilities.

| Function | Description | Parameters |
|---|---|---|
| `TRHinsTBL(is_all)` | Draw TABA table: calls `c:tr_parc`, prompts for `.cor` file, draws table with columns | `is_all` — T=full table, nil=summary |
| `TRHascTBL()` | Draw TABA ASCII table content from open file pointer | Reads `fp` global |
| `TRHwrtTBLtxt(lst,prev)` | Write one table row (SUM or data row) | `lst` — parsed CSV row; `prev` — previous category |

---

### File: `PitronimMnu.lsp`
**Purpose:** Load additional optional menu modules.

| Command | Description |
|---|---|
| `c:Pit3Dmenu` | Load PitCadastre3D English menu (`PitCadastre3D.mnu`); activate pop20 |
| `c:Pit3Dheb` | Load PitCadastre3D Hebrew menu (`PitCadastre3Dheb.mnu`); activate pop20 |
| `c:PitronMenu` | Load Pitron English menu (`Pitron.mnu`); activate pop21 |
| `c:PitronHeb` | Load Pitron Hebrew menu (`Pitronheb.mnu`); activate pop21 |
| `c:MapConmenu` | Load MapContours English menu (`MapContours.mnu`); activate pop23 |
| `c:MapConHeb` | Load MapContours Hebrew menu (`MapContoursheb.mnu`); activate pop23 |
| `c:MapPitMenu` | Load MapPit English toolbar menu (`MapPitMNU.mnu`); activate pop22 |
| `c:MapPitMNUHeb` | Load MapPit Hebrew toolbar menu (`MapPitMNUheb.mnu`); activate pop22 |

---

### File: `tra_flex\Tra_flex.lsp`
**Purpose:** AreaFlex flexible toolbar — parcel area editing subsystem.

| Command | Description |
|---|---|
| `c:flex_help` | Show AreaFlex help (calls `arfhelp` ARX) |
| `c:flex_about` | Show AreaFlex about box (calls `arfabout` ARX) |
| `c:ARFconf` | AreaFlex configuration DCL dialog (`arf_conf`); calls `trscnf_a` ARX |
| `c:ARFnameLOTS` | Interactive lot naming for AreaFlex: pick inside polygon, assign sequential or special names; calls `trilot_a` ARX |
| `c:flex` | Main AreaFlex parcel-definition dialog (`arf_parc_def`); calls `pitron 5` with selection set |

---

### File: `tra_flex\flex_mnu.lsp`
**Purpose:** Flex menu loading utilities.

| Command | Description |
|---|---|
| `c:flexmenu` | Load Flex English menu (`flex.mnu`); activate pop24 |
| `c:flexheb` | Load Flex Hebrew menu (`flexheb.mnu`); activate pop24 |

---

### File: `BricsCAD\tra_brx.lsp`
**Purpose:** BricsCAD menu loading commands.

| Command | Description |
|---|---|
| `c:PitBrxMenu` | Load BricsCAD English menu (`pit_brx.mnu`); activate pop20–pop23 |
| `c:HebBrxMenu` | Load BricsCAD Hebrew menu (`heb_brx.mnu`); activate pop20–pop23 |

---

### File: `USR\chtext.lsp`
**Purpose:** Autodesk CHTEXT utility — global text property editor. Copyright 1997 Autodesk, Inc.

| Command | Description |
|---|---|
| `c:cht` | Main command: select text/mtext/attdef entities; then choose Height/Justification/Location/Rotation/Style/Text/Undo/Width to change |
| `c:CHGTEXT` | Simple find-and-replace text editor (subset of CHT) |

---

## DCL Dialogs

### `tra_dcl\TRA_BASE.DCL` (shared component library)

**Prototype tiles:**

| Tile Key | Type | Description |
|---|---|---|
| `tr_lcode` | `boxed_row` | Lot lines layer code selector: toggle "Only with code" + code edit box |
| `tr_steps` | `boxed_row` | Correlation steps number edit box |
| `tr_chkpt` | `column` | Check/don't-check points toggle |
| `tr_entsel` | `boxed_radio_row` | Entity selection radio: All / Visible / Select |
| `tr_entsel_col` | `radio_column` | Same as tr_entsel as column layout |
| `tr_error` | `text` | Standard error display text tile |
| `tr_img` | `image_button` | Color swatch image button |
| `img_tog` | `toggle` | Image color toggle |
| `img_item` | `boxed_row` | Image item container 4×4 |
| `img_col` | `column` | Image column container h=3 |

**Full dialogs:**

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_select_ent` | "Pitron Select Box" — advanced entity selection | All/Visible/Select radio; VirtuLine toggle; Block/Layer/Pit filter toggles; Use PitSet button |
| `tra_ow_col` | Overwrite/Reject mode cluster | Overwrite/Reject radio; By Name toggle; By Coord toggle with radius; NONE text; Select entities toggle |
| `tra_overwrite` | Standalone overwrite dialog | `tra_ow_col` + ok_cancel |
| `tra_import_pnt` | Import Points dialog | Import filter (Name/Code patterns) + `tra_ow_col` + ok_cancel |
| `tra_ini_files` | Change Code System dialog | System Ini pick + Get/Save default buttons; Do Mapping section (codes/layers/mapping file) |
| `tra_view_pnt` | MapPit Point View | Values: Layer, Name, Symbol Code, Mark Code, Height, Extended Codes; Att Mapping: Name/Mark/Height att names |
| `tra_view_anot` | MapPit Annotation View | Values: Layer, Code, Type; Att Mapping: Annotation att |
| `tra_view_line` | MapPit Lines View | Values: Layer, Entity Type, Line Code, VirtuLine membership, Extended Codes |
| `tra_view_reg` | Regular Entity view | Entity Type, Layer |
| `tra_sys_ini` | View System Files dialog | list_box (file list) + View/Modify/OK buttons |
| `tra_file_view` | File View dialog | File Name text + list_box + OK |
| `tra_yes_no` | Verify Action dialog | Text prompt + ok_cancel |

---

### `tra_dcl\TRA_DDT.DCL`
Includes `tra_base.dcl`.

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_points` | Add POINTS dialog | Check points toggle, place points toggle, snap toggle, step number, scale edit, layer code, selection radio |
| `tr_linarc` | Modify Lines and Arcs dialog | Break long lines toggle, replace existing toggle, `tr_lcode`, `tr_entsel`, `tr_error` |
| `tr_parc_def` | Parcels Definition dialog | `tr_lcode`, correlation steps, `tr_entsel`, `tr_error` |
| `tr_areas_cor` | Areas Correlation dialog | Correlation parameters, lot code, steps |
| `tr_plan_cor` | Plan Correlation dialog | Plan correlation parameters |
| `tr_plans_cor` | Multiple Plans Correlation dialog | Multi-plan parameters |
| `tr_parts_cor` | Parts Correlation dialog | Parts parameters |
| `tr_set_gush` | Set Block to Lots dialog | Gush block assignment |
| `tr_topo_dlg` | Auto Topology dialog | Topology build parameters |
| `tr_note_err` | Errors and Notes viewer | Errors list_box + Save Errs button; Notes list_box + Save Notes button |
| `tr_outfiles` | Output ASCII Files dialog | Toggles for SRV, PNT, YXZ, HEB, LOT, DEF, ARE output formats |

---

### `tra_dcl\TRA_PCRT.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_pcreate_dcl` | Point creation settings | 6 attribute groups (Name/Symbol/Mark/Height/Parenthesis/Layer), each with visibility popup, value popup, edit box |
| `tra_lines_con` | Lines connection dialog | Connection parameters |
| `tra_file_lines_con` | File-based lines connection | Connection with curve fitting options |
| `tra_ml_con` | VirtuLine connection dialog | VirtuLine-specific connection parameters |
| `tra_imp_pnt` | Import points dialog | Import filter |
| `tra_pit_filter` | Complex entity filter | Multi-tab: points/annotations/lines/other with list_boxes |
| `tra_line_type` | Line type selector | Line type popup |
| `tra_dist_params` | Distance parameters | Min/max distance settings |

---

### `tra_dcl\TRA_CONF.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_conf_dlg` | MapPit Configuration | Drawing Scale, Symbols base size, Accur level, Heights display accuracy, Auto rebuild flag; Attribute Scaling (Name/Mark/Height mm sizes); Max fronts, First num, Add-tag, Error text size; `CONF_USE_SELECT` toggle |

---

### `tra_dcl\TRA_TRNS.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_trans` | Full 7-point coordinate transformation | For each of 7 points: Pick button, Name, Level, Old X/Y; New Pick button, New X/Y, Skip toggle; layer-load buttons; iteration count; save/read dialog; Calculate (3 variants) / Write / Transform action buttons |

---

### `tra_dcl\TRNS_12.DCL`

| Dialog | Description |
|---|---|
| `tr_trans` | Compact 7-point transformation (same structure as TRA_TRNS but narrower widths; single Calculate button) |

---

### `tra_dcl\TRA_IMG.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `IMGDCL` | Symbol selection image picker | list_box + 5 rows × 4 columns = 20 image_button tiles (IMG1–IMG20) + PREV/NEXT navigation buttons |

---

### `tra_dcl\TRA_LAY.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `setlayer` | Layer selector | Current layer display; layer list_box (LIST_LAY); Set Layer Name edit_box (LAYER); Find button; Error text |

---

### `tra_dcl\TRA_ALRT.DCL`

| Dialog | Description |
|---|---|
| `tr_note_dlg` | Standard Note dialog with centered text_part (MSG) |
| `tr_err_dlg` | Standard Error/Alert dialog with centered text_part (MSG) |

---

### `tra_dcl\TRA_SELD.DCL`

| Dialog | Description |
|---|---|
| `tr_select_dlg` | Entity selection choice: radio row with All / Visible / Select |

---

### `tra_dcl\TRA_RGV.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_regev_dcl` | REGEV interface main dialog | Actions: Go Diary/Edit/Calc; Edit modes: EDM/Coord/Polyg/Level/Stadia; Setup/File Translate/YXZ Transform buttons |
| `tra_regev_select` | REGEV entity selector | Selection criteria |
| `tra_regev_overwrite` | REGEV overwrite mode | Overwrite mode + entity select |
| `tra_regev_verify` | REGEV verify dialog | Verification display |
| `tra_regev_verify_save` | REGEV verify with save | Verification + save option |

---

### `tra_dcl\DCL_CODS.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_cods_lst` | Code list selector | Options list_box + "other" edit box |
| `tra_mcods_box` | Code/remark entry | Code edit box + remark edit box |
| `tra_ecods_dlg` | Entity codes dialog | C/P/S/M/OTHER tabs with list_boxes + Add/Del buttons |
| `tra_lcods_dlg` | Layer codes dialog | Same structure as `tra_ecods_dlg` for layers |

---

### `tra_dcl\TRA_IDAN.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `TRidan_get_cont` | Contour layer settings | Regular/Intermediate/Principal layer names; gaps; rounding; text height; text distance |

---

### `tra_dcl\TRA_PERP.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_perp_del` | Delete perpendicular elements | Lines: None/All/By-length radio + min/max; Annotations: None/All/By-length + min/max; Distances: same |

---

### `tra_dcl\TRA_VER.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_ver_dlg` | Registration key entry | KEY1 edit_box (19 char); KEY2 edit_box (19 char, initial focus, allow_accept) |

---

### `tra_dcl\SNP_SHOT.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tra_cods_lst` | Snap shots manager | Snap list_box + Add/Del/Restore buttons + Layers toggle + View toggle + Name edit_box |

---

### `tra_dcl\TR_VFILE.DCL`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_vfile` | Notes/text file viewer | list_box + Save to File button + OK |

---

### `tra_dcl\tr_cords.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_cords` | Coordinate annotation settings | X/Y/Z use toggles; prefix edit boxes; precision popups; text size; Draw rectangle toggle; Draw leader toggle; layer edit box |

---

### `tra_dcl\Tra_sect.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_sect` | Sector management | None/Poly/Range radio column; Define Sectors button; Range Width/Height edit boxes |

---

### `tra_dcl\TRA_CONS.DCL` (dimension comparison)

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_dim_diff` | Planned/Measured dimension difference | UCS button; Planned section (Choose circles / Choose points + status text); Measured section (same); Report toggle; Name-from radio (planned/measured); Min/Max diff, dim line length edit boxes; Use rounding toggle |

---

### `tra_dcl\tr_ptsvl.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_pts_vl` | Points By VirtuLine Parameters | Interval/Divide radio + Interval edit + Parts edit; Add Start/End toggles; Rotate/Up/Straighten/Height/Break VL toggles |

---

### `tra_dcl\Tr_txtd.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_txtd` | TABA table check viewer | Fixed-width list_box (70 wide, tab stops) + View button + OK |

---

### `tra_dcl\Tr_p2d.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_p2d` | Point-to-document file selector | 10 rows each with toggle (TOG1–TOG10), file name text (FNAME1–10), description text (DESC1–10); Project Header edit box; Project Page Header edit box |

---

### `tra_dcl\Tra_ate.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `tr_ate` | Edit block attributes | Block name display; 7 attribute rows each with: Att Name, Prompt, Value edit_box, Dos Heb toggle, Copy toggle; Translation file toggle + file edit + Browse button; Prev/Next navigation + ok_cancel |
| `tr_single_ate` | Single attribute edit box | Value edit_box + Dos Heb toggle + ok_cancel |

---

### `tra_flex\arf_dcl\ARF_base.dcl`

Mirrors `TRA_BASE.DCL` with AreaFlex-specific prototypes: `my_spacer`, `tr_lcode`, `tr_steps`, `tr_chkpt`, `tr_entsel`, `tr_entsel_col`, `tr_error`, `tr_img`, `img_tog`, `img_item`, `img_col`.

Full dialogs same as TRA_BASE: `tra_select_ent`, `tra_ow_col`, `tra_overwrite`, `tra_import_pnt`, `tra_ini_files`, `tra_view_pnt`, `tra_view_anot`, `tra_view_line`, `tra_view_reg`, `tra_sys_ini`, `tra_file_view`, `tra_yes_no`.

---

### `tra_flex\arf_dcl\ARF_ddt.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `arf_linarc` | AreaFlex Modify Lines and Arcs | `tr_lcode`; Break long lines toggle; Replace existing toggle; `tr_entsel`; `tr_error` |
| `arf_parc_def` | AreaFlex Define Lots | `tr_lcode`; `tr_entsel`; `tr_error` |
| `arf_note_err` | AreaFlex Errors and Notes | Errors list_box + Save Errs button; Notes list_box + Save Notes button |
| `arf_conf` | AreaFlex Display Control | Areas text: Show toggle, Size edit, Color swatch; Lot names text: same; Mekadem coefficient: Use toggle, value edit |
| `arf_mov_param` | AreaFlex Move Parameters | Move method radio (Free/Locked/Rotation/Junction); Arc constant radio (Keep Radius/Keep Bulge) |
| `arf_help` | AreaFlex Help box | list_box |
| `arf_about` | AreaFlex About box | list_box |

---

### `tra_flex\arf_dcl\ARF_lay.dcl`

| Dialog | Description | Key tiles |
|---|---|---|
| `setlayer` | Layer selector (AreaFlex variant) | Current layer text; LIST_LAY list_box; LAYER edit_box; Find button; ERROR_MSG text |

---

### `tra_flex\arf_dcl\ARF_ver.dcl`

| Dialog | Description |
|---|---|
| `tra_ver_dlg` | Registration key entry (KEY1, KEY2) — identical structure to TRA_VER.DCL |

---

### `tra_flex\arf_dcl\ARF_alrt.dcl`

| Dialog | Description |
|---|---|
| `tr_note_dlg` | AreaFlex Message dialog — centered text_part |
| `tr_err_dlg` | AreaFlex Alert dialog — centered text_part |

---

## Menu Files

| File | Description | Popup slot |
|---|---|---|
| `pit_sub.mnu` / `pit_sub.cuix` | Main Pitronim dropdown menu (English) | p20–p23 |
| `pit_heb.mnu` | Hebrew main menu | p20–p23 |
| `MapPitMNU.mnu` / `.cuix` | MapPit toolbar menu (English) | p22 |
| `MapPitMNUheb.mnu` | MapPit toolbar menu (Hebrew) | p22 |
| `PitCadastre3D.mnu` | 3D Cadastre submenu | p20 |
| `PitCadastre3Dheb.mnu` | 3D Cadastre submenu (Hebrew) | p20 |
| `Pitron.mnu` | Classic Pitron submenu | p21 |
| `Pitronheb.mnu` | Classic Pitron submenu (Hebrew) | p21 |
| `MapContours.mnu` | Contour operations menu | p23 |
| `MapContoursheb.mnu` | Contour menu (Hebrew) | p23 |
| `tr_taba.mnu` | TABA land-use menu | p24 |
| `mami_heb.mnu` | MAMI menu (Hebrew) | unknown |
| `BricsCAD\pit_brx.mnu` | BricsCAD English menu | p20–p23 |
| `BricsCAD\heb_brx.mnu` | BricsCAD Hebrew menu | p20–p23 |
| `tra_flex\flex.mnu` | Flex toolbar (English) | p24 |
| `tra_flex\flexheb.mnu` | Flex toolbar (Hebrew) | p24 |

---

## Configuration System

### `TR_CFG.INI` — Master Runtime Configuration

| Section | Key | Description |
|---|---|---|
| `[GENERAL]` | `SYSTEM` | Path to active code-system INI (e.g. `HANIT\Mapi_Hanit.ini`) |
| `[GENERAL]` | `ALT_SYSTEMS` | Semicolon-separated fallback search paths |
| `[PITRON]` | `SCALE` | Drawing scale (e.g. 500) |
| `[PITRON]` | `ACCUR` | Coordinate tolerance in meters |
| `[PITRON]` | `SYMB_SCALE` | Symbol scale factor |
| `[LINE_CON]` | (multiple) | Auto-connection parameters |
| `[COORD_TEXT]` | (multiple) | Coordinate annotation text format |
| `[DEBUG]` | (flags) | Set to `ON` to enable performance logging |

### `HANIT\Mapi_Hanit.ini` — Code System Master

Points to five INI files, SLB libraries, and PTF point-format files. Sections:
- `[INI]` — `PCOD`, `LCOD`, `ANOT`, `PROTO`, `GIL` keys → paths to INI files
- `[GENERAL]` — `DWG_PATH`, `SLB_PATH`
- `[PTF]` — point format file paths

### `HANIT\INI\Hanit_Pcod.INI`
Per-code sections. Each code section contains:
- `SYMB_BLOCK` — block name to insert
- `LAYER_NAME` — target layer
- `SYMB_DESC` — Hebrew description
- `NAME_ATT` — attribute tag for point name
- `MARK_ATT` — attribute tag for mark
- `HEIGHTM_ATT` — attribute tag for height (metric)
- `HEIGHTC_ATT` — attribute tag for height (centesimal)

### `HANIT\INI\Hanit_Lcod.ini`
Line connection codes. Per-code:
- `LINE_LAYER` — layer for line
- `LINE_DESC` — description

### `HANIT\INI\Hanit_ANOT.INI`
Annotation block definitions per code.

### `HANIT\INI\Hanit_Proto.ini`
Layer color and linetype definitions per layer name.

### `HANIT\INI\Hanit_GIL.INI`
Map sheet frame block definitions (A0–A4, dynamic).

---

## Data Files

| File | Format | Description |
|---|---|---|
| `tr_lots.mdb` | MS Access | Cadastral lot records database |
| `TR_YEUDEI_KARKA.TXT` | Text, tab-delimited | Land-use category lookup table |
| `TR_CFG.INI` | Windows INI | Session state and configuration |
| `USR\TRA_SYS\PTF\*.ptf` | PTF | User point-format files |
| `HANIT\DWG\*.dwg` | AutoCAD DWG (2013 format) | Symbol block drawings |
| `HANIT\SLB\*.slb` | AutoCAD SLB | Compiled slide library for symbol picker |
| `pit_sub.cuix` | AutoCAD CUIX | Compiled CUI menu for AutoCAD 2010+ |
| `MapPitMNU.cuix` | AutoCAD CUIX | Compiled toolbar CUI |

---

## Global State Variables

| Variable | Set in | Description |
|---|---|---|
| `TRAppName` | TRA_INIT.LSP | `"TR_DXF"` — extended data app name |
| `NOTRAppName` | TRA_INIT.LSP | `"NOTR_DXF"` — non-MapPit xdata app |
| `TRPname` | TRA_INIT.LSP | `"TR_PNAME"` |
| `TRFname` | TRA_INIT.LSP | `"TR_FRONT"` |
| `TRAname` | TRA_INIT.LSP | `"TR_AREA"` |
| `TRLname` | TRA_INIT.LSP | `"TR_LOT"` |
| `TRHname` | TRA_INIT.LSP | `"TR_HIGHT"` |
| `TRArcDT` | TRA_INIT.LSP | `"TR_ARCD"` |
| `TRWrngLay` | TRA_INIT.LSP | Invalid layer name prefix list |
| `TRerrsDESC` | TRA_INIT.LSP | Error layer descriptions |
| `TRfilt0` | TRA_INIT.LSP | Entity selection filter |
| `is_icad_ver` | TRA_INIT.LSP | T if IntelliCAD host |
| `tr_flag2000` | TRA_INIT.LSP | T if AutoCAD 2000+ (supports layouts) |
| `TRsel_T` | TRA_INIT.LSP | Selection type: 1=All, 2=Visible, 3=Select |
| `scale` | TRgetSCALE | Current drawing scale |
| `dirc` | various | Current direction for tr_direc |
| `trchk_p` | TRA_DDT.LSP | Check-points flag (1=on) |
| `trplc_l` | TRA_DDT.LSP | Place-lines flag |
| `trstp_n` | TRA_DDT.LSP | Stop number default |
| `trlay_c` | TRA_DDT.LSP | Current layer code |
| `tra_ss` | TRA_DDT.LSP | Current working selection set |
| `trch_cf` | TRA_DDT.LSP | Config-changed flag |
| `tr_symbol_list` | TR_SYMBOL.LSP | Symbol library list |
| `tr_current_symbol` | TR_SYMBOL.LSP | Currently selected symbol name |
| `tr_thin_inserts` | TR_THIN.LSP | List of INSERT enames for entupd after thinning |

---

## ARX-Exposed Functions

These functions are defined in the C++ binary and callable from LISP:

| Function | Description |
|---|---|
| `pitron(n)` | Core Pitronim operation dispatcher; n=operation code |
| `tragcf_a(type,key)` | Get configuration value (STR/SPC/INT types) |
| `trapcf_a(key,value)` | Put/set configuration value |
| `trfblk_a(bname)` | Find/load block definition |
| `trpins_a(bname,pt,sx,sy,ang,flag)` | Insert point block with attributes |
| `tralert_a(msg)` | Show alert message box |
| `trlincon_a(ss)` | Run line-connection algorithm |
| `trbldpts_a(ss)` | Build points from selection set |
| `trfindp_a(name)` | Find point by name |
| `trmfindp_a(name)` | Find point by name with pan |
| `tridnprj_a` | DTM: change project |
| `trruncnt_a` | DTM: run contour calculation |
| `trgetcnt_a` | DTM: get/draw contours |
| `trwreg_a` | DTM: write REG file |
| `trwdis_a` | DTM: write DIS file |
| `trreadis_a` | DTM: read DIS file |
| `trwbou_a` | DTM: write BOU file |
| `triremod_a` | DTM: change elevation mode |
| `trice_a` | DTM: run ICE |
| `trice3d_a` | DTM: run ICE 3D |
| `trtmrcommand_a(keyword)` | 3D Cadastre TAMAR command dispatcher |
| `trgetgil` | Get/insert gilyon frame block |
| `trautogil(ss,gilnum)` | Auto-process gilyon |
| `tr_getrect(gil,ss,lst)` | Get gilyon rectangle corners |
| `tr_pspace(p1,p2,p3,p4,gil,tmplt,lay)` | Create paper-space layout for gilyon |
| `TRFULP_A(bdir,fname,mode)` | Resolve full file path |
| `treditf_a(path)` | Edit file with configured editor |
| `trshell_a(cmd)` | Execute shell command |
| `trgetp_a(prompt)` | Get point with snap handling |
| `TRgetPTstr` | Point-get string input handler |
| `TRTAZARTABLE_A` | Insert TAZAR table (.NET) |
| `TR_SHOWLOTTREE_A` | Show lot tree view (.NET) |
| `TR_SHOWTAZARUI_A` | Show TAZAR UI (.NET) |
| `TRraznizav_A` | Raznizav calculation |
| `TRRNZRESTORE_A` | Restore raznizav |
| `trilot_a(mode,...)` | Lot insertion/naming ARX handler |
| `trscnf_a` | AreaFlex configuration |
| `arfhelp` | AreaFlex help |
| `arfabout` | AreaFlex about |
| `mmove(ss)` | Quick move entity |
| `labelsplacer_a` | Labels optimizer |
| `trstrtok_a(delim,str)` | String tokenizer |
| `traupdpt_a` | Update point (interactive dialog version) |
| `trpvizoff` / `trvizhn_a` | Point height visibility off/on |

---

## Call Graph Summary

```
c:pitmenu / c:hebmenu
    command "menuload" → pit_sub.mnu / pit_heb.mnu

c:trlincon
    trlincon_a (ARX) ← selection set from tra_select_ent dialog

c:tr_points / c:tr_linarc / c:tr_parc / c:tr_topo
    tra_ddt.dcl dialogs
    pitron(N) (ARX) ← tra_ss selection set

c:TRoutFILES
    tra_ddt.dcl / tr_outfiles dialog
    ARX write functions

c:gildiv → gildivGroup / gildivSingle
    trautogil (ARX)
    tr_getrect (ARX)
    tr_pspace (ARX)

c:trruncnt → trruncnt_a (ARX)
c:trgetcnt → trgetcnt_a (ARX)

c:TRinsgil
    trgetgil (ARX)

c:trinstzr_hanit → TRTAZARTABLE_A (ARX/.NET)
c:trLotTreeView → TR_SHOWLOTTREE_A (ARX/.NET)
c:trtazarmenu → TR_SHOWTAZARUI_A (ARX/.NET)

3D TAMAR commands → trtmrcommand_a("keyword") (ARX)

c:TRUPDCODE
    tr_updcode_find_entity (scan INSERTs)
    ‖ c:trmfindp (ARX pan/find)
    ‖ entsel (manual)
    tr_updcode_lookup_code → Hanit_Pcod.INI
    tr_updcode_ensure_block → command "_.insert"
    tr_updcode_apply → entmod

c:THINHEIGHTS
    tr_thin_get_height_tags → Hanit_Pcod.INI
    tr_thin_collect → ssget M1502_P
    tr_thin_process_radius (greedy spatial sort)
    tr_thin_hide_enames → entmod + TRTHIN xdata

c:tr_Image_Helmrt_trans
    collect control point pairs (interactive)
    least-squares Helmert solve
    apply transform → entmod
```
