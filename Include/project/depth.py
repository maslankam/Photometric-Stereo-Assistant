from Include.project.segment import Segment
import numpy as np
import scipy, cv2, csv
import scipy.sparse.linalg
from pathlib import Path
import numpy.linalg
import os


class Depth(Segment):
    """Height segment reponsible for Height map processing"""

    _content = None

    def __init__(self, project):
        self.content = {'mask': None, 'images': None, 'depth': None}
        self.project = project
        self.state = {'data': False, 'save': False}

        if 'depth.csv' in os.listdir(project.directories['results']):
            self.state['save'] = True
            self._read_depth() # TODO

    def __str__(self):
        return 'Depth map:'

    def import_from(self):
        pass

    def save(self):
        if self.content['depth'] is None:
            print("Nothing to save")
            return

        if 'depth.csv' in os.listdir(self.project.directories['results']):
            os.remove(str(self.project.directories['results']) + '/depth.csv')

        _path = Path(str(self.project.directories['results']) + '/depth.csv')

        _file = open(_path, mode='a', newline='')

        with _file:
            _writer = csv.writer(_file, delimiter=',')

            depth = self.content['depth']
            for line in depth:
                points_list = []
                for point in line:
                    points_list.append(point)
                _writer.writerow(points_list)
        self.state['save'] = True

    def show(self):
        if self.content['depth'] is None:
            print('Nothing to show')
            return

        cv2.imshow('depth', self.content['depth'])
        cv2.waitKey()

    def compute(self, threshold = 100):
        mask_array = self.project.segments['normal'].content['mask']
        normal_array = self.project.segments['normal'].content['normals']

        depth_map = -np.ones(mask_array.shape)

        x = []
        y = []
        index = 0
        for (xy, value) in np.ndenumerate(mask_array):
            if value > threshold:
                depth_map[xy] = index
                x.append(xy[1])
                y.append(-xy[0])
                index = index + 1

        row = []
        col = []
        data = []
        b = []

        i = 0
        for xy, value in np.ndenumerate(depth_map):
            if value >= 0:
                normal = normal_array[xy]
                normal = normal * 125

                if not np.isnan(np.sum(normal)):

                    iother = depth_map[xy[0], xy[1] + 1]
                    if abs(normal[2]) > 0.01:
                        if iother >= 0:
                            row.append(i)
                            col.append(value)
                            data.append(-normal[2])
                            row.append(i)
                            col.append(iother)
                            data.append(normal[2])
                            b.append(-normal[0])
                            i = i + 1

                        iother = depth_map[xy[0] - 1, xy[1]]
                        if iother >= 0:
                            row.append(i)
                            col.append(value)
                            data.append(normal[2])
                            row.append(i)
                            col.append(iother)
                            data.append(normal[2])
                            b.append(-normal[1])
                            i = i + 1

        mat = scipy.sparse.coo_matrix((data, (row, col)), (i, index)).tocsc()
        b = np.array(b)

        z = scipy.sparse.linalg.lsqr(mat, b, iter_lim=1000, show=False)

        index = 0
        for (xy, value) in np.ndenumerate(depth_map):
            if value >= 0:
                depth_map[xy] = z[0][index]
                index = index + 1

        min = depth_map.min()
        max = depth_map.max()
        sigma = np.std(depth_map)
        mean = np.mean(depth_map)

        thresh_min = mean - 5 * sigma
        thresh_max = mean + 5 * sigma

        print('min', min)
        print('max', max)
        print('sigma', sigma)
        print('mean', mean)
        print('thresh_min', thresh_min)
        print('thresh_max', thresh_max)

        sigma_map = depth_map

        for xy, value in np.ndenumerate(depth_map):
            if value == -1.0:
                sigma_map[xy] = -1.0
            elif thresh_min > value:
                sigma_map[xy] = thresh_min
            elif thresh_min < value  < thresh_max:
                pass
            else:
                sigma_map[xy] = thresh_max

        sigma_map_min = sigma_map.min()
        sigma_map_max = sigma_map.max()
        sigma_map_sigma = np.std(sigma_map)
        sigma_map_mean = np.mean(sigma_map)

        result = sigma_map

        #Norm
        for xy, value in np.ndenumerate(sigma_map):
            result[xy] = (value - sigma_map_mean) / sigma_map_sigma

        result_max = result.max()
        result = result / result_max

        print('sigma_map_min', sigma_map_min)
        print('sigma_mapmax', sigma_map_max)
        print('sigma_mapsigma', sigma_map_sigma)
        print('sigma_mapmean', sigma_map_mean)

        min = result.min()
        max = result.max()
        sigma = np.std(result)
        mean = np.mean(result)

        print('min', min)
        print('max', max)
        print('sigma', sigma)
        print('mean', mean)

        kernel = np.ones((3, 3), np.float32) / 25
        result = cv2.filter2D(result, -1, kernel)

        self.content['depth'] = result
        self.state['data'] = True

    def _read_depth(self):
        path = Path(str(self.project.directories['results']) + '/depth.csv')

        try:
            csv_file = open(path)
        except FileNotFoundError as e:
            print("File Not Found")

        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            depth = []

            for line in csv_reader:
                # print('line', line)
                value_list = []
                for value in line:
                    value_list.append(float(value))
                depth.append(value_list)

            depth = np.array(depth)
            csv_file.close()

        self.content['depth'] = depth
        self.state['data'] = True