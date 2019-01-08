#!/usr/bin/env python3
from PyQt5 import uic
from PyQt5.QtWidgets import *

Ui_MainWindow, _ = uic.loadUiType("patriciasql_main.ui")
from db_settings_logic import DBSettingsDialog
from config import PatriciaConfig
import syntax

import sys
import db

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.highlight = syntax.PgSQLHighlighter(self.sqlEditorArea.document())
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        self.show()
        # wire up signals & slots
        self.actionQuit.triggered.connect(self.exitApplication)
        self.actionExecute.triggered.connect(self.executeQuery)
        self.actionExecute_selected.triggered.connect(self.executeSelected)
        self.actionSettings.triggered.connect(self.showSettings)
        self.actionExplain.triggered.connect(self.explain)
        self.actionExplain_Selected.triggered.connect(self.explain_selected)
        # read config
        self.psqlConfig = PatriciaConfig()
        self.psqlConfig.read()
        # try to connect (most recent connection)
        self.pgsql = db.PostgreSQL()
        self.updateDBConnection(self.psqlConfig)

    def exitApplication(self):
        sys.exit(0)

    def updateDBConnection(self, conp):
        self.pgsql.reconnect(conp)
        self.lbldb.setText("connected to: " + self.pgsql.getCurrentDBName())

    def showSettings(self):
        retval, newConfig = DBSettingsDialog.getConnectionProperties(self.pgsql, self.psqlConfig)
        if retval == 1:
            self.psqlConfig = newConfig
            self.updateDBConnection(newConfig)

    def explain(self):
        query_text = self.sqlEditorArea.toPlainText()
        self.__execute_and_explain__(query_text)

    def explain_selected(self):
        query_text = self.__extract_selection__()
        self.__execute_and_explain__(query_text)


    def executeQuery(self):
        query_text = self.sqlEditorArea.toPlainText()
        self.__execute_query(query_text)

    def __extract_selection__(self):
        start = self.sqlEditorArea.textCursor().selectionStart()
        end = self.sqlEditorArea.textCursor().selectionEnd()
        whole_text = self.sqlEditorArea.toPlainText()
        query_text = whole_text[start:end]
        return query_text

    def executeSelected(self):
        query_text = self.__extract_selection__()
        self.__execute_query(query_text)

    def __execute_query(self, query_text):
        if self.pgsql is not None and self.pgsql.isConnectionOpen():
            model = self.pgsql.getModel(query_text)
            self.tableView.setModel(model)
            self.tableView.show()
            self.lblstatus.setText("rows: " + str(model.rowCount()))
        else:
            msg = QMessageBox()
            msg.setText("Not connected to PostgreSQL!")
            msg.setWindowTitle("Error executing query!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            self.lblstatus.setText("rows: 0")

    def __execute_and_explain__(self, query_text):
        new_query_text = "explain %s" % query_text
        self.__execute_query(new_query_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PatriciaSQL")
    window = MainWindow()
    app.exec_()
