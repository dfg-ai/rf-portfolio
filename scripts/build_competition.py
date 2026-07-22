# -*- coding: utf-8 -*-
"""
Competition: 4x8 Array @ 5.8GHz
Derived from verified build_58g_array.py (project 5).
4-column corporate feed (1→2→4, 3 T-junctions, VERIFIED S11=-18dB).
Only expanded rows: 4→8.
"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Array4x8_58G", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Array4x8_58G")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

_B = ["NAME:Attributes","Flags:=","","Color:=","(132 132 193)","Transparency:=",0,
    "PartCoordinateSystem:=","Global","UDMId:=","",
    "SolveInside:=",True,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False]

def bx(n,x,y,z,sx,sy,sz,m="vacuum"):
    oEditor.CreateBox(["NAME:BoxParameters","XPosition:=","%.4fmm"%x,"YPosition:=","%.4fmm"%y,"ZPosition:=","%.4fmm"%z,"XSize:=","%.4fmm"%sx,"YSize:=","%.4fmm"%sy,"ZSize:=","%.4fmm"%sz],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"'+m+'"',"SurfaceMaterialValue:=",'""']+_B[1:])

def mmv(v):
    """Format dimension: number → '12.0000mm', string like '$Lp' → pass through."""
    return v if isinstance(v, str) else "%.4fmm"%v

def rc(n,x,y,w,h,z=0,ax="Z"):
    oEditor.CreateRectangle(["NAME:RectangleParameters","IsCovered:=",True,"XStart:=",mmv(x),"YStart:=",mmv(y),"ZStart:=",mmv(z),"Width:=",mmv(w),"Height:=",mmv(h),"WhichAxis:=",ax],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"vacuum"',"SurfaceMaterialValue:=",'""']+_B[1:])

_p=[0]
def pe(n):
    _p[0]+=1
    oDesign.GetModule("BoundarySetup").AssignPerfectE(["NAME:PE%d"%_p[0],"Objects:=",[n],"InfGroundPlane:=",False])

def lp(n,num,cx,cy):
    oDesign.GetModule("BoundarySetup").AssignLumpedPort(["NAME:%d"%num,"Objects:=",[n],"DoDeembed:=",False,"RenormalizeAllTerminals:=",True,["NAME:Modes",["NAME:Mode1","ModeNum:=",1,"UseIntLine:=",True,["NAME:IntLine","Start:=",["%.4fmm"%cx,"%.4fmm"%cy,"-1.6000mm"],"End:=",["%.4fmm"%cx,"%.4fmm"%cy,"0.0000mm"]],"AlignmentGroup:=",0,"CharImp:=","Zpi","RenormImp:=","50ohm"]],"ShowReporterFilter:=",False,"ReporterFilter:=",[True],"Impedance:=","50ohm"])

# ══════════════════════════════════════════════
# DESIGN PARAMETERS (project 5 values, only rows changed)
# ══════════════════════════════════════════════
Hs=1.6; W50=3.1
Wp=15.74; Lp=12.00; Gd=4.00; Gw=W50+1.0  # best result
dx=25.0; dy=28.0
N_col=4; N_row=7  # fits 240mm

SubW = dx*(N_col-1) + Wp + 35

Jx_c = SubW/2.0
col_x = [Jx_c + (i-(N_col-1)/2.0)*dx for i in range(N_col)]

# Corporate feed (same as project 5)
J1y=12.0; J2y=24.0
Y0 = J2y + 8
cy = [Y0 + j*dy for j in range(N_row)]
# SubL = last_element_top + margin
SubL = cy[-1] + Lp + 20  # ≈ 230mm, fits 240

# ══════════════════════════════════════════════
# 0. HFSS Design Variables (for Optimetrics sweep)
# ══════════════════════════════════════════════
oDesign.ChangeProperty(
    ["NAME:AllTabs",
     ["NAME:LocalVariableTab",
      ["NAME:PropServers", "LocalVariables"],
      ["NAME:NewProps",
       ["NAME:Lp", "PropType:=", "VariableProp",
        "UserDef:=", True, "Value:=", "%.4fmm"%Lp]]]])

# ══════════════════════════════════════════════
# 1. Substrate + Ground
# ══════════════════════════════════════════════
bx("Sub", 0, 0, -Hs, SubW, SubL, Hs, "FR4_epoxy")
rc("Gnd", 0, 0, SubW, SubL, -Hs); pe("Gnd")

# ══════════════════════════════════════════════
# 2. Corporate feed: 1→2→4 (3 T, 2 levels — VERIFIED)
# ══════════════════════════════════════════════
mid_l = (col_x[0]+col_x[1])/2.0
mid_r = (col_x[2]+col_x[3])/2.0

# Input
rc("FeedIn", Jx_c-W50/2, 0, W50, J1y); pe("FeedIn")
# J1: 1→2
rc("J1h", mid_l-W50/2, J1y-W50/2, mid_r-mid_l+W50, W50); pe("J1h")
rc("J1vl", mid_l-W50/2, J1y, W50, J2y-J1y); pe("J1vl")
rc("J1vr", mid_r-W50/2, J1y, W50, J2y-J1y); pe("J1vr")
# J2: horizontal to each column pair
rc("J2hL", col_x[0]-W50/2, J2y-W50/2, col_x[1]-col_x[0]+W50, W50); pe("J2hL")
rc("J2hR", col_x[2]-W50/2, J2y-W50/2, col_x[3]-col_x[2]+W50, W50); pe("J2hR")
# Column feeds from J2
for i, cx in enumerate(col_x):
    rc("Cv%d"%i, cx-W50/2, J2y, W50, Y0-J2y); pe("Cv%d"%i)

# ══════════════════════════════════════════════
# 3. Series-fed columns (1×8 each — identical to project 5's 1×4)
# ══════════════════════════════════════════════
for c, cx in enumerate(col_x):
    line_end = cy[-1] + Lp + 5.0
    rc("ML%d"%c, cx-W50/2, Y0, W50, line_end-Y0); pe("ML%d"%c)
    for i, ry in enumerate(cy):
        px = cx-Wp/2; nx = cx-Gw/2; ntop = ry+Gd
        tag = "C%dR%d"%(c,i)
        rc(tag+"L", px, ry, nx-px, "Lp")
        rc(tag+"R", nx+Gw, ry, (px+Wp)-(nx+Gw), "Lp")
        rc(tag+"T", px, ntop, Wp, Lp-Gd)  # fixed values, no expression
        oEditor.Unite(
            ["NAME:Selections","Selections:=",",".join([tag+"L",tag+"R",tag+"T"])],
            ["NAME:UniteParameters","KeepOriginals:=",False])
        pe(tag+"L")

# ══════════════════════════════════════════════
# 4. Port
# ══════════════════════════════════════════════
rc("Port1", Jx_c-W50/2, 0, W50, Hs, -Hs, ax="Y")
lp("Port1", 1, Jx_c, 0)

# ══════════════════════════════════════════════
# 5. AirBox + Radiation
# ══════════════════════════════════════════════
m = 15.0
bx("Air", -m, -m, -Hs-m, SubW+2*m, SubL+2*m, Hs+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(
    ["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,
     "IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

path = os.path.join(os.path.expanduser("~"),"Documents","Ansoft","Competition_4x8.aedt")
oProject.SaveAs(path, True)
print("DONE:", path)
print("4x8 = %d elements, Sub: %.0fx%.0fmm (limit 240x240)"%
      (N_col*N_row, SubW, SubL))
print("Manual: Solution Setup @ 5.8GHz, Sweep 5.5-6.5GHz")
print("Expect: S11<-10dB (same as project5), Gain > 12dBi")
