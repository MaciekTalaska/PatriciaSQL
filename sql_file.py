from PyQt5.QtWidgets import QFileDialog

SQL_FILE_FILTER = "SQL files (*.sql)"


class SQLFile:
    @staticmethod
    def save(content: str):
        filename, _ = QFileDialog \
            .getSaveFileName(None, "Export data to CSV",
                             ".",
                             SQL_FILE_FILTER, SQL_FILE_FILTER)
        with open(filename, "a") as f:
            f.writelines(content)

    @staticmethod
    def load():
        filename, _ = QFileDialog \
            .getOpenFileName(None, "Export data to CSV",
                             ".",
                             SQL_FILE_FILTER, SQL_FILE_FILTER)
        with open(filename, "r") as f:
            data = f.readlines()
        return "".join(data)
