import time
from PyQt5 import QtSql


class PostgreSQL:
    def __init__(self):
        self.connection = QtSql.QSqlDatabase.addDatabase("QPSQL")

    # Posgtgres 9.x does not allow conneting to server without specifying database name
    # so in case there is a need to connect to retrieve available databases
    # it is the best to connect to 'Postgres' database
    def __databaseNameOrPostgres__(self, dbname):
        if not dbname:
            return 'postgres'
        else:
            return dbname

    def reconnect(self, conp):
        if (self.connection is not None and
                self.connection.isOpen() and
                conp.isConnectionDataAndDBValid()):
            self.connection.close()
        self.connect(conp)

    def getModel(self, query):
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

    def checkConnection(self, conp):
        clone = QtSql.QSqlDatabase.cloneDatabase(self.connection, "connectivityTest")
        clone.setUserName(conp.user)
        clone.setHostName(conp.host)
        clone.setPort(conp.port)
        clone.setPassword(conp.password)
        db = self.__databaseNameOrPostgres__(conp.db)
        clone.setDatabaseName(db)
        clone.open()
        status = clone.isOpen()
        if status:
            clone.close()
        QtSql.QSqlDatabase.removeDatabase("connectivityTest")
        return status

    def retrieveAvailableDatabases(self, conp):
        databases = list()
        if not self.connection.isOpen():
            self.connect(conp)
        if self.connection.isOpen():
            query = QtSql.QSqlQuery('SELECT datname FROM pg_database WHERE datistemplate = false;')
            while query.next():
                databases.append(query.value(0))
        return databases

    def connect(self, conp):
        if (conp.isConnectionDataValid()):
            self.connection.setHostName(conp.host)
            self.connection.setUserName(conp.user)
            self.connection.setPassword(conp.password)
            self.connection.setPort(conp.port)
            db = self.__databaseNameOrPostgres__(conp.db)
            self.connection.setDatabaseName(db)
            self.connection.open()

