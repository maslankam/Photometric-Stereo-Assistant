from Include.project.project import Project
from setup import ROOT_DIR

import numpy
from pathlib import Path

import unittest, shutil, os


class TestLightModel(unittest.TestCase):

    def setUp(self):
        self.venv_path = ROOT_DIR
        self._name_path = Path(str(self.venv_path) + "/Projects/Dummy")

        self._test_list = [
            [0.497239, 0.467590, 0.730831],
            [0.242239, 0.134516, 0.960846],
            [-0.039076, 0.174182, 0.983938],
            [-0.092171, 0.443696, 0.891425],
            [-0.320376, 0.501764, 0.803488],
            [-0.110444, 0.560479, 0.820771],
            [0.281349, 0.424216, 0.860746],
            [0.100207, 0.430122, 0.897192],
            [0.206193, 0.333679, 0.919860],
            [0.086330, 0.331788, 0.939396],
            [0.128565, 0.044748, 0.990691],
            [-0.139927, 0.360562, 0.922180]]

        self._test_list2 = [  # Different set of data
            [1.237239, 0.467590, 0.730851],
            [4.2452239, 0.134516, 0.960886],
            [- 3.049076, 0.134182, 0.983238],
            [- 0.092171, 0.443696, 0.891425],
            [- 0.320376, 0.501764, 0.823488],
            [- 0.130444, 0.560379, 0.825771],
            [0.281349, 0.424116, 0.860746],
            [0.102207, 0.430122, 0.895192],
            [0.306193, 0.333679, 0.919860],
            [0.086330, 0.331388, 0.939326],
            [0.528565, 0.044748, 0.990691],
            [- 0.131927, 0.362562, 0.922980]]

    def tearDown(self):
        try:
            shutil.rmtree(self._name_path)
            pass
        except FileNotFoundError as e:
            pass

    def test_reading_from_file_when_created(self):
        self._project = Project()
        self._project.open('Buddha')
        self.segment = self._project.segments['light_model']

        self.assertEqual(self._test_list, self.segment.content['lights'])
        self._project = None

    def test_importing(self):
        self._project = Project()
        self._project.new('Dummy')
        self.segment = self._project.segments['light_model']

        self.assertEqual(None, self.segment.content['lights'])

        # Import OK data set
        self._test_csv_file('test.csv')

        # Import NOK data set - less than 3 lines
        self._test_csv_file('test2.csv')

        # Import NOK data set - not a float
        self._test_csv_file('test3.csv')

        # Import NOK data set - not a 3 dim vector
        self._test_csv_file('test4.csv')

        # Import NOK data set - not a .csv file
        self._test_csv_file('test5.txt')

        shutil.rmtree(self._name_path)
        self._project = None

    def test_reading_images(self):
        self._project = Project()
        self._project.open('Buddha')
        self.segment = self._project.segments['light_model']

        # Hard cleaning
        self.segment.content = {'mask': None, 'images': None, 'lights': None}

        self.segment._read_images()

        self.assertEqual(str(type(self.segment.content['mask'])), '<class \'numpy.ndarray\'>')
        self.assertEqual(str(type(self.segment.content['images'])), '<class \'list\'>')

        for image in self.segment.content['images']:
            self.assertEqual(str(type(image)), '<class \'numpy.ndarray\'>')

        self._project = None

    def test_computing(self):
        self._project = Project()
        self._project.new('Dummy')
        self.segment = self._project.segments['light_model']

        # Hard import form Tests
        src_path = Path(str(self.venv_path) + '/Tests/project/Lights')
        dest_path = Path(str(self._name_path) + '/Lights')
        os.rmdir(dest_path)
        shutil.copytree(str(src_path), str(dest_path))

        self.segment.compute()

        print(self.segment.content['lights'])
        self.assertEqual(str(type(self.segment.content['lights'])), '<class \'list\'>')
        for image in self.segment.content['images']:
            self.assertEqual(str(type(image)), '<class \'numpy.ndarray\'>')

        self._project = None

        shutil.rmtree(self._name_path)

    def test_save(self):
        self._project = Project()
        self._project.new('Dummy')
        self.segment = self._project.segments['light_model']

        _path = Path(str(self.venv_path) + '/Tests/project/test.csv')
        print(self.segment.content['lights'])
        self.segment.import_from(str(_path))

        self.segment.save()

        _new_path = Path(str(self._name_path) + '/Lights')

        self.assertTrue('lights.csv' in os.listdir(str(_new_path)))

        shutil.rmtree(self._name_path)
        self._project = None

    def _test_csv_file(self, file):
        _path = Path(str(self.venv_path) + '/Tests/project/{}'.format(file))
        self.segment.import_from(str(_path))

        self.assertEqual(self._test_list2, self.segment.content['lights'])

if __name__ == '__main__':
    unittest.main()
