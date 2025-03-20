import math
import re
from dataclasses import dataclass
from enum import Enum
from typing import List

from qgis.core import QgsGeometry, QgsMultiPoint, QgsPoint, QgsPointXY

from .typo import TYPES_PAVAGES, Typo


class Movement(Enum):
    MOVE_ALL = "MOVE_ALL"
    STRECH_X = "STRECH_X"
    STRECH_Y = "STRECH_Y"
    ROTATION = "ROTATION"


@dataclass
class Node:
    x: float
    y: float

    def copy(self):
        return Node(self.x, self.y)

    def xy(self):
        return (self.x, self.y)

    def pointXY(self):
        return QgsPointXY(self.x, self.y)

    def setXY(self, x, y):
        self.x, self.y = x, y

    def translate(self, n1, n2):
        self.x = self.x + n2.x - n1.x
        self.y = self.y + n2.y - n1.y

    def distance(self, n):
        return self.pointXY().distance(n.pointXY())

    def project(self, d, a):
        return Node.fromPointXY(self.pointXY().project(d, a))

    def azimuth(self, p):
        return self.pointXY().azimuth(p.pointXY())

    def distanceToLine(self, p1, p2):
        """
        Calculate the distance between the point and a line defined by two points (x1, y1) and (x2, y2).
        """
        # Calculate the length of the segment
        segment_length = math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

        if segment_length == 0:
            # The segment is actually a point
            return math.sqrt((self.x - p1.x) ** 2 + (self.y - p1.y) ** 2)

        # Project point onto the line, finding the projection factor t
        t = (
            (self.x - p1.x) * (p2.x - p1.x) + (self.y - p1.y) * (p2.y - p1.y)
        ) / segment_length**2

        # Find the projection point on the line
        proj_x = p1.x + t * (p2.x - p1.x)
        proj_y = p1.y + t * (p2.y - p1.y)

        # Calculate the distance from the point to the projection point
        distance = math.sqrt((self.x - proj_x) ** 2 + (self.y - proj_y) ** 2)

        return distance

    def pointSideOfSegment(self, a, b):
        """
        Détermine de quel côté du segment de droite AB se situe le point P.

        :param p: Tuple (x, y) représentant les coordonnées du point P.
        :param a: Tuple (x, y) représentant les coordonnées du point A (début du segment).
        :param b: Tuple (x, y) représentant les coordonnées du point B (fin du segment).
        :return: Un nombre positif si P est à gauche du segment AB, négatif si P est à droite, et 0 si P est sur le segment.
        """
        # Calcul du produit vectoriel
        x = (b.x - a.x) * (self.y - a.y) - (b.y - a.y) * (self.x - a.x)
        return -1 if x > 0 else 1 if x < 0 else 0

    @staticmethod
    def axialSymmetry(p, p1, p2):
        """
        Calcule l'image d'un point selon une symétrie axiale définie par deux points.

        :param point: tuple (x, y) représentant le point à transformer
        :param p1: tuple (x1, y1) représentant le premier point définissant l'axe de symétrie
        :param p2: tuple (x2, y2) représentant le deuxième point définissant l'axe de symétrie
        :return: tuple (x', y') représentant l'image du point par symétrie axiale
        """
        if isinstance(p, QgsPointXY) or isinstance(p, QgsPoint):
            p = Node(p.x(), p.y())

        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        # Calcul de l'équation de la droite axiale
        if x1 == x2:  # Cas particulier : droite verticale
            x_sym = 2 * x1 - p.x
            y_sym = p.y
        elif y1 == y2:  # Cas particulier : droite horizontale
            x_sym = p.x
            y_sym = 2 * y1 - p.y
        else:
            # Calcul de la pente et de l'ordonnée à l'origine de la droite
            pente = (y2 - y1) / (x2 - x1)
            intercept = y1 - pente * x1

            # Calcul de la projection du point sur la droite
            d = (p.x + (p.y - intercept) * pente) / (1 + pente**2)
            x_proj = 2 * d - p.x
            y_proj = 2 * d * pente - p.y + 2 * intercept

            x_sym = x_proj
            y_sym = y_proj

        return Node(x_sym, y_sym)

    def perpendicularProjection(self, p1, p2):
        """
        Projette un point sur un segment perpendiculairement.

        :param p1: tuple (x1, y1) représentant le point de départ du segment
        :param p2: tuple (x2, y2) représentant le point de fin du segment
        :return: Node représentant le point projeté sur le segment
        """
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        # Calcul du vecteur directeur du segment
        dx, dy = x2 - x1, y2 - y1

        # Calcul du vecteur du point au début du segment
        dpx, dpy = self.x - x1, self.y - y1

        # Calcul de la projection scalaire
        t = (dpx * dx + dpy * dy) / (dx * dx + dy * dy)

        # Calcul des coordonnées du point projeté
        x_proj = x1 + t * dx
        y_proj = y1 + t * dy

        return Node(x_proj, y_proj)

    @staticmethod
    def middle(n1, n2):
        return Node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2)

    @staticmethod
    def fromPointXY(p):
        return Node(p.x(), p.y())


