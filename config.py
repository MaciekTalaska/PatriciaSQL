import pickle

configFileName = '__patricia-connection.dat'
import os

class PatriciaConfig:
    def __init__(self):
        self.conp = dict()

    @property
    def user(self):
        return self.conp['user']

    @user.setter
    def user(self, val):
        self.conp['user'] = val

    @property
    def host(self):
        return self.conp['host']

    @host.setter
    def host(self, val):
        self.conp['host'] = val

    @property
    def password(self):
        return self.conp['password']

    @password.setter
    def password(self, val):
        self.conp['password'] = val

    @property
    def port(self):
        p = self.conp['port']
        n = int(p)
        if p is not None and n is not None:
            return n
        else:
            raise Exception("no port defined!")

    @port.setter
    def port(self, val):
        self.conp['port'] = val

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
        validity = (self.conp is not None) and self.host and self.user and self.port and self.db and self.password
        return validity

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
