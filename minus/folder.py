from .object import MinusObject
from .list import MinusList
from .file import FileList

class Folder(MinusObject):

    def get_update_values(self):
        return {
            'name': self['name'],
            'is_public': self['is_public'],
            'item_ordering': self['item_ordering']
        }

    def get_create_values(self):
        return {
            'name': self['name'],
            'is_public': self['is_public']
        }

    def get_files(self):
        return FileList(self._client, self['files'])

    def add_file(self, file_object, filename, caption=''):
        """Add (upload) new file to the folder.

        Arguments:
            :file_object: file like object
            :filename: filename string
            :caption: caption
        """
        params = {
            'filename': filename, 
            'caption': caption, 
            'file': file_object,
        }
        return self._client.post(self['files'], params=params)
     
class FolderList(MinusList):
    object_cls = Folder
