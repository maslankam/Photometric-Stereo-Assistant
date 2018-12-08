from Include.commands.command import Command


class ShowDepth(Command):
    """Concrete Command"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['depth'].show()

    def undo(*args, **kwargs):
        pass