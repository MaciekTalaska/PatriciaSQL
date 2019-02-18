from PyQt5 import QtWidgets, uic

ui_dialog, _ = uic.loadUiType("db_settings.ui")
from connection_config import ConnectionConfig


class DBSettingsDialog(QtWidgets.QDialog, ui_dialog):
    def __init__(self, pgsql, config):
        QtWidgets.QDialog.__init__(self)
        ui_dialog.__init__(self)
        self.setupUi(self)
        self.pgsql = pgsql
        self.btnResetPort.clicked.connect(self.resetPort)
        self.btnTestConnection.clicked.connect(self.__testConnection__)
        self.btnBrowseDatabases.clicked.connect(self.__populateAvailableDBs__)
        # populate controls with saved data (if config has it)
        if config is not None:
            if config.host is not None:
                self.txtHostName.setText(config.host)
            self.txtUserName.setText(config.user)
            self.txtPassword.setText(config.password)
            if config.port is not None:
                self.txtPort.setText(str(config.port))
            if config.db and self.pgsql.isConnectionOpen():
                self.setUsedDatabase(config.db)
        # update connection info when a field has been changed
        self.txtUserName.editingFinished.connect(self.showConnectionState)
        self.txtPassword.editingFinished.connect(self.showConnectionState)
        self.txtHostName.editingFinished.connect(self.showConnectionState)
        self.txtPort.editingFinished.connect(self.showConnectionState)

    def setUsedDatabase(self, dbname):
        self.__populateAvailableDBs__()
        self.cbxDBs.setCurrentText(dbname)

    def resetPort(self):
        self.txtPort.setText('5432')

    def __populateAvailableDBs__(self):
        conp = self.__createConnectionProperties__()
        dbs = self.pgsql.retrieveAvailableDatabases(conp)
        for i in range(len(dbs)):
            self.cbxDBs.addItem(str(dbs[i]))

    def __createConnectionProperties__(self):
        cp = ConnectionConfig()
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
            msg.setWindowTitle("Success!")
            msg.setText("Connection to database established succesfully")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()
        else:
            msg.setWindowTitle("Erorr!")
            msg.setText("Unable to connect to PostgreSQL server!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()

    def getConnectionPropertiesInternal(self):
        props = self.__createConnectionProperties__()
        ConnectionConfig.save(props)
        return self.__createConnectionProperties__()

    def showConnectionState(self):
        connectionProperties = self.__createConnectionProperties__()
        if self.pgsql.checkConnection(connectionProperties):
            self.lblConnectionState.setText("success!")
            self.lblConnectionState.setStyleSheet("color:rgb(85, 170, 127)")
            if self.cbxDBs.count() < 1:
                self.__populateAvailableDBs__()
        else:
            self.lblConnectionState.setText("error connecting...")
            self.lblConnectionState.setStyleSheet("color:rgb(170, 0, 0)")

    @staticmethod
    def getConnectionProperties(pgsql, config):
        dialog = DBSettingsDialog(pgsql, config)
        retval = dialog.exec_()
        newConfig = None
        if retval == 1:
            newConfig = dialog.getConnectionPropertiesInternal()
        return retval, newConfig
