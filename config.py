import pickle
import os

configFileName: str = '__patricia-connection.dat'


class PatriciaConfig:
    def __init__(self):
        self.props = dict()

    @property
    def user(self):
        return self.props.get('user')

    @user.setter
    def user(self, val: str):
        self.props['user'] = val

    @property
    def host(self):
        return self.props.get('host')

    @host.setter
    def host(self, val: str):
        self.props['host'] = val

    @property
    def password(self):
        return self.props.get('password')

    @password.setter
    def password(self, val: str):
        self.props['password'] = val

    @property
    def port(self):
        return self.props.get('port')

    @port.setter
    def port(self, val: str):
        if val is not None and str(val).isdigit():
            self.props['port'] = int(val)

    @property
    def db(self):
        return self.props.get('db')

    @db.setter
    def db(self, val: str):
        self.props['db'] = val

    @property
    def connectionConfig(self):
        return self.props

    # TODO: to be removed
    #    def readDefaultConfig(self):
    #        self.conp = PatriciaConfig.read()

    def read(self):
        exists = PatriciaConfig.configExists()
        data = dict()
        if exists:
            with open(configFileName, 'rb') as infile:
                data = pickle.load(infile)
            self.props = data.conp

    def isConnectionDataValid(self):
        return ((self.props is not None)
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
