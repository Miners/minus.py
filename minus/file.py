from .list import MinusList
from .object import MinusObject

class File(MinusObject):
    """ Minus File dictionary like object repsesents a file in Folder.

    Files can be created by `Folder.add_file` method."""

    def __init__(self, client, url, *args, **kwargs):
        """ Initialize File object 
        Arguments:
            :client: minus.MinusClient object
            :url: URL of File object
        Key arguments:
            other File fields
        """
        super(File, self).__init__(client, url, *args, **kwargs)

    def _get_update_values(self):
        return {
            'caption': self['caption'],
        }

    def _get_create_values(self):
        return {
            'caption': self['caption'],
            'filename': self['filename']
        }

    def save(self):
        """ Update File fields on Server side. """
        if self['id']:
            self.update(self._client.put(self._url, params=self._get_update_values()))

    def get_folder(self):
        """ Returns File's Folder. """
        from .folder import Folder
        return Folder(self._client, self['folder'])
        
class FileList(MinusList):
    """ List of Files (i.e. in a Folder)."""
    object_cls = File
