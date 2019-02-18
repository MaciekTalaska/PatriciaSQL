import time
from PyQt5 import QtSql
from connection_config import ConnectionConfig

class PostgreSQLConnection:
    def __init__(self):
        self.connection = QtSql.QSqlDatabase.addDatabase("QPSQL")

    # Postgres 9.x does not allow connecting to server without specifying database name
    # so in case there is a need to connect to retrieve available databases
    # it is the best to connect to 'Postgres' database
    def __databaseNameOrPostgres__(self, dbname: str):
        if not dbname:
            return 'postgres'
        else:
            return dbname

    def reconnect(self, cp):
        if (self.connection is not None and
                self.connection.isOpen() and
                cp.isConnectionDataAndDBValid()):
            self.connection.close()
        self.connect(cp)

    def getModel(self, query: str):
        model = QtSql.QSqlQueryModel()
        start = time.time()
        model.setQuery(query)
        end = time.time()
        return model, (end-start)

    def getCurrentDBName(self):
        if (self.connection is not None and
                self.connection.isOpen()):
            return self.connection.databaseName()
        else:
            return 'none'

    def isConnectionOpen(self):
        return self.connection.isOpen()

    def checkConnection(self, cp: ConnectionConfig):
        clone = QtSql.QSqlDatabase.cloneDatabase(self.connection, "connectivityTest")
        clone.setUserName(cp.user)
        clone.setHostName(cp.host)
        clone.setPort(cp.port)
        clone.setPassword(cp.password)
        db = self.__databaseNameOrPostgres__(cp.db)
        clone.setDatabaseName(db)
        clone.open()
        status = clone.isOpen()
        if status:
            clone.close()
        QtSql.QSqlDatabase.removeDatabase("connectivityTest")
        return status

    def retrieveAvailableDatabases(self, cp: ConnectionConfig):
        databases = list()
        if not self.connection.isOpen():
            self.connect(cp)
        if self.connection.isOpen():
            query = QtSql.QSqlQuery('SELECT datname FROM pg_database WHERE datistemplate = false;')
            while query.next():
                databases.append(query.value(0))
        return databases

    def connect(self, cp: ConnectionConfig):
        if (cp.isConnectionDataValid()):
            self.connection.setHostName(cp.host)
            self.connection.setUserName(cp.user)
            self.connection.setPassword(cp.password)
            self.connection.setPort(cp.port)
            db = self.__databaseNameOrPostgres__(cp.db)
            self.connection.setDatabaseName(db)
            self.connection.open()

