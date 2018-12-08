import setup

from Include.project.light_model import LightModel
from Include.project.normal import Normal
from Include.project.albedo import Albedo
from Include.project.depth import Depth
from Include.project.surface import Surface

import os
from pathlib import Path


class Project():
    """Class representing current active project"""
    
    def __init__(self):
        """Making new project instance for program"""
        pass

    def __str__(self):
        return str(self.name)


    def save(self):
        """Save all data to 'project.txt' """
        pass

    def show(self):
        """Project info"""
        def segment_status(segment):
            if segment.state['data']:
                data = 'ready'
            else:
                data = 'not ready'

            if segment.state['save']:
                save = 'saved'
            else:
                save = 'not saved'

            print(segment, data, save)

        segment_status(self.segments['light_model'])
        segment_status(self.segments['normal'])
        segment_status(self.segments['depth'])

    def new(self, name, dir = None):
        """Making project from scratch, makes new directory in Projects"""

        self.name = name
        self.directories = Project._default_directories(name, dir)

        self._exists = self._check_existence()

        if self._exists == -1:
            print("Directory doesn't exist")
            return None

        if self._exists:
            print("Project already exist")
            return None

        self._make_directories()

        self.segments = {
            'light_model': LightModel(self),
            'normal': Normal(self),
            'albedo': Albedo(self),
            'depth': Depth(self),
            'surface': Surface(self)}

        self._make_config_file()

        return self
    
    def open(self, name, dir = None):
        """Opening existing project"""
        self.name = name
        self.directories = Project._default_directories(name, dir)

        self._exists = self._check_existence()

        if self._exists == -1:
            print("Directory doesn't exist")
            return None


        if not self._exists:
            print("Project doesn't exist")
            self.name = None
            return None

        self.segments = {
            'light_model': LightModel(self),
            'normal': Normal(self),
            'albedo': Albedo(self),
            'depth': Depth(self),
            'surface': Surface(self)}

        self._read_config_file()

        return self

    def import_from(self, dir, new_dir):
        """Import project from exterior directory, and make new"""

        pass

    def _default_directories(project_name, dir = None):
        """Static method, Returns dictionary with default project directories
        dict(home, projects, name, lights, images, results)
        """
        if dir == None:
            home = setup.ROOT_DIR
        else:
            home = Path(dir)

        projects = Path(str(home) + '/Projects')
        name = Path(str(projects) + "/" + str(project_name))
        lights = Path(str(name) + "/Lights")
        images = Path(str(name) + "/Images")
        results = Path(str(name) + "/Results")
        config = Path(str(name) + "/config.txt")

        directories = {'home': home,
                           'projects': projects,
                           'name': name,
                           'lights': lights,
                           'images': images,
                           'results': results,
                           'config': config}
        return directories

    def _make_directories(self):
        if 'Projects' not in os.listdir(self.directories['home']):
            os.mkdir(self.directories['projects'])

        os.mkdir(self.directories['name'])
        os.mkdir(self.directories['lights'])
        os.mkdir(self.directories['images'])
        os.mkdir(self.directories['results'])

    def _make_config_file(self):
        with open(str(self.directories['name']) + "/config.txt", "w+") as config:
            config.write(str(self.name) + '\n')
            config.write(str(self.directories))

    def _read_config_file(self):
        pass

    def _check_existence(self):
        try:
            _home_list = os.listdir(self.directories['home'])
        except FileNotFoundError as e:
            errno, strerror = e.args
            print("FileNotFoundError({0}): {1}".format(errno, strerror))
            return -1

        if 'Projects' not in _home_list:
            os.mkdir(self.directories['projects'])

        if self.name in os.listdir(self.directories['projects']):
            return True
        else:
            return False
