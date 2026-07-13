# -*- coding: utf-8 -*-
"""Wilkinson Power Divider @ 2.44GHz, FR4 - NO rotation, all orthogonal traces."""
import sys, os, math

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Wilkinson_2p4GHz", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Wilkinson_2p4GHz")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

_B = ["NAME:Attributes","Flags:=","","Color:=","(132 132 193)","Transparency:=",0,
    "PartCoordinateSystem:=","Global","UDMId:=","",
    "SolveInside:=",True,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False]

def bx(n,x,y,z,sx,sy,sz,m="vacuum"):
    oEditor.CreateBox(["NAME:BoxParameters","XPosition:=","%.4fmm"%x,"YPosition:=","%.4fmm"%y,"ZPosition:=","%.4fmm"%z,"XSize:=","%.4fmm"%sx,"YSize:=","%.4fmm"%sy,"ZSize:=","%.4fmm"%sz],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"'+m+'"',"SurfaceMaterialValue:=",'""']+_B[1:])

def rc(n,x,y,w,h,z=0,ax="Z"):
    oEditor.CreateRectangle(["NAME:RectangleParameters","IsCovered:=",True,"XStart:=","%.4fmm"%x,"YStart:=","%.4fmm"%y,"ZStart:=","%.4fmm"%z,"Width:=","%.4fmm"%w,"Height:=","%.4fmm"%h,"WhichAxis:=",ax],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"vacuum"',"SurfaceMaterialValue:=",'""']+_B[1:])

def pe(n):
    oDesign.GetModule("BoundarySetup").AssignPerfectE(["NAME:PE_"+n,"Objects:=",[n],"InfGroundPlane:=",False])

def lp(n,num,cx,cy):
    oDesign.GetModule("BoundarySetup").AssignLumpedPort(["NAME:%d"%num,"Objects:=",[n],"DoDeembed:=",False,"RenormalizeAllTerminals:=",True,["NAME:Modes",["NAME:Mode1","ModeNum:=",1,"UseIntLine:=",True,["NAME:IntLine","Start:=",["%.4fmm"%cx,"%.4fmm"%cy,"-1.6000mm"],"End:=",["%.4fmm"%cx,"%.4fmm"%cy,"0.0000mm"]],"AlignmentGroup:=",0,"CharImp:=","Zpi","RenormImp:=","50ohm"]],"ShowReporterFilter:=",False,"ReporterFilter:=",[True],"Impedance:=","50ohm"])

# ── PARAMS (no rotation, orthogonal layout) ──
W50, W70 = 3.1, 1.3
Lq = 17.0       # 70.7Ω λ/4 length
Lin_v = 20.0    # input vertical line
Lout_v = 12.0   # output vertical line
H, Ws, Ls = 1.6, 50.0, 60.0
Jx, Jy = Ws/2.0, 25.0  # junction at center

# Endpoints of horizontal 70.7Ω branches
rx = Jx + Lq  # right branch end X = 42
lx = Jx - Lq  # left branch end X = 8
ry = Jy       # same Y for both = 25

# Overlap margin
mrg = 3.0

# ═══════════════════════════
# 1. Substrate
# ═══════════════════════════
bx("Sub", 0, 0, -H, Ws, Ls, H, "FR4_epoxy")

# ═══════════════════════════
# 2. Ground
# ═══════════════════════════
rc("Gnd", 0, 0, Ws, Ls, -H); pe("Gnd")

# ═══════════════════════════
# 3. Junction pad (connects all 3 lines)
# ═══════════════════════════
rc("Pad_J", Jx-4, Jy-4, 8, 8)

# ═══════════════════════════
# 4. Input 50Ω line (vertical, from Port1 to junction pad)
# ═══════════════════════════
rc("L1", Jx-W50/2, 0, W50, Lin_v+mrg)  # extends into pad

# ═══════════════════════════
# 5. Right 70.7Ω branch (horizontal, from pad to right pad)
# ═══════════════════════════
rc("L2R", Jx, Jy-W70/2, Lq-W70/2, W70)  # from Jx to Jx+Lq-W70/2 ≈ Jx+Lq
# Actually: XStart=Jx=25, Width=Lq+some_overlap, need to reach rx

# Let me just do full length with pad overlap
rc("L2R", Jx-W70/2, Jy-W70/2, Lq+W70/2, W70)  # from Jx-W70/2 to Jx+Lq

# Left 70.7Ω branch
rc("L2L", Jx-Lq-W70/2, Jy-W70/2, Lq+W70/2, W70)  # from Jx-Lq-W70/2 to Jx+W70/2

# ═══════════════════════════
# 6. Output pads
# ═══════════════════════════
rc("Pad_R", rx-3, ry-3, 6, 6)
rc("Pad_L", lx-3, ry-3, 6, 6)

# ═══════════════════════════
# 7. Output 50Ω lines (vertical, from pad up)
# ═══════════════════════════
rc("L3R", rx-W50/2, ry-mrg, W50, Lout_v+mrg)
rc("L3L", lx-W50/2, ry-mrg, W50, Lout_v+mrg)

# ═══════════════════════════
# 8. UNITE all traces → one conductor
# ═══════════════════════════
oEditor.Unite(
    ["NAME:Selections","Selections:=","Pad_J,L1,L2R,L2L,Pad_R,Pad_L,L3R,L3L"],
    ["NAME:UniteParameters","KeepOriginals:=",False])
pe("Pad_J")  # one Perfect E for entire united conductor

# ═══════════════════════════
# 9. Isolation Resistor — SKIPPED (v2 will add with proper no-overlap layout)
# ═══════════════════════════

# ═══════════════════════════
# 9. Ports (all vertical traces → ports in XZ plane)
# ═══════════════════════════
rc("P1", Jx-W50/2, 0, W50, H, -H, ax="Y"); lp("P1", 1, Jx, 0)
py_out = Jy + Lout_v
rc("P2", rx-W50/2, py_out, W50, H, -H, ax="Y"); lp("P2", 2, rx, py_out)
rc("P3", lx-W50/2, py_out, W50, H, -H, ax="Y"); lp("P3", 3, lx, py_out)

# ═══════════════════════════
# 10. AirBox
# ═══════════════════════════
m=15; bx("Air", -m, -m, -H-m, Ws+2*m, Ls+2*m, H+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,"IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

p = os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "Wilkinson_v1.aedt")
oProject.SaveAs(p, True)
print("DONE:", p)
