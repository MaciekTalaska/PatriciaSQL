import pickle

configFileName = '__patricia-connection.dat'
import os

class PatriciaConfig:
    def __init__(self):
        self.conp = dict()

    @property
    def user(self):
        return self.conp.get('user')

    @user.setter
    def user(self, val):
        self.conp['user'] = val

    @property
    def host(self):
        return self.conp.get('host')

    @host.setter
    def host(self, val):
        self.conp['host'] = val

    @property
    def password(self):
        return self.conp.get('password')

    @password.setter
    def password(self, val):
        self.conp['password'] = val

    @property
    def port(self):
        return self.conp.get('port')

    @port.setter
    def port(self, val):
        if val is not None and str(val).isdigit():
            self.conp['port'] = int(val)

    @property
    def db(self):
        return self.conp['db']

    @db.setter
    def db(self, val):
        self.conp['db'] = val

    @property
    def connectionConfig(self):
        return self.conp

    def readDefaultConfig(self):
        self.conp = PatriciaConfig.read()

    def read(self):
        exists = PatriciaConfig.configExists()
        data = dict()
        if exists:
            infile = open(configFileName, 'rb')
            data = pickle.load(infile)
            infile.close()
            self.conp = data.conp

    def isConnectionDataValid(self):
        return ((self.conp is not None)
                          and self.host
                          and self.user
                          and self.port
                          and self.password)

    def isConnectionDataAndDBValid(self):
       return self.isConnectionDataValid() and self.db

    # static methods
    @staticmethod
    def configExists():
        return os.path.isfile(configFileName)

    @staticmethod
    def save(data):
        filename = configFileName
        outfile = open(filename, 'wb')
        pickle.dump(data, outfile)
        outfile.close()
