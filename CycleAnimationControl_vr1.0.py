from PySide2.QtWidgets import *
from PySide2.QtGui import  *
from PySide2.QtCore import *
from functools import partial
import cPickle
import maya.OpenMayaUI as mui
import shiboken2
import pymel.core as pm
from operator import itemgetter
import time
import os


#convert string to data (pickle)
def string2Data(string):
    
    data = cPickle.loads(string)
    return data
#convert data to string (pickle)
def data2String(data):
    stringData = cPickle.dumps(data)
    return stringData
#Create node that stores cycles in maya scene
def creatCACNode():
    
    try:
        pm.select("cycleAnimationListNode", replace = True)
        return None

    except:
        startLib = {}
        startAtt = str(data2String(startLib))

        animNode = pm.createNode('transform', name= 'cycleAnimationListNode')
        
        pm.addAttr(animNode, longName='cycles', dataType='string')
        pm.setAttr('cycleAnimationListNode.cycles', startAtt)

        proj = pm.system.workspace.getPath() + '/movies'

        pm.addAttr(animNode, longName='path', dataType='string')
        pm.setAttr('cycleAnimationListNode.path', proj)

        pm.addAttr(animNode, longName='camera', dataType='string')
        pm.setAttr('cycleAnimationListNode.camera', "Active")

        pm.addAttr(animNode, longName='whichPb', at='bool')
        pm.setAttr('cycleAnimationListNode.whichPb', False)

        pm.addAttr(animNode, longName='namespace', dataType='string')
        pm.setAttr('cycleAnimationListNode.namespace' , '')

        pm.addAttr(animNode, longName='overWrite', at='bool')
        pm.setAttr('cycleAnimationListNode.overWrite', False)

        pm.addAttr(animNode, longName='subFolder', at='bool')
        pm.setAttr('cycleAnimationListNode.subFolder', True)

        pm.addAttr(animNode, longName='sufix', dataType='string')
        pm.setAttr('cycleAnimationListNode.sufix', '')

        pm.addAttr(animNode, longName='pbSize', dataType='string')
        pm.setAttr('cycleAnimationListNode.pbSize', 'HD 1080')

        pm.addAttr(animNode, longName='format', dataType='string')
        pm.setAttr('cycleAnimationListNode.format', '')

        pm.addAttr(animNode, longName='compression', dataType='string')
        pm.setAttr('cycleAnimationListNode.compression', '')

        pm.addAttr(animNode, longName='animator', dataType='string')
        pm.setAttr('cycleAnimationListNode.animator', '')
        
        pm.lockNode(animNode)

        return None
# Get maya window
def getMayaWindow():
    mayaWindowPointer = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(mayaWindowPointer), QWidget)
# Ui Objetc
class UI():

    def __init__(self):

        if pm.window("CycleAnimationListUI", query = True, exists = True):
            pm.deleteUI("CycleAnimationListUI", wnd = True)

        self.name = "CycleAnimationListUI"
    # Parent window
        mayaWindow = getMayaWindow()
    # Main Ui   
        self.ui = QMainWindow(parent = mayaWindow)
        self.ui.setMinimumHeight(710)
        self.ui.setMaximumHeight(710)
        self.ui.setMinimumWidth(800)
        self.ui.setMaximumWidth(800)
        self.ui.setObjectName(self.name)
        self.ui.setWindowTitle('Cycle Animation Playblast and Version Control - 1.0')
    # Central Widget    
        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout()
        self.ui.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.centralLayout)
    
 ########  HEADER  ##########
    
    ####  creando o node
        creatCACNode()

    # Add Menu bar and menu
        self.menuBar = MenuBar(self)
        self.centralLayout.addWidget(self.menuBar)
    # Add Tabs
        self.tabs = Tabs()
        self.centralLayout.addWidget(self.tabs)
    # MAIN TAB
        self.mainTab = self.tabs.mainTabLayout

 ########  BODY  ###########

    # Table group layout
        self.tableGroup = QGroupBox()
        self.tableGroup.setMaximumHeight(375)
        self.tableGroup.setMinimumHeight(375)
        self.tableGroup.setTitle("Cycle Animations")
        self.tableGroupLayout = QVBoxLayout()
        self.tableGroup.setLayout(self.tableGroupLayout)
        self.mainTab.addWidget(self.tableGroup)
    # Table
        
        self.table = Table()
        self.tableGroupLayout.addWidget(self.table)
        
        data = []
        cycles =  string2Data(str(pm.getAttr('cycleAnimationListNode.cycles')))
        for key in cycles:
            data.append(cycles[key])

        headers = ["Select", "  Cycle Name  ", " Start ", "  End  ", "Info", "V."," Del "]

        self.model = Model(self, headers)
        self.table.setModel(self.model)
        self.table.sortByColumn(2)

        self.table.resizeColumnsToContents()
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)
        #self.table.setSortingEnabled(True)
        self.table.setFocusPolicy(Qt.NoFocus);
        


    # New Cycle Input

        self.animInput = NewAnimationInput(self.model)
        self.tableGroupLayout.addWidget(self.animInput)

    # Playblast Opts
        self.pbGroup = QGroupBox()
        self.pbGroup.setTitle("Playblast Options") 
        self.pbGroup.setMinimumHeight(200)
        self.pbGroup.setMaximumHeight(200)
        self.pbGroupLayout = QVBoxLayout()
        self.pbGroup.setLayout(self.pbGroupLayout)
        self.mainTab.addWidget(self.pbGroup)
        self.pbOtions = PbOtions()
        self.pbGroupLayout.addWidget(self.pbOtions)
        self.pbNameSpace = PbName()
        self.pbGroupLayout.addWidget(self.pbNameSpace)
        self.pbDir = PbDir()
        self.pbGroupLayout.addWidget(self.pbDir)
        self.camOpts = PbCam()
        self.pbGroupLayout.addWidget(self.camOpts)
        self.pbBtn = self.camOpts.pbBtn
        self.pbBtn.clicked.connect(partial(self.startPbProcess))

        self.warningField = warningField()
        self.mainTab.addWidget(self.warningField)



    ####  INFO TAB

        self.ui.show()
        pm.select(clear = True)


    def startPbProcess(self):
        
        path = self.pbDir.path.text()
        namespace = self.pbNameSpace.nameSpace.text()
        cam = self.camOpts.camOpts.currentText()
        whichpb = self.pbOtions.all.isChecked()
        overwrite = self.pbOtions.overWrite.isChecked()
        subfolder = self.pbNameSpace.checkBox.isChecked()
    


        if (path == ''):
            self.model.warn( "Select a path first",1)
            return False
        else:


            playblast(self, path, namespace, cam, whichpb, overwrite, subfolder, self.model)    
