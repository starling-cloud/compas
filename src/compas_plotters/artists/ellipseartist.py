from typing import Tuple
from typing import List
from typing import Any
from typing_extensions import Literal

from matplotlib.patches import Ellipse as EllipsePatch
from compas.geometry import Ellipse

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class EllipseArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS ellipses."""

    def __init__(self,
                 ellipse: Ellipse,
                 linewidth: float = 1.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 facecolor: Color = (1.0, 1.0, 1.0),
                 edgecolor: Color = (0, 0, 0),
                 fill: bool = True,
                 alpha: float = 1.0,
                 zorder: int = 1000,
                 **kwargs: Any):

        super().__init__(primitive=ellipse, **kwargs)

        self._mpl_ellipse = None
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha
        self.zorder = zorder

    @property
    def ellipse(self):
        return self.primitive

    @ellipse.setter
    def ellipse(self, ellipse):
        self.primitive = ellipse

    @property
    def data(self) -> List[List[float]]:
        points = [
            self.ellipse.center[:2],
            self.ellipse.center[:2],
            self.ellipse.center[:2],
            self.ellipse.center[:2]
        ]
        points[0][0] -= self.ellipse.major
        points[1][0] += self.ellipse.major
        points[2][1] -= self.ellipse.minor
        points[3][1] += self.ellipse.minor
        return points

    def draw(self) -> None:
        ellipse = EllipsePatch(
            self.ellipse.center[:2],
            width=2*self.ellipse.major,
            height=2*self.ellipse.minor,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            alpha=self.alpha,
            zorder=self.zorder)
        self._mpl_ellipse = self.plotter.axes.add_artist(ellipse)

    def redraw(self) -> None:
        self._mpl_ellipse.center = self.ellipse.center[:2]
        self._mpl_ellipse.set_width(2*self.ellipse.major)
        self._mpl_ellipse.set_height(2*self.ellipse.minor)
        self._mpl_ellipse.set_edgecolor(self.edgecolor)
        self._mpl_ellipse.set_facecolor(self.facecolor)