def decomposeTransform(text: str):
    regpattern = r"(([\-0-9]*)[x]{0,1})([ABFMRTZ]{1}[hv]{0,1}[0-9]*)\(([^)]+)\)"
    match = re.match(regpattern, text)

    if match:
        # Extract the components
        fact = match.group(2)
        try:
            if fact == "-":
                fact = -1
            else:
                fact = int(fact)
        except Exception:
            fact = 1

        letter = match.group(3)
        variables = match.group(4).split(",")
        return fact, letter, variables
    else:
        # print(text, "non reconnu")
        return None


class Transformation:
    def __init__(self):
        pass

    def getValueRotation(self):
        return 0

    def getValueFlip(self):
        return 1

    @staticmethod
    def rot(c, p, alpha):
        # Convertir l'angle en radians

        if isinstance(p, Node):
            g = QgsGeometry.fromPointXY(p.pointXY())
        if isinstance(p, QgsPointXY):
            g = QgsGeometry.fromPointXY(p)
        if isinstance(p, QgsPoint):
            g = QgsGeometry.fromPoint(p)

        g.rotate(alpha, c.pointXY())

        return (g.asPoint().x(), g.asPoint().y())

    @staticmethod
    def copyNode(n):
        if isinstance(n, Node):
            return Node(n.x, n.y)
        if isinstance(n, QgsPointXY):
            return QgsPointXY(n.x(), n.y())
        if isinstance(n, QgsPoint):
            return QgsPoint(n.x(), n.y())
        return None

    @staticmethod
    def copyOrNot(p, pp, copy=False):
        if isinstance(p, Node):
            if copy:
                return Node(pp.x, pp.y)

            p.x = pp.x
            p.y = pp.y
            return p

        if isinstance(p, QgsPointXY):
            if copy:
                return QgsPointXY(pp.x, pp.y)

            p.setX(pp.x)
            p.setY(pp.y)
            return p

        if isinstance(p, QgsPoint):
            if copy:
                return QgsPoint(pp.x, pp.y)

            p.setX(pp.x)
            p.setY(pp.y)
            return p

        return None

    @staticmethod
    def copySeg(seg):
        return [Transformation.copyNode(n) for n in seg]

    @staticmethod
    def copySegs(segs):
        return [Transformation.copySeg(s) for s in segs]

    @staticmethod
    def copyGeom(geom):
        return QgsGeometry(geom)

    @staticmethod
    def copyGeoms(geoms):
        return [QgsGeometry(g) for g in geoms]

    def transformNode(self, p, copy=False):
        if copy:
            p = Transformation.copyNode(p)

        return p

    def transformGeom(self, g, copy=False):
        if copy:
            g = Transformation.copyGeom(g)

        for nid, v in enumerate(g.vertices()):
            v = self.transformNode(QgsPointXY(v))
            g.moveVertex(v.x(), v.y(), nid)

        return g

    def transformGeoms(self, geoms, copy=False):
        return [self.transformGeom(g, copy) for g in geoms]

    def transformSeg(self, seg, copy=False, extremites=True):
        if not extremites and copy:
            newSeg = (
                [seg[0].copy()]
                + [self.transformNode(p, copy) for p in seg[1:-1]]
                + [seg[-1].copy()]
            )
        elif not extremites and not copy:
            newSeg = (
                [seg[0]] + [self.transformNode(p, copy) for p in seg[1:-1]] + [seg[-1]]
            )
        else:
            newSeg = [self.transformNode(p, copy) for p in seg]

        return newSeg

    def transformSegs(self, segs, copy=False, extremites=True):
        if isinstance(segs, dict):
            return {k: self.transformSeg(s, copy, extremites) for k, s in segs.items()}
        else:
            return [self.transformSeg(s, copy, extremites) for s in segs]


class Attach(Transformation):
    def __init__(self, p0=None):
        self.p0 = p0
        self.dx = None
        self.dy = None

    def __str__(self):
        return "Attach"

    def transformNode(self, p, copy=False):
        if copy:
            p = Transformation.copyNode(p)

        if isinstance(p, Node):
            if self.dx is None:
                self.dx = self.p0.x - p.x
                self.dy = self.p0.y - p.y
            p.x = p.x + self.dx
            p.y = p.y + self.dy
            return p

        if isinstance(p, QgsPointXY) or isinstance(p, QgsPoint):
            if self.dx is None:
                self.dx = self.p0.x - p.x()
                self.dy = self.p0.y - p.y()
            p.setX(p.x() + self.dx)
            p.setY(p.y() + self.dy)
            return p

        return None

    def transformSeg(self, seg, copy=False, extremites=True):
        self.dx = self.p0.x - seg[0].x
        self.dy = self.p0.y - seg[0].y
        return super().transformSeg(seg, copy, extremites)


