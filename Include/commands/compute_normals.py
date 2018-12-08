from Include.commands.command import Command


class ComputeNormals(Command):
    """Compute normals, requires light model and images to process"""

    def do(*args, **kwargs):
        """Make new preoject directory and return new project"""

        project = args[0]

        project.segments['normal'].compute()

    def undo(*args, **kwargs):
        pass