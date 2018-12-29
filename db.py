from PyQt5 import QtSql
from PyQt5 import QtCore

class PostgreSQL:
    def __init__(self, hostName='127.0.0.1', userName='postgres', password='postgres'):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.databaseName = 'postgres'

    def getModel(self):
        db = self.__connect__()
        model = QtSql.QSqlQueryModel()
        model.setQuery("SELECT datname FROM pg_database WHERE datistemplate = false;")
        return model

    def __connect__(self):
        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.hostName)
        db.setDatabaseName(self.databaseName)
        db.setUserName(self.userName)
        db.setPassword(self.password)
        db.open()
        return db