class Middle(Transformation):
    def __init__(self, p0, p1):
        self.p = Node.middle(p0, p1)

    def __str__(self):
        return "Middle"

    def transformNode(self, p, copy=False):
        if copy:
            p = Transformation.copyNode(p)

        if isinstance(p, Node):
            p.x = self.p.x
            p.y = self.p.y
            return p

        if isinstance(p, QgsPointXY) or isinstance(p, QgsPoint):
            p.setX(self.p.x)
            p.setY(self.p.y)
            return p

        return None


class Translation(Transformation):
    def __init__(self, p0=None, p1=None, dx=None, dy=None):
        if p0 is not None:
            self.p0 = p0
            self.p1 = p1
        if dx is not None:
            self.p0 = None
            self.p1 = None
            self.dx = dx
            self.dy = dy

    def __str__(self):
        return "Translation"

    def getValueRotation(self):
        return 0

    def getValueFlip(self):
        return 1

    def transformNode(self, p, copy=False):
        if copy:
            p = Transformation.copyNode(p)

        if self.p0 is not None:
            self.dx = self.p1.x - self.p0.x
            self.dy = self.p1.y - self.p0.y

        if isinstance(p, Node):
            p.x = p.x + self.dx
            p.y = p.y + self.dy
            return p

        if isinstance(p, QgsPointXY) or isinstance(p, QgsPoint):
            p.setX(p.x() + self.dx)
            p.setY(p.y() + self.dy)
            return p

        return None

    def transformGeom(self, g, copy=False):
        if copy:
            g = Transformation.copyGeom(g)

        if self.p0 is not None:
            self.dx = self.p1.x - self.p0.x
            self.dy = self.p1.y - self.p0.y

        g.translate(self.dx, self.dy)

        return g

    def __add__(self, o):
        if self.p0 is not None:
            self.dx = self.p1.x - self.p0.x
            self.dy = self.p1.y - self.p0.y
        return Translation(dx=self.dx + o.dx, dy=self.dy + o.dy)

    def __sub__(self, o):
        if self.p0 is not None:
            self.dx = self.p1.x - self.p0.x
            self.dy = self.p1.y - self.p0.y
        return Translation(dx=self.dx - o.dx, dy=self.dy - o.dy)

    def __neg__(self):
        if self.p0 is not None:
            self.dx = self.p1.x - self.p0.x
            self.dy = self.p1.y - self.p0.y
        return Translation(dx=-self.dx, dy=-self.dy)

    def __mul__(self, o):
        if self.p0 is not None:
            self.dx = self.p1.x - self.p0.x
            self.dy = self.p1.y - self.p0.y
        return Translation(dx=self.dx * o, dy=self.dy * o)


class Stretch(Transformation):

    def __init__(self, xy, f, p0, p1, p2):
        """Projeter des points selon la direction p0-p1, à la distance au segment p0-p2 * f

        Args:
            p0 (_type_): _description_
            p1 (_type_): _description_
            p2 (_type_): _description_
            f (_type_): _description_
        """
        self.xy = xy
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.f = f

    def __str__(self):
        return f"Stretch({self.f})"

    def getValueRotation(self):
        return 0

    def getValueFlip(self):
        return 1

    def transformNode(self, p, copy=False):
        if not isinstance(p, Node):
            newP = Node(p.x(), p.y())
        else:
            newP = Transformation.copyNode(p)

        a = self.p0.azimuth(self.p1)
        d = newP.distanceToLine(self.p0, self.p2)
        d = (
            ((self.f * d) - d)
            * newP.pointSideOfSegment(self.p0, self.p2)
            * (1 if self.xy == "x" else -1)
        )
        pp = newP.project(d, a)

        return Transformation.copyOrNot(p, pp, copy)


class Shear(Transformation):

    def __init__(self, d, p0, p1, p2):
        """Cisaillement

        Args:
            p0 (_type_): _description_
            p1 (_type_): _description_
            p2 (_type_): _description_
            f (_type_): _description_
        """
        self.d = d
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.h = self.p0.distance(self.p2)

    def __str__(self):
        return "Shear"

    def getValueRotation(self):
        return 0

    def getValueFlip(self):
        return 1

    def transformNode(self, p, copy=False):
        if not isinstance(p, Node):
            newP = Node(p.x(), p.y())
        else:
            newP = Transformation.copyNode(p)

        dd = (
            self.d
            * newP.distanceToLine(self.p0, self.p1)
            / self.h
            * (-newP.pointSideOfSegment(self.p0, self.p1))
        )

        a = self.p0.azimuth(self.p1)

        pp = newP.project(dd, a)

        return Transformation.copyOrNot(p, pp, copy)


