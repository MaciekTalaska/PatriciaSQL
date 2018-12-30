import pickle

configFileName = '__patricia-connection.dat'

class PatriciaConfig:
    @staticmethod
    def read():
        pass

    @staticmethod
    def save(data):
        #props = self.createConnectionProperties()
        filename = configFileName
        outfile = open(filename, 'wb')
        pickle.dump(data, outfile)
        outfile.close()