# Menu Bar 
class MenuBar(QMenuBar):

    def __init__(self, ui):
        super(MenuBar, self).__init__()

        self.ui = ui

        resetAction = QAction("Reset fields", self)
        resetAction.setShortcut("Ctrl+Shift+R")
        resetAction.setStatusTip('Clear input fields and set options to default')
        resetAction.triggered.connect(self.resetSettings)


        removeNodeAction = QAction("Remove node", self)
        removeNodeAction.setShortcut("Ctrl+Shift+D")
        removeNodeAction.setStatusTip('Delete cycles node from maya scene file')
        removeNodeAction.triggered.connect(self.removeNodeAction)


        self.edit = QMenu("Edit")
        self.addMenu(self.edit)
        self.edit.addAction(resetAction)
        self.edit.addAction(removeNodeAction)
        self.edit.insertSeparator(removeNodeAction)


        helpme = QAction('How to use', self)
        helpme.setShortcut("Ctrl+Shift+H")
        helpme.setStatusTip('Instruction on how to use this tool.')
        helpme.triggered.connect(self.helpMe)

        about = QAction("About", self)
        about.setStatusTip('Information about license and Author.')
        about.triggered.connect(self.aboutMe)


        self.help = QMenu("Help")
        self.help.addAction(helpme)
        self.help.addAction(about)
        self.addMenu(self.help)

    def helpMe(self): 
        pm.showHelp("https://mendelreis.wordpress.com/2018/01/10/cycle-animation-playblast-and-version-control/", absolute=True, )  

    def aboutMe(self):

        about = AboutUi(self.ui.ui)

    def resetSettings(self):
        
        self.ui.animInput.name.setText("")
        self.ui.animInput.start.setText("")
        self.ui.animInput.end.setText("")
        self.ui.animInput.info.setText("")

        self.ui.pbNameSpace.nameSpace.setText("")
        self.ui.pbNameSpace.sufix.setText("")
        self.ui.pbNameSpace.animator.setText("")
        self.ui.pbDir.path.setText("")

        self.ui.camOpts.camOpts.setCurrentText("Active")

        self.ui.pbNameSpace.checkBox.setChecked(True)

        self.ui.pbOtions.selected.setChecked(True)
        self.ui.pbOtions.nVersion.setChecked(True)

        try:
            self.ui.camOpts.formats.setCurrentText("qt")
        except:
            print 'qt not available'

        self.ui.camOpts.sizeOpt.setCurrentText('HD 1080')

    def removeNodeAction(self):

        pm.select("cycleAnimationListNode", r = True)


        a = pm.selected()[0]
        pm.lockNode(a, lock = False)
        pm.delete(a)
        pm.deleteUI("CycleAnimationListUI", wnd = True)       
# Tab layout 
class Tabs(QTabWidget):

    def __init__(self):
        super(Tabs, self).__init__()     

    # tabs
        self.mainTab = QWidget()
        self.mainTabLayout = QVBoxLayout()
        self.mainTab.setLayout(self.mainTabLayout)

        self.infoTab = QWidget()
        self.infoTabLayout = QVBoxLayout()
        self.infoTab.setLayout(self.infoTabLayout)
        self.addTab(self.mainTab, "Cycle Animation List" )
