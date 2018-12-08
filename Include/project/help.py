import Include.commands.translator as tr


class Help:

    def __init__(self):
        pass

    def do(self):
        print('Commands list:')
        dicto = tr.Translator.dictionary

        for key, value in dicto:
            print(key, '-', value.__doc__)

        _interpreter = None