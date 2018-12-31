from PyQt5 import QtSql
from PyQt5 import QtCore

class PostgreSQL:
    def __init__(self, host='127.0.0.1', user='postgres', password='postgres', dbname='postgres'):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.connection = self.__connect__()

    def getModel(self, query='SELECT datname FROM pg_database WHERE datistemplate = false;'):
        model = QtSql.QSqlQueryModel()
        model.setQuery(query)
        return model

    def closeCurrentConnection(self):
        if self.db.isOpen():
            self.db.close()

    @staticmethod
    def checkConnection(connArgs):
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(connArgs['host'])
        db.setUserName(connArgs['user'])
        db.setPassword(connArgs['password'])
        db.open()
        status = db.isOpen()
        if status:
            db.close()
        return status

    @staticmethod
    def getAvailableDatabases(connArgs):
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(connArgs['host'])
        db.setUserName(connArgs['user'])
        db.setPassword(connArgs['password'])
        db.setPort(int(connArgs['port']))
        db.open()
        databases = list()
        if db.isOpen():
            query = QtSql.QSqlQuery('SELECT datname FROM pg_database WHERE datistemplate = false;')
            while query.next():
                databases.append(query.value(0))
            db.close()
        return databases


    def __connect__(self):
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.host)
        db.setDatabaseName(self.dbname)
        db.setUserName(self.user)
        db.setPassword(self.password)
        db.open()
        return db

