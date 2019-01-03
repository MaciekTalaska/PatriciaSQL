from PyQt5 import QtWidgets, uic

ui_dialog, _ = uic.loadUiType("db_settings.ui")
from config import PatriciaConfig

class DBSettingsDialog(QtWidgets.QDialog, ui_dialog):
    def __init__(self, pgsql, config):
        QtWidgets.QDialog.__init__(self)
        ui_dialog.__init__(self)
        self.setupUi(self)
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
        self.pgsql = pgsql

    # TODO:
    def setUsedDatabase(self):
        #1 get all available databases
        #2 populate combobox
        #3 set combobox to the value from config - if possible
        #4 if not possible? - what to do?
        pass


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

    def getConnectionPropertiesInternal(self):
        props = self.__createConnectionProperties__()
        PatriciaConfig.save(props)
        return self.__createConnectionProperties__()

    @staticmethod
    def getConnectionProperties(pgsql, config):
        dialog = DBSettingsDialog(pgsql, config)
        retval = dialog.exec_()
        if retval == 1:
            newConfig = dialog.getConnectionPropertiesInternal()
        return retval, newConfig
