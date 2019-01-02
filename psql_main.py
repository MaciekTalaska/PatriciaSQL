#!/usr/bin/env python3
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

Ui_MainWindow, _ = uic.loadUiType("patriciasql_main.ui")
from db_settings_logic import DBSettingsDialog
from config import PatriciaConfig

import sys
import db

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        # wire up signals & slots
        self.actionQuit.triggered.connect(self.exitApplication)
        self.actionExecute.triggered.connect(self.executeQuery)
        self.actionSettings.triggered.connect(self.showSettings)
        # read config
        patriciaConfig = PatriciaConfig()
        config = patriciaConfig.connectionConfig
        # try to connect (most recent connection)
        self.pgsql = db.PostgreSQL()
        self.updateDBConnection(config)

    def exitApplication(self):
        sys.exit(0)

    def updateDBConnection(self, conp):
        self.pgsql.reconnect(conp)
        self.lbldb.setText("connected to: " +str(self.pgsql.getCurrentDBName()))

    def showSettings(self):
        dialog = DBSettingsDialog(self.pgsql)
        retval = dialog.exec_()
        if retval == 1:
            conp = dialog.getConnectionProperties()
            self.updateDBConnection(conp)

    def executeQuery(self):
        if self.pgsql is not None:
            queryText = self.sqlEditorArea.toPlainText()
            model = self.pgsql.getModel(queryText)
            self.tableView.setModel(model)
            self.tableView.show()
            self.lblstatus.setText("rows: " + str(model.rowCount()))
        else:
            msg = QMessageBox()
            msg.setText("Not connected to DB!")
            msg.exec_()
            self.lblstatus.setText("rows: " + str(model.rowCount()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PatriciaSQL")
    window = MainWindow()
    app.exec_()
