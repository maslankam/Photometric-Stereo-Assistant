from Include.project.segment import Segment


class Albedo(Segment): # TODO: ALBEDO
    """Albedo segment reponsible for albedo map procesing"""

    _content = None

    def __init__(self, project):
        # TODO: if albedo.png exists in project load it if not inform that user need to compute
        pass

    def __str__(self):
        pass

    def import_from(self):
        # Don't import albedo map
        pass

    def save(self):
        pass

    def show(self):
        """Returning image representation of albedo map"""
        pass

    def compute(self):
        """Compute albedo using images saved in project/Images """
        pass

