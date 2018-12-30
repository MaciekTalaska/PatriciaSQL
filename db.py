from PyQt5 import QtSql
from PyQt5 import QtCore

class PostgreSQL:
    def __init__(self, hostName='127.0.0.1', userName='postgres', password='postgres'):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.databaseName = 'postgres'
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
        return db.isOpen()

    def __connect__(self):
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.hostName)
        db.setDatabaseName(self.databaseName)
        db.setUserName(self.userName)
        db.setPassword(self.password)
        db.open()
        return db

