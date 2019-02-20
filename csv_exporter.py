from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from PyQt5 import QtSql

CSV_FILE_FILTER = "CSV files (*.csv)"


class CSV:
    @staticmethod
    def write_csv(model: QtSql.QSqlQueryModel):
        filename, _ = QFileDialog \
            .getSaveFileName(None, "Export data to CSV",
                             ".",
                             CSV_FILE_FILTER, CSV_FILE_FILTER)
        data = list()
        with open(filename, "a") as f:
            # process headers
            for i in range(0, model.columnCount()):
                header = str(model.headerData(i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                data.append('"' + header + '"')
            # write headers
            f.write(";".join(data))
            f.write("\n")
            # process rows
            for i in range(model.rowCount()):
                data.clear()
                for j in range(model.columnCount()):
                    cell = str(model.data(model.index(i, j)))
                    data.append('"' + cell + '"')
                f.write(";".join(data))
                f.write("\n")
