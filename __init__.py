import BakeSymmetry.BakeSymmetry_v2 as Bake

def starts_SymmetryBake():
	reload(Bake)
	#Bake.BakeSymmetry()
	print "--- INIT BAKE SYMMETRY ---"

actionShowSymmetryBakeUI = mari.actions.create('Show Bake Symmetry UI', "starts_SymmetryBake()")
actionShowSymmetryBakeUI.setShortcut('Ctrl+Alt+S')
#mari.menus.addAction(actionShowSymmetryBakeUI, "MainWindow/d&eTools/&Symmetry")
print "BAKE SYMMETRY IMPORTED..."