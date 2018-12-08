from Include.commands.command import Command


class SaveNormals(Command):
    """Concrete Command"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['normal'].save()

    def undo(*args, **kwargs):
        pass