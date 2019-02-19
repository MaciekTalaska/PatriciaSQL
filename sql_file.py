from PyQt5 import QtWidgets

SQL_FILE_FILTER = "SQL files (*.sql)"

class SQLFile:
    @staticmethod
    def save(content: str):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export data to CSV",
                                                            ".",
                                                            SQL_FILE_FILTER, SQL_FILE_FILTER)
        with open(filename, "a") as f:
            f.writelines(content)

    @staticmethod
    def load():
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Export data to CSV",
                                                            ".",
                                                            SQL_FILE_FILTER, SQL_FILE_FILTER)
        with open(filename, "r") as f:
            data = f.readlines()
        return "".join(data)