# New animaito input
class NewAnimationInput(QWidget):
    def __init__(self,model,):
        super(NewAnimationInput, self).__init__()

        model = model
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        
        self.setLayout(self.layout)

    # new start 
        self.name = LineEdit()
        self.name.setMaximumWidth(130)
        self.name.setMinimumHeight(25)
        self.name.setPlaceholderText("New cycle name")
        self.name.setMaxLength(15)

    # new start 
        self.start = LineEdit()
        self.start.setMaximumWidth(50)
        self.start.setMinimumHeight(25)
        self.start.setPlaceholderText("Start")
        self.start.setMaxLength(4)

    # new end   
        self.end = LineEdit()
        self.end.setMaximumWidth(50)
        self.end.setMinimumHeight(25)
        self.end.setPlaceholderText("End")
        self.end.setMaxLength(4)

    # new info  
        self.info = LineEdit()
        self.info.setMaximumWidth(400)
        self.info.setMinimumHeight(25)
        self.info.setPlaceholderText("Information")
        self.info.setMaxLength(60)
    # new button
        self.button = QPushButton("Add cycle")
        self.button.setMinimumWidth(70)
        self.button.setMaximumWidth(70)
        self.button.clicked.connect(partial(self.newAnim, model))
    # Add to layout
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.start)
        self.layout.addWidget(self.end)
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.button)


    def newAnim(self, model, *args):
        
        cycles = string2Data(str(pm.getAttr("cycleAnimationListNode.cycles")))

        model = model

        #item = QItemDelegate()
        name = self.name.text()
        start = self.start.text()
        end = self.end.text()
        info = self.info.text()

        if len(name) <= 0:
            model.warn("Name not Valid. Must input something", 1)
            return False

        if name in cycles:
            model.warn("Cycle with such name already exists", 1)
            return False

        try:
            str(info)
        except:
            model.warn("Not valid information", 1)
            return False

        if start == '':
            model.warn("Must input a start frame for cycle", 1)
            return False

        if end == '' :
            model.warn("Must input an end frame for cycle", 1)
            return False

        try:
            int(start)
            if not int(start) < int(end):
                model.warn("Not a valid start frame. It must be an integer between -999 and 9999 and smaller than end frame", 1)
                return False
        except:
            model.warn("Not a valid start frame. It must be an integer between -999 and 9999 and smaller than end frame", 1)
            return False

        try:
            int(end)
            if not int(end) > int(start):
                model.warn("Not a valid end frame. It must be an integer between -999 and 9999 and bigger than start frame", 1)
                return False
        except:
            model.warn("Not a valid end frame. It must be an integer between -999 and 9999 and bigger than start frame", 1)
            return False

        values = [True, name, int(start), int(end), info, "000", ""]

        model.insertRows(0,1, values)

        self.name.setText("")
        self.start.setText("")
        self.end.setText("")
        self.info.setText("")

        model.warn("",2)
# button delegate
class ButtonDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)


    def paint(self, painter, option, index):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        btn = QPushButton("X")
        btn.setStyleSheet("background-color:rgb(75,75,75)")
        ix = QPersistentModelIndex(index)
        btn.clicked.connect(lambda ix = ix : self.onClicked(ix))
        layout.addWidget(btn)
        layout.setContentsMargins(2,2,2,2)
        if not self.parent().indexWidget(index):
            self.parent().setIndexWidget(index, widget)

    def onClicked(self, ix):
        model = ix.model()
        model.removeRow(ix.row())
        self.parent().clearSelection()
        model.warn("",2)
# Playblast optinos
class PbOtions(QWidget):

    def __init__(self):
        super(PbOtions, self).__init__()

        

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        
        self.setLayout(self.layout)

        self.whichPb = QFrame()
        self.whichPb.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.whichPbLayout = QHBoxLayout(self.whichPb)
        self.whichPb.setLayout(self.whichPbLayout)
        self.all = QRadioButton("Playblast all")
        self.selected = QRadioButton("Playblast selected")
        self.whichPbLayout.addWidget(self.all)
        self.whichPbLayout.addWidget(self.selected)

        self.version = QFrame()
        self.version.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.versionLayout = QHBoxLayout(self.version)
        self.version.setLayout(self.versionLayout)
        self.nVersion = QRadioButton("Make new version")
        self.overWrite = QRadioButton("Make it same version")
        self.versionLayout.addWidget(self.nVersion)
        self.versionLayout.addWidget(self.overWrite)
                
        self.layout.addWidget(self.whichPb)
        self.layout.addWidget(self.version)

        self.nVersion.toggled.connect(partial(self.saveOptions))
        self.all.toggled.connect(partial(self.saveOptions))


        which = pm.getAttr("cycleAnimationListNode.whichPb")
        v = pm.getAttr("cycleAnimationListNode.overWrite")

        if which:
            self.all.setChecked(True)
        else:
            self.selected.setChecked(True)

        if v:
            self.overWrite.setChecked(True)
        else:
            self.nVersion.setChecked(True)



    def saveOptions(self, *args):

        if self.nVersion.isChecked():
            pm.setAttr('cycleAnimationListNode.overWrite', False)
        else:
            pm.setAttr('cycleAnimationListNode.overWrite', True)

        if self.all.isChecked():
            pm.setAttr('cycleAnimationListNode.whichPb', True)
        else:
            pm.setAttr('cycleAnimationListNode.whichPb', False)
