# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db_settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 398)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 350, 461, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.txtUserName = QtWidgets.QLineEdit(Dialog)
        self.txtUserName.setGeometry(QtCore.QRect(180, 60, 261, 32))
        self.txtUserName.setObjectName("txtUserName")
        self.txtPassword = QtWidgets.QLineEdit(Dialog)
        self.txtPassword.setGeometry(QtCore.QRect(180, 100, 261, 32))
        self.txtPassword.setObjectName("txtPassword")
        self.txtHostName = QtWidgets.QLineEdit(Dialog)
        self.txtHostName.setGeometry(QtCore.QRect(180, 140, 261, 32))
        self.txtHostName.setObjectName("txtHostName")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 180, 151, 32))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lblUserName = QtWidgets.QLabel(Dialog)
        self.lblUserName.setGeometry(QtCore.QRect(50, 70, 121, 18))
        self.lblUserName.setObjectName("lblUserName")
        self.lblPassword = QtWidgets.QLabel(Dialog)
        self.lblPassword.setGeometry(QtCore.QRect(50, 110, 121, 18))
        self.lblPassword.setObjectName("lblPassword")
        self.lblHostname = QtWidgets.QLabel(Dialog)
        self.lblHostname.setGeometry(QtCore.QRect(50, 150, 121, 18))
        self.lblHostname.setObjectName("lblHostname")
        self.lblPort = QtWidgets.QLabel(Dialog)
        self.lblPort.setGeometry(QtCore.QRect(50, 190, 121, 18))
        self.lblPort.setObjectName("lblPort")
        self.lblDatabase = QtWidgets.QLabel(Dialog)
        self.lblDatabase.setGeometry(QtCore.QRect(50, 230, 121, 18))
        self.lblDatabase.setObjectName("lblDatabase")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(350, 180, 88, 34))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(180, 220, 151, 32))
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 220, 88, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lblConnectionName = QtWidgets.QLabel(Dialog)
        self.lblConnectionName.setGeometry(QtCore.QRect(50, 30, 121, 18))
        self.lblConnectionName.setObjectName("lblConnectionName")
        self.txtConnectionName = QtWidgets.QLineEdit(Dialog)
        self.txtConnectionName.setGeometry(QtCore.QRect(180, 20, 261, 32))
        self.txtConnectionName.setObjectName("txtConnectionName")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(307, 270, 131, 34))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.txtConnectionName, self.txtUserName)
        Dialog.setTabOrder(self.txtUserName, self.txtPassword)
        Dialog.setTabOrder(self.txtPassword, self.txtHostName)
        Dialog.setTabOrder(self.txtHostName, self.lineEdit_4)
        Dialog.setTabOrder(self.lineEdit_4, self.pushButton)
        Dialog.setTabOrder(self.pushButton, self.lineEdit_5)
        Dialog.setTabOrder(self.lineEdit_5, self.pushButton_2)
        Dialog.setTabOrder(self.pushButton_2, self.pushButton_3)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit_4.setText(_translate("Dialog", "5432"))
        self.lblUserName.setText(_translate("Dialog", "user name:"))
        self.lblPassword.setText(_translate("Dialog", "password:"))
        self.lblHostname.setText(_translate("Dialog", "host name:"))
        self.lblPort.setText(_translate("Dialog", "port"))
        self.lblDatabase.setText(_translate("Dialog", "database name:"))
        self.pushButton.setText(_translate("Dialog", "Reset"))
        self.pushButton_2.setText(_translate("Dialog", "Browse"))
        self.lblConnectionName.setText(_translate("Dialog", "connection name:"))
        self.pushButton_3.setText(_translate("Dialog", "Test Connection"))

