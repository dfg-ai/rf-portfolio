# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2021.1.0
# 10:29:49  7月 13, 2026
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project4")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignLumpedPort(
	[
		"NAME:1",
		"Objects:="		, ["Rectangle1"],
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
					"Start:="		, ["0.8mm","0mm","0mm"],
					"End:="			, ["0.3mm","0mm","0mm"]
				],
				"AlignmentGroup:="	, 0,
				"CharImp:="		, "Zpi",
				"RenormImp:="		, "50ohm"
			]
		],
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [True],
		"Impedance:="		, "50ohm"
	])
