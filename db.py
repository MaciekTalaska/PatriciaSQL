from PyQt5 import QtSql
from PyQt5 import QtCore

class PostgreSQL:
    def __init__(self):
        self.connection = None
        self.connection = QtSql.QSqlDatabase.addDatabase("QPSQL")
        #self.connection = PostgreSQL.connect(conp)

    def __isProperConnectionProperties__(self, props):
        if ('host' in props and
           'user' in props and
           'password' in props and
           'db' in props):
            return True
        else:
            return False

    def reconnect(self, conp):
        print("-- reconnect --")
        if ((self.connection is not None) and
                (self.connection.isOpen()) and
                self.__isProperConnectionProperties__(conp)):
            self.connection.close()
        self.connect(conp)
        #self.connection = PostgreSQL.connect(conp)

    def getModel(self, query):
        model = QtSql.QSqlQueryModel()
        model.setQuery(query)
        return model

    def getCurrentDBName(self):
        if (self.connection is not None and
                self.connection.isOpen()):
            return self.connection.databaseName()
        else:
            return 'none'

#    def closeCurrentConnection(self):
#        if self.db.isOpen():
#            self.db.close()




    def checkConnection(self, conp):
        clone = QtSql.QSqlDatabase.cloneDatabase(self.connection, "connectivityTest")
        print("is open?: " + str(clone.isOpen()))
        clone.setUserName(conp['user'])
        clone.setHostName(conp['host'])
        clone.setPort(int(conp['port']))
        clone.setPassword(conp['password'])
        clone.open()
        print("is open?: " + str(clone.isOpen()))
        status = clone.isOpen()
        if status:
            clone.close()
        QtSql.QSqlDatabase.removeDatabase("connectivityTest")
        return status

    def checkConnection3(self, conp):
        print('connection properties to test: ' + str(conp))
        #clone = self.connection.cloneDatabase("connectivityTest")
        clone = QtSql.QSqlDatabase.cloneDatabase(self.connection, "connectivityTest")
        #clone = QtSql.QSqlDatabase.addDatabase("QPSQL", "connectivityTest")
        #clone = QtSql.QSqlDatabase.database("connectivityTest")
        print("is new connection open: " + str(clone.isOpen()))
        clone.setUserName = conp['user']
        clone.setHostName = conp['host']
        clone.setPassword = conp['password']
        #clone.setPort = int(conp['port'])
        clone.setPort = 5432
        clone.setDatabaseName = 'postgres'
        #clone.setDatabaseName = con['db']
        #print("about to open new connection with properties: "+str(clone.password()))
        print("real properties of clone connection: ")
        print("user: " + clone.userName())
        print("host: " + clone.hostName())
        print("password: " + clone.password())
        print("port: " + str(clone.port()))
        print("database: " + clone.databaseName())
        clone.open()
        status = clone.isOpen()
        print("connections: " + str(QtSql.QSqlDatabase.connectionNames()))
        print("error: " + str(clone.lastError()))
        if status:
            clone.close()
            QtSql.QSqlDatabase.removeDatabase("connectivityTest")
        print("it was success: " + str(status))
        return status


#    @staticmethod
#    def checkConnection(conp):
#        # this works with static connect only
#        pass
##        db = PostgreSQL.connect(conp)
##        status = db.isOpen()
##        if status:
##            db.close()
##        return status

    def retrieveAvailableDatabases(self, conp):
        databases = list()
        if not self.connection.isOpen():
            self.connect(conp)
        if self.connection.isOpen():
            print("connection is open, selecting databases")
            query = QtSql.QSqlQuery('SELECT datname FROM pg_database WHERE datistemplate = false;')
            while query.next():
                databases.append(query.value(0))
        print("retrieved databases: ")
        print(databases)
        return databases



#    @staticmethod
#    def retrieveAvailableDatabases(conp):
#        # this works only with static connect
#        pass
##        db = PostgreSQL.connect(conp)
##        databases = list()
##        if db.isOpen():
##            query = QtSql.QSqlQuery('SELECT datname FROM pg_database WHERE datistemplate = false;')
##            while query.next():
##                databases.append(query.value(0))
##            #db.close()
##        return databases


    def connect(self, conp):
        if (len(conp)>=4):
            self.connection.setHostName(conp['host'])
            self.connection.setUserName(conp['user'])
            self.connection.setPassword(conp['password'])
            self.connection.setPort(int(conp['port']))
            if 'db' in conp:
                self.connection.setDatabaseName(conp['db'])
            self.connection.open()
#        if not self.connection.isOpen():
#            self.connection.open()


#    @staticmethod
#    def connect(conp):
#        db = QtSql.QSqlDatabase.addDatabase("QPSQL")
#        if (len(conp)>=4):
#            db.setHostName(conp['host'])
#            db.setUserName(conp['user'])
#            db.setPassword(conp['password'])
#            db.setDatabaseName(conp['db'])
#            db.setPort(int(conp['port']))
#            db.open()
#        else:
#            db = None
#        return db

