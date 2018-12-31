from PyQt5 import QtSql
from PyQt5 import QtCore

class PostgreSQL:
    def __init__(self, conp):
        self.connection = PostgreSQL.connect(conp)

    def getModel(self, query='SELECT datname FROM pg_database WHERE datistemplate = false;'):
        model = QtSql.QSqlQueryModel()
        model.setQuery(query)
        return model

    def closeCurrentConnection(self):
        if self.db.isOpen():
            self.db.close()

    @staticmethod
    def checkConnection(conp):
        db = PostgreSQL.connect(conp)
        status = db.isOpen()
        if status:
            db.close()
        return status

    @staticmethod
    def getAvailableDatabases(conp):
        db = PostgreSQL.connect(conp)
        databases = list()
        if db.isOpen():
            query = QtSql.QSqlQuery('SELECT datname FROM pg_database WHERE datistemplate = false;')
            while query.next():
                databases.append(query.value(0))
            db.close()
        return databases


    @staticmethod
    def connect(conp):
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(conp['host'])
        db.setUserName(conp['user'])
        db.setPassword(conp['password'])
        db.setDatabaseName(conp['db'])
        db.setPort(int(conp['port']))
        db.open()
        return db

