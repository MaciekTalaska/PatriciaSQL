from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from patriciasql_main import Ui_MainWindow

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
#            self.actionAbout.triggered.connect(self.showMessage)
            p = db.PostgreSQL()
            model = p.getModel()
            self.tableView.setModel(model)
            self.tableView.show()

      def exitApplication(self):
			sys.exit(0)

      def executeQuery(self):
            queryText = self.sqlEditorArea.toPlainText()
            p = db.PostgreSQL()
            model = p.getModel(queryText)
            self.tableView.setModel(model)
            self.tableView.show()


if __name__ == "__main__":
      app = QApplication([])
      app.setApplicationName("PatriciaSQL")
      window = MainWindow()
      app.exec_()
