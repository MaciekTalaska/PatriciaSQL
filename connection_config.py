import json
import os

CONNECTION_CONFIG_FILE_NAME: str = '_patricia-connection.json'


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
        if exists:
            with open(CONNECTION_CONFIG_FILE_NAME, 'r') as infile:
                content = infile.read()
                data = json.loads(content)
            self.props = data

    def validate_connection_data(self, include_db: bool = False):
        connection_valid = ((self.props is not None)
                            and self.host
                            and self.user
                            and self.password
                            and self.port)
        return connection_valid and (self.db or (not include_db))

    @staticmethod
    def config_file_exists():
        return os.path.isfile(CONNECTION_CONFIG_FILE_NAME)

    # TODO: type info should be added (ConnectionConfig can not be used)
    @staticmethod
    def save_configuration(data):
        with open(CONNECTION_CONFIG_FILE_NAME, 'w') as outfile:
            content = json.dumps(data.props, sort_keys=True, indent=4, separators=(',', ': '))
            outfile.write(content)

    @staticmethod
    def from_data(host: str, user: str, password: str, port: str = '5432', db: str = 'postgres'):
        config = ConnectionConfig()
        config.host = host
        config.user = user
        config.password = password
        config.port = port
        config.db = db
        return config
