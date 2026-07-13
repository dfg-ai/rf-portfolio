# -*- coding: utf-8 -*-
"""T-junction test: 1 input → 2 output (no rotation, no λ/4 matching)"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "TestTee", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("TestTee")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(
    ["NAME:Design Settings Data", "Units:=", "mm", "Rescale when change units:=", False])

_B = ["NAME:Attributes", "Flags:=", "", "Color:=", "(132 132 193)", "Transparency:=", 0,
    "PartCoordinateSystem:=", "Global", "UDMId:=", "",
    "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False]

def bx(n,x,y,z,sx,sy,sz,m="vacuum"):
    oEditor.CreateBox(["NAME:BoxParameters","XPosition:=","%.4fmm"%x,"YPosition:=","%.4fmm"%y,"ZPosition:=","%.4fmm"%z,"XSize:=","%.4fmm"%sx,"YSize:=","%.4fmm"%sy,"ZSize:=","%.4fmm"%sz],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"'+m+'"',"SurfaceMaterialValue:=",'""']+_B[1:])

def rc(n,x,y,w,h,z=0,ax="Z"):
    oEditor.CreateRectangle(["NAME:RectangleParameters","IsCovered:=",True,"XStart:=","%.4fmm"%x,"YStart:=","%.4fmm"%y,"ZStart:=","%.4fmm"%z,"Width:=","%.4fmm"%w,"Height:=","%.4fmm"%h,"WhichAxis:=",ax],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"vacuum"',"SurfaceMaterialValue:=",'""']+_B[1:])

_p=[0]
def pe(n):
    _p[0]+=1
    oDesign.GetModule("BoundarySetup").AssignPerfectE(["NAME:PE%d"%_p[0],"Objects:=",[n],"InfGroundPlane:=",False])

def lp(n,num,cx,cy):
    oDesign.GetModule("BoundarySetup").AssignLumpedPort(["NAME:%d"%num,"Objects:=",[n],"DoDeembed:=",False,"RenormalizeAllTerminals:=",True,["NAME:Modes",["NAME:Mode1","ModeNum:=",1,"UseIntLine:=",True,["NAME:IntLine","Start:=",["%.4fmm"%cx,"%.4fmm"%cy,"%.4fmm"%(-1.6)],"End:=",["%.4fmm"%cx,"%.4fmm"%cy,"%.4fmm"%(0.0)]],"AlignmentGroup:=",0,"CharImp:=","Zpi","RenormImp:=","50ohm"]],"ShowReporterFilter:=",False,"ReporterFilter:=",[True],"Impedance:=","50ohm"])

W,Jx,Jy,H=3.1,25.0,25.0,1.6
# Sub + Gnd
bx("Sub",0,0,-H,50,60,H,"FR4_epoxy")
rc("Gnd",0,0,50,60,-H); pe("Gnd")
# Input 50Ω line: Y=0 to Y=25
rc("L1",Jx-W/2,0,W,Jy); pe("L1")
# Output right: X=25 to X=45, Y=25 (horizontal)
rc("L2",Jx,Jy,W,20); pe("L2")
# Output left: X=5 to X=25, Y=25
rc("L3",Jx-20,Jy,W,20); pe("L3")
# Port 1: input at Y=0
rc("P1",Jx-W/2,0,W,H,-H,ax="Y"); lp("P1",1,Jx,0)
# Port 2: right output at X=45
rc("P2",45,Jy,W,H,-H,ax="Y"); lp("P2",2,45+W/2,Jy)
# Port 3: left output at X=5
rc("P3",5-W,Jy,W,H,-H,ax="Y"); lp("P3",3,5-W/2,Jy)

m=15; bx("Air",-m,-m,-H-m,50+2*m,60+2*m,H+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,"IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

p=os.path.join(os.path.expanduser("~"),"Documents","Ansoft","_test_tee.aedt")
oProject.SaveAs(p,True)
print("DONE:",p)
