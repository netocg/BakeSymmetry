import mari
import PySide
import os

class BakeSymmetry(PySide.QtGui.QWidget):

    def __init__(self):
        super(BakeSymmetry, self).__init__()
        self.script_path = self.script_path()
        self.scriptIconDir = os.path.join(self.script_path, 'Icons')
        print "V2 BAKE ICONS: " + self.scriptIconDir
        
        self.initUI()
        #self.shortcuts_menu()

    
    def initUI(self):
        ''' Creating UI and Connections '''

        bakeIcon = PySide.QtGui.QIcon()
        bakeIcon.addPixmap(PySide.QtGui.QPixmap('%s/BakeShader.png' % self.scriptIconDir))

        grid = PySide.QtGui.QGridLayout()
        grid.setSpacing(10)

        # Combo Box
        self.comboSymmetryXYZ = PySide.QtGui.QComboBox()
        self.comboSymmetryXYZ.setToolTip("Defines the mode of how Symmetry Paint Buffer will work. \nManual Clear Buffer - Does not clear the buffer after the paint get's mirrored through the symmetry axis by clicking on the 'bake button'. \nAuto Clear Buffer - Automatically clear the buffer after the paint get's mirrored through the symmetry axis by clicking on the 'bake button'. \nAuto Mirror Paint - Automate the process of mirror, bake&clear the paint buffer into the symmetry axis every time you or Mari is baking some paint.")
        self.comboSymmetryXYZ.addItem("Manual Clear Buffer")
        self.comboSymmetryXYZ.addItem("Auto Clear Buffer")
        self.comboSymmetryXYZ.addItem("Auto Mirror Paint")
        grid.addWidget(self.comboSymmetryXYZ,0,0,1,2)

        # Radio Buttons
        self.x_axis = PySide.QtGui.QRadioButton("X")
        self.y_axis = PySide.QtGui.QRadioButton("Y")
        self.z_axis = PySide.QtGui.QRadioButton("Z")
        self.x_axis.setChecked(True)

        # Setting Grid view
        grid.addWidget(self.x_axis,0,2)
        grid.addWidget(self.y_axis,0,3)
        grid.addWidget(self.z_axis,0,4)

        # Bake Button
        self.bSymmetry = PySide.QtGui.QPushButton("Bake")
        self.bSymmetry.setIcon(bakeIcon)
        self.bSymmetry.setToolTip("Bake the paint from the buffer when using the 'Manual Clear Buffer' or the 'Auto Clear Buffer' option.")
        grid.addWidget(self.bSymmetry,1,0,5,0)

        self.setLayout(grid)

        self.SymmetryMode()
        mari.utils.connect(self.comboSymmetryXYZ.activated[str], lambda: self.SymmetryMode())

    def disconnectBakeFunction(self):        
        #Use a try in case there is something already connect or disconnect from some previous option, like switching between modes 0 and 1.
        try:
            self.bSymmetry.clicked.disconnect(self.mirror_bake)
            print "bsymmetry disconnected"
        except:
            pass                        
        try:
            paintBuffer = mari.canvases.paintBuffer()
            paintBuffer.aboutToBake.disconnect(self.mirror_bake)
            print "paintBuffer disconnected"
        except:
            pass    

    def SymmetryMode(self):
        paintBuffer = mari.canvases.paintBuffer()
        if self.comboSymmetryXYZ.currentIndex() == 2:
            self.disconnectBakeFunction()
            paintBuffer.aboutToBake.connect(self.mirror_bake)
        else:
            self.disconnectBakeFunction()
            self.bSymmetry.clicked.connect(self.mirror_bake)

    def script_path(self):
        ''' Loops through the Mari user dirs finding the script location '''
        for script_paths in mari.resources.path(mari.resources.USER_SCRIPTS).split(";"):
    		for dirname, folder, files in os.walk(script_paths):
    			if "BakeSymmetry" in str(dirname):
    				scriptPath = os.path.join(dirname)
    				print "Script Install Path: " + str(scriptPath)
    				return scriptPath

    def shortcuts_menu(self):
        #Mari custom shortcuts actions.
        actionSymmetryBakeX = mari.actions.create('Bake Symmetry X', 'mirror_bake()')
        actionSymmetryBakeX.setShortcut("Shift+X")
        mari.menus.addAction( actionSymmetryBakeX, "MainWindow/d&eTools/&Symmetry" )

        actionSymmetryBakeY = mari.actions.create('Bake Symmetry Y', 'symmetryBakeY()')
        actionSymmetryBakeY.setShortcut("Shift+Y")
        mari.menus.addAction( actionSymmetryBakeY, "MainWindow/d&eTools/&Symmetry")

        actionSymmetryBakeZ = mari.actions.create('Bake Symmetry Z', 'symmetryBakeZ()')
        actionSymmetryBakeZ.setShortcut("Shift+Z")
        mari.menus.addAction( actionSymmetryBakeZ, "MainWindow/d&eTools/&Symmetry")

        actionCameraInverseX = mari.actions.create('Invert Canvas X', 'cameraInverseX()')
        actionCameraInverseX.setShortcut("Ctrl+Shift+X")
        mari.menus.addAction( actionCameraInverseX, "MainWindow/d&eTools/&Symmetry")

        actionCameraInverseY = mari.actions.create('Invert Canvas Y', 'cameraInverseY()')
        actionCameraInverseY.setShortcut("Ctrl+Shift+Y")
        mari.menus.addAction( actionCameraInverseY, "MainWindow/d&eTools/&Symmetry")

        actionCameraInverseZ = mari.actions.create('Invert Canvas Z', 'cameraInverseZ()')
        actionCameraInverseZ.setShortcut("Ctrl+Shift+Z")
        mari.menus.addAction( actionCameraInverseZ, "MainWindow/d&eTools/&Symmetry")

    def is_checked():
        ''' Checks or sets the axis '''

        self.x_axis.setChecked(True)

    def bake(self):
        ''' '''

    def mirror_bake(self):

        x=1
        y=1
        z=1
        pbx=1
        pby=1

        if self.x_axis.isChecked():
            x = -1
            pbx = -1
        elif self.y_axis.isChecked():
            y = -1
            pbx = -1
        elif self.z_axis.isChecked():
            z = -1
            pbx = -1

        canvas = mari.canvases.current()
        camera = canvas.camera()

        #Avoid Mirroring in the UV Viewport.
        if camera.UV == camera.type():
            return


        bake = mari.actions.find("/Mari/Canvas/Bake")

        paintBuffer = mari.canvases.paintBuffer()
        currentpaint = paintBuffer.saveContent()

        pb_scale = paintBuffer.scale()
        pb_rotation = paintBuffer.rotation()
        pb_translation = paintBuffer.translation()

        lookAt = camera.lookAt()
        translation = camera.translation()
        up = camera.up()

        #Move to mirrored position
        camera.setLookAt(mari.VectorN(x*lookAt.x(),y*lookAt.y(),z*lookAt.z()))
        camera.setTranslation(mari.VectorN(x*translation.x(),y*translation.y(),z*translation.z()))
        camera.setUp(mari.VectorN(x*up.x(),y*up.y(),z*up.z()))

        #Mirror paint buffer
        paintBuffer.setScale(PySide.QtCore.QSizeF(pbx*pb_scale.width(),pby*pb_scale.height()))
        paintBuffer.setTranslation(pb_translation)
        paintBuffer.setRotation(pb_rotation)

        #disconnect to avoid looping
        if self.comboSymmetryXYZ.currentIndex() == 2:
            paintBuffer.aboutToBake.disconnect(self.mirror_bake)

        #Bake from the mirrored position first
        bake.trigger()

        #Restore the original position
        camera.setLookAt(lookAt)
        camera.setTranslation(translation)
        camera.setUp(up)
        #Resotre the original paint buffer
        paintBuffer.setScale(pb_scale)
        paintBuffer.setTranslation(pb_translation)
        paintBuffer.setRotation(pb_rotation)
        paintBuffer.restoreContent()

        currentBehave = mari.projection.getProperty("Projection/bakeBehavior")

        # Set behaviour of bake
        #print self.comboSymmetryXYZ.currentIndex()

        if self.comboSymmetryXYZ.currentIndex() == 0:
            mari.projection.setProperty("Projection/bakeBehavior", "Manual")
        else:
            mari.projection.setProperty("Projection/bakeBehavior", "AutoBakeAndClear")
        
        #Bake again from the original position
        bake.trigger()
        mari.projection.setProperty("Projection/bakeBehavior", currentBehave)

        print("Resetting Bake Behavior")

        self.clearType = self.comboSymmetryXYZ.currentIndex()
        #print self.clearType

        #reconnect if was previously disconnected.
        if self.comboSymmetryXYZ.currentIndex() == 2:
            paintBuffer.aboutToBake.connect(self.mirror_bake)


    
bakeWidget = BakeSymmetry()

#Try to remove any previous Bake Symmetry V2 created palette in order to create a new one in case the user had closed the palette UI.
try:
    pal = mari.palettes.get("Bake Symmetry V2")    
    pal.show()
except ValueError:
    pal = mari.palettes.create("Bake Symmetry V2", bakeWidget)
    pal.show()

if __name__ == "__main__":
    BakeSymmetry()