# Playblast path options
class PbName(QWidget):

    def __init__(self):
        super(PbName,self).__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        nameSpaceLabel = QLabel("Prefix:  ")
        nameSpaceLabel.setMinimumHeight(25)
        nameSpaceLabel.setMinimumWidth(40)
        self.nameSpace = LineEdit()
        self.nameSpace.setMinimumHeight(25)
        self.nameSpace.setMaximumWidth(150)
        self.nameSpace.setPlaceholderText("Prefix")

        sufixLabel = QLabel("Suffix:")
        sufixLabel.setMinimumWidth(35)
        sufixLabel.setMinimumHeight(25)
        self.sufix = LineEdit()
        self.sufix.setMinimumHeight(25)
        self.sufix.setMaximumWidth(150)
        self.sufix.setPlaceholderText("Suffix")

        animatorLabel = QLabel("Animator:")
        animatorLabel.setMinimumWidth(35)
        animatorLabel.setMaximumWidth(50)
        animatorLabel.setMinimumHeight(25)
        self.animator = LineEdit()
        self.animator.setMinimumHeight(25)
        self.animator.setMinimumWidth(150)
        self.animator.setMaximumWidth(150)
        self.animator.setPlaceholderText("Animator's name")

                  
        self.checkBox = QCheckBox("Folder for each cycle")
        self.checkBox.setChecked(pm.getAttr('cycleAnimationListNode.subFolder'))
        self.checkBox.setMinimumHeight(25)
        self.checkBox.setMinimumWidth(132)
        self.checkBox.toggled.connect(partial(self.setSubFolder))

        self.layout.addWidget(nameSpaceLabel)
        self.layout.addWidget(self.nameSpace)
        self.layout.addWidget(sufixLabel)
        self.layout.addWidget(self.sufix)
        self.layout.addWidget(animatorLabel)
        self.layout.addWidget(self.animator)
        self.layout.addWidget(self.checkBox)

        self.sufix.textChanged.connect(partial(self.saveSufix))
        self.nameSpace.textChanged.connect(partial(self.saveNamespace))
        self.animator.textChanged.connect(partial(self.saveAnimator))

        self.nameSpace.setText(pm.getAttr("cycleAnimationListNode.namespace"))
        self.sufix.setText(pm.getAttr("cycleAnimationListNode.sufix"))

        print "test", (pm.getAttr("cycleAnimationListNode.animator"))
        self.animator.setText(pm.getAttr("cycleAnimationListNode.animator"))

    def saveNamespace(self, *args):
        prefix = self.nameSpace.text()
        pm.setAttr('cycleAnimationListNode.namespace', prefix)

    def setSubFolder(self, *args):

        if self.checkBox.isChecked():
            pm.setAttr('cycleAnimationListNode.subFolder', True)
        else:
            pm.setAttr('cycleAnimationListNode.subFolder', False)

    def saveSufix(self, *args):

        sufix = self.sufix.text()
        pm.setAttr('cycleAnimationListNode.sufix', sufix)

    def returnSufix(self, *args):
        sufix = pm.getAttr('cycleAnimationListNode.sufix')
        pm.setAttr('cycleAnimationListNode.sufix', sufix)

    def saveAnimator(self, *args):
        animator = self.animator.text()
        pm.setAttr('cycleAnimationListNode.animator', animator)
# Playblast directory
class PbDir(QWidget):

    def __init__(self):
        super(PbDir,self).__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Save to:")
        #self.label.setMinimumHeight(25)
        #self.label.setMaximumWidth(75)

        self.path = LineEdit()
        self.path.setEnabled(True)
        self.path.setPlaceholderText("Select a directory")
        #self.path.setMaximumWidth(500)
        self.path.setMinimumHeight(25)
        self.getPathBtn = QPushButton("Select directory")
        self.getPathBtn.setMinimumHeight(24)
        self.getPathBtn.setMinimumWidth(130)  ###  change this width
        self.getPathBtn.clicked.connect(partial(self.getDirectory))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.path)
        self.layout.addWidget(self.getPathBtn)

        self.path.setText(pm.getAttr("cycleAnimationListNode.path"))

        self.path.textChanged.connect(partial(self.saveDir))


    def saveDir(self, *args):

        a = self.path.text()
        pm.setAttr('cycleAnimationListNode.path', a)


    def getDirectory(self, *args):

        a = pm.workspace(q=True, rootDirectory=True)
        b = QFileDialog.getExistingDirectory(None, 'Open working directory', pm.workspace(q=True, rootDirectory=True), QFileDialog.ShowDirsOnly)

        if (b != ''):
            self.path.setText(b)
            pm.setAttr('cycleAnimationListNode.path', b)
            self.value = self.path.text()
