
class MinusObject(dict):
    """ This is a base object to create/modify/read/delete Minus objects easily.
    A Minus Object is a dictionary like object. Fields are readeable like a
    normal dictionary. """
    _url = None
    _client = None

    def __init__(self, client, url, *args, **kwargs):
        """ Initializes a new object.
        
        Arguments:
            :client: MinusClient object
            :url: URL of Object"""
        self._client = client
        self._url = url
        if kwargs: 
            self.update(kwargs)
        else:
            self.update(self._client.get(self._url))

    @property
    def url(self):
        """ Every object has a particular URL. """
        return self._url

    def _get_update_values(self):
        raise NotImplementedError()

    def _get_create_values(self):
        raise NotImplementedError()

    def save(self, create_url=None):
        """ Creates or Updates the object on server side. """
        if self['id']:
            self.update(self._client.put(self._url, params=self._get_update_values()))
        elif create_url:
            self.update(self._client.post(create_url, params=self._get_create_values()))

    def delete(self):
        """ Deletes the object on server side. """
        self._client.delete(self._url)
        
