from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from db import PostgreSQLConnection

VIEW_SUFFIX = ' (v)'


class PgTreeView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(PgTreeView, self).__init__(parent)
        self.setItemsExpandable(True)
        self.setExpandsOnDoubleClick(True)
        self.setWordWrap(True)
        self.collapseAll()
        self.doubleClicked.connect(self.update_table_info)
        self.setRootIsDecorated(True)
        self.db_connection = None

    def set_db_connection(self, db_connection: PostgreSQLConnection):
        self.db_connection = db_connection

    def update_table_info(self, index: QtCore.QModelIndex):
        model = self.model()
        item = model.itemFromIndex(index)
        if item.parent() is not None and item.parent().parent() is None and item.rowCount() == 0:
            data = str(model.data(index)).replace(VIEW_SUFFIX, '')
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
                    item_data = "%s (%s)" % (column_name, column_type)
                new_item = QtGui.QStandardItem(item_data)
                new_item.setToolTip(item_data)
                new_item.setEditable(False)
                item.appendRow(new_item)

    def read_schemas_tables(self):
        # if self.model() is None or self.model().rowCount() == 0:
        # TODO: line above is commented because schema and table info has to be refreshed when a different database
        #       is chosen to connect to. But from a performance perspective (and due to the fact that information on
        #       tables/views is loaded on demand by issuing SQL query) it would be best to think about not losing
        #       already obtained info. This could be done by:
        #       1) Leaving non-public schemas as they are
        #       2) hiding the public/user schema
        #       3) show the currently selected schema
        #       This approach has such an advantage, that switching between schemas will result in no requirement
        #       for obtaining already retrieved info.
        if self.db_connection.isConnectionOpen():
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
            table_name = row.value(1)
            table_type = row.value(2)
            if current_schema != schema:
                current_schema = schema
                current_parent = QtGui.QStandardItem(schema)
                current_parent.setEditable(False)
                root_node.appendRow(current_parent)
            item_data = table_name
            if 'view' in table_type.lower():
                item_data += VIEW_SUFFIX
            child = QtGui.QStandardItem(item_data)
            child.setEditable(False)
            current_parent.appendRow(child)

        return new_model

    def get_tables(self):
        if self.db_connection.isConnectionOpen():
            query = "select table_schema, table_name, table_type from information_schema.tables " \
                    "group by table_schema, table_name, table_type " \
                    "order by table_schema, table_name, table_type"
            model, _ = self.db_connection.getModel(query)
            return model

    def get_table_fields(self, table_name: str):
        if self.db_connection.isConnectionOpen():
            query = "select column_name, data_type, character_maximum_length " \
                    "from INFORMATION_SCHEMA.COLUMNS " \
                    "where table_name ='%s';"
            model, _ = self.db_connection.getModel(query % table_name)
            return model

