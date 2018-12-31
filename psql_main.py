#!/usr/bin/env python
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
        patriciaConfig = PatriciaConfig()
        self.__connect2Database__(patriciaConfig.getConfig())

    def exitApplication(self):
		sys.exit(0)

    # this should be move to db.py
    def __connect2Database__(self, conp):
        if (len(conp))>=4:
            self.db = db.PostgreSQL(conp)
            self.lbldb.setText("connected to: " + str(conp['db']))
        else:
            self.db = None
            self.lbldb.setText("connected to: none")

    def showSettings(self):
         dialog = DBSettingsDialog()
         retval = dialog.exec_()
         if retval == 1:
             conp = dialog.getData()
             self.__connect2Database__(conp)

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
