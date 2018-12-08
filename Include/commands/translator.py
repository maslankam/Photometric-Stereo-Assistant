from Include.commands.new_project import NewProject
from Include.commands.open_project import OpenProject
from Include.commands.import_lights import ImportLights
from Include.commands.compute_lights import ComputeLights
from Include.commands.compute_normals import ComputeNormals
from Include.commands.compute_depth import ComputeDepth
from Include.commands.save_lights import SaveLights
from Include.commands.save_normals import SaveNormals
from Include.commands.save_depth import SaveDepth
from Include.commands.show_lights import ShowLights
from Include.commands.show_depth import ShowDepth
from Include.commands.close_project import CloseProject
from Include.commands.exit_app import ExitApp
from Include.commands.show_surface import ShowSurface
from Include.commands.show_normals import ShowNormals
from Include.commands.help import Help


class Translator:
    dictionary = {
        'new': NewProject,
        'open': OpenProject,
        'close': CloseProject,
        'exit': ExitApp,
        'lcompute': ComputeLights,
        'limport': ImportLights,
        'lshow': ShowLights,
        'lsave': SaveLights,
        'ncompute': ComputeNormals,
        'nsave': SaveNormals,
        'nshow': ShowNormals,
        'dcompute': ComputeDepth,
        'dshow': ShowDepth,
        'dsave': SaveDepth,
        'sshow': ShowSurface,
        'help': Help
    }

    def __init__(self):
        pass

    def interpret(self, text = None):
        if text not in Translator.dictionary:
            print('Unknown command, type \'help\' to find command list')
            return None

        command = Translator.dictionary[str(text)]

        return command


