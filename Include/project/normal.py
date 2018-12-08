from Include.project.segment import Segment

from Include.project.image_reader import ImageReader
import numpy as np
from pathlib import Path

import os, cv2, csv, math


class Normal(Segment):
    """Normal segment reponsible for normal field processing"""

    def __init__(self, project):
        self.content = {'mask': None, 'images': None, 'normals': None}
        self.project = project
        self.state = {'data': False, 'save': False}

        if 'normals.csv' in os.listdir(project.directories['results']):
            self.state['save'] = True
            self.read_normals()
            self.read_images()

    def __str__(self):
        return 'Normals'

        
    def import_from(self):
        # Don't import normal map
        pass

    def save(self):
        if self.content['normals'] is None:
            print("Nothing to save")
            return

        if 'lights.csv' in os.listdir(self.project.directories['results']):
            os.remove(self.project.directories['results']) + '/normals.csv'

        _path = Path(str(self.project.directories['results']) + '/normals.csv')

        _file = open(_path, mode='a', newline='')

        with _file:
            _writer = csv.writer(_file, delimiter=',')

            normals = self.content['normals']
            for line in normals:
                vectors_list = []
                for vector in line:
                    vectors_list.append([vector[0], vector[1], vector[2]])
                _writer.writerow(vectors_list)
        self.state['save'] = True

    def show(self):
        cv2.imshow('normal', self.content['normals'])
        X, Y, Z = cv2.split(self.content['normals'])
        cv2.imshow('X', X)
        cv2.imshow('Y', Y)
        cv2.imshow('Z',Z)


        cv2.waitKey()
        pass

    def compute(self, THRESH = 100):
        """Compute normal vector field using images saved in project/Images directory"""
        # TODO: template pattern

        L = self.project.segments['light_model'].content['lights']

        if self.content['images'] is None:
            self.read_images()

        mask = self.content['mask']
        image_shape = mask.shape
        images_list = self.content['images']

        kd_array = np.zeros((image_shape[0], image_shape[1]))
        n_array = np.zeros((image_shape[0], image_shape[1], 3))

        for xy, mask_value in np.ndenumerate(mask):
            I = np.zeros(len(images_list))
            if mask_value > THRESH:
                i = 0
                for image in images_list:
                    I[i] = image[xy]
                    i = i + 1

                g = np.linalg.lstsq(L, I, rcond=None)

                kd = math.sqrt(g[0][0] ** 2 + g[0][1] ** 2 + g[0][2] ** 2)
                kd_array[xy] = kd / 255

                if kd != 0:
                    n = (1.0 / kd) * g[0]
                else:
                    n = [0.0, 0.0, 0.0]
                n_array[xy] = n


            else:
                kd_array[xy] = 0.0
                n_array[xy] = [0., 0., 0.]

        self.content['normals'] = n_array
        self.state['data'] = True

    def read_normals(self):
        path = Path(str(self.project.directories['results']) + '/normals.csv')

        try:
            csv_file = open(path)
        except FileNotFoundError as e:
            print("File Not Found")


        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            normals = []

            for line in csv_reader:
                #print('line', line)
                vectors_list = []
                for vector in line:
                    vector = vector[1:-1]  # Removing brackets []
                    vector_content_list = vector.split(',')  # Content extraction
                    #print('vector',vector)
                    #print('vector_content_list', vector_content_list)

                    for i in range(3):
                        v = float(vector_content_list[i])
                        vector_content_list[i] = v
                        #i =+ 1 # TODO: RLY?

                    vectors_list.append(vector_content_list)
                normals.append(vectors_list)

            normals = np.array(normals)

        self.content['normals'] = normals
        self.state['data'] = True

    def read_images(self):
        reader = ImageReader()
        images = reader.read(str(self.project.directories['images']))
        images_list = []

        for name in images:
            if 'mask' in name:
                mask = images[name]
                self.content['mask'] = mask
            else:
                images_list.append(images[name])
                self.content['images'] = images_list