class Rotation(Transformation):
    def __init__(self, angle, c, c2=None):
        if c2 is None:
            self.cxy = c.pointXY()
        else:
            self.cxy = Node.middle(c, c2).pointXY()
        self.angle = angle

    def __str__(self):
        return f"Rotation({self.angle})"

    def getValueRotation(self):
        return self.angle

    def getValueFlip(self):
        return 1

    def transformNode(self, p, copy=False):
        if copy:
            p = Transformation.copyNode(p)

        if isinstance(p, Node):
            g = QgsGeometry.fromPointXY(p.pointXY())
        if isinstance(p, QgsPointXY):
            g = QgsGeometry.fromPointXY(p)
        if isinstance(p, QgsPoint):
            g = QgsGeometry.fromPoint(p)

        g.rotate(self.angle, self.cxy)

        if isinstance(p, Node):
            p.x, p.y = g.asPoint().x(), g.asPoint().y()

        if isinstance(p, QgsPointXY) or isinstance(p, QgsPoint):
            p.setX(g.asPoint().x())
            p.setY(g.asPoint().y())

        return p


class Flip(Transformation):

    def __init__(self, d1: Node, d2: Node, c: Node, az=0):
        dd1 = d1.copy()
        dd1.translate(d1, c)
        dd2 = d2.copy()
        dd2.translate(d1, c)
        self.d1 = dd1
        self.d2 = dd2
        self.az = az

    def __str__(self):
        return "Flip"

    def getValueRotation(self):
        return self.az % 360

    def getValueFlip(self):
        return -1

    def transformNode(self, p, copy=False):
        if copy:
            p = Transformation.copyNode(p)

        s = Node.axialSymmetry(p, self.d1, self.d2)
        if isinstance(p, Node):
            p.x = s.x
            p.y = s.y
            return p

        if isinstance(p, QgsPointXY) or isinstance(p, QgsPoint):
            p.setX(s.x)
            p.setY(s.y)
            return p

        return None


