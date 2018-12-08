from Include.commands.command import Command


class SaveLights(Command):
    """Concrete Command"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['light_model'].save()

    def undo(*args, **kwargs):
        pass