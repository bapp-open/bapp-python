import json
import os
import requests


class BappException(Exception):
    pass


class BappClient(object):
    """A standard HTTP REST client used by BAPP"""

    DEFAULT_CONFIG_FILE = '~/.bapp'
    HOSTS = {
        'production': 'https://api.bapp.ro',
        'dev': 'https://api-dev.bapp.ro',
    }

    def __init__(self, config_path=None, test_api=False, email=None, password=None):
        if config_path:
            self.load_config(config_path)
        else:
            if os.path.exists(os.path.expanduser(self.DEFAULT_CONFIG_FILE)):
                self.load_config(self.DEFAULT_CONFIG_FILE)
            else:
                if test_api:
                    self._host = self.HOSTS['dev']
                else:
                    self._host = self.HOSTS['production']
                self._path = self.DEFAULT_CONFIG_FILE
                self._token = None
        if not self._token:
            if email and password:
                result = self.execute('POST', 'account/authenticate', json={'email': email, 'password': password})
                self._token = result.get('token')
                self.save_config(self.DEFAULT_CONFIG_FILE)

    def load_config(self, path):
        """
        Load JSON config file from disk at the given path

        :param str path: path to config file
        """
        if '~' in path:
            path = os.path.expanduser(path)
        f = open(path)
        body = f.read()
        f.close()
        self._path = path
        try:
            config = json.loads(body)
        except Exception as e:
            raise BappException('%s: invalid config body: %s' %(self._path, e.message))
        self._token = config.get('token')
        self._host = config.get('host')

    def save_config(self, path):
        if not self._path and not path:
            raise BappException('no config path given')
        if path:
            self._path = path
        if '~' in self._path:
            self._path = os.path.expanduser(self._path)
        f = open(self._path, 'w')
        f.write(json.dumps({'token': self._token, 'host': self._host}))
        f.close()

    def execute(self, method, path, **kwargs):
        if self._token:
            headers = {'Content-type': 'application/json', 'Authorization': 'Token ' + self._token}
        else:
            headers = {'Content-type': 'application/json'}
        url = "{}/{}/".format(self._host, path)
        response = requests.request(method, url, headers=headers, **kwargs)
        return response.json()
