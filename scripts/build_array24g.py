# -*- coding: utf-8 -*-
"""
24GHz 2x2 Patch Array on FR4 — derived from verified single-patch diagnostic.
Corporate feed network: Port1 → T1 → T2L/T2R → 4 elements.
All orthogonal (no rotation), Unite for connectivity.
"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Array24G_2x2", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Array24G_2x2")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

# ── Verified helpers ──
_B = ["NAME:Attributes","Flags:=","","Color:=","(132 132 193)","Transparency:=",0,
    "PartCoordinateSystem:=","Global","UDMId:=","",
    "SolveInside:=",True,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False]

def bx(n,x,y,z,sx,sy,sz,m="vacuum"):
    oEditor.CreateBox(["NAME:BoxParameters","XPosition:=","%.4fmm"%x,"YPosition:=","%.4fmm"%y,"ZPosition:=","%.4fmm"%z,"XSize:=","%.4fmm"%sx,"YSize:=","%.4fmm"%sy,"ZSize:=","%.4fmm"%sz],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"'+m+'"',"SurfaceMaterialValue:=",'""']+_B[1:])

def rc(n,x,y,w,h,z=0,ax="Z"):
    oEditor.CreateRectangle(["NAME:RectangleParameters","IsCovered:=",True,"XStart:=","%.4fmm"%x,"YStart:=","%.4fmm"%y,"ZStart:=","%.4fmm"%z,"Width:=","%.4fmm"%w,"Height:=","%.4fmm"%h,"WhichAxis:=",ax],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"vacuum"',"SurfaceMaterialValue:=",'""']+_B[1:])

_p=[0]
def pe(n):
    _p[0]+=1
    oDesign.GetModule("BoundarySetup").AssignPerfectE(["NAME:PE%d"%_p[0],"Objects:=",[n],"InfGroundPlane:=",False])

def lp(n,num,cx,cy):
    oDesign.GetModule("BoundarySetup").AssignLumpedPort(["NAME:%d"%num,"Objects:=",[n],"DoDeembed:=",False,"RenormalizeAllTerminals:=",True,["NAME:Modes",["NAME:Mode1","ModeNum:=",1,"UseIntLine:=",True,["NAME:IntLine","Start:=",["%.4fmm"%cx,"%.4fmm"%cy,"-1.6000mm"],"End:=",["%.4fmm"%cx,"%.4fmm"%cy,"0.0000mm"]],"AlignmentGroup:=",0,"CharImp:=","Zpi","RenormImp:=","50ohm"]],"ShowReporterFilter:=",False,"ReporterFilter:=",[True],"Impedance:=","50ohm"])

# ── DESIGN PARAMETERS ──
W50  = 3.1;  Hs = 1.6;  Ws = 30.0;  Ls = 30.0;  Jx = Ws/2.0
Wp   = 3.80; Lp = 2.50; Gw = 3.40;  Gd = 0.70  # Lp scaled: 3.0→2.8→2.5
dx   = 8.0;  dy = 8.0   # element spacing
# Element bottom Y (lower/upper row)
Ey_lo = 18.0;  Ey_hi = Ey_lo + dy  # 18, 26
# J2 at midpoint of FEED ENDS (Ey+Gd), so paths up/down equal
J2y   = (Ey_lo + Ey_hi)/2.0 + Gd  # = 22.8
J1y   = 8.0    # first T-junction (below J2)

# ═══════════════════════════
# 1. Substrate + Ground
# ═══════════════════════════
bx("Sub", 0, 0, -Hs, Ws, Ls, Hs, "FR4_epoxy")
rc("Gnd", 0, 0, Ws, Ls, -Hs); pe("Gnd")

# ═══════════════════════════
# 2. Feed network — 3 T-junctions (orthogonal, 50Ω lines)
# ═══════════════════════════
# Port1 input line: vertical, from Y=0 to J1y
rc("FeedIn", Jx-W50/2, 0, W50, J1y); pe("FeedIn")

# J1 horizontal split: J1y, X from Jx-dx/2 to Jx+dx/2
rc("J1h", Jx-dx/2, J1y-W50/2, dx, W50); pe("J1h")

# J2L vertical: from J1y to J2y at X = Jx-dx/2
j2lx = Jx-dx/2
rc("J2Lv", j2lx-W50/2, J1y, W50, J2y-J1y); pe("J2Lv")

# J2R vertical: from J1y to J2y at X = Jx+dx/2
j2rx = Jx+dx/2
rc("J2Rv", j2rx-W50/2, J1y, W50, J2y-J1y); pe("J2Rv")

# J2L horizontal split: J2y, X from Jx-dx to Jx
rc("J2Lh", Jx-dx, J2y-W50/2, dx, W50); pe("J2Lh")

# J2R horizontal split: J2y, X from Jx to Jx+dx
rc("J2Rh", Jx, J2y-W50/2, dx, W50); pe("J2Rh")

# ═══════════════════════════
# 3. Element feeds — vertical from J2y to Ey+Gd (into patch notch)
# ═══════════════════════════
e1x = Jx-dx/2; e2x = Jx+dx/2

# E1/E2: feed goes DOWN from J2y to Ey_lo+Gd (overlap 0.1mm into top bar)
ov = 0.1
rc("E1f", e1x-W50/2, Ey_lo+Gd-ov, W50, J2y-(Ey_lo+Gd-ov)); pe("E1f")
rc("E2f", e2x-W50/2, Ey_lo+Gd-ov, W50, J2y-(Ey_lo+Gd-ov)); pe("E2f")

# E3/E4: feed goes UP from J2y to Ey_hi+Gd (overlap 0.1mm into top bar)
rc("E3f", e1x-W50/2, J2y, W50, (Ey_hi+Gd+ov)-J2y); pe("E3f")
rc("E4f", e2x-W50/2, J2y, W50, (Ey_hi+Gd+ov)-J2y); pe("E4f")

# ═══════════════════════════
# 4. Patch elements (U-shape with inset feed)
# ═══════════════════════════
def make_patch(name, cx, cy):
    """Create a U-shaped patch with inset feed at (cx, cy)."""
    px = cx - Wp/2; nx = cx - Gw/2; ntop = cy + Gd
    rc(name+"_L", px, cy, nx-px, Lp)
    rc(name+"_R", nx+Gw, cy, (px+Wp)-(nx+Gw), Lp)
    rc(name+"_T", px, ntop, Wp, Lp-Gd)
    oEditor.Unite(
        ["NAME:Selections","Selections:=",",".join([name+"_L",name+"_R",name+"_T"])],
        ["NAME:UniteParameters","KeepOriginals:=",False])
    pe(name+"_L")

make_patch("E1", e1x, Ey_lo)
make_patch("E2", e2x, Ey_lo)
make_patch("E3", e1x, Ey_hi)
make_patch("E4", e2x, Ey_hi)

# ═══════════════════════════
# 5. Port
# ═══════════════════════════
rc("Port1", Jx-W50/2, 0, W50, Hs, -Hs, ax="Y")
lp("Port1", 1, Jx, 0)

# ═══════════════════════════
# 6. AirBox + Radiation
# ═══════════════════════════
m = 8.0
bx("Air", -m, -m, -Hs-m, Ws+2*m, Ls+2*m, Hs+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(
    ["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,
     "IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

path = os.path.join(os.path.expanduser("~"),"Documents","Ansoft","Array24G_v1.aedt")
oProject.SaveAs(path, True)
print("DONE:", path)
print("Manual: Solution Setup @ 24GHz, Sweep 20-28GHz")
print("Expect: S11 dip near 24GHz + check radiation pattern (Gain, 3D polar)")