class Pattern:
    typo: Typo
    segs: dict
    p0: Node
    p1: Node
    p2: Node

    def __init__(self, typo, p0, w):
        self.typo = typo
        self.p0 = p0
        self.w = w
        self.typo = dict(TYPES_PAVAGES[typo])

        # origin node
        if "p0" not in self.typo["controls"]:
            self.typo["controls"]["p0"] = {"pos": (0, 0), "mouse": "move_all()"}

        self.controles = {}
        self.segs = {}
        self.sketch = []

        # les points clés positionnés de façon absolue
        fxy = self.typo["fxy"] if "fxy" in self.typo else (1, 1)
        for k, p in self.typo["controls"].items():
            if isinstance(p["pos"], tuple):
                self.controles[k] = Node(
                    p0.x() + w * p["pos"][0] * fxy[0], p0.y() + w * p["pos"][1] * fxy[1]
                )

        # les points clés calculés
        for k, p in self.typo["controls"].items():
            if isinstance(p["pos"], str):
                for t in p["pos"].split(";"):
                    sourceNode, trsf = self.getTransformation2(t)
                    self.controles[k] = trsf.transformNode(sourceNode, copy=True)

        # les segments
        for k, seed in self.typo["seeds"].items():
            # extrémités = points de contrôle
            p1, p2 = self.controles[seed[0]], self.controles[seed[1]]
            self.segs[k] = [p1, p2]

    def getTransformation(self, t: str):
        fact, kt, targs = decomposeTransform(t)
        points = self.getControlPoints(targs)
        if kt == "M":  # milieu du segment
            return Middle(*points)
        if kt == "A":  # accroche au point (translation)
            return Attach(*points)
        if kt == "T":
            return Translation(*points) * fact
        if kt == "R2":
            return Rotation(180 * fact, *points)
        if kt == "R3":
            return Rotation(120 * fact, *points)
        if kt == "R4":
            return Rotation(90 * fact, *points)
        if kt == "R6":
            return Rotation(60 * fact, *points)
        if kt == "F":
            return Flip(*points)
        if kt == "Fv":
            return Flip(*points, az=0)
        if kt == "Fh":
            return Flip(*points, az=180)

        return None

    def getTransformation2(self, t: str):
        fact, kt, targs = decomposeTransform(t)
        points = self.getControlPoints(targs)
        if kt == "M":  # milieu du segment
            return points[0], Middle(*points)
        elif kt == "T":
            return points[0], Translation(*points[1:]) * fact
        elif kt == "R2":
            return points[0], Rotation(180 * fact, *points[1:])
        elif kt == "R3":
            return points[0], Rotation(120 * fact, *points[1:])
        elif kt == "R4":
            return points[0], Rotation(90 * fact, *points[1:])
        elif kt == "R6":
            return points[0], Rotation(60 * fact, *points[1:])
        elif kt == "F":
            return points[0], Flip(*points[1:])
        elif kt == "Fv":
            return points[0], Flip(*points[1:], az=0)
        elif kt == "Fh":
            return points[0], Flip(*points[1:], az=180)
        elif kt == "Z":
            pk = targs[1]
            if pk in self.segs:
                return points[0], Attach(self.segs[targs[1]][-1])
            if pk in self.images:
                return points[0], Attach(self.images[targs[1]][-1])
        elif kt == "B":  # beginning
            pk = targs[1]
            if pk in self.segs:
                return points[0], Attach(self.segs[targs[1]][1])
            if pk in self.images:
                return points[0], Attach(self.images[targs[1]][1])

        return None

    def getImages(self):
        imagesSegs = {}
        for kimg, (imgsrc, imgtransfos) in self.typo["images"].items():
            newseg = None
            if imgsrc in self.segs:
                newseg = Transformation.copySeg(self.segs[imgsrc])
            if imgsrc in imagesSegs:
                newseg = Transformation.copySeg(imagesSegs[imgsrc])

            if newseg is not None:
                for t in imgtransfos.split(";"):
                    trsf = self.getTransformation(t)
                    if t is None:
                        raise Exception(f"invalid transformation {t}")
                    newseg = trsf.transformSeg(newseg, copy=False)
                imagesSegs[kimg] = newseg

        return imagesSegs

    def getTileSegments(self):
        """Retourne une liste des point d'une tuile seule (la tuile de base)

        Returns:
            list(QgsPointXY): liste des points d'une tuile
        """
        imagesSegs = self.getImages()

        # "tile": ["+s1", "+s2", "+s3", "-i1", "-i2", "-i3"],
        segments = []
        for order in self.typo["tile"]:
            regpattern = r"([+-])([a-z0-9]+)"
            match = re.match(regpattern, order)

            if match:
                # Extract the components
                sens = match.group(1)
                kseg = match.group(2)

                if kseg in self.segs:  # original segment
                    segment = self.segs[kseg][:: (-1 if sens == "-" else 1)]
                if kseg in imagesSegs:  # images segment
                    segment = imagesSegs[kseg][:: (-1 if sens == "-" else 1)]

                segments.append(segment)

        return segments

    def getTileLineString(self, segments) -> List[Node]:
        linestring = []
        for seg in segments:
            for n in seg[:-1]:
                linestring.append(n)

        linestring.append(segments[0][0])
        return linestring

    def toMultiPolylineXY(self, segments):
        return [[QgsPointXY(n.x, n.y) for n in seg] for seg in segments]

    def getPatternLinestrings(self):
        patternFromSrc = (
            True
            if "conf" in self.typo and "patternfromsource" in self.typo["conf"]
            else False
        )

        tileSegs = self.getTileSegments()
        line = self.getTileLineString(tileSegs)
        r = [line]

        rotations = [0]
        flips = [1]

        rotation = 0
        flip = 1

        newTile = Transformation.copySeg(line)
        for tileTransforms in self.typo["pattern"].values():
            if patternFromSrc:
                newTile = Transformation.copySeg(line)
                rotation = 0
                flip = 1

            for tileTransform in tileTransforms.split(";"):
                t = self.getTransformation(tileTransform)
                if t is None:
                    raise Exception(f"invalid transformation {tileTransform}")
                newTile = t.transformSeg(newTile, copy=False)

                rotation = (rotation + t.getValueRotation()) % 360
                flip = flip * t.getValueFlip()

            rotations.append(rotation)
            flips.append(flip)
            r.append(Transformation.copySeg(newTile))

        return r, rotations, flips

    def getImagesGeomPattern(self, geom: QgsGeometry) -> List[QgsGeometry]:
        """Projette l'image d'une géométrie quelconque sur les tuiles du pattern de base

        Args:
            geom (QgsGeometry): _description_

        Raises:
            Exception: _description_

        Returns:
            List[QgsGeometry]: _description_
        """
        patternFromSrc = (
            True
            if "conf" in self.typo and "patternfromsource" in self.typo["conf"]
            else False
        )

        r = [geom]

        newGeom = Transformation.copyGeom(geom)
        for tileTransforms in self.typo["pattern"].values():
            if patternFromSrc:
                newGeom = Transformation.copyGeom(geom)

            for tileTransform in tileTransforms.split(";"):
                t = self.getTransformation(tileTransform)
                if t is None:
                    raise Exception(f"invalid transformation {tileTransform}")

                newGeom = t.transformGeom(newGeom, copy=False)

            r.append(Transformation.copyGeom(newGeom))

        return r

    def getImagesGeomPavage(
        self, geom: QgsGeometry, pavageTransfos, patternPositions
    ) -> List[QgsGeometry]:
        """Retourne l'image d'une geom quelconque sur l'ensemble du pavage

        Args:
            geom (QgsGeometry): _description_

        Returns:
            List[QgsGeometry]: _description_
        """
        r = []
        patternGeoms = self.getImagesGeomPattern(geom)

        for posx, posy in patternPositions:
            newPattern = Transformation.copyGeoms(patternGeoms)
            for trsf in pavageTransfos["tx"]:
                tx = trsf * posx
                newPattern = tx.transformGeoms(newPattern, copy=False)
            for trsf in pavageTransfos["ty"]:
                ty = trsf * posy
                newPattern = ty.transformGeoms(newPattern, copy=False)

            for g in newPattern:
                r.append(g)

        return r

    def getOtherNodeXY(self):
        pts = {}
        for k, p in self.controles.items():
            if "visible" in self.typo["controls"][k]:
                pts[k] = QgsPointXY(p.x, p.y)
        return pts

    def getHandlesNodeXY(self):
        """Retourne une liste des noeuds de manipulation (handles) pour déplacer les points (hors points clés)

        Returns:
            dict(QgsPointXY): liste des noeuds de manipulation
        """
        pts = {}

        # tous les noeuds sauf extrémités
        for sid, seg in self.segs.items():
            # idmid = len(seg) // 2
            for k, node in enumerate(seg[1:-1]):
                pts[(sid, k + 1)] = QgsPointXY(node.x, node.y)

        return pts

    def getHandlesAddNodeXY(self):
        """Retourne une liste des noeuds de manipulation (handles) pour ajouter des points à la tuile de base

        Returns:
            dict(QgsPointXY): liste des noeuds de manipulation
        """
        pts = {}

        # milieu de chaque segment "graine"
        for sid, seg in self.segs.items():
            for k, n1 in enumerate(seg[:-1]):
                n2 = seg[k + 1]
                pts[(sid, k)] = QgsPointXY((n1.x + n2.x) / 2, (n1.y + n2.y) / 2)

        return pts

    def getIsHandleMoveNode(self, x, y, dist):
        handles = self.getHandlesNodeXY()
        for pk, ptXY in handles.items():
            if ptXY.distance(QgsPointXY(x, y)) < dist:
                return pk

        return (None, None)

    def getIsHandleP(self, x, y, dist):
        for k, p in self.controles.items():
            if "mouse" in self.typo["controls"][k]:
                ptXY = p.pointXY()
                if ptXY.distance(QgsPointXY(x, y)) < dist:
                    return k

        return None

    def getPMouseMovement(self, nid):
        m = self.typo["controls"][nid]["mouse"]

        r = []
        if "move_all" in m:
            r.append(Movement.MOVE_ALL)
        if "stretch_x" in m:
            r.append(Movement.STRECH_X)
        if "stretch_y" in m:
            r.append(Movement.STRECH_Y)
        if "rotation" in m:
            r.append(Movement.ROTATION)

        return r

    def getIsHandleAdd(self, x, y, dist):
        handles = self.getHandlesAddNodeXY()
        for pk, ptXY in handles.items():
            if ptXY.distance(QgsPointXY(x, y)) < dist:
                return pk

        return (None, None)

    def setNodeXY(self, sid, nid, pointXY):
        seg = self.segs[sid]
        seg[nid].setXY(pointXY.x(), pointXY.y())

    def getRotationPointXY(self):
        for p in self.typo["controls"].values():
            if "mouse" in p:
                regpattern = r".*rotation\(([a-z0-9]+)\).*"
                match = re.match(regpattern, p["mouse"])
                if match:
                    pk = match.group(1)
                    return self.controles[pk].pointXY()

        return None

    def transformAll(self, t: Transformation):
        for node in self.controles.values():
            t.transformNode(node)

        self.segs = t.transformSegs(self.segs, extremites=False)
        self.sketch = t.transformSegs(self.sketch, extremites=True)

    def moveP(self, pid, dx, dy, alpha):
        currentNode = self.controles[pid]
        oldNode = currentNode.copy()
        pointSettings = self.typo["controls"][pid]
        mouseActions = (pointSettings["mouse"]).split(";")
        p0 = self.controles["p0"]

        # distance à P0, nouvelle distance à P0
        d1 = currentNode.distance(p0)
        newNode = Node(currentNode.x + dx, currentNode.y + dy)
        d2 = newNode.distance(p0)
        dec = newNode.distance(oldNode)

        if "constraints" in pointSettings:
            constraints = (pointSettings["constraints"]).split(";")
            for constraint in constraints:
                regpattern = r"([a-z]+)\(([a-z0-9,]+)\)"
                match = re.match(regpattern, constraint)
                if match:
                    verb = match.group(1)
                    args = (match.group(2)).split(",")
                    if verb == "ontheline":
                        p1 = self.controles[args[0]].copy()
                        p2 = self.controles[args[1]].copy()
                        c = self.controles[args[2]].copy()
                        p1.translate(p0, c)
                        p2.translate(p0, c)

                        proj = newNode.perpendicularProjection(p1, p2)
                        dx, dy = proj.x - oldNode.x, proj.y - oldNode.y

        for action in mouseActions:
            # pattern transformation
            regpattern = r"([a-z_]+)\(([a-z0-9,]*)\)"
            match = re.match(regpattern, action)
            if match:
                verb = match.group(1)
                args = (match.group(2)).split(",")

                if verb == "middle":
                    points = self.getControlPoints(args)
                    t = Middle(*points)
                    t.transformNode(currentNode)
                elif verb == "move":
                    points = self.getControlPoints(args)
                    t = Translation(dx=dx, dy=dy)
                    t.transformSeg(points)

                    for s in args:
                        if s in self.segs:
                            t.transformSeg(self.segs[s])
                else:
                    if verb == "move_all":
                        t = Translation(dx=dx, dy=dy)

                    elif verb == "rotation":
                        c = self.getControlPoints(args)[0]
                        t = Rotation(alpha, c)

                    elif verb == "stretch_x":
                        points = self.getControlPoints(args)
                        t = Stretch("x", d2 / d1, *points)

                    elif verb == "stretch_y":
                        points = self.getControlPoints(args)
                        t = Stretch("y", d2 / d1, *points)

                    elif verb == "shear":
                        points = self.getControlPoints(args)
                        lr = newNode.pointSideOfSegment(points[0], points[2])
                        t = Shear(lr * dec, *points)

                    self.transformAll(t)

            # move specific point
            regpattern = r"([a-z0-9]+)=(.*)"
            match = re.match(regpattern, action)
            if match:
                target = match.group(1)
                func = match.group(2)

                self.images = self.getImages()
                sourceNode, trsf = self.getTransformation2(func)
                targetNode = self.controles[target]

                newP = trsf.transformNode(sourceNode, copy=True)
                targetNode.setXY(newP.x, newP.y)

    def getControlPoints(self, args):
        r = []
        for arg in args:
            if arg in self.controles:
                r.append(self.controles[arg])
            # else:
            #   print(f"Point {arg} non trouvé")
        return r

    def addNode(self, segId, nodeId, pointXY):
        seg = self.segs[segId]
        seg.insert(nodeId + 1, Node(pointXY.x(), pointXY.y()))
        return segId, nodeId + 1

    def removeNode(self, segId, nodeId):
        seg = self.segs[segId]
        del seg[nodeId]

    def hasSketch(self):
        return len(self.sketch) > 0

    def getSketchGeom(self):
        return QgsGeometry.fromMultiPolylineXY(
            [[QgsPointXY(n.x(), n.y()) for n in line] for line in self.sketch]
        )

    def removeSketch(self, ptXY, tolerance):
        geoms = [
            QgsGeometry.fromPolylineXY([QgsPointXY(n.x(), n.y()) for n in line])
            for line in self.sketch
        ]
        # print(len(geoms))
        for i, g in enumerate(geoms):
            if g.distance(QgsGeometry.fromPointXY(ptXY)) < tolerance:
                self.sketch.pop(i)
                break


