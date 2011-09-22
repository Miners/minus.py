import simplejson as json
from .restclient import rest_invoke

class MinusError(Exception):
    _error = {}

    @property
    def error(self):
        return self._error

    def __init__(self, error={}):
        self._error = error

class MinusAuthenticationError(MinusError):
    pass

class MinusNotFoundError(MinusError):
    pass

class MinusBadRequestError(MinusError):
    pass

class MinusClient(object):
    access_key = ''

    def __init__(self, access_key):
        self.access_key = access_key

    def _get_auth_header(self):
        return {
            'Authorization': 'Bearer %s' % self.access_key
        }
    
    def _rest_invoke(self, url, method, params={}):
        status, content = rest_invoke(url, method=method, params=params, 
            headers=self._get_auth_header())

        json_content = json.loads(content)

        if status == 404:
            raise MinusNotFoundError(json_content)

        if status == 401:
            raise MinusAuthenticationError(json_content)

        if status != 200:
            raise MinusBadRequestError(json_content)

        return json_content


    def put(self, url, params, files=None):
        return self._rest_invoke(url, method="PUT", params=params)

    def post(self, url, params, files=None):
        return self._rest_invoke(url, method="POST", params=params)

    def delete(self, url):
        return self._rest_invoke(url, method="DELETE")

    def get(self, url):
        return self._rest_invoke(url, method="GET")

