import pickle

configFileName = '__patricia-connection.dat'
import os

class PatriciaConfig:
    def __init__(self):
        self.conp = PatriciaConfig.read()

    @property
    def user(self):
        return self.conp['user']

    @property
    def host(self):
        return self.conp['host']

    @property
    def password(self):
        return self.conp['password']

    @property
    def port(self):
        p = self.conp['port']
        n = int(p)
        if p is not None and n is not None:
            return n
        else:
            raise "no port defined!"

    @property
    def dbname(self):
        return self.conp['db']

    @property
    def connectionConfig(self):
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
