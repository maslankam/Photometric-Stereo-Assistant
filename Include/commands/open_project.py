from Include.commands.command import Command
from Include.project.project import Project


class OpenProject(Command):
    """Concrete Command
    Opening project"""
    
    def do(*args, **kwargs):
        """Open existing project"""
        name = args[0][0]
        path = None

        if len(args) == 3:
            path = args[1][2]

        project = Project()
        project.open(name, path)

        if project.name is None:
            project = None

        return project

    def undo(*args, **kwargs):
        pass
