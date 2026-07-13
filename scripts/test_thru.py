# -*- coding: utf-8 -*-
"""Minimal test: 50Ω microstrip thru line — 2 ports only"""
import sys, os, math

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "TestThru", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("TestThru")
oEditor = oDesign.SetActiveEditor("3D Modeler")

oDesign.SetDesignSettings(
    ["NAME:Design Settings Data", "Units:=", "mm", "Rescale when change units:=", False])

# Helpers
_BATTR = ["NAME:Attributes", "Flags:=", "", "Color:=", "(132 132 193)",
    "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=", "",
    "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False]

def box(name, x, y, z, sx, sy, sz, mat="vacuum"):
    oEditor.CreateBox(
        ["NAME:BoxParameters",
         "XPosition:=", "%.4fmm"%x, "YPosition:=", "%.4fmm"%y, "ZPosition:=", "%.4fmm"%z,
         "XSize:=", "%.4fmm"%sx, "YSize:=", "%.4fmm"%sy, "ZSize:=", "%.4fmm"%sz],
        ["NAME:Attributes", "Name:=", name,
         "MaterialValue:=", '"'+mat+'"', "SurfaceMaterialValue:=", '""'] + _BATTR[1:])

def rect(name, x, y, w, h, z=0.0, axis="Z"):
    oEditor.CreateRectangle(
        ["NAME:RectangleParameters", "IsCovered:=", True,
         "XStart:=", "%.4fmm"%x, "YStart:=", "%.4fmm"%y, "ZStart:=", "%.4fmm"%z,
         "Width:=", "%.4fmm"%w, "Height:=", "%.4fmm"%h, "WhichAxis:=", axis],
        ["NAME:Attributes", "Name:=", name,
         "MaterialValue:=", '"vacuum"', "SurfaceMaterialValue:=", '""'] + _BATTR[1:])

_pec = [0]
def pe(name):
    _pec[0] += 1
    oDesign.GetModule("BoundarySetup").AssignPerfectE(
        ["NAME:PerfE%d"%_pec[0], "Objects:=", [name], "InfGroundPlane:=", False])

def lport(name, num, cx, cy, z0=50):
    oDesign.GetModule("BoundarySetup").AssignLumpedPort([
        "NAME:%d"%num,
        "Objects:=", [name],
        "DoDeembed:=", False,
        "RenormalizeAllTerminals:=", True,
        ["NAME:Modes",
         ["NAME:Mode1",
          "ModeNum:=", 1,
          "UseIntLine:=", True,
          ["NAME:IntLine",
           "Start:=", ["%.4fmm"%cx, "%.4fmm"%cy, "%.4fmm"%(-1.6)],
           "End:=",   ["%.4fmm"%cx, "%.4fmm"%cy, "%.4fmm"%(0.0)]],
          "AlignmentGroup:=", 0,
          "CharImp:=", "Zpi",
          "RenormImp:=", "%dohm"%z0]],
        "ShowReporterFilter:=", False,
        "ReporterFilter:=", [True],
        "Impedance:=", "%dohm"%z0])

# Params
W50, Hs, Ws, Ls, Lline = 3.1, 1.6, 50.0, 60.0, 30.0
cx = Ws/2.0  # center X

# Substrate
box("Sub", 0, 0, -Hs, Ws, Ls, Hs, "FR4_epoxy")

# Ground
rect("Gnd", 0, 0, Ws, Ls, -Hs)
pe("Gnd")

# 50Ω line — centered, from Y=15 to Y=45
rect("TL", cx-W50/2, 15, W50, Lline)
pe("TL")

# Port 1 (Y=15) and Port 2 (Y=45)
rect("P1", cx-W50/2, 15, W50, Hs, -Hs, axis="Y")
rect("P2", cx-W50/2, 45, W50, Hs, -Hs, axis="Y")
lport("P1", 1, cx, 15)
lport("P2", 2, cx, 45)

# AirBox
m = 15.0
box("Air", -m, -m, -Hs-m, Ws+2*m, Ls+2*m, Hs+2*m, "vacuum")
oDesign.GetModule("BoundarySetup").AssignRadiation(
    ["NAME:Rad", "Objects:=", ["Air"],
     "IsFfdInterface:=", False, "IsForPML:=", False,
     "IncludeForNearField:=", True, "UseAdaptiveIE:=", False])

path = os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "_test_thru.aedt")
oProject.SaveAs(path, True)
print("DONE:", path)
print("Manual: Add Solution Setup @ 2.44GHz, Sweep 1.5-3.5GHz, then solve")
print("Expect: S11 < -15dB, S21 > -1dB (low-loss thru line)")
