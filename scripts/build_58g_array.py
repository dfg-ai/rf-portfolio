# -*- coding: utf-8 -*-
"""
5.8GHz 4x4 Series-Fed Array — Step 3: Full 4x4.
4 columns of 1x4 series-fed patches, combined via corporate feed.
"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Array58G_4x4", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Array58G_4x4")
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

# ── DESIGN PARAMETERS ──
W50=3.1; Hs=1.6; Jx_center = 70.0
Wp=15.74; Lp=10.50; Gd=3.50; Gw=W50+1.0
lambdag=25.0; N=4; Lfeed=10.0  # 3rd scale: 5.70→5.8GHz
dx=26.0    # column spacing (λ₀/2 ≈ 26mm)
SubW = dx*3 + Wp + 20  # = 26*3 + 15.74 + 20 = 113.74
SubL = lambdag*3 + Lp + Lfeed + 15

# Column X centers
col_x = [Jx_center + (i-1.5)*dx for i in range(4)]  # equally spaced
Y0 = 15.0  # first patch Y in each column
Yc = [Y0 + i*lambdag for i in range(N)]

# ═══════════════════════════
# 1. Substrate + Ground
# ═══════════════════════════
bx("Sub", 0, 0, -Hs, SubW, SubL, Hs, "FR4_epoxy")
rc("Gnd", 0, 0, SubW, SubL, -Hs); pe("Gnd")

# ═══════════════════════════
# 2. Corporate feed network (input → 4 equal outputs)
# ═══════════════════════════
J1y = 8.0  # first T-junction Y
J2y = 12.0  # second T-junction Y

# Input line: Port1 → J1
rc("FeedIn", Jx_center-W50/2, 0, W50, J1y); pe("FeedIn")

# J1 horizontal split
jx1 = col_x[0]+dx/2; jx2 = col_x[3]-dx/2
rc("J1h", jx1-W50/2, J1y-W50/2, jx2-jx1+W50, W50); pe("J1h")

# J2 level: vertical lines from J1 to J2 at the two branch points
# Left branch: feeds columns 0,1. Right branch: feeds columns 2,3.
bjx_l = (col_x[0]+col_x[1])/2  # midpoint of left 2 columns
bjx_r = (col_x[2]+col_x[3])/2  # midpoint of right 2 columns

# Connect J1 to J2 level
rc("J2vl", bjx_l-W50/2, J1y, W50, J2y-J1y); pe("J2vl")
rc("J2vr", bjx_r-W50/2, J1y, W50, J2y-J1y); pe("J2vr")

# J2 horizontal splits
rc("J2hl", col_x[0]-W50/2, J2y-W50/2, col_x[1]-col_x[0]+W50, W50); pe("J2hl")
rc("J2hr", col_x[2]-W50/2, J2y-W50/2, col_x[3]-col_x[2]+W50, W50); pe("J2hr")

# Column feeds: vertical from J2 to each column
col_feed_y = J2y+5  # transition point
for i, cx in enumerate(col_x):
    rc("Cf%d"%i, cx-W50/2, J2y, W50, col_feed_y-J2y); pe("Cf%d"%i)

# ═══════════════════════════
# 3. Series-fed columns — each identical to 1x4 line array
# ═══════════════════════════
for c, cx in enumerate(col_x):
    line_end = Yc[-1] + Lp/2 + 5.0
    rc("ML%d"%c, cx-W50/2, col_feed_y, W50, line_end-col_feed_y); pe("ML%d"%c)
    for i, cy in enumerate(Yc):
        px = cx - Wp/2; nx = cx - Gw/2; ntop = cy + Gd
        tag = "C%dP%d" % (c, i+1)
        rc(tag+"L", px, cy, nx-px, Lp)
        rc(tag+"R", nx+Gw, cy, (px+Wp)-(nx+Gw), Lp)
        rc(tag+"T", px, ntop, Wp, Lp-Gd)
        oEditor.Unite(
            ["NAME:Selections","Selections:=",",".join([tag+"L",tag+"R",tag+"T"])],
            ["NAME:UniteParameters","KeepOriginals:=",False])
        pe(tag+"L")

# ═══════════════════════════
# 4. Port
# ═══════════════════════════
rc("Port1", Jx_center-W50/2, 0, W50, Hs, -Hs, ax="Y")
lp("Port1", 1, Jx_center, 0)

# ═══════════════════════════
# 5. AirBox + Radiation
# ═══════════════════════════
m = 12.0
bx("Air", -m, -m, -Hs-m, SubW+2*m, SubL+2*m, Hs+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(
    ["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,
     "IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

path = os.path.join(os.path.expanduser("~"),"Documents","Ansoft","Array58G_v1.aedt")
oProject.SaveAs(path, True)
print("DONE:", path)
print("Manual: Solution Setup @ 5.8GHz, Sweep 4-8GHz")
print("Then: 3D Far Field → GainTotal — expect beam narrow in both X and Y")
