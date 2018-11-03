
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.geometry import BlenderGeometry


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'BlenderPoint',
]


class BlenderPoint(BlenderGeometry):

    def __init__(self, guid):
        super(BlenderPoint, self).__init__()


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    @property
    def xyz(self):

        raise NotImplementedError


    def closest_point(self, point, maxdist=None):

        raise NotImplementedError


    def closest_points(self, points, maxdist=None):

        raise NotImplementedError


    def project_to_curve(self, curve, direction=(0, 0, 1)):

        raise NotImplementedError


    def project_to_surface(self, surface, direction=(0, 0, 1)):

        raise NotImplementedError


    def project_to_mesh(self, mesh, direction=(0, 0, 1)):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
