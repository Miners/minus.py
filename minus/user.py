from .object import MinusObject
from .list import MinusList
from .folder import FolderList

class User(MinusObject):
    def get_update_values(self):
        return {
            'display_name': self['display_name']
        }

    def get_folders(self):
        return FolderList(self._client, self['folders'])

    def create_folder(self, name, is_public=False):
        params = {
            'name': name, 
            'is_public': is_public,
        }
        return self._client.post(self['folders'], params=params)

class UserList(MinusList):
    object_cls = User
