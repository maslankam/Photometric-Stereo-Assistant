from Include.commands.command import Command
from Include.project.help import Help
import Include.commands.translator as tr

class Help(Command):
    """Printing commands list and help"""


    def do(*args, **kwargs):
        print('Commands list:')
        dicto = tr.Translator.dictionary

        for key in dicto:
            print(key, '-', dicto[key].__doc__)

    def undo(*args, **kwargs):
        pass