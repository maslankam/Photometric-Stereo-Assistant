from Include.project.abstract_reader import AbstractReader

from pathlib import Path
import cv2, os


class ImageReader(AbstractReader):
    def __init__(self):
        pass

    def read(self, path, extension = '.png'):
        """Read entire directory and returns dictionary {name: data}"""
        images = {}

        try:
            _files_list = os.listdir(str(path))
        except FileNotFoundError as e:
            print('Path doesnt exist')
        except NotADirectoryError as e:
            print('Not a Directory')

        for file in _files_list:
            if file[-4:] == extension:
                _file_path = Path(str(path) + '/' + file)
                images[file] = cv2.imread(str(_file_path), cv2.IMREAD_GRAYSCALE)  # TODO: RGB reading

        return images
