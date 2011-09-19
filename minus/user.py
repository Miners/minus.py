from .object import MinusObject
from .list import MinusList
from .folder import FolderList

class User(MinusObject):
    def get_update_values(self):
        return {
            'display_name': self['display_name']
        }

    def get_folders(self):
        return FolderList(self['folders'])

class UserList(MinusList):
    object_cls = User
