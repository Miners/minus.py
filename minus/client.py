import simplejson as json
from .restclient import GET, POST, PUT, DELETE

class MinusClient(object):
    access_key = ''

    def __init__(self, access_key):
        self.access_key = access_key

    def _get_auth_header(self):
        return {
            'Authorization': 'Bearer %s' % self.access_key
        }

    def put(self, url, params, files=None):
        content = PUT(url, params=params, headers=self._get_auth_header(), async=False)
        return json.loads(content)

    def post(self, url, params, files=None):
        content = POST(url, params=params, headers=self._get_auth_header(), async=False)
        return json.loads(content)

    def delete(self, url):
        content = DELETE(url, headers=self._get_auth_header(), async=False)
        return json.loads(content)

    def get(self, url):
        content = GET(url, headers=self._get_auth_header(), async=False)
        return json.loads(content)
