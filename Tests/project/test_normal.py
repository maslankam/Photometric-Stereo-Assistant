from Include.project.project import Project
from setup import ROOT_DIR

from pathlib import Path

import unittest, os, shutil


class TestNormal(unittest.TestCase):
    def setUp(self):
        self.venv_path = ROOT_DIR
        self._name_path = Path(str(self.venv_path) + "/Projects/Dummy")

    def tearDown(self):
        try:
            shutil.rmtree(self._name_path)
            pass
        except FileNotFoundError as e:
            pass

    def test_computing_and_saving(self):
        self._project = Project()
        self._project.new('Dummy')

        # Hard import from Tests
        src_path = Path(str(self.venv_path) + '/Tests/project/Lights')
        dest_path = Path(str(self._name_path) + '/Lights')
        shutil.rmtree(dest_path)
        shutil.copytree(str(src_path), str(dest_path))

        src_path = Path(str(self.venv_path) + '/Tests/project/Images')
        dest_path = Path(str(self._name_path) + '/Images')
        shutil.rmtree(dest_path)
        shutil.copytree(str(src_path), str(dest_path))

        self._project = None
        self._project = Project()
        self._project.open('Dummy')
        self.segment = self._project.segments['normal']

        self.segment.compute()

        self.assertEqual(str(type(self.segment.content['normals'])), '<class \'numpy.ndarray\'>')

        self.segment.save()
        self.assertTrue('normals.csv' in os.listdir(self._project.directories['results']))

        shutil.rmtree(self._name_path)
        self._project = None

    '''def reading_from_existing_csv_normals(self):
        _project = Project()
        _project.new('Dummy')

        # Hard import from Tests
        src_path = Path(str(self.venv_path) + '/Tests/project/Lights')
        dest_path = Path(str(self._name_path) + '/Lights')
        shutil.rmtree(str(dest_path))
        shutil.copytree(str(src_path), str(dest_path))

        src_path = Path(str(self.venv_path) + '/Tests/project/Images')
        dest_path = Path(str(self._name_path) + '/Images')
        os.rmdir(str(dest_path))
        shutil.copytree(str(src_path), str(dest_path))

        src_path = Path(str(self.venv_path) + '/Tests/project/Results')
        dest_path = Path(str(self._name_path) + '/Results')
        os.rmdir(str(dest_path))
        shutil.copytree(str(src_path), str(dest_path))

        # Open Dummy again with prepared data
        _project = Project()
        _project.open('Dummy')

        self.assertEqual(str(type(self.segment.content['normals'])), '<class \'numpy.ndarray\'>')

        shutil.rmtree(self._name_path)
        self._project = None'''



