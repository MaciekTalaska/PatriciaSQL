#!/usr/bin/env python3

# This is Python port of Custom Completer Example in C++
# link to the original C++ version: https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html

from PyQt5 import QtGui, QtCore, QtWidgets
import sys


class SQLEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super(SQLEditor, self).__init__(parent)
        self.completer = None

    def setCompleter(self, new_completer):
        if self.completer:
            self.completer.disconnect()

        self.completer = new_completer

        if not self.completer:
            return
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        if self.completer.widget() != self:
            return
        tc = self.textCursor()
        extra = len(self.completer.completionPrefix())
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[extra:] + " ")
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QtWidgets.QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        # The following keys are forwarded by the completer to the widget
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
                    QtCore.Qt.Key_Enter,
                    QtCore.Qt.Key_Return,
                    QtCore.Qt.Key_Escape,
                    QtCore.Qt.Key_Tab,
                    QtCore.Qt.Key_Backtab):
                event.ignore()
                return  # let the completer do default behavior

        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_K)
        if not self.completer or not isShortcut:  # do not process the shortcut when we have a completer
            QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

        isCtrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier,
                                              QtCore.Qt.ShiftModifier)
        if isCtrlOrShift and not event.text():
            return
        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # end of word
        isOtherModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                           not isCtrlOrShift)
        currentText = self.textUnderCursor()
        if (not isShortcut and (isOtherModifier or not event.text() or
                                len(currentText) < 2) or
                (event.text()[:1] in eow)):
            self.completer.popup().hide()
            return
        self.showPopup(currentText)

    def showPopup(self, currentText):
        if currentText != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(currentText)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                    + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)  # popup it up!


class SQLKeywordsCompleter(QtWidgets.QCompleter):
    def read_keywords(self, file_name):
        words = []
        with open(file_name, "r") as input_file:
            for line in input_file:
                words.append(line.strip())
        model = QtCore.QStringListModel()
        model.setStringList(words)
        self.setModel(model)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    completer = SQLKeywordsCompleter()
    completer.read_keywords("sqlkeywords.txt")

    mainWindow = QtWidgets.QMainWindow()
    editor = SQLEditor()
    editor.setCompleter(completer)
    editor.setCompleter(completer)

    mainWindow.setCentralWidget(editor)
    mainWindow.setMinimumHeight(300)
    mainWindow.setMinimumWidth(500)
    mainWindow.setWindowTitle("Completer")
    mainWindow.show()

    app.exec_()
