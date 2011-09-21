from .list import MinusList
from .object import MinusObject

class File(MinusObject):
    _fileobj = None

    def __init__(self, client, url, fileobj=None, *args, **kwargs):
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

    def save(self):
        if self['id']:
            self.update(self._client.put(self._url, params=self.get_update_values()))

    def get_folder(self):
        from .folder import Folder
        return Folder(self._client, self['folder'])
        
        

class FileList(MinusList):
    object_cls = File
