

import datetime

class GitHubClientBase(object):
    def __init__(self, token, url="https://api.github.com"):
        """Git hub access token
        if token is callable it will be invoked to produce the token """
        self._token = token
        self._url = url
        self._rateLimitRemaining = None
        self._rateLimitReset = None
        
    def _headers(self, additionHeaders=dict()):
        headers = {}
        headers.update(additionHeaders)
        if( self._token ):
            if callable(self._token):
                headers["Authorization"] = f"token {self._token()}"
            else:
                headers["Authorization"] = f"token {self._token}"
        
        if headers:
            return headers
        return None
    
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