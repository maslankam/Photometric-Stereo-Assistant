from Include.commands.command import Command


class ShowLights(Command):
    """Concrete Command"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['light_model'].show()

    def undo(*args, **kwargs):
        pass