class Pavage(Pattern):
    def __init__(self, typo, center, width):
        super().__init__(typo, center, width)

    def getAllControlsPointsXY(self) -> QgsGeometry:
        points = []
        pks = []
        for k, n in self.controles.items():
            pks.append(k)
            points.append(n.pointXY())

        return points, pks

    def getPControlsPointsXY(self) -> QgsGeometry:
        points = []
        pks = []
        for k, n in self.controles.items():
            if "mouse" in self.typo["controls"][k]:
                pks.append(k)
                points.append(n.pointXY())

        return points, pks

    def getPControlsGeom(self) -> QgsGeometry:
        points, _ = self.getPControlsPointsXY()
        return QgsGeometry(QgsMultiPoint(points))

    def getTilePolygon(self) -> QgsGeometry:
        tileSegs = self.getTileSegments()
        linestring = self.getTileLineString(tileSegs)
        g = QgsGeometry.fromPolygonXY([[QgsPointXY(n.x, n.y) for n in linestring]])
        return g

    def getPatternPolygons(self) -> List[QgsGeometry]:
        r = []
        linestrings, rotations, flips = self.getPatternLinestrings()
        for linestring in linestrings:
            g = QgsGeometry.fromPolygonXY([[QgsPointXY(n.x, n.y) for n in linestring]])
            r.append(g)

        attrs = {
            "rotation": {"fieldtype": "int", "values": rotations},
            "flip": {"fieldtype": "int", "values": flips},
        }
        return r, attrs

    def getPavagePolygonsXY(self, extent, i, j, dx, dy, pattern, protations, pflips):
        N = 15
        r = []
        rotations = []
        flips = []
        transformations = {"tx": [], "ty": []}
        positions = []
        for t in self.typo["pavage"]["x"].split(";"):
            transformations["tx"].append(self.getTransformation(t))
        for t in self.typo["pavage"]["y"].split(";"):
            transformations["ty"].append(self.getTransformation(t))

        firstPattern = Transformation.copySegs(pattern)
        if i != 0:
            for trsf in transformations["tx"]:
                tx = trsf * i
                firstPattern = tx.transformSegs(firstPattern, copy=False)

        if j != 0:
            for trsf in transformations["ty"]:
                ty = trsf * j
                firstPattern = ty.transformSegs(firstPattern, copy=False)

        firstPatternX = Transformation.copySegs(firstPattern)
        for posx in range(N):
            for trsf in transformations["tx"]:
                ti = trsf * dx
                firstPatternX = ti.transformSegs(firstPatternX, copy=False)

            newPatternY = Transformation.copySegs(firstPatternX)
            for posy in range(N):
                for trsf in transformations["ty"]:
                    tj = trsf * dy
                    newPattern = tj.transformSegs(newPatternY, copy=False)

                patternGeoms = []
                inExtentJ = False
                for tileLinestring in newPattern:
                    # tile
                    g = QgsGeometry.fromPolygonXY(
                        [[QgsPointXY(n.x, n.y) for n in tileLinestring]]
                    ).makeValid()

                    patternGeoms.append(g)

                    if g.intersects(QgsGeometry.fromRect(extent)):
                        inExtentJ = True

                if inExtentJ:
                    positions.append((i + (posx + 1) * dx, j + (posy + 1) * dy))
                    r = r + patternGeoms
                    rotations = rotations + protations
                    flips = flips + pflips

        return r, transformations, positions, rotations, flips

    def getPavagePolygons(self, extent) -> List[QgsGeometry]:
        r = []
        rotations = []
        flips = []
        positions = []

        pattern, protations, pflips = self.getPatternLinestrings()

        # Bottom Left sector
        xgeoms, xtransfo, xpositions, xrotations, xflips = self.getPavagePolygonsXY(
            extent, 1, 1, -1, -1, pattern, protations, pflips
        )
        r = r + xgeoms
        positions = positions + xpositions
        rotations = rotations + xrotations
        flips = flips + xflips

        # Top Right sector
        xgeoms, xtransfo, xpositions, xrotations, xflips = self.getPavagePolygonsXY(
            extent, 0, 0, 1, 1, pattern, protations, pflips
        )
        r = r + xgeoms
        positions = positions + xpositions
        rotations = rotations + xrotations
        flips = flips + xflips

        # Top Left
        xgeoms, xtransfo, xpositions, xrotations, xflips = self.getPavagePolygonsXY(
            extent, 1, 0, -1, 1, pattern, protations, pflips
        )
        r = r + xgeoms
        positions = positions + xpositions
        rotations = rotations + xrotations
        flips = flips + xflips

        # Bottom Right sector
        xgeoms, xtransfo, xpositions, xrotations, xflips = self.getPavagePolygonsXY(
            extent, 0, 1, 1, -1, pattern, protations, pflips
        )
        r = r + xgeoms
        positions = positions + xpositions
        rotations = rotations + xrotations
        flips = flips + xflips

        attrs = {
            "rotation": {"fieldtype": "int", "values": rotations},
            "flip": {"fieldtype": "int", "values": flips},
        }

        return r, xtransfo, positions, attrs

    def getHandlesNodeGeom(self) -> QgsGeometry:
        return QgsGeometry.fromMultiPointXY(self.getHandlesNodeXY().values())

    def getOtherNodeGeom(self) -> QgsGeometry:
        return QgsGeometry.fromMultiPointXY(self.getOtherNodeXY().values())

    def getHandlesAddNodeGeom(self) -> QgsGeometry:
        return QgsGeometry.fromMultiPointXY(self.getHandlesAddNodeXY().values())

    def getInvalidTileGeom(self) -> QgsGeometry:
        geom = self.getTilePolygon()
        if not geom.isGeosValid():
            return geom

        return None

    def getJson(self):
        s = {}

        s["type"] = self.typo.value
        s["p0"] = [self.p0.x(), self.p0.y()]
        s["w"] = self.w

        s["controls"] = {}
        for k, p in self.controles.items():
            s["controls"][k] = [p.x, p.y]
        s["segs"] = {}
        for ks, seg in self.segs.items():
            s["segs"][ks] = []
            for p in seg:
                s["segs"][ks].append([p.x, p.y])

        s["sketch"] = [[(n.x(), n.y()) for n in line] for line in self.sketch]

        return s

    @staticmethod
    def fromJson(struct):
        pav = Pavage(
            Typo(struct["type"]),
            QgsPointXY(struct["p0"][0], struct["p0"][1]),
            struct["w"],
        )
        for k, c in struct["controls"].items():
            pav.controles[k].setXY(c[0], c[1])

        for ks, points in struct["segs"].items():
            seg = pav.segs[ks]
            seg[0].setXY(points[0][0], points[0][1])
            seg[1].setXY(points[-1][0], points[-1][1])

            for i, p in enumerate(points[1:-1]):
                seg.insert(i + 1, Node(p[0], p[1]))

        if "sketch" in struct:
            for xy in struct["sketch"]:
                pav.sketch.append([QgsPointXY(n[0], n[1]) for n in xy])

        return pav
