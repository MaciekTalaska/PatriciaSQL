import pickle
import os

CONNECTION_CONFIG_FILE_NAME: str = '_patricia-connection.dat'


class ConnectionConfig:
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

    def read_configuration(self):
        exists = ConnectionConfig.config_file_exists()
        data = dict()
        if exists:
            with open(CONNECTION_CONFIG_FILE_NAME, 'rb') as infile:
                data = pickle.load(infile)
            self.props = data.props

    def validate_connection_data(self):
        return ((self.props is not None)
                and self.host
                and self.user
                and self.port
                and self.password)

    def validate_connection_data_and_dbname(self):
        return self.validate_connection_data() and self.db

    @staticmethod
    def config_file_exists():
        return os.path.isfile(CONNECTION_CONFIG_FILE_NAME)

    # TODO: add type info
    @staticmethod
    def save_configuration(data: dict):
        filename = CONNECTION_CONFIG_FILE_NAME
        outfile = open(filename, 'wb')
        pickle.dump(data, outfile)
        outfile.close()
