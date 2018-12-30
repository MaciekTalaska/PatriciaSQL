from PyQt5 import QtCore, QtGui, QtWidgets, uic

ui_dialog, _ = uic.loadUiType("db_settings.ui")
from db import PostgreSQL

class DBSettingsDialog(QtWidgets.QDialog, ui_dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        ui_dialog.__init__(self)
        self.setupUi(self)
        self.btnResetPort.clicked.connect(self.resetPort)
        self.btnTestConnection.clicked.connect(self.testConnection)

    def resetPort(self):
        self.txtPort.setText('5432')

    def createConnectionProperties(self):
        cp = dict()
        cp['host'] = self.txtHostName.text()
        cp['port'] = self.txtPort.text()
        cp['user'] = self.txtUserName.text()
        cp['password'] = self.txtPassword.text()
        cp['db'] = self.txtdbName.text()
        return cp

    def testConnection(self):
        #print(self.txtPort.text())
        connProps = self.createConnectionProperties()
        msg = QtWidgets.QMessageBox()
        if PostgreSQL.checkConnection(connProps):
            msg.setText("Success!")
            msg.exec_()
        else:
            msg.setText("Error!")
            msg.exec_()


    def getData(self):
        return self.createConnectionProperties()
