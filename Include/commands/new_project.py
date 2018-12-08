from Include.commands.command import Command
from Include.project.project import Project


class NewProject(Command):
    """[name] [path] Creating new project in default directory or on specified path"""
    
    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""
        
        name = args[0][0]
        dir = None
        
        if len(args) == 2:
            dir = args[1][0]
            
        project = Project()
        project.new(name, dir)
        return project
    
    def undo(*args, **kwargs):
        pass
