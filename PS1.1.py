# -*- coding: utf-8 -*-
"""
Created on 15/08/2018
@author: Simon Lane
"""

#imports
from PyQt4          import QtGui
import sys, glob, serial, time


class PScontroller(QtGui.QMainWindow):
    def __init__(self):
        super(PScontroller, self).__init__()
        self.syringe_list = ["BD. 2.5mL", "BD. 5mL", "BD. 10mL", "Torumo 2.5mL", "Torumo 5mL", "Torumo 10mL"]
        self.coms_list = self.serial_ports()
        self.initUI()
        time.sleep(1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               #Setup main Window
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def initUI(self):

        self.setWindowTitle('Perpetual Sedimentation v2.0')
#        palette = QtGui.QPalette()
#        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(80,80,80))
#        self.setPalette(palette)
        
        sizePolicyMin = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicyMin.setHorizontalStretch(0)
        sizePolicyMin.setVerticalStretch(0)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               #Setup Panes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.PSGroup        = QtGui.QGroupBox('Perpetual Sedimentation')
        self.SyringeGroup   = QtGui.QGroupBox('Syringe Pumps')
        self.PSGroup.setEnabled(False)
        self.SyringeGroup.setEnabled(False)

# COMS
            
        self.Coms                           = QtGui.QComboBox()
        self.Coms.addItems(self.coms_list)
        
        self.ConnectButton                  = QtGui.QPushButton('Connect')
        self.DisconnectButton               = QtGui.QPushButton('Disconnect')
        self.ConnectButton.clicked.connect(lambda: self.connect('C'))
        self.DisconnectButton.clicked.connect(lambda: self.connect('D'))
        self.DisconnectButton.setEnabled(False)
        
#Stop Button
        self.StopButton                     = QtGui.QPushButton('STOP')
        self.StopButton.released.connect(self.StopAll)

#Syringe Pumps
        
        self.CellLabel                      = QtGui.QLabel('Cells')
        self.CellPump = [QtGui.QRadioButton('R'),QtGui.QRadioButton('Off'),QtGui.QRadioButton('F')]
        self.CellPump[1].setChecked(True)
        self.CellPump_group = QtGui.QButtonGroup()
        for r in range(3):
            self.CellPump[r].released.connect(self.toggle)
            self.CellPump_group.addButton(self.CellPump[r],r)
        self.CellSyringe                    = QtGui.QComboBox()
        self.CellSyringe.addItems(self.syringe_list)
        self.L1                             = QtGui.QLabel('uL/min')
        self.CellRate                       = QtGui.QLineEdit('15')
        self.CellRate.setValidator(QtGui.QIntValidator(1,5000))
        self.CellRate.returnPressed.connect(self.toggle)
        
        self.BeadLabel                      = QtGui.QLabel('Beads')
        self.BeadPump = [QtGui.QRadioButton('R'),QtGui.QRadioButton('Off'),QtGui.QRadioButton('F')]
        self.BeadPump[1].setChecked(True)
        self.BeadPump_group = QtGui.QButtonGroup()
        for r in range(3):
            self.BeadPump[r].released.connect(self.toggle)
            self.BeadPump_group.addButton(self.BeadPump[r],r)
        self.BeadSyringe                    = QtGui.QComboBox()
        self.BeadSyringe.addItems(self.syringe_list)
        self.L1                             = QtGui.QLabel('uL/min')
        self.BeadRate                       = QtGui.QLineEdit('60')
        self.BeadRate.setValidator(QtGui.QIntValidator(1,5000))
        self.BeadRate.returnPressed.connect(self.toggle)

        self.OilLabel                      = QtGui.QLabel('Oil')
        self.OilPump = [QtGui.QRadioButton('R'),QtGui.QRadioButton('Off'),QtGui.QRadioButton('F')]
        self.OilPump[1].setChecked(True)
        self.OilPump_group = QtGui.QButtonGroup()
        for r in range(3):
            self.OilPump[r].released.connect(self.toggle)
            self.OilPump_group.addButton(self.OilPump[r],r)
        self.OilSyringe                    = QtGui.QComboBox()
        self.OilSyringe.addItems(self.syringe_list)
        self.L1                             = QtGui.QLabel('uL/min')
        self.OilRate                       = QtGui.QLineEdit('180')
        self.OilRate.setValidator(QtGui.QIntValidator(1,5000))
        self.OilRate.returnPressed.connect(self.toggle)
        
# Perpetual Sedimentation       
        
        self.RotationButton                 = QtGui.QPushButton('ON')
        self.RotationButton.setCheckable(True)
        self.RotationButton.clicked.connect(self.rotation)
        self.RotationButton.state           = 0
        self.L4                             = QtGui.QLabel('R.P.M.')
        self.RotationRate                   = QtGui.QLineEdit('20')
        self.RotationRate.setValidator(QtGui.QIntValidator(1,60))
        self.RotationRate.returnPressed.connect(self.rotation)
        

#add widgets to groups
        self.SyringeGroup.setLayout(QtGui.QGridLayout())
        self.SyringeGroup.layout().addWidget(self.CellLabel,              0,0,1,1)
        self.SyringeGroup.layout().addWidget(self.CellPump[0],            0,1,1,1)
        self.SyringeGroup.layout().addWidget(self.CellPump[1],            0,2,1,1)
        self.SyringeGroup.layout().addWidget(self.CellPump[2],            0,3,1,1)
        self.SyringeGroup.layout().addWidget(self.CellSyringe,            0,4,1,2)
        self.SyringeGroup.layout().addWidget(self.L1,                     0,6,1,1)
        self.SyringeGroup.layout().addWidget(self.CellRate,               0,8,1,1)
        
        self.SyringeGroup.setLayout(QtGui.QGridLayout())
        self.SyringeGroup.layout().addWidget(self.BeadLabel,              1,0,1,1)
        self.SyringeGroup.layout().addWidget(self.BeadPump[0],            1,1,1,1)
        self.SyringeGroup.layout().addWidget(self.BeadPump[1],            1,2,1,1)
        self.SyringeGroup.layout().addWidget(self.BeadPump[2],            1,3,1,1)
        self.SyringeGroup.layout().addWidget(self.BeadSyringe,            1,4,1,2)
        self.SyringeGroup.layout().addWidget(self.L1,                     1,6,1,1)
        self.SyringeGroup.layout().addWidget(self.BeadRate,               1,8,1,1)
        
        self.SyringeGroup.setLayout(QtGui.QGridLayout())
        self.SyringeGroup.layout().addWidget(self.OilLabel,              2,0,1,1)
        self.SyringeGroup.layout().addWidget(self.OilPump[0],            2,1,1,1)
        self.SyringeGroup.layout().addWidget(self.OilPump[1],            2,2,1,1)
        self.SyringeGroup.layout().addWidget(self.OilPump[2],            2,3,1,1)
        self.SyringeGroup.layout().addWidget(self.OilSyringe,            2,4,1,2)
        self.SyringeGroup.layout().addWidget(self.L1,                    2,6,1,1)
        self.SyringeGroup.layout().addWidget(self.OilRate,               2,8,1,1)
    
        self.PSGroup.setLayout(QtGui.QGridLayout())
        self.PSGroup.layout().addWidget(self.RotationButton,              0,0,1,1)
        self.PSGroup.layout().addWidget(self.L4,                          0,1,1,1)
        self.PSGroup.layout().addWidget(self.RotationRate,                0,2,1,2)
        

#==============================================================================
# Overall assembly
#==============================================================================
        OverallLayout = QtGui.QGridLayout()
        OverallLayout.addWidget(self.PSGroup,                       0,0,2,4)
        OverallLayout.addWidget(self.StopButton,                    0,5,2,1)
        OverallLayout.addWidget(self.SyringeGroup,                  3,0,4,6)
        OverallLayout.addWidget(self.Coms,                          8,1,1,2)
        OverallLayout.addWidget(self.ConnectButton,                 8,3,1,2)
        OverallLayout.addWidget(self.DisconnectButton,              8,5,1,2)
        

        self.MainArea = QtGui.QFrame()
        self.MainArea.setLineWidth(0)
        self.MainArea.setLayout(OverallLayout)
        self.setCentralWidget(self.MainArea)

    def connect(self, state):
        if state == "C":
            p = self.Coms.currentText()
            print(p)
            self.arduino = serial.Serial(port="%s" %p, baudrate=115200, timeout=0.5)
            time.sleep(1) #essential to have this delay!
            print('send "hello"')
            self.arduino.write(str.encode("/hello;\n"))
            print('get reply')
            reply = self.arduino.readline().strip()
            print('reply:',reply)
            if reply == b'Hi there':
                print('connection established')
                self.ConnectButton.setEnabled(False)
                self.DisconnectButton.setEnabled(True)
                self.Coms.setEnabled(False)
                self.SyringeGroup.setEnabled(True)
                self.PSGroup.setEnabled(True) 
            else:
                print('no connection')
                self.arduino.close()
                
        if state == "D":
            self.StopAll()
            self.arduino.close()
            self.ConnectButton.setEnabled(True)
            self.DisconnectButton.setEnabled(False)
            self.Coms.setEnabled(True)
            self.SyringeGroup.setEnabled(False)
            self.PSGroup.setEnabled(False) 
        

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def rotation(self):
        if self.RotationButton.text() =='ON':
            #turn the rotation on
            rpm = int(self.RotationRate.text())
            self.arduino.write(str.encode("/on.%s;\n" %(rpm)))
            print(self.arduino.readline().strip())
            self.RotationButton.setText("OFF")
        elif self.RotationButton.text() =='OFF':    
            self.arduino.write(str.encode("/off;\n"))
            print(self.arduino.readline().strip())
            self.RotationButton.setText("ON")

    def to_rpm(self, syringe, rate):
        area = [58.9,114.4,165.1,63.6,133.6,195.8]
        rpm = float(int(rate))/(area[syringe]*0.3175) * 100  #multiply number to avoid using floats (revs per 100 minutes)
        print(rate, area[syringe], rpm)
        return rpm 

    def toggle(self):
        Cell_rpm = self.to_rpm(self.CellSyringe.currentIndex(),self.CellRate.text())
        if self.CellPump_group.checkedId() == 0: self.arduino.write(str.encode("/cr.%s;\n" %(Cell_rpm)))
        if self.CellPump_group.checkedId() == 1: self.arduino.write(str.encode("/coff;\n" ))
        if self.CellPump_group.checkedId() == 2: self.arduino.write(str.encode("/cf.%s;\n" %(Cell_rpm)))
        
        Bead_rpm = self.to_rpm(self.BeadSyringe.currentIndex(),self.BeadRate.text())
        if self.BeadPump_group.checkedId() == 0: self.arduino.write(str.encode("/br.%s;\n" %(Bead_rpm)))
        if self.BeadPump_group.checkedId() == 1: self.arduino.write(str.encode("/boff;\n" ))
        if self.BeadPump_group.checkedId() == 2: self.arduino.write(str.encode("/bf.%s;\n" %(Bead_rpm)))
        
        Oil_rpm = self.to_rpm(self.OilSyringe.currentIndex(),self.OilRate.text())
        if self.OilPump_group.checkedId() == 0: self.arduino.write(str.encode("/ar.%s;\n" %(Oil_rpm)))
        if self.OilPump_group.checkedId() == 1: self.arduino.write(str.encode("/aoff;\n" ))
        if self.OilPump_group.checkedId() == 2: self.arduino.write(str.encode("/af.%s;\n" %(Oil_rpm)))
        
    def StopAll(self):
        self.arduino.write(str.encode("/stop;\n"))
        self.CellPump[1].setChecked(True)
        self.BeadPump[1].setChecked(True)
        self.OilPump[1].setChecked(True)
        self.RotationButton.setText("ON")
        self.RotationButton.setChecked(False)

    def closeEvent(self, event): #to do upon GUI being closed
        #if connection still open issue stop command
        if self.arduino.is_open:
            self.StopAll()
        self.arduino.close()
        print('closed connection')


if __name__ == '__main__':
    app = 0
    app = QtGui.QApplication(sys.argv)
    gui = PScontroller()
    gui.show()
    app.exec_()
