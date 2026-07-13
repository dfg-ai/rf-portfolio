# -*- coding: utf-8 -*-
"""3-port straight thru: 1 line, 3 ports — does 3-port even work?"""
import sys, os

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "Test3Port", "Driven Modal", "")
oDesign = oProject.SetActiveDesign("Test3Port")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oDesign.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

_B=["NAME:Attributes","Flags:=","","Color:=","(132 132 193)","Transparency:=",0,"PartCoordinateSystem:=","Global","UDMId:=","","SolveInside:=",True,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False]

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

W,Jx,H=3.1,25.0,1.6
# Sub + Gnd
bx("Sub",0,0,-H,50,60,H,"FR4_epoxy")
rc("Gnd",0,0,50,60,-H); pe("Gnd")
# ONE continuous 50Ω line Y=10 to Y=50
rc("TL",Jx-W/2,10,W,40); pe("TL")
# 3 ports on the SAME line
rc("P1",Jx-W/2,10,W,H,-H,ax="Y"); lp("P1",1,Jx,10)
rc("P2",Jx-W/2,30,W,H,-H,ax="Y"); lp("P2",2,Jx,30)
rc("P3",Jx-W/2,50,W,H,-H,ax="Y"); lp("P3",3,Jx,50)

m=15; bx("Air",-m,-m,-H-m,50+2*m,60+2*m,H+2*m)
oDesign.GetModule("BoundarySetup").AssignRadiation(["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,"IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

p=os.path.join(os.path.expanduser("~"),"Documents","Ansoft","_test_3port.aedt")
oProject.SaveAs(p,True)
print("DONE:",p)
print("If S11~0dB => 3-port fundamentally broken")
print("If S11<-10dB => junction geometry is the issue")
