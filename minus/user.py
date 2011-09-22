from .object import MinusObject
from .list import MinusList
from .folder import Folder, FolderList

class User(MinusObject):
    def _get_update_values(self):
        return {
            'display_name': self['display_name']
        }

    def get_folders(self):
        """ Returns the Folders of the User."""
        return FolderList(self._client, self['folders'])

    def create_folder(self, name, is_public=False):
        """ Create a new Folder.
        
        Arguments:
            :name: Name of Folder
            :is_public: Folder can be public (True) or private (False).
        """
        params = {
            'name': name, 
            'is_public': is_public,
        }
        raw_folder = self._client.post(self['folders'], params=params)
        return Folder(self._client, **raw_folder)

class UserList(MinusList):
    """ List of Users. """
    object_cls = User
