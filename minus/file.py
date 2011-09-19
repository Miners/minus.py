from .list import MinusList
from .object import MinusObject

class File(MinusObject):

    def __init__(self, client, url, fileobj, *args, **kwargs):
        self._fileobj = fileobj
        super(File, self).__init__(client, url, *args, **kwargs)

    def get_update_values(self):
        return {
            'caption': self['caption'],
        }

    def get_create_values(self):
        return {
            'caption': self['caption'],
            'filename': self['filename']
        }

    def save(self, create_url=None):
        if self._id:
            self.update(self._client.put(self._url, params=self.get_update_values()))
        elif create_url:
            self.update(self._client.post(create_url, params=self.get_create_values(), files={'file': self._fileobj}))
        

class FileList(MinusList):
    object_cls = File
