from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from patriciasql_main import Ui_MainWindow
from db_settings import Ui_Dialog

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
            # this is temporaty and should be removed soon
            self.db = db.PostgreSQL()
            model = self.db.getModel()
            self.tableView.setModel(model)
            self.tableView.show()

      def exitApplication(self):
			sys.exit(0)

      def showSettings(self):
            dialog = QDialog()
            dialog.ui = Ui_Dialog()
            dialog.ui.setupUi(dialog)
            dialog.exec_()
            dialog.show()

      def executeQuery(self):
            queryText = self.sqlEditorArea.toPlainText()
            model = self.db.getModel(queryText)
            self.tableView.setModel(model)
            self.tableView.show()


if __name__ == "__main__":
      app = QApplication([])
      app.setApplicationName("PatriciaSQL")
      window = MainWindow()
      app.exec_()
