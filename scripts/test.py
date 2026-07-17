# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 16:38:27  7月 17, 2026
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Array24G_v1")
oDesign = oProject.SetActiveDesign("Array24G_2x2")
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignWavePort(
	[
		"NAME:2",
		"Objects:="		, ["Port1"],
		"NumModes:="		, 1,
		"UseLineModeAlignment:=", False,
		"DoDeembed:="		, False,
		"RenormalizeAllTerminals:=", True,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, True,
				[
					"NAME:IntLine",
					"Start:="		, ["9.25mm","7.96639400082368e-17mm","-1.6mm"],
					"End:="			, ["9.25mm","5.78181961407994e-16mm","1.5mm"]
				],
				"AlignmentGroup:="	, 0,
				"CharImp:="		, "Zpi"
			]
		],
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [True],
		"UseAnalyticAlignment:=", False
	])
