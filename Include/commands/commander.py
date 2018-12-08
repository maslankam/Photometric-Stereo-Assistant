from Include.commands import *

class Commander:
    """Calling command specified by Client"""
    
    def do(self, command, *args, **kwargs):
        return command.do(*args, **kwargs)
        
    def undo(self, command, *args, **kwargs):
        command.undo(*args, **kwargs)