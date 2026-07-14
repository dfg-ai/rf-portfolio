# -*- coding: utf-8 -*-
"""
End-Coupled Bandpass Filter @ 2.44GHz, FR4
2-pole Chebyshev (0.5dB ripple), 5% FBW
All vertical lines, no rotation, gaps between segments.
"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Filter_2p4GHz", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Filter_2p4GHz")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

# ── Verified helpers (same format as build_wilkinson.py) ──
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
W50  = 3.1     # 50-ohm line width
Hs   = 1.6      # substrate thickness
Ws   = 50.0     # substrate width
Ls   = 90.0     # substrate length (taller for filter)
Jx   = Ws / 2.0 # center X = 25
Lfeed= 10.0     # feed line length
Lres = 30.8     # resonator length — best after 5 iterations
G01  = 0.15     # input gap — best balance coupling vs radiation loss
G12  = 0.6      # inter-resonator gap
G23  = 0.15     # output gap

# Y positions
Y0 = 0.0
Y1 = Y0 + Lfeed          # 10.0
Y2 = Y1 + G01            # 10.3
Y3 = Y2 + Lres           # 43.6
Y4 = Y3 + G12            # 44.1
Y5 = Y4 + Lres           # 77.4
Y6 = Y5 + G23            # 77.7
Y7 = Y6 + Lfeed          # 87.7

# ═══════════════════════════
# 1. Substrate
# ═══════════════════════════
bx("Sub", 0, 0, -Hs, Ws, Ls, Hs, "FR4_epoxy")

# ═══════════════════════════
# 2. Ground
# ═══════════════════════════
rc("Gnd", 0, 0, Ws, Ls, -Hs)
pe("Gnd")

# ═══════════════════════════
# 3. Trace segments (each with own Perfect E)
# ═══════════════════════════
# Feed line 1 (Port 1 side)
rc("Feed1", Jx-W50/2, Y0, W50, Lfeed)
pe("Feed1")

# Resonator 1
rc("Res1", Jx-W50/2, Y2, W50, Lres)
pe("Res1")

# Resonator 2
rc("Res2", Jx-W50/2, Y4, W50, Lres)
pe("Res2")

# Feed line 2 (Port 2 side)
rc("Feed2", Jx-W50/2, Y6, W50, Lfeed)
pe("Feed2")

# ═══════════════════════════
# 4. Ports (centered on feed lines)
# ═══════════════════════════
rc("Port1", Jx-W50/2, Y0, W50, Hs, -Hs, ax="Y")
lp("Port1", 1, Jx, Y0)

rc("Port2", Jx-W50/2, Y7, W50, Hs, -Hs, ax="Y")
lp("Port2", 2, Jx, Y7)

# ═══════════════════════════
# 5. AirBox + Radiation
# ═══════════════════════════
m = 15.0
bx("Air", -m, -m, -Hs-m, Ws+2*m, Ls+2*m, Hs+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(
    ["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,
     "IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

# ═══════════════════════════
# Save
# ═══════════════════════════
path = os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "Filter_v1.aedt")
oProject.SaveAs(path, True)
print("DONE:", path)
print("Manual: Add Solution Setup @ 2.44GHz, Sweep 1.5-3.5GHz")
print("Expect: S21 peak near 2.44GHz (bandpass), S11 dip at center freq")
