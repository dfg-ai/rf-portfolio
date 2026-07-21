# -*- coding: utf-8 -*-
"""
Competition: 8x4 Array @ 5.8GHz
4-row series-fed columns (PROVEN: S11=-18dB from project 5)
8-column corporate feed (1→2→4→8, 7 T-junctions, 3 levels)
32 elements total. Expected gain: 11.4-12.4 dBi.
"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Array8x4_58G", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Array8x4_58G")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

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

# ══════════════════════════════════════════════
# DESIGN PARAMETERS (exact project5 values, scaled up columns)
# ══════════════════════════════════════════════
Hs=1.6; W50=3.1; W70=1.3
Wp=15.74; Lp=10.00; Gd=3.30; Gw=W50+1.0  # more aggressive shift
dx=25.0; dy=24.0
N_col=8; N_row=4  # 8 cols × 4 rows = 32 elements

SubW = dx*(N_col-1) + Wp + 30   # ≈ 210mm
Jx_c = SubW/2.0

# Column centers
col_x = [Jx_c + (i-(N_col-1)/2.0)*dx for i in range(N_col)]

# Corporate feed Y levels (must be before Y0)
J1y = 4.0; J2y = 8.0; J3y = 13.0

Y0 = J3y + 6   # first row after feed
cy = [Y0 + j*dy for j in range(N_row)]
SubL = dy*(N_row-1) + Lp + Y0 + 12  # ≈ 105mm

# ══════════════════════════════════════════════
# 1. Substrate + Ground
# ══════════════════════════════════════════════
bx("Sub", 0, 0, -Hs, SubW, SubL, Hs, "FR4_epoxy")
rc("Gnd", 0, 0, SubW, SubL, -Hs); pe("Gnd")

# ══════════════════════════════════════════════
# 2. Corporate feed: 1→2→4→8 (3 levels, 7 T-junctions)
# ══════════════════════════════════════════════
# Input line (J1y, J2y, J3y defined in param section above)
rc("FeedIn", Jx_c-W50/2, 0, W50, J1y); pe("FeedIn")

# J1: split left 4 vs right 4
mid_l4 = (col_x[0]+col_x[3])/2.0
mid_r4 = (col_x[4]+col_x[7])/2.0
rc("J1h", mid_l4-W50/2, J1y-W50/2, mid_r4-mid_l4+W50, W50); pe("J1h")
rc("J1vl", mid_l4-W50/2, J1y, W50, J2y-J1y); pe("J1vl")
rc("J1vr", mid_r4-W50/2, J1y, W50, J2y-J1y); pe("J1vr")

# J2: long horizontals covering each half (cols 0-3, cols 4-7)
rc("J2hL", col_x[0]-W50/2, J2y-W50/2, col_x[3]-col_x[0]+W50, W50); pe("J2hL")
rc("J2hR", col_x[4]-W50/2, J2y-W50/2, col_x[7]-col_x[4]+W50, W50); pe("J2hR")

# J2→J3 verticals for each sub-half midpoint
for left, right in [(0,1),(2,3),(4,5),(6,7)]:
    mid = (col_x[left]+col_x[right])/2.0
    rc("J2v_%d%d"%(left,right), mid-W50/2, J2y, W50, J3y-J2y); pe("J2v_%d%d"%(left,right))

# J3: horizontal pairs → individual column verticals
for left, right in [(0,1),(2,3),(4,5),(6,7)]:
    rc("J3h_%d%d"%(left,right), col_x[left]-W50/2, J3y-W50/2,
       col_x[right]-col_x[left]+W50, W50); pe("J3h_%d%d"%(left,right))
    for ci in [left, right]:
        rc("J3v_%d"%ci, col_x[ci]-W50/2, J3y, W50, cy[0]-J3y); pe("J3v_%d"%ci)

# ══════════════════════════════════════════════
# 3. Series-fed columns (1×4 each — PROJECT 5 VERIFIED)
# ══════════════════════════════════════════════
for c, cx in enumerate(col_x):
    line_end = cy[-1] + Lp + 5.0
    rc("ML%d"%c, cx-W50/2, cy[0], W50, line_end-cy[0]); pe("ML%d"%c)
    for i, ry in enumerate(cy):
        px = cx-Wp/2; nx = cx-Gw/2; ntop = ry+Gd
        tag = "C%dR%d"%(c,i)
        rc(tag+"L", px, ry, nx-px, Lp)
        rc(tag+"R", nx+Gw, ry, (px+Wp)-(nx+Gw), Lp)
        rc(tag+"T", px, ntop, Wp, Lp-Gd)
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

path = os.path.join(os.path.expanduser("~"),"Documents","Ansoft","Competition_8x4.aedt")
oProject.SaveAs(path, True)
print("DONE:", path)
print("8x4 = %d elements, Substrate: %.0fx%.0fmm (limit 240x240)"%
      (N_col*N_row, SubW, SubL))
print("Manual: Solution Setup @ 5.8GHz, Sweep 5.5-6.5GHz")
