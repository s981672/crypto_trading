

class Log():
    
    def _log(self, msg, *args, **kwargs):
        print(f'### {msg}')
    
    def debug(self, msg, *args, **kwargs):
        self._log(msg)
        
        