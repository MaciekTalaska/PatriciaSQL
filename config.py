import pickle

configFileName = '__patricia-connection.dat'
import os

class PatriciaConfig:
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
