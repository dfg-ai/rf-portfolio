# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 11:53:29  7月 13, 2026
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project4")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "-0.6mm",
		"YStart:="		, "-1mm",
		"ZStart:="		, "0mm",
		"Width:="		, "1.2mm",
		"Height:="		, "2.2mm",
		"WhichAxis:="		, "Z"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Rectangle1",
		"Flags:="		, "",
		"Color:="		, "(143 175 143)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"IsMaterialEditable:="	, True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignLumpedRLC(
	[
		"NAME:LumpRLC1",
		"Objects:="		, ["Rectangle1"],
		[
			"NAME:CurrentLine",
			"Start:="		, ["0.4mm","-0.2mm","0mm"],
			"End:="			, ["0mm","-0.2mm","0mm"]
		],
		"RLC Type:="		, "Parallel",
		"UseResist:="		, True,
		"Resistance:="		, "100ohm",
		"UseInduct:="		, False,
		"UseCap:="		, False
	])