# Combo box on click event
class ComboBox(QComboBox):
    popupAboutToBeShown = Signal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()
# Cameras and playblast
class PbCam(QWidget):

    def __init__(self):
        super(PbCam, self).__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    ## cams
        self.label = QLabel("Camera:")
        self.label.setMinimumHeight(22)
        self.label.setMaximumWidth(39)
        self.camOpts = ComboBox()
        self.camOpts.setMinimumHeight(24)
        self.camOpts.setMaximumWidth(100)
        self.camOpts.popupAboutToBeShown.connect(partial(self.populateCams))

    ## formt
        self.formatLabel = QLabel("Format:")
        self.formatLabel.setMaximumWidth(40)
        self.formatLabel.setMinimumHeight(24)
        self.formats = QComboBox()
        self.formats.setMinimumHeight(24)
        self.formats.setMaximumWidth(75)

        availableFormats = pm.playblast(query = True, format = True)

        for item in availableFormats:
            self.formats.addItem(item)

        if pm.getAttr("cycleAnimationListNode.format") == '':
            print 'first time'
            pm.setAttr("cycleAnimationListNode.format", self.formats.currentText())

        self.formats.setCurrentText(pm.getAttr("cycleAnimationListNode.format"))

    ## compression
        self.compressionLabel = QLabel("Compression:")
        self.compressionLabel.setMaximumWidth(72)
        self.compressionLabel.setMinimumHeight(24)
        self.compression = QComboBox()
        self.compression.setMinimumHeight(24)
        self.compression.setMaximumWidth(110)
        
        compressions  = pm.mel.eval('playblast -format "{0}" -q -compression;'.format(self.formats.currentText()))
        for c in compressions :
            self.compression.addItem(c)

        if pm.getAttr("cycleAnimationListNode.compression") == '':
            pm.setAttr("cycleAnimationListNode.compression", self.compression.currentText())

        self.compression.setCurrentText(pm.getAttr("cycleAnimationListNode.compression"))

    #size
        self.sizeLabel = QLabel("Size:")
        self.sizeLabel.setMaximumWidth(30)
        self.sizeLabel.setMinimumHeight(24)
        self.sizeOpt = ComboBox()
        self.sizeOpt.setMinimumHeight(24)
        self.sizeOpt.setMaximumWidth(72)
        self.sizeOpt.addItem("HD 1080")
        self.sizeOpt.addItem("HD 720")
        self.sizeOpt.addItem("HD 540")

    #button
        self.pbBtn = QPushButton("Playblast!")
        #self.pbBtn.setMaximumWidth(200)
        self.pbBtn.setMinimumHeight(24)
        self.pbBtn.setMaximumWidth(130)

    ##  add widgets
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.camOpts)
        self.layout.addWidget(self.formatLabel)
        self.layout.addWidget(self.formats)
        self.layout.addWidget(self.compressionLabel)
        self.layout.addWidget(self.compression)
        self.layout.addWidget(self.sizeLabel)
        self.layout.addWidget(self.sizeOpt)
        self.layout.addWidget(self.pbBtn)
        self.populateCams()

        self.camOpts.activated.connect(partial(self.saveCam))
        self.formats.activated.connect(partial(self.saveFormat))
        self.compression.activated.connect(partial(self.saveCompression))
        self.sizeOpt.activated.connect(partial(self.saveSize))

        self.camOpts.setCurrentText(pm.getAttr("cycleAnimationListNode.camera"))
        self.sizeOpt.setCurrentText(pm.getAttr("cycleAnimationListNode.pbSize"))


        
        

    def saveSize(self, *args):
        size = self.sizeOpt.currentText()
        pm.setAttr("cycleAnimationListNode.pbSize", size)

    def saveFormat(self, *args):
        print "hey"
        f = self.formats.currentText()
        pm.setAttr("cycleAnimationListNode.format", f)

        compressions  = pm.mel.eval('playblast -format "{0}" -q -compression;'.format(f))

        self.compression.clear()
        #while self.compression.count() > 0:
        #    self.compression.removeItem(0)
        for c in compressions :
            self.compression.addItem(c)

        self.saveCompression()


    def saveCompression(self, *args):
        c = self.compression.currentText()
        pm.setAttr("cycleAnimationListNode.compression",c)

    def saveCam(self, *args):

        cam = self.camOpts.currentText()
        pm.setAttr("cycleAnimationListNode.camera", cam)


    def populateCams(self, *args):

        self.camOpts.clear()
        self.camOpts.addItem("Active")

        scnCams = pm.ls(type = "camera")

        for cam in scnCams:
            cam = str(cam.listRelatives(parent = True)[0])
            self.camOpts.addItem(cam)
