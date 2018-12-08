from Include.commands.command import Command


class ComputeLights(Command):
    """Compute light model"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['light_model'].compute()

    def undo(*args, **kwargs):
        pass