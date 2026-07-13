# -*- coding: utf-8 -*-
"""Test 2: Create rect, rotate it, verify."""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Test2", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Test2")
oEditor = oDesign.SetActiveEditor("3D Modeler")

oDesign.SetDesignSettings(
    ["NAME:Design Settings Data",
     "Units:=", "mm",
     "Rescale when change units:=", False])

# Create substrate for reference
oEditor.CreateBox(
    ["NAME:BoxParameters",
     "XPosition:=", "0mm", "YPosition:=", "0mm", "ZPosition:=", "-1.6mm",
     "XSize:=", "50mm", "YSize:=", "60mm", "ZSize:=", "1.6mm"],
    ["NAME:Attributes",
     "Name:=", "Sub", "Flags:=", "", "Color:=", "(132 132 193)",
     "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=", "",
     "MaterialValue:=", '"FR4_epoxy"', "SurfaceMaterialValue:=", '""',
     "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False])

# Create a vertical rectangle at junction
oEditor.CreateRectangle(
    ["NAME:RectangleParameters",
     "IsCovered:=", True,
     "XStart:=", "24.35mm", "YStart:=", "15mm", "ZStart:=", "0mm",
     "Width:=", "1.3mm", "Height:=", "17mm", "WhichAxis:=", "Z"],
    ["NAME:Attributes",
     "Name:=", "Branch", "Flags:=", "", "Color:=", "(255 200 150)",
     "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=", "",
     "MaterialValue:=", '"vacuum"', "SurfaceMaterialValue:=", '""',
     "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False])

# Rotate around Z at (25, 15) by -45 deg
oEditor.Rotate(
    ["NAME:Selections", "Selections:=", "Branch", "NewPartsModelFlag:=", "Model"],
    ["NAME:RotateParameters",
     "RotateAxis:=", "Z",
     "RotateAngle:=", "-45deg",
     "RotateOriginX:=", "25mm",
     "RotateOriginY:=", "15mm",
     "RotateOriginZ:=", "0mm"])

path = os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "_test_rotate.aedt")
oProject.SaveAs(path, True)
print("OK:", path)
