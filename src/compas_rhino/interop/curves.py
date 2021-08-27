from compas.geometry import Line
from compas.geometry import NurbsCurve

from .exceptions import COMPASRhinoInteropError

from .primitives import compas_line_to_rhino_line
from .primitives import compas_circle_to_rhino_circle
from .primitives import compas_ellipse_to_rhino_ellipse
from .primitives import rhino_point_to_compas_point
from .primitives import rhino_circle_to_compas_circle
from .primitives import rhino_ellipse_to_compas_ellipse
from .primitives import rhino_polyline_to_compas_polyline

from Rhino.Geometry import NurbsCurve as RhinoNurbsCurve


def rhino_curve_to_compas_line(curve):
    """Convert a Rhino curve to a COMPAS line.

    Parameters
    ----------
    curve: :class:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Line`
    """
    return Line(rhino_point_to_compas_point(curve.PointAtStart),
                rhino_point_to_compas_point(curve.PointAtEnd))


def compas_line_to_rhino_curve(line):
    """Convert a COMPAS line to a Rhino curve.

    Parameters
    ----------
    line: :class:`compas.geometry.Line`

    Returns
    -------
    :class:`Rhino.Geometry.Curve`
    """
    return NurbsCurve.CreateFromLine(compas_line_to_rhino_line(line))


def rhino_curve_to_compas_circle(curve):
    """Convert a Rhino curve to a COMPAS circle.

    Parameters
    ----------
    curve: :class:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Circle`

    Raises
    ------
    COMPASRhinoInteropError
        If the curve cannot be converted to a circle.
    """
    result, circle = curve.TryGetCircle()
    if not result:
        raise COMPASRhinoInteropError('The curve cannot be converted to a circle.')
    return rhino_circle_to_compas_circle(circle)


def compas_circle_to_rhino_curve(circle):
    """Convert a COMPAS circle to a Rhino curve.

    Parameters
    ----------
    circle: :class:`compas.geometry.Circle`

    Returns
    -------
    :class:`Rhino.Geometry.Curve`
    """
    return NurbsCurve.CreateFromCircle(compas_circle_to_rhino_circle(circle))


def rhino_curve_to_compas_ellipse(curve):
    """Convert a Rhino curve to a COMPAS ellipse.

    Parameters
    ----------
    curve: :class:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Ellipse`

    Raises
    ------
    COMPASRhinoInteropError
        If the curve cannot be converted to an ellipse.
    """
    result, ellipse = curve.TryGetEllipse()
    if not result:
        raise COMPASRhinoInteropError('The curve cannot be converted to an ellipse.')
    return rhino_ellipse_to_compas_ellipse(ellipse)


def compas_ellipse_to_rhino_curve(ellipse):
    """Convert a COMPAS ellipse to a Rhino curve.

    Parameters
    ----------
    ellipse: :class:`compas.geometry.Ellipse`

    Returns
    -------
    :class:`Rhino.Geometry.Curve`
    """
    return NurbsCurve.CreateFromEllipse(compas_ellipse_to_rhino_ellipse(ellipse))


def rhino_curve_to_compas_polyline(curve):
    """Convert a Rhino curve to a COMPAS polyline.

    Parameters
    ----------
    curve: :class:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.Polyline`

    Raises
    ------
    COMPASRhinoInteropError
        If the curve cannot be converted to a polyline.
    """
    result, polyline = curve.TryGetPolyline()
    if not result:
        raise COMPASRhinoInteropError('The curve cannot be converted to a polyline.')
    return rhino_polyline_to_compas_polyline(polyline)


def rhino_curve_to_compas_curve(curve):
    """Convert a Rhino curve to a COMPAS curve.

    Parameters
    ----------
    curve: :class:`Rhino.Geometry.Curve`

    Returns
    -------
    :class:`compas.geometry.NurbsCurve`
    """
    curve = curve.ToNurbsCurve()
    points = []
    weights = []
    knots = []
    multiplicities = []
    degree = curve.Degree
    is_periodic = curve.IsPeriodic

    for index in range(curve.Points.Count):
        point = curve.Points.Item[index]
        points.append(rhino_point_to_compas_point(point.Location))
        weights.append(point.Weight)

    for index in range(curve.Knots.Count):
        knots.append(curve.Knots.Item[index])
        multiplicities.append(curve.Knots.KnotMultiplicity(index))

    return NurbsCurve.from_parameters(points, weights, knots, multiplicities, degree, is_periodic)


def compas_curve_to_rhino_curve(curve):
    """Convert a COMPAS curve to a Rhino curve.

    Parameters
    ----------
    curve: :class:`compas.geometry.NurbsCurve`

    Returns
    -------
    :class:`Rhino.Geometry.NurbsCurve`
    """
    rhinocurve = RhinoNurbsCurve(3, curve.is_rational, curve.order, len(curve.points))
    for index, point in enumerate(curve.points):
        rhinocurve.Points.SetPoint(index, point.x, point.y, point.z)
    for index, knot in enumerate(curve.knots):
        rhinocurve.Knots.Item[index] = knot
    return rhinocurve
