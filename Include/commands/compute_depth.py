from Include.commands.command import Command


class ComputeDepth(Command):
    """Computing depth, requires lights and normals"""

    def do(*args, **kwargs):
        project = args[0]

        project.segments['depth'].compute()

    def undo(*args, **kwargs):
        pass