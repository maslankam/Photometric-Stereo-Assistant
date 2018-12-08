from Include.commands.command import Command


class SaveDepth(Command):
    """Concrete Command"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['depth'].save()

    def undo(*args, **kwargs):
        pass