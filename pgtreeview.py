from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from db import PostgreSQLConnection


class PgTreeView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(PgTreeView, self).__init__(parent)
        self.setItemsExpandable(True)
        self.setExpandsOnDoubleClick(True)
        self.setWordWrap(True)
        self.collapseAll()
        self.doubleClicked.connect(self.update_treeView)
        self.setRootIsDecorated(True)
        self.db_connection = None

    def set_db_connection(self, db_connection: PostgreSQLConnection):
        self.db_connection = db_connection

    def update_treeView(self, index):
        model = self.model()
        item = model.itemFromIndex(index)
        if item.parent() is not None and item.parent().parent() is None:
            data = model.data(index)
            table_fields = self.get_table_fields(data)
            row_count = table_fields.rowCount()
            for i in range(row_count):
                row = table_fields.record(i)
                column_name = row.value(0)
                column_type = row.value(1)
                type_length = row.value(2)
                if type_length != 0:
                    item_data = "%s (%s [%d])" % (column_name, column_type, type_length)
                else:
                    item_data = "%s (%s)" %(column_name, column_type)
                new_item = QtGui.QStandardItem(item_data)
                new_item.setToolTip(item_data)
                new_item.setEditable(False)
                item.appendRow(new_item)

    def read_schemas_tables(self):
        if self.model() is None or self.model().rowCount() == 0:
            schemas = self.get_table_schema_hierarchy()
            self.setModel(schemas)

    def get_table_schema_hierarchy(self):
        model = self.get_tables()

        new_model = QtGui.QStandardItemModel()
        new_model.setHorizontalHeaderItem(0, QtGui.QStandardItem("schema/table"))
        current_parent = None
        root_node = new_model.invisibleRootItem()

        rows_count = model.rowCount()
        current_schema = ""
        for index in range(rows_count):
            row = model.record(index)
            schema = row.value(0)
            if current_schema != schema:
                current_schema = schema
                current_parent = QtGui.QStandardItem(schema)
                current_parent.setEditable(False)
                root_node.appendRow(current_parent)
            child = QtGui.QStandardItem(row.value(1))
            child.setEditable(False)
            current_parent.appendRow(child)

        return new_model

    def get_tables(self):
        if self.db_connection.isConnectionOpen():
            query = "select table_schema, table_name from information_schema.tables" \
                    " where table_type like '%TABLE' " \
                    "group by table_schema, table_name " \
                    "order by table_schema, table_name"
            model, _ = self.db_connection.getModel(query)
            return model

    def get_table_fields(self, table_name: str):
        if self.db_connection.isConnectionOpen():
            query = "select column_name, data_type, character_maximum_length " \
                    "from INFORMATION_SCHEMA.COLUMNS " \
                    "where table_name ='%s';"
            model, _ = self.db_connection.getModel(query % table_name)
            return model

