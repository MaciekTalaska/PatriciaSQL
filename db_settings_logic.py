from PyQt5 import QtWidgets, uic
from connection_config import ConnectionConfig
from db import PostgreSQLConnection

ui_dialog, _ = uic.loadUiType("db_settings.ui")


class DBSettingsDialog(QtWidgets.QDialog, ui_dialog):
    def __init__(self, connection: PostgreSQLConnection, config: ConnectionConfig):
        QtWidgets.QDialog.__init__(self)
        ui_dialog.__init__(self)
        self.setupUi(self)
        self.connection = connection
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
            if config.db and self.connection.isConnectionOpen():
                self.setUsedDatabase(config.db)
        # update connection info when a field has been changed
        self.txtUserName.editingFinished.connect(self.showConnectionState)
        self.txtPassword.editingFinished.connect(self.showConnectionState)
        self.txtHostName.editingFinished.connect(self.showConnectionState)
        self.txtPort.editingFinished.connect(self.showConnectionState)

    def setUsedDatabase(self, db_name: str):
        self.__populateAvailableDBs__()
        self.cbxDBs.setCurrentText(db_name)

    def resetPort(self):
        self.txtPort.setText('5432')

    def __populateAvailableDBs__(self):
        connection_config = self.__createConnectionConfig__()
        db_names = self.connection.retrieveAvailableDatabases(connection_config)
        for i in range(len(db_names)):
            self.cbxDBs.addItem(str(db_names[i]))

    def __createConnectionConfig__(self):
        config = ConnectionConfig.from_data(
            self.txtHostName.text(),
            self.txtUserName.text(),
            self.txtPassword.text(),
            self.txtPort.text(),
            self.cbxDBs.currentText())
        return config

    def __testConnection__(self):
        connection_config = self.__createConnectionConfig__()
        msg = QtWidgets.QMessageBox()
        if self.connection.checkConnection(connection_config):
            msg.setWindowTitle("Success!")
            msg.setText("Connection to database established successfully")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()
        else:
            msg.setWindowTitle("Error!")
            msg.setText("Unable to connect to PostgreSQL server!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()

    def showConnectionState(self):
        connection_config = self.__createConnectionConfig__()
        if self.connection.checkConnection(connection_config):
            self.lblConnectionState.setText("success!")
            self.lblConnectionState.setStyleSheet("color:rgb(85, 170, 127)")
            if self.cbxDBs.count() < 1:
                self.__populateAvailableDBs__()
        else:
            self.lblConnectionState.setText("error connecting...")
            self.lblConnectionState.setStyleSheet("color:rgb(170, 0, 0)")

    def getConnectionPropertiesInternal(self):
        connection_config = self.__createConnectionConfig__()
        ConnectionConfig.save_configuration(connection_config)
        return self.__createConnectionConfig__()

    @staticmethod
    def getConnectionProperties(connection: PostgreSQLConnection, connection_config: ConnectionConfig):
        dialog = DBSettingsDialog(connection, connection_config)
        success = (dialog.exec_() == 1)
        new_config = None
        if success:
            new_config = dialog.getConnectionPropertiesInternal()
        return success, new_config
