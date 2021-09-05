

class UnexpectedResult(Exception):
    def __init__(self, result, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self._result = result
        
    def __repr__(self):
        return f"UnexpectedResult({self._result})"
    ##
    ##
    ##
    def _getresult(self):
        return self._result
  
    result = property(_getresult, doc="get result")