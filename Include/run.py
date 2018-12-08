'''Photometric Stereo Assistant v.0.1.0 by Mikołaj Maślanka 06-12-2018 MIT '''

import argparse
import sys
from Include.core import Core


# TODO: KNOWN BUGS
# ??
# ?? Not tested on LINUX

# TODO: PLANNED FEATURES:
# GUI
# camera acquisition, callibration
# more abstractions
# more tests
# executable for WIN and LINUX
#


class Run:
    """Initializing the Program"""
    def initialize(self):
        print("Initializing...")
        core = Core()
        print("Welcome in Photometric Stereo Assistant, type help to learn more")
        core.go()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    if len(sys.argv) == 1:  # Interactive mode
        run = Run()
        run.initialize()
    else:
        print("Not implemented yet")  # TODO: batch mode