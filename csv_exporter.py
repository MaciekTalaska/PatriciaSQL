from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtSql

class CSV:
    @staticmethod
    def write_csv(model: QtSql.QSqlQueryModel):
        file_filter = "CSV files (*.csv)"
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export data to CSV",
                                                            ".",
                                                            file_filter, file_filter)
        f = open(filename, "a")

        data = list()
        for i in range(0, model.columnCount()):
            header = str(model.headerData(i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
            data.append('"' + header + '"')

        f.write(";".join(data))
        f.write("\n")

        for i in range(model.rowCount()):
            data.clear()
            for j in range(model.columnCount()):
                cell = str(model.data(model.index(i, j)))
                data.append('"' + cell + '"')
            f.write(";".join(data))
            f.write("\n")
        f.close()
