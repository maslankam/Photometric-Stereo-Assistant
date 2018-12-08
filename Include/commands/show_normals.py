from Include.commands.command import Command


class ShowNormals(Command):
    """Concrete Command"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['normal'].show()

    def undo(*args, **kwargs):
        pass
