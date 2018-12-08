from setup import ROOT_DIR

from Include.project.project import Project

import os, unittest, shutil, sys, getpass
from pathlib import Path


class TestProject(unittest.TestCase):
    """Testing the parser class"""


    def setUp(self):
        self.venv_path = ROOT_DIR
        self._name_path = Path(str(self.venv_path) + "/Projects/Dummy")
        self.project = None

        if sys.platform == 'linux':
            self._custom_path = Path('/home/{}/Custom/'.format(getpass.getuser()))

        if sys.platform == 'win32':
            self._custom_path = Path('C:\\Users\\{}\\Custom\\'.format(getpass.getuser()))

    def tearDown(self):
        try:
            shutil.rmtree(self._name_path)
        except FileNotFoundError as e:
            pass
        try:
            shutil.rmtree(self._custom_path)
        except FileNotFoundError as e:
            pass

    def test_making_new_project_default(self):
        self.project = Project()

        self.project.new('Dummy')

        self.assertEqual(self.project.name, 'Dummy')

        self._check_directories(self.venv_path)

        # Checking what if new project will be invoked whith existing name
        _copy_of_dummy_project = self.project
        self.project.new('Dummy')

        self.assertEqual(self.project, _copy_of_dummy_project)

        # Hard delete of project and his directory

        shutil.rmtree(self._name_path)
        self.project = None

    def test_making_new_project_with_custom_path(self):
        if sys.platform == 'linux':
            self._custom_path = Path('/home/{}/Custom/'.format(getpass.getuser()))

        if sys.platform == 'win32':
            self._custom_path = Path('C:\\Users\\{}\\Custom\\'.format(getpass.getuser()))

        self.project = Project()
        # Checking what if directory doesnt exist

        self.assertEqual(None, self.project.new('Dummy', self._custom_path))

        # Checking with existing path
        os.mkdir(self._custom_path)
        self.project.new('Dummy', self._custom_path)
        self.assertEqual(self.project.name, 'Dummy')

        self._check_directories(self._custom_path)

        # Checking what if new project will be invoked with existing name
        _copy_of_dummy_project = self.project
        self.project.new('Dummy', self._custom_path)

        self.assertEqual(self.project, _copy_of_dummy_project)

        # Hard delete of project and his directory
        self.project = None
        shutil.rmtree(self._custom_path)

    def test_open_default_project(self):
        self.project = Project()
        self.project.new('Dummy')

        self.project = None

        self.project = Project()
        self.project.open('Dummy')

        self.assertEqual(self.project.name, 'Dummy')

        self._check_directories(self.venv_path)

        shutil.rmtree(self._name_path)

    def test_open__with_custom_path(self):


        self.project = Project()
        os.mkdir(self._custom_path)
        self.project.new('Dummy', self._custom_path)

        self.project = None

        self.project = Project()
        self.project.open("Dummy", self._custom_path)

        self.assertEqual(self.project.name, 'Dummy')

        self._check_directories(self._custom_path)

        shutil.rmtree(self._custom_path)

    def _check_directories(self, dir):
        self.assertEqual(self.project.directories['home'], dir)

        _projects_path = Path(str(dir) + "/Projects")
        self.assertEqual(self.project.directories['projects'], _projects_path)

        _name_path = Path(str(dir) + "/Projects/Dummy")
        self.assertEqual(self.project.directories['name'], _name_path)

        _images_path = Path(str(dir) + "/Projects/Dummy/Images")
        self.assertEqual(self.project.directories['images'], _images_path)

        _results_path = Path(str(dir) + "/Projects/Dummy/Results")
        self.assertEqual(self.project.directories['results'], _results_path)

        _config_path = Path(str(dir) + "/Projects/Dummy/config.txt")
        self.assertEqual(self.project.directories['config'], _config_path)


if __name__ == '__main__':
    unittest.main()