# Table view
class Table(QTableView):
    
    def __init__(self, *args, **kwargs):
        QTableView.__init__(self, *args, **kwargs)

        self.setItemDelegateForColumn(6, ButtonDelegate(self))
        self.setItemDelegateForColumn(0, EmptyDelegate(self))

        self.setSortingEnabled(True)

        self.setStyleSheet("background-color:rgb(45,45,45)")

        hHeader = self.horizontalHeader()
        hHeader.setStyleSheet("background-color:rgb(75,75,75)")

        vHeader = self.verticalHeader()
        vHeader.hide()
        #vHeader.setStyleSheet("background-color:rgb(75,75,75)")

    def cellButtonClicked(self, index,  *args):

        model = self.model()
        model.removeRow(index.row())
# Model
class Model(QAbstractTableModel):

    def __init__(self, ui,  headers = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        cycles = string2Data(str(pm.getAttr("cycleAnimationListNode.cycles")))
        
        self.ui = ui
        self.cycles = []
        
        if len(cycles) > 0:
            for cycle in cycles:
                array = []
                for j in range(len(cycles[cycle])):
                    if (j == 2) or (j == 3):    
                        array.append(int(cycles[cycle][j]))
                    else:
                        array.append(cycles[cycle][j])
                self.cycles.append(array)

        self.headers = headers
        self.values_checked = []

        

    def rowCount(self, parent):
        return len(self.cycles)

    def columnCount(self, parent):
        return 7

    def flags(self, index):
        fl = Qt.ItemIsEnabled  
        if index.column() == 0:
            fl |= Qt.ItemIsUserCheckable
        elif index.column() == 5:
            fl = fl
        else:
            fl |= Qt.ItemIsEditable | Qt.ItemIsSelectable
        return fl

    def data(self, index, role):
        if not index.isValid():
            return 
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            value = self.cycles[row][column]
            return value

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter;

        elif role == Qt.CheckStateRole and column==0:
            return Qt.Checked if self.cycles[row][column] else Qt.Unchecked  

        elif role == Qt.EditRole: 
            index = index 
            return index.data()     



    def setData(self, index, value, role = Qt.EditRole):

        change = False
        row = index.row()
        column = index.column()

        if role == Qt.CheckStateRole:
            value =  value != Qt.Unchecked
            change = True
        if role == Qt.EditRole:
            if (column == 1):
                try:
                    str(value)
                    change = True
                    c = string2Data(str(pm.getAttr("cycleAnimationListNode.cycles")))
                    if value in c:
                        self.warn("Cycle already exists", 1)
                        change = False
                    if len(value)==0 or len(value) > 15:
                        self.warn("Must have a name with more than 0 and less than 15 characters",1)
                        change = False
                except:
                    self.warn("Not a valid name",1)
                    change = False
            elif (column == 2):
                try:
                    int(value)
                    end = self.index(row, column+1).data()
                    if int(value) < int(end) and len(str(value))<=4:
                        change = True
                    else:
                        self.warn("Start frame must be smaller then end frame and between -999 and 9999",1)
                        change = False
                except:
                    self.warn("Not a valid frame",1)
                    change = False
            elif (column == 3):
                try:
                    int(value)
                    start = self.index(row, column-1).data()
                    if int(value) > int(start) and len(str(value)) <= 4:
                        change = True
                    else:
                        self.warn("End frame must be bigger then start frame and between -999 and 9999",1)
                        change = False
                except:
                    self.warn("Not a valid frame",1)
                    change = False
            elif (column == 4):
                if len(value) < 60:
                    change = True
                else:
                    self.warn("Information cannot have more tha 60 characters",1)
                    change = False
            elif (column == 5):
                try:
                    int(value)
                    change = True
                except:
                    self.warn("Not a valid version number",1)
                    change = False
        if change:
            self.cycles[row][column] = value
            self.dataChanged.emit(row, column)
            self.getData()
            self.warn("",2)
            return True
        return False            

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]

    def insertRows(self, position, rows, values = [] , parent = QModelIndex()):

        lastposition = self.rowCount(0)

        self.beginInsertRows(parent, lastposition, lastposition) #+rows-1
        self.cycles.insert(lastposition, values)

        self.endInsertRows()

        self.getData()

    
    def removeRow(self, row, parent = QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        self.cycles.remove(self.cycles[row])
        self.endRemoveRows()
        self.getData()  
    
    def roleNames(self):
        roles = QAbstractTableModel.roleNames(self)
        roles["Checked"] = Qt.CheckStateRole
        return roles


    def getData(self):
            rows = self.rowCount(1)
            data = []
            for row in range(rows):
                array = []
                for column in range (7):
                    index = self.index(row, column)
                    info = index.data()
                    if column == 0:
                        array.append(info)  
                    else: 
                        array.append(str(info))
                data.append(array)

            dic = {}
            for item in data:
                dic[item[1]]=item

            newData = data2String(dic)
            pm.setAttr("cycleAnimationListNode.cycles", newData)

            '''   Uncoment this to print the cycles dictionary when inserting or deleting onde
            print ''
            print "data:"
            for key in dic:
                print dic[key]
            '''

    def sort(self, column, order):

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.cycles = sorted(self.cycles, key=itemgetter(column))
        if order == Qt.DescendingOrder:
            self.cycles.reverse()
        self.emit(SIGNAL("layoutChanged()"))


    def warn(self, text, opt):

        color = ''

        if opt == 0 :
            color = "DarkSeaGreen"
        elif opt == 1:
            color = "Khaki"
        elif opt == 2:
            color = "rgb(75,75,75)"
        elif opt == 3:
            color = "coral"

        style = "color:rgb(75,75,75); background-color:" + color
        text = "Warning: " + text

        self.ui.warningField.setText(text)
        self.ui.warningField.setStyleSheet(style)
# Empty delegate for check box
class EmptyDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        if index.column() == 0:
            textMargin = QApplication.style().pixelMetric(QStyle.PM_FocusFrameHMargin) + 1
            newRect = QStyle.alignedRect(option.direction, Qt.AlignCenter,
                                         QSize(option.decorationSize.width() ,
                                               option.decorationSize.height()),
                                         QRect(option.rect.x() + textMargin, option.rect.y(),
                                               option.rect.width() - (2 * textMargin),
                                               option.rect.height()))
            opt.rect = newRect

        QStyledItemDelegate.paint(self, painter, opt, index)

    def editorEvent(self, event, model, option, index):
        flags = model.flags(index)
        if not (flags & Qt.ItemIsUserCheckable) or not (flags & Qt.ItemIsEnabled):
            return False
        value = index.data(Qt.CheckStateRole)

        if event.type() == QEvent.MouseButtonRelease:
            textMargin = QApplication.style().pixelMetric(QStyle.PM_FocusFrameHMargin) + 1
            checkRect = QStyle.alignedRect(option.direction, Qt.AlignCenter,
                                           option.decorationSize,
                                           QRect(option.rect.x() + (2 * textMargin),
                                                 option.rect.y(),
                                                 option.rect.width() - (2 * textMargin),
                                                 option.rect.height()))
            if not checkRect.contains(event.pos()):
                return False

        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
        else:
            return False

        state = Qt.Unchecked if value == Qt.Checked else Qt.Checked
        return model.setData(index, state, Qt.CheckStateRole)
# custom QlineEdit
class LineEdit(QLineEdit):

    buttonPressed = Signal(name='buttonPressed')

    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.readyToEdit = True

        self.value = ''

    def mousePressEvent(self, e, Parent=None):
        super(LineEdit, self).mousePressEvent(e) #required to deselect on 2e click
        if self.readyToEdit:
            self.selectAll()
            self.readyToEdit = False
            self.value = self.text()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.buttonPress()
        else:
            QLineEdit.keyPressEvent(self, event)
  
    def buttonPress(self):
        self.value = self.text()
        self.focusNextChild()
# warning field Class
class warningField(QLineEdit):

    def __init__(self, parent = None):
        super(warningField, self).__init__()

        self.setMinimumHeight(25)
        self.setMaximumHeight(25)
        self.setStyleSheet("background-color:rgb(75,75,75)")
        self.setReadOnly(True)
        self.setTextMargins(15,0,0,0)
# Playblast         
def playblast(self, path, namespace, cam, whichpb, overwrite, subfolder, model):

    model = model
    
    try:
        pane = pm.getPanel( withFocus=True ) # Get panel on focus
        userOldCam = pm.listRelatives(pm.modelEditor(pane, query = True, camera=True))[0] # Get active camera on that panel
    except:
        model.warn("Active pane is not right for playblast. Click on any viewport pane (front, top, side, any camera) and retry.", 1)
        return False

    sizeOpt = pm.getAttr("cycleAnimationListNode.pbSize")
    size = []

    if sizeOpt == "HD 1080":
        size = [1920,1080]
    elif sizeOpt == "HD 720":
        size = [1280,720]
    elif sizeOpt == "HD 540":
        size = [960,540]

    f = pm.getAttr("cycleAnimationListNode.format")
    c = pm.getAttr("cycleAnimationListNode.compression")


    if (cam != "Active"):
        pm.lookThru(cam)

    cycles = model.rowCount(1)

    savePath = path 

    for row in range(cycles):
        model.index(row, 0).data()
        if model.index(row, 0).data() or whichpb:
            
            name = model.index(row, 1).data()
            start = int(model.index(row, 2).data())
            end = int(model.index(row, 3).data())
            info = model.index(row, 4).data()
            version = int(model.index(row, 5).data())
            
            index = model.index(row, 5)

            if subfolder:
                savePath += "/" + name

            if (namespace != ''):
                savePath += "/" + namespace +"_"+ name
            else:
                savePath += "/" + name

            if  overwrite:
                a = str(version)
                while len(a) < 3:
                    a = "0" + a
                model.setData(index, a, role = Qt.EditRole)
                savePath += "_" + a
            else:
                version += 1
                a = str(version)
                while len(a) < 3:
                    a = "0" + a
                model.setData(index, a, role = Qt.EditRole)
                savePath += "_" + a

            sufix = pm.getAttr("cycleAnimationListNode.sufix")
            if not sufix == '':
                savePath += "_" + sufix


            setHUD(name, info, version)

            print "aqui"
            print name, info, version, f , c

            if (os.path.exists(path)) :

                pm.playblast(startTime = start, 
                            endTime = end,
                            format = f, 
                            filename = savePath, 
                            forceOverwrite = overwrite, 
                            compression = c, 
                            offScreen = True, 
                            percent = 100, 
                            quality = 100,
                            widthHeight = size,
                            clearCache = 1,
                            sequenceTime= False,
                            showOrnaments = True)
            else:
                model.warn('The specified path does not exist. Choose a valid path', 1)
                removeHUD()
                return False
            
            removeHUD()
                
    pm.lookThru(userOldCam)

    model.warn("Playblast sucessfully executed", 0)

def getCycleName(name, *args):
    name = name
    return name

def getCycleVersion(version, *args):
    version = str(version)
    while len(version) < 3:
        version = '0'+ version
    return version

def getCycleInfo(info, *args):
    info = str(info)
    return info

def getAnimator(*args):
    animator = pm.getAttr("cycleAnimationListNode.animator")
    return str(animator)

def getDate(*args):
    d = (time.strftime("%y/%m/%d"))
    return str(d)

def setHUD(name, info, version):
    name = name 
    info = info
    version = version

    pm.displayColor('headsUpDisplayLabels', 17, dormant = True)

    pm.headsUpDisplay("cycles", section = 5, block = 6, blockSize='small', label = 'Cycle:',  command = partial(getCycleName,name), dfs = 'large', lfs = 'large')
    print 1
    pm.headsUpDisplay("info", section = 5, block = 5, blockSize='small',  label = 'Info:', command = partial(getCycleInfo,info), dfs = 'large', lfs = 'large')
    print 2
    pm.headsUpDisplay("version", section = 5, block = 4,  blockSize='small',  label = 'Version:', command = partial(getCycleVersion,version), dfs = 'large', lfs = 'large')
    print 3
    pm.headsUpDisplay("animator", section = 5, block = 2,  blockSize='small', label = 'Animator:', command = partial(getAnimator), dfs = 'large', lfs = 'large')
    print 4
    pm.headsUpDisplay("frames", section = 5, block = 1, blockSize='small',  label = 'Frame:', preset = 'currentFrame', dfs = 'large', lfs = 'large')
    print 5
    pm.headsUpDisplay("date", section = 5, block = 3,  blockSize='small', label = 'Date:', command = partial(getDate), dfs = 'large', lfs = 'large')
    print 6
    pm.headsUpDisplay("cycles", edit=True, visible = True);
    pm.headsUpDisplay("info", edit=True, visible = True);
    pm.headsUpDisplay("version", edit=True, visible = True);
    pm.headsUpDisplay("frames", edit=True, visible = True);
    pm.headsUpDisplay("animator", edit=True, visible = True);
    pm.headsUpDisplay("date", edit=True, visible = True);

    print 7

def removeHUD():

    pm.headsUpDisplay("cycles", rem=True)
    pm.headsUpDisplay("info", rem=True)
    pm.headsUpDisplay("version", rem=True)
    pm.headsUpDisplay("frames", rem=True)
    pm.headsUpDisplay("animator", rem=True)
    pm.headsUpDisplay("date", rem=True)

# Start 


class AboutUi():

    def __init__(self,parent):
        #super(AboutUi, self).__init__() 

        self.name = "CycleAnimationListUI_about"

        self.ui = QMainWindow(parent)
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.setMinimumHeight(400)
        self.ui.setMaximumHeight(400)
        self.ui.setMinimumWidth(300)
        self.ui.setMaximumWidth(300)
        self.ui.setObjectName(self.name)
        self.ui.setWindowTitle('CAPVC.1.0  -  ABOUT')


        centralWidget = QWidget()
        self.ui.setCentralWidget(centralWidget)
        self.layout = QVBoxLayout()
        centralWidget.setLayout(self.layout)

        line1 = QLabel('Created by Mendel Reis')
        line1.setAlignment(Qt.AlignCenter)
        line2 = QLabel('mendelreis@gmail.com')
        line2.setAlignment(Qt.AlignCenter)
        line3 = QLabel("Copyright 2018 MENDEL REIS.    MIT License:")
        line3.setAlignment(Qt.AlignCenter)

        line4 = QLabel('Tool scripted for Autodesk Maya 2017')
        line4.setAlignment(Qt.AlignCenter)
        #line5 = QLineEdit('MIT License')
        line6 = QLabel("    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.")
        line6.setWordWrap(True)
        line6.setAlignment(Qt.AlignJustify)

        line7= QLabel("    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
        line7.setWordWrap(True)
        line7.setAlignment(Qt.AlignJustify)

        self.layout.addWidget(line1)
        self.layout.addWidget(line2)
        self.layout.addWidget(line4)
        self.layout.addWidget(line3)
        self.layout.addWidget(line6)
        self.layout.addWidget(line7)

        self.ui.show()


ccUI = UI()










