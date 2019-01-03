from PyQt5 import QtCore, QtGui, QtWidgets, uic

ui_dialog, _ = uic.loadUiType("db_settings.ui")
from db import PostgreSQL
from config import PatriciaConfig

class DBSettingsDialog(QtWidgets.QDialog, ui_dialog):
    def __init__(self, pgsql):
        QtWidgets.QDialog.__init__(self)
        ui_dialog.__init__(self)
        self.setupUi(self)
        self.btnResetPort.clicked.connect(self.resetPort)
        self.btnTestConnection.clicked.connect(self.__testConnection__)
        self.btnBrowseDatabases.clicked.connect(self.__populateAvailableDBs__)
        self.pgsql = pgsql

    def resetPort(self):
        self.txtPort.setText('5432')

    def __populateAvailableDBs__(self):
        conp = self.__createConnectionProperties__()
        dbs = self.pgsql.retrieveAvailableDatabases(conp)
        for i in range(len(dbs)):
            self.cbxDBs.addItem(str(dbs[i]))

    def __createConnectionProperties__(self):
        cp = PatriciaConfig()
        cp.host = self.txtHostName.text()
        cp.port = int(self.txtPort.text())
        cp.user = self.txtUserName.text()
        cp.password = self.txtPassword.text()
        cp.db = self.cbxDBs.currentText()
        return cp

    def __testConnection__(self):
        connProps = self.__createConnectionProperties__()
        msg = QtWidgets.QMessageBox()
        if self.pgsql.checkConnection(connProps):
            msg.setText("Success!")
            msg.exec_()
        else:
            msg.setText("Error!")
            msg.exec_()

    @staticmethod
    def getConnectionProperties(pgsql):
        dialog = DBSettingsDialog(pgsql)
        retval = dialog.exec_()
        if retval == 1:
            newConfig = dialog.getConnectionPropertiesInternal()
        return retval, newConfig
