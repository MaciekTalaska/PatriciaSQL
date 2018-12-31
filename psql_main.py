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
        # read config & use last saved connection
        patriciaConfig = PatriciaConfig()
        config = patriciaConfig.getConfig()
        self.updateDBConnection(config)

    def exitApplication(self):
        sys.exit(0)

    def updateDBConnection(self, conp):
        self.db = db.PostgreSQL(conp)
        if self.db is not None:
            self.lbldb.setText("connected to: " + conp['db'])
        else:
            self.lbldb.setText("connected to: none")

    def showSettings(self):
        dialog = DBSettingsDialog()
        retval = dialog.exec_()
        if retval == 1:
            conp = dialog.getData()
            self.updateDBConnection(conp)

    def executeQuery(self):
        if self.db is not None:
            queryText = self.sqlEditorArea.toPlainText()
            model = self.db.getModel(queryText)
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
