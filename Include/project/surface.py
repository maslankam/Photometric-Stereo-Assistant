from Include.project.segment import Segment
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
import cv2
import scipy.signal
import math

class Surface(Segment):
    """Surface segment reponsible for surface procesing"""

    _content = None

    def __init__(self, project):
        self.project = project


    def import_from(self):
        pass

    def save(self):
        pass

    def show(self):
        pass

    def compute(self):
        pass

    def show(self):

        if self.project.segments['depth'].content['depth'] is None:
            print('Nothing to show')
            return

        depth = self.project.segments['depth'].content['depth']

        x = []
        y = []
        z = []

        for xy, value in np.ndenumerate(depth):

            if value > 0:
                x.append(xy[0])
                y.append(xy[1])
                z.append(value)

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        fig = plt.figure()
        ax = fig.gca(projection='3d')


        x = scipy.signal.decimate(x, 10)
        y = scipy.signal.decimate(y, 10)
        z = scipy.signal.decimate(z, 10)

        print('x', x.shape)
        print('y', y.shape)
        print('z', z.shape)

        ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True, cmap=plt.cm.CMRmap)
        ax.set_xlim(0, depth.shape[0])
        ax.set_ylim(0, depth.shape[1])
        ax.set_zlim(-0.2, 0.8)
        plt.show()


