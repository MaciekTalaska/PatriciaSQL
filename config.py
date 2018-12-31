import pickle

configFileName = '__patricia-connection.dat'
import os

class PatriciaConfig:
    def __init__(self):
        self.conp = PatriciaConfig.read()

    def setUser(self, user):
        self.conp['user'] = user

    def setHost(self, host):
        self.conp['host'] = host

    def setPassword(self, password):
        self.conp['password'] = password

    def setPort(self, port):
        self.conp['port'] = port

    def getConfig(self):
        return self.conp

    @staticmethod
    def configExists():
        return os.path.isfile(configFileName)

    @staticmethod
    def read():
        data = dict()
        exists = PatriciaConfig.configExists()
        if exists:
            infile = open(configFileName, 'rb')
            data = pickle.load(infile)
            infile.close()
        return data

    @staticmethod
    def save(data):
        filename = configFileName
        outfile = open(filename, 'wb')
        pickle.dump(data, outfile)
        outfile.close()
