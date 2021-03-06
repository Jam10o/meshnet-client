#!/usr/bin/env python2
#===============================================================================
#    Copyright 2013 Jonathan Frederickson
#
#     This file is part of meshnet-client.
# 
#     Meshnet-client is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Meshnet-client is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with meshnet-client.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from admin import AdminInterface
from error import ErrorWindow
from socket import error as socket_error
    
class MainWindow(QtGui.QMainWindow):
    
    ui = None
    admin = None
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.ui = uic.loadUi('mainwindow.ui', self)
        self.setWindowIcon(QtGui.QIcon('marylandmesh.png'))
        self.show()
        self.ui.actionAdd_Peer.triggered.connect(self.addPeer)
        self.ui.actionAdd_Peer.setEnabled(False)
        self.ui.actionStart.triggered.connect(self.connectAdmin)
        self.ui.actionStop.triggered.connect(self.disconnectAdmin)
    
    def addPeer(self):
        peerWindow = AddPeerWindow()
        peerWindow.setModal(True)
        peerWindow.exec_()
        
    def connectAdmin(self):
        try:
            global admin
            admin = AdminInterface()
            self.ui.actionAdd_Peer.setEnabled(True)
        except socket_error:
            ErrorWindow(self, 'Error', 'Unable to connect to admin interface. Is cjdns running?')
        except ValueError:
            ErrorWindow(self, 'Error', 'Could not read cjdroute.conf. Have you run cleanconf?')
            
    def disconnectAdmin(self):
        global admin
        admin = None
        self.ui.actionAdd_Peer.setEnabled(False)

class AddPeerWindow(QtGui.QDialog):
    
    ui = None
    
    def __init__(self):
        super(AddPeerWindow, self).__init__()
        self.__initUI()
        
    def __initUI(self):
        self.setWindowIcon(QtGui.QIcon('marylandmesh.png'))
        self.setWindowTitle('Add Peer')
        self.ui = uic.loadUi('addpeer.ui', self)
        self.ui.accepted.connect(self.addPeer)
        self.ui.advButton.released.connect(self.jsonWindow)
        
    def addPeer(self):
        global admin
        name = str(self.ui.nameField.text())
        key = str(self.ui.keyField.text())
        pw = str(self.ui.passField.text())
        v4 = str(self.ui.v4Field.text())
        port = str(self.ui.portField.text())
        
        admin.addPeer(key, pw, v4, port)
        
    def jsonWindow(self):
        window = AddJSON()
        window.setModal(True)
        window.exec_()
        
    def addPeerFromJson(self):
        print('stuff')
        
class AddJSON(QtGui.QDialog):
    ui = None
    
    def __init__(self):
        super(AddJSON, self).__init__()
        self.__initUI()
        
    def __initUI(self):
        self.setWindowIcon(QtGui.QIcon('marylandmesh.png'))
        self.setWindowTitle('Advanced')
        self.ui = uic.loadUi('json.ui', self)
        self.ui.accepted.connect(self.__addJSON)
        
    def __addJSON(self):
        global admin
        peer = str(self.ui.plainTextEdit.toPlainText())
        try:
            admin.addJSON(peer)
        except ValueError:
            ErrorWindow(self, 'Error', 'Invalid peer info')
        
        

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Meshnet Client')
    w = MainWindow()
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()

