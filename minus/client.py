import simplejson as json
from .restclient import rest_invoke

class MinusError(Exception):
    _error = {}

    @property
    def error(self):
        return self._error

    def __init__(self, error={}):
        self._error = error

class MinusAuthenticationError(MinusError):
    pass

class MinusNotFoundError(MinusError):
    pass

class MinusBadRequestError(MinusError):
    pass

class MinusClient(object):
    access_key = ''
    secret = ''
    username = ''
    password = ''
    authurl = ''
    bearer_token = None
    refresh_token = None

    def __init__(self, access_key,secret,username,password,authurl='https://minus.com/oauth/token'):
        self.access_key = access_key
        self.secret = secret
        self.username = username
        self.password = password    
        self.authurl = authurl
        
        json_content = self._authenticate()
        
        self.bearer_token=json_content['access_token']
        self.refresh_token=json_content['refresh_token']
            
    def _rest_invoke(self, url, method, params={}):
        headers_params={}
        
        if self.bearer_token:
            params['bearer_token']=self.bearer_token            
                     
        status, content = rest_invoke(url, method=method, params=params,headers=headers_params)

        json_content = json.loads(content)

        if status == 404:
            raise MinusNotFoundError(json_content)

        if status == 401:
            raise MinusAuthenticationError(json_content)

        if status != 200:
            raise MinusBadRequestError(json_content)

        return json_content
    
    def _authenticate(self):
        # scope = read_public || upload_new
        params={'grant_type':'password','client_id':self.access_key,'client_secret':self.secret,'scope':'upload_new','username':self.username,'password':self.password}
        return self.post(self.authurl,params)
        
    def put(self, url, params, files=None):
        return self._rest_invoke(url, method="PUT", params=params)

    def post(self, url, params, files=None):
        return self._rest_invoke(url, method="POST", params=params)

    def delete(self, url):
        return self._rest_invoke(url, method="DELETE")

    def get(self, url):    
        return self._rest_invoke(url, method="GET")

