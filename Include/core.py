from Include.commands.commander import Commander
from Include.commands.new_project import NewProject
from Include.commands.open_project import OpenProject
from Include.commands.close_project import CloseProject
from Include.commands.exit_app import ExitApp
from Include.commands.translator import Translator


class Core:
    """Program Core"""

    def __init__(self):
        self.exit = False
        self.commander = Commander()
        self.project = None
        self.interpreter = Translator()

    def go(self):
        while not self.exit:
            if self.project is None:
                prompt = ">>>"
            else:
                prompt = ">>>" + str(self.project) + ">>>"

            args = input(prompt).split()

            command = self.interpreter.interpret(args[0])

            if command is None:
                pass
            elif command == ExitApp:
                self.exit = True
            elif command == CloseProject:
                self.project = None
            elif command == NewProject or command == OpenProject:
                self.project = self.commander.do(command, args[1:])
            else:
                self.commander.do(command, self.project, args[1:])

            if self.project is not None:
                self.project.show()
