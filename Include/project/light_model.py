from Include.project.segment import Segment
from Include.project.image_reader import ImageReader

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import shutil

import os, cv2, csv, math


class LightModel(Segment):
    """LightModel segment reponsible for light sources procesing"""

    def __init__(self, project):
        self.content = {'mask': None, 'images': None, 'lights': None}
        self.project = project
        self.state = {'data': False, 'save': False}

        if 'lights.csv' in os.listdir(project.directories['lights']):
            self.state['save'] = True
            self._read_lights()

    def __str__(self):
        return 'Lights:'

    def __del__(self):
        pass

    def import_from(self, path):
        """Importing table of lights from exterior path"""
        self._read_lights(path)

    def save(self):
        """Saving table of lights in project directory"""
        if self.content['lights'] is None:
            print("Nothing to save")
            return

        if 'lights.csv' in os.listdir(self.project.directories['lights']):
            os.remove(str(self.project.directories['lights']) + '/lights.csv')

        _path = Path(str(self.project.directories['lights']) + '/lights.csv')

        with open(_path, 'a', newline='') as _file:
            for light in self.content['lights']:
                writer = csv.writer(_file, delimiter=',')
                data = [[str(light[0]), str(light[1]), str(light[2])]]
                writer.writerows(data)

        self.state['save'] = True

    def show(self, representation = 'both'):
        """"Showing representation of light model"""
        if self.content['lights'] is None:
            print('Nothing to show')
            return

        def show2D(vectors):
            colors = ['r', 'g', 'b', 'y']
            BASE = []
            x = []
            y = []

            for vector in vectors:
                BASE.append(0)
                x.append(vector[0])
                y.append(vector[1])

            plt.quiver(BASE, BASE, x, y, color=colors, angles='xy', scale_units='xy',
                       scale=1)

            LIM = max(np.max(x), np.max(y))

            plt.xlim(-LIM, LIM)
            plt.ylim(-LIM, LIM)
            plt.grid(b=True, which='major', axis='both')
            plt.show()

        def show3D(vectors):
            U, V, W = zip(*vectors)

            X = np.zeros((1, len(V)))
            Y = np.zeros((1, len(V)))
            Z = np.zeros((1, len(V)))
            print('U', U)
            print('V', V)
            print('W', W)
            print('X', X)
            print('Y', Y)
            print('Z', Z)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.quiver(X, Y, Z, U, V, W, color=['r'])
            ax.set_xlim([-0.5, 0.5])
            ax.set_ylim([0, 1.0])
            ax.set_zlim([0, 1])
            plt.show()

        if representation == 'both' or representation == '2D':
            show2D(self.content['lights'])

        if representation == 'both' or representation == '3D':
            show3D(self.content['lights'])

    def compute(self):
        """Computing light model from photos in project/Lights directory"""
        # TODO: use Template Pattern
        def compute_centroid(image, threshold=125):
            """
            Computing centroid of given image.
            Please notice that this function can't check if given image is
            continuous blob, image must be preprocessed.

            :param image:
            :param threshold:
            :return: {x, y}
            """
            xsum = 0
            ysum = 0
            count = 0
            for xy, value in np.ndenumerate(image):
                if value > threshold:
                    xsum = xsum + xy[0]
                    ysum = ysum + xy[1]
                    count = count + 1
            return [xsum / count, ysum / count]

        def compute_radius(mask, threshold=125):
            area = 0
            for xy, value in np.ndenumerate(mask):
                if value > threshold:
                    area = area + 1
            return math.sqrt(float(area) / math.pi)

        if os.listdir(self.project.directories['lights']) == [] or os.listdir(self.project.directories['lights']) == ['lights.csv']:
            print('No images to process')
            return


        self._read_images()

        cx, cy = compute_centroid(self.content['mask'])
        r = compute_radius(self.content['mask'])

        light_vector = []
        for image in self.content['images']:
            px, py = compute_centroid(image)

            ny = -(px - cx)
            nx = py - cy
            nz = math.sqrt(r ** 2 - nx ** 2 - ny ** 2)

            N = np.array([nx / r, ny / r, nz / r])
            R = np.array([0, 0, 1])

            L = 2 * (np.dot(N, R) * N) - R

            light_vector.append(L)

        self.content['lights'] = light_vector

    def _read_images(self):
        """
        Returning np.array of images and mask using cv2.imread()

        images are always provided as GRAYSCALE

        mask image as GRAYSCALE

        :param self:
        :return: [mask_image, bgr_images, grayscale_images]
        """

        reader = ImageReader()

        _path = self.project.directories['lights']

        extension = '.png'
        images_dict = reader.read(_path, extension)
        images = []

        _mask_readed = False
        for name in images_dict:
            name_list = name.split(".")

            if len(name_list) != 3:
                print("Image with invalid format: ", name)
                return

            if str(name_list[1]) == 'mask':
                if not _mask_readed:
                    self.content['mask'] = images_dict[name]
                    _mask_readed = True
                else:
                    print("Only one mask allowed")
                    return
            else:
                try:
                    number = int(name_list[1])
                except ValueError as e:
                    print(name, ' Not a integer')
                    return

                if 0 <= int(name_list[1]) <= 99:
                    images.append(images_dict[name])

        self.content['images'] = images[:]
        self.state['data'] = True

    def _read_lights(self, path = None):
        # TODO: Abstraction e.g. LightReader
        '''
            Reading header file with specify format and returning
            number of images, path to images and mask.

            Format of header file:

            n
            img.0.png
            img.1.png
            ...
            img.n.png
            img.mask.png

            Where:
            n - number of files
            img - name of photographed object


            :param self
            :return: {images, mask, count}:


        '''
        if path is None:
            path = str(self.project.directories['lights']) + '/lights.csv'

        path = Path(path)

        if str(path)[-4:] != '.csv':
            print('Not a .csv file')
            return

        try:
            csv_file = open(path)
        except FileNotFoundError as e:
            print("File Not Found")

        lights = []

        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            count = 0
            for row in csv_reader:
                count += 1
                try:
                    lights.append([float(row[0]), float(row[1]), float(row[2])])
                except ValueError as e:
                    print('Data in file is not float. First invalid data in row:{}'.format(count))
                    return
                except IndexError as e:
                    print('Less than 3 cols in row:{}'.format(count))
                    return


        if count >= 3:
            self.content['lights'] = lights
            self.state['data'] = True

        else:
            print('Minimum 3 lights required')
            return

