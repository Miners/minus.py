from .object import MinusObject
from .list import MinusList
from .file import File, FileList

class Folder(MinusObject):
    """ Folder represents a Minus Folder which belongs to a User and can have
    Files.
    
    Folders can be created using User.create_folder method"""

    def _get_update_values(self):
        return {
            'name': self['name'],
            'is_public': self['is_public'],
            'item_ordering': self['item_ordering']
        }

    def _get_create_values(self):
        return {
            'name': self['name'],
            'is_public': self['is_public']
        }

    def get_files(self):
        """ Returns a list of files in the Folder. """
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
        raw_file = self._client.post(self['files'], params=params)
        return File(self._client, **raw_file)
     
class FolderList(MinusList):
    """ List of Folders (i.e. User's folders)"""
    object_cls = Folder
