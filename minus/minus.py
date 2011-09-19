from .client import MinusClient
from .user import User
from .folder import Folder, FolderList
from .file import File

class Minus(object):
    _client = None
    _baseurl = None

    def __init__(self, access_key, baseurl='https://minus.com/api/v2'):
        self._client = MinusClient(access_key)
        self._baseurl = baseurl
        
    def get_activeuser(self):
        return User(self._client, '%s/activeuser' % self.baseurl)
        
    def get_activeuser_feed(self):
        return FolderList(self._client, '%s/activeuser/feed' % self.baseurl)
        
    def get_activeuser_history(self):
        return FolderList(self._client, '%s/activeuser/history' % self.baseurl)
        
    def get_activeuser_mine(self):
        return FolderList(self._client, '%s/activeuser/mine' % self.baseurl)

    def get_folder(self, id):
        return Folder(self._client, '%s/folders/%s' % (self.baseurl, id))

    def get_user(self, id):
        return User(self._client, '%s/users/%s' % (self.baseurl, id))

    def get_file(self, id):
        return File(self._client, '%s/files/%s' % (self.baseurl, id))
