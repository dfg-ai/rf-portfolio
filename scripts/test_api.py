# -*- coding: utf-8 -*-
"""Minimal test: create one rectangle. If this works, API format is correct."""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Test", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Test")
oEditor = oDesign.SetActiveEditor("3D Modeler")

# Set units to mm
oDesign.SetDesignSettings(
    ["NAME:Design Settings Data",
     "Units:=", "mm",
     "Rescale when change units:=", False])

# Create ONE test rectangle
oEditor.CreateRectangle(
    ["NAME:RectangleParameters",
     "IsCovered:=", True,
     "XStart:=", "10mm",
     "YStart:=", "10mm",
     "ZStart:=", "0mm",
     "Width:=", "20mm",
     "Height:=", "5mm",
     "WhichAxis:=", "Z"],
    ["NAME:Attributes",
     "Name:=", "TestRect",
     "Flags:=", "",
     "Color:=", "(132 132 193)",
     "Transparency:=", 0,
     "PartCoordinateSystem:=", "Global",
     "UDMId:=", "",
     "MaterialValue:=", '"vacuum"',
     "SurfaceMaterialValue:=", '""',
     "SolveInside:=", True,
     "IsMaterialEditable:=", True,
     "UseMaterialAppearance:=", False])

# Save
path = os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "_test_api.aedt")
oProject.SaveAs(path, True)
print("OK:", path)
