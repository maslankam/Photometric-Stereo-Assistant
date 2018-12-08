from Include.commands.command import Command


class ImportLights(Command):
    """[path] importing lights.csv file"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]
        path = args[1][0]

        project.segments['light_model'].import_from(path)

    def undo(*args, **kwargs):
        pass