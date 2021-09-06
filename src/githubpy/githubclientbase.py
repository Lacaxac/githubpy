

import datetime, requests, sys

class GitHubClientBase(object):
    def __init__(self, username=None, password=None, token=None, url="https://api.github.com", usesession=False):
        """Git hub access token
        if token is callable it will be invoked to produce the token """
        self._username = username
        self._password = password
        self._token = token
        self._url = url
        self._rateLimitRemaining = None
        self._rateLimitReset = None
        
        self.usesession = usesession
        
    def _setusesession(self, usesession):
        if usesession:
            self._session = requests.session()
        else:
            self._session = requests
            
    def _getusesession(self):
        return self._session != requests

    usesession = property(_getusesession, _setusesession, doc="Use requests' sessions")
        
    def resetSession(self):
        if not self.usesession:
            return
        self._session = requests.session()
        
    def _requests_kwargs(self, additionHeaders=dict()):
        r_kwargs = { 'headers': {} }
        r_kwargs['headers'].update(additionHeaders)
        if( self._token ):
            if callable(self._token):
                r_kwargs['headers']["Authorization"] = f"token {self._token()}"
            else:
                r_kwargs['headers']["Authorization"] = f"token {self._token}"
        elif self._username:
            r_kwargs['auth'] = (self._username, self._password)
        
        
        return r_kwargs
        
    
    def _updateStats(self, headers:dict):
        remaining = headers.get('X-RateLimit-Remaining')
        if remaining is not None:
            self._rateLimitRemaining = int(remaining)
        
        reset = headers.get('X-RateLimit-Reset')
        if reset is not None:
            self._rateLimitReset = reset
        
    
    
    ##
    ##
    ##
    def _getrateLimitRemaining(self):
        return self._rateLimitRemaining
  
    rateLimitRemaining = property(_getrateLimitRemaining, doc="get rateLimitRemaining")
    
    
    ##
    ##
    ##
    def _getrateLimitReset(self):
        return datetime.datetime.fromtimestamp(int(self._rateLimitReset))
  
    rateLimitReset = property(_getrateLimitReset, doc="get local time when rate limit will reset")
    
    @classmethod
    def paginate(clazz, methodcall, *args, **kwargs):
        """Utility method that will paginate a request, gathering the results
        up to the pagination_limit_parameter
        
        arguments:
        methodcall -- method that can be paginated
        page -- optional starting page(defaults to 1)
        pagination_limit -- maximum number of results to return
        
        """
        
        if 'pagination_limit' in kwargs:
            limit = kwargs.pop('pagination_limit')
        else:
            limit = sys.maxsize
        
        if 'page' in kwargs:
            page = kwargs['page']
        else:
            page = 1
            
        if 'per_page' not in kwargs:
            per_page = kwargs['per_page'] = 100
        else:
            per_page = kwargs['per_page']
            
        results = []
        while limit > 0:
            
            if limit < per_page:
                kwargs['per_page'] = limit
            
            kwargs['page'] = page
            data = methodcall(*args, **kwargs)
            if not isinstance(data, list):
                return data # an error of some description
            if len(data) == 0:
                return results 
            results.extend(data)
            page += 1
            limit -= len(data)
            
        return results 
            
        