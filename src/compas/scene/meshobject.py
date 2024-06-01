from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
from compas.geometry import transform_points

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


class MeshObject(SceneObject):
    """Base class for all mesh scene objects.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh data structure.
    vertex_xyz : dict[int, list[float]]
        View coordinates of the vertices.
        Defaults to the real coordinates.
    color : :class:`compas.colors.Color`
        The base RGB color of the mesh.
    vertexcolor : :class:`compas.colors.ColorDict`
        Vertex colors.
    edgecolor : :class:`compas.colors.ColorDict`
        Edge colors.
    facecolor : :class:`compas.colors.ColorDict`
        Face colors.
    vertexsize : float
        The size of the vertices. Default is ``1.0``.
    edgewidth : float
        The width of the edges. Default is ``1.0``.
    show_vertices : Union[bool, sequence[float]]
        Flag for showing or hiding the vertices, or a list of keys for the vertices to show.
        Default is ``False``.
    show_edges : Union[bool, sequence[tuple[int, int]]]
        Flag for showing or hiding the edges, or a list of keys for the edges to show.
        Default is ``True``.
    show_faces : Union[bool, sequence[int]]
        Flag for showing or hiding the faces, or a list of keys for the faces to show.
        Default is ``True``.

    See Also
    --------
    :class:`compas.scene.GraphObject`
    :class:`compas.scene.VolMeshObject`

    """

    vertexcolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    facecolor = ColorDictAttribute()

    def __init__(self, mesh, **kwargs):
        # type: (compas.datastructures.Mesh, dict) -> None
        super(MeshObject, self).__init__(item=mesh, **kwargs)
        self._mesh = None
        self._vertex_xyz = None
        self.mesh = mesh
        self.vertexcolor = kwargs.get("vertexcolor", self.contrastcolor)
        self.edgecolor = kwargs.get("edgecolor", self.contrastcolor)
        self.facecolor = kwargs.get("facecolor", self.color)
        self.vertexsize = kwargs.get("vertexsize", 1.0)
        self.edgewidth = kwargs.get("edgewidth", 1.0)
        self.show_vertices = kwargs.get("show_vertices", False)
        self.show_edges = kwargs.get("show_edges", False)
        self.show_faces = kwargs.get("show_faces", True)

    @property
    def settings(self):
        # type: () -> dict
        settings = super(MeshObject, self).settings
        # perhaps this should be renamed to just "vertices", "edges", "faces"
        settings["show_vertices"] = self.show_vertices
        settings["show_edges"] = self.show_edges
        settings["show_faces"] = self.show_faces
        # end of perhaps
        settings["vertexcolor"] = self.vertexcolor
        settings["edgecolor"] = self.edgecolor
        settings["facecolor"] = self.facecolor
        return settings

    @property
    def mesh(self):
        # type: () -> compas.datastructures.Mesh
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        # type: (compas.datastructures.Mesh) -> None
        self._mesh = mesh
        self._transformation = None
        self._vertex_xyz = None

    @property
    def transformation(self):
        # type: () -> compas.geometry.Transformation | None
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        # type: (compas.geometry.Transformation) -> None
        self._vertex_xyz = None
        self._transformation = transformation

    @property
    def vertex_xyz(self):
        # type: () -> dict[int, list[float]]
        if self._vertex_xyz is None:
            points = self.mesh.vertices_attributes("xyz")  # type: ignore
            points = transform_points(points, self.worldtransformation)
            self._vertex_xyz = dict(zip(self.mesh.vertices(), points))  # type: ignore
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        # type: (dict[int, list[float]]) -> None
        self._vertex_xyz = vertex_xyz

    def draw_vertices(self):
        """Draw the vertices of the mesh.

        Vertices are drawn based on the values of

        * `self.show_vertices`
        * `self.vertexcolor`
        * `self.vertextext`
        * `self.vertexsize`

        Returns
        -------
        list
            The identifiers of the objects representing the vertices in the visualization context.

        """
        raise NotImplementedError

    def draw_edges(self):
        """Draw the edges of the mesh.

        Edges are drawn based on the values of

        * `self.show_edges`
        * `self.edgecolor`
        * `self.edgetext`
        * `self.edgewidth`

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    def draw_faces(self):
        """Draw the faces of the mesh.

        Faces are drawn based on the values of

        * `self.show_faces`
        * `self.facecolor`
        * `self.facetext`

        Returns
        -------
        list
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    def draw_mesh(self, *args, **kwargs):
        """Draw the mesh of the mesh.

        .. deprecated:: 1.14.1
            Use :meth:`~MeshObject.draw` instead.

        Returns
        -------
        list
            The identifiers of the objects representing the mesh in the visualization context.

        """
        return self.draw(*args, **kwargs)

    def draw(self):
        """draw the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        """Clear all components of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_vertices(self):
        """Clear the vertices of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_edges(self):
        """Clear the edges of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_faces(self):
        """Clear the faces of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError
