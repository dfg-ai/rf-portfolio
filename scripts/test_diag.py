# -*- coding: utf-8 -*-
"""Diagonal line test: 2 ports at different X positions.
   If S11 good => rotated traces are fine, issue is junction.
   If S11 bad => ports at different X positions breaks things."""
import sys,os,math

oP=oDesktop.NewProject(); oP.InsertDesign("HFSS","Diag","Driven Modal","")
oD=oP.SetActiveDesign("Diag"); oE=oD.SetActiveEditor("3D Modeler")
oD.SetDesignSettings(["NAME:Design Settings Data","Units:=","mm","Rescale when change units:=",False])

_B=["NAME:Attributes","Flags:=","","Color:=","(132 132 193)","Transparency:=",0,"PartCoordinateSystem:=","Global","UDMId:=","","SolveInside:=",True,"IsMaterialEditable:=",True,"UseMaterialAppearance:=",False]

def bx(n,x,y,z,sx,sy,sz,m="vacuum"):
    oE.CreateBox(["NAME:BoxParameters","XPosition:=","%.4fmm"%x,"YPosition:=","%.4fmm"%y,"ZPosition:=","%.4fmm"%z,"XSize:=","%.4fmm"%sx,"YSize:=","%.4fmm"%sy,"ZSize:=","%.4fmm"%sz],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"'+m+'"',"SurfaceMaterialValue:=",'""']+_B[1:])

def rc(n,x,y,w,h,z=0,ax="Z"):
    oE.CreateRectangle(["NAME:RectangleParameters","IsCovered:=",True,"XStart:=","%.4fmm"%x,"YStart:=","%.4fmm"%y,"ZStart:=","%.4fmm"%z,"Width:=","%.4fmm"%w,"Height:=","%.4fmm"%h,"WhichAxis:=",ax],["NAME:Attributes","Name:=",n,"MaterialValue:=",'"vacuum"',"SurfaceMaterialValue:=",'""']+_B[1:])

_p=[0]
def pe(n):
    _p[0]+=1; oD.GetModule("BoundarySetup").AssignPerfectE(["NAME:PE%d"%_p[0],"Objects:=",[n],"InfGroundPlane:=",False])

def lp(n,num,cx,cy):
    oD.GetModule("BoundarySetup").AssignLumpedPort(["NAME:%d"%num,"Objects:=",[n],"DoDeembed:=",False,"RenormalizeAllTerminals:=",True,["NAME:Modes",["NAME:Mode1","ModeNum:=",1,"UseIntLine:=",True,["NAME:IntLine","Start:=",["%.4fmm"%cx,"%.4fmm"%cy,"-1.6000mm"],"End:=",["%.4fmm"%cx,"%.4fmm"%cy,"0.0000mm"]],"AlignmentGroup:=",0,"CharImp:=","Zpi","RenormImp:=","50ohm"]],"ShowReporterFilter:=",False,"ReporterFilter:=",[True],"Impedance:=","50ohm"])

def rot(n,a,cx,cy):
    oE.Rotate(["NAME:Selections","Selections:=",n,"NewPartsModelFlag:=","Model"],["NAME:RotateParameters","RotateAxis:=","Z","RotateAngle:=","%.6fdeg"%a,"RotateOriginX:=","%.4fmm"%cx,"RotateOriginY:=","%.4fmm"%cy,"RotateOriginZ:=","0mm"])

W,H,Jx,Jy=3.1,1.6,25.0,15.0
bx("Sub",0,0,-H,50,60,H,"FR4_epoxy")
rc("Gnd",0,0,50,60,-H); pe("Gnd")

# Diagonal line: from (Jx,0) to (Jx+15, 30) — same angle as Wilkinson branch
rc("TL",Jx-W/2,0,W,15); pe("TL")
rot("TL",-45,Jx,0)

# Port 1 at start, Port 2 at end
rc("P1",Jx-W/2,0,W,H,-H,ax="Y"); lp("P1",1,Jx,0)

# Endpoint: Jx+15*sin(45)=Jx+10.6=35.6, 15*cos(45)=10.6
ex,ey=Jx+15*0.7071,10.6
rc("P2",ex-W/2,ey,W,H,-H,ax="Y"); lp("P2",2,ex,ey)

m=15; bx("Air",-m,-m,-H-m,50+2*m,60+2*m,H+2*m)
oD.GetModule("BoundarySetup").AssignRadiation(["NAME:Rad","Objects:=",["Air"],"IsFfdInterface:=",False,"IsForPML:=",False,"IncludeForNearField:=",True,"UseAdaptiveIE:=",False])

p=os.path.join(os.path.expanduser("~"),"Documents","Ansoft","_test_diag.aedt")
oP.SaveAs(p,True)
print("DONE:",p)
