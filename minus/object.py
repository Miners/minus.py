
class MinusObject(dict):
    _url = None
    _client = None

    def __init__(self, client, url, *args, **kwargs):
        self._client = client
        self._url = url
        if kwargs: 
            self.update(kwargs)
        else:
            self.update(self._client.get(self._url))

    @property
    def url(self):
        return self._url

    def get_update_values(self):
        raise NotImplementedError()

    def get_create_values(self):
        raise NotImplementedError()

    def save(self, create_url=None):
        if self['id']:
            self.update(self._client.put(self._url, params=self.get_update_values()))
        elif create_url:
            self.update(self._client.post(create_url, params=self.get_create_values()))

    def delete(self):
        self._client.delete(self._url)
        
