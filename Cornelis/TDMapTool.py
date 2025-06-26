import json
from enum import Enum

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsMapLayerStyle,
    QgsPointXY,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt.QtGui import QColor, QCursor, QPixmap
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
from qgis.utils import iface

from .__about__ import DIR_PLUGIN_ROOT
from .logic.pavage import Movement, Pavage
from .logic.tools import getLayers
from .logic.typo import Typo

globals()["globalPavage"] = None


class Mode(Enum):
    MOVE_NODE = 1
    MOVE_P = 2
    DEL_NODE = 3
    DRAWING = 4


class TDMapTool(QgsMapTool):
    """
    'Tool' class, displays the button bar, controls mouse events on the map (selection...)
    """

    pavage: Pavage
    pavageVisible: bool

    def __init__(self, plugin, canvas):
        """
        Initilizations

        rubber band...
        """
        QgsMapTool.__init__(self, canvas)

        self._plugin = plugin
        self._canvas = canvas
        self.x = self._canvas.getCoordinateTransform()

        self.currentLayer = None
        self.pavage = None
        self.currentNodeId = None
        self.pavageVisible = False
        self.drawingMode = False
        self.mousePressed = False
        self.mode = None

        # single tile
        self.rbTile = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PolygonGeometry
        )
        self.rbTile.setStrokeColor(QColor(150, 20, 100, 100))
        self.rbTile.setFillColor(QColor(150, 20, 100, 100))
        self.rbTile.setWidth(6)

        # pattern
        self.rbPattern = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PolygonGeometry
        )
        self.rbPattern.setStrokeColor(QColor(30, 80, 150, 100))
        self.rbPattern.setFillColor(QColor(30, 80, 150, 50))
        self.rbPattern.setWidth(3)

        # pavage sample
        self.rbPavage = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PolygonGeometry
        )
        self.rbPavage.setStrokeColor(QColor(30, 100, 60, 200))
        self.rbPavage.setFillColor(QColor(30, 100, 60, 0))
        self.rbPavage.setWidth(2)

        self.rbInvalid = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PolygonGeometry
        )
        self.rbInvalid.setFillColor(QColor(230, 150, 150, 80))
        self.rbInvalid.setWidth(0)

        self.rbSamplePoly = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PolygonGeometry
        )
        self.rbSamplePoly.setFillColor(QColor(100, 230, 150, 150))
        self.rbSamplePoly.setStrokeColor(QColor(50, 50, 120, 200))
        self.rbSamplePoly.setWidth(3)

        self.rbSamplePoint = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PointGeometry
        )
        self.rbSamplePoint.setFillColor(QColor(100, 230, 150, 150))
        self.rbSamplePoint.setStrokeColor(QColor(50, 50, 120, 200))
        self.rbSamplePoint.setWidth(3)

        self.rbSampleLine = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.LineGeometry
        )
        self.rbSampleLine.setStrokeColor(QColor(50, 50, 120, 200))
        self.rbSampleLine.setWidth(3)

        # Croquis
        self.rbSketch = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.LineGeometry
        )
        self.rbSketch.setStrokeColor(QColor(170, 50, 50, 200))
        self.rbSketch.setWidth(2)

        self.rbSketches = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.LineGeometry
        )
        self.rbSketches.setStrokeColor(QColor(150, 50, 50, 100))
        self.rbSketches.setWidth(2)

        # noeuds déplaçables
        self.rbNodes = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PointGeometry
        )
        self.rbNodes.setStrokeColor(QColor(40, 100, 180, 200))
        self.rbNodes.setWidth(5)

        # autres noeuds (centres de rotation...)
        self.rbOtherNodes = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PointGeometry
        )
        self.rbOtherNodes.setStrokeColor(QColor(30, 30, 30, 150))
        self.rbOtherNodes.setFillColor(QColor(30, 30, 30, 10))
        self.rbOtherNodes.setWidth(3)
        self.rbOtherNodes.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        self.rbOtherNodes.setIconSize(7)

        # pour ajouter des noeuds intermédiaires
        self.rbAddNode = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PointGeometry
        )
        self.rbAddNode.setStrokeColor(QColor(50, 50, 200, 200))
        self.rbAddNode.setFillColor(QColor(120, 120, 200, 150))
        self.rbAddNode.setWidth(3)
        self.rbAddNode.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        self.rbAddNode.setIconSize(7)

        # points de contrôle (déplacement, rotation...)
        self.rbControls = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PointGeometry
        )
        self.rbControls.setStrokeColor(QColor(130, 80, 160, 250))
        self.rbControls.setFillColor(QColor(255, 30, 30, 220))
        self.rbControls.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        self.rbControls.setIconSize(12)

        self.rbCursors = QgsRubberBand(
            self._canvas, QgsWkbTypes.GeometryType.PointGeometry
        )
        self.rbCursors.setFillColor(QColor(100, 230, 150, 50))
        self.rbCursors.setStrokeColor(QColor(50, 50, 120, 100))
        self.rbCursors.setWidth(3)
        self.rbCursors.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        self.rbCursors.setIconSize(6)

        self.rubbers = [
            self.rbCursors,
            self.rbControls,
            self.rbSketch,
            self.rbSketches,
            self.rbTile,
            self.rbPavage,
            self.rbPattern,
            self.rbNodes,
            self.rbOtherNodes,
            self.rbAddNode,
            self.rbInvalid,
            self.rbSamplePoly,
            self.rbSamplePoint,
            self.rbSampleLine,
        ]

        self.keyModifier = None

        self.cursorRotation = self.getCursor("cursor-rotation.png")
        self.cursorScale = self.getCursor("cursor-scale.png")

    def getCursor(self, name):
        url = str(DIR_PLUGIN_ROOT / "resources" / name)
        img = QPixmap(url)
        mask = img.createMaskFromColor(QColor(0, 255, 255), Qt.MaskMode.MaskInColor)
        img.setMask(mask)
        return QCursor(img)

    def reset(self):
        for rb in self.rubbers:
            rb.reset()

    def activate(self):
        QgsMapTool.activate(self)
        self._canvas.extentsChanged.connect(self.buildRubberBand)

    def deactivate(self):
        self.reset()
        QgsMapTool.deactivate(self)
        self._plugin.deactivate()
        self._canvas.extentsChanged.disconnect(self.buildRubberBand)

    def initPavage(self, typo=Typo.T1a):
        if self.pavage is not None:
            promptReply = QMessageBox.question(
                iface.mainWindow(),
                self.tr("New pavage"),
                self.tr("Abandon the current tessellation ?"),
                QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.No,
            )
            if promptReply == QMessageBox.StandardButton.Yes:
                self.pavage = None

        if self.pavage is None:
            extent = self._canvas.extent()
            w = min(extent.width() // 5, extent.height() // 5)
            self.pavage = Pavage(typo, extent.center(), w)
            globals()["globalPavage"] = self.pavage
            self.reset()

    def zoomToPavage(self):
        if self.pavage is not None:
            bb = self.pavage.getTilePolygon().boundingBox()
            bb.scale(5)
            self._canvas.setExtent(bb)
            self._canvas.refresh()

    def savePavage(self, fileName):
        configFile = open(fileName, "w", encoding="utf-8")
        js = self.pavage.getJson()
        json.dump(js, configFile, indent=4)
        configFile.close()

    def loadPavage(self, fileName):
        configFile = open(fileName, newline="", encoding="utf-8")
        j = json.load(configFile)
        configFile.close()
        self.pavage = Pavage.fromJson(j)
        globals()["globalPavage"] = self.pavage
        self.showPavage(True)

    def showPavage(self, visible):
        """ """
        self.pavageVisible = visible

        if self.pavage is None:
            self.initPavage(Typo.T1a)

        self.buildRubberBand()

    def modeDrawing(self, drawingMode):
        """ """
        if self.pavage is None:
            return False

        self.drawingMode = drawingMode
        return True

    def getFaceContains(self, polysGeom, vertex):
        for fid, geom in polysGeom.items():
            if geom.contains(QgsPointXY(vertex)):
                return fid

        return None

    def layerFromGeoms(self, geoms, attrs={}, name="extent", typ="Polygon"):
        crs = self._canvas.mapSettings().destinationCrs()

        fields = QgsFields()

        for fk, fieldef in attrs.items():
            if fieldef["fieldtype"] == "int":
                field = QgsField(fk, QVariant.Int, fk, 4, 0)
                fields.append(field)
            if fieldef["fieldtype"] == "double":
                field = QgsField(fk, QVariant.Double, fk, 4, 2)
                fields.append(field)
            if fieldef["fieldtype"] == "str":
                field = QgsField(fk, QVariant.String)
                fields.append(field)

        vl = QgsVectorLayer("{}?crs={}".format(typ, crs.authid()), name, "memory")
        pr = vl.dataProvider()
        vl.startEditing()

        pr.addAttributes(fields)

        for i, geom in enumerate(geoms):
            feat = QgsFeature()
            feat.setGeometry(geom)

            if len(attrs) > 0:
                feat.setFields(fields)
                for fk, fieldef in attrs.items():
                    if "values" in fieldef:
                        feat.setAttribute(fk, fieldef["values"][i])
                    if "value" in fieldef:
                        feat.setAttribute(fk, fieldef["value"])

            pr.addFeature(feat)

        vl.commitChanges()

        return vl

    def layerFromXY(self, axy: dict, name: str = "extent"):
        geoms = []
        for xy in axy.values():
            for p in xy:
                geoms.append(QgsGeometry.fromPointXY(QgsPointXY(p[0], p[1])))

        return self.layerFromGeoms(geoms, name=name, typ="Point")

    def layerFromGeom(self, geom, attrs={}, name="extent"):
        return self.layerFromGeoms([geom], attrs=attrs, name=name)

    def getStyle(self, layer):
        smg = layer.styleManager()
        style = {}
        style["current"] = smg.currentStyle()
        style["styles"] = {}
        for k in smg.mapLayerStyles():
            style["styles"][k] = smg.style(k).xmlData()

        return style

    def pasteStyle(self, newLayer, style):
        smg = newLayer.styleManager()
        smg.reset()
        for k in style["styles"]:
            smg.renameStyle(k, "tmpstyletodelete")
            smg.addStyle(k, QgsMapLayerStyle(style["styles"][k]))
            smg.removeStyle("tmpstyletodelete")
        smg.setCurrentStyle(style["current"])

    def copyPasteStyle(self, fromLayer, toLayer):
        self.pasteStyle(toLayer, self.getStyle(fromLayer))

    def addLayer(self, group, layer, visible=True):
        QgsProject.instance().addMapLayer(layer, False)
        t = group.addLayer(layer)
        t.setItemVisibilityChecked(visible)

    def prepareNewVectorLayer(self, g, layer, layerMask):
        # new layer in map projection
        layer_crs = QgsCoordinateReferenceSystem(layer.crs().authid())
        mask_crs = QgsCoordinateReferenceSystem(layerMask.crs().authid())
        transformationRequired = layer.crs().authid() != layerMask.crs().authid()

        # Extract by location, transform and clip
        fmask = layerMask.getFeatures("1=1").__next__()
        gmask = fmask.geometry()
        gmask2 = QgsGeometry(gmask)
        if transformationRequired:
            gmask2.transform(
                QgsCoordinateTransform(mask_crs, layer_crs, QgsProject.instance())
            )
        ids = []
        for f in layer.getFeatures(gmask2.boundingBox()):
            geom = f.geometry()
            if transformationRequired:
                geom.transform(
                    QgsCoordinateTransform(layer_crs, mask_crs, QgsProject.instance())
                )
            if geom.intersects(gmask):
                ids.append(f.id())

        newLayer = layer.materialize(QgsFeatureRequest().setFilterFids(ids))

        # clip geometry
        newLayer.startEditing()
        try:
            for f in newLayer.getFeatures():
                geom = f.geometry()
                if transformationRequired:
                    geom.transform(
                        QgsCoordinateTransform(
                            layer_crs, mask_crs, QgsProject.instance()
                        )
                    )
                geom = geom.intersection(gmask)

                f.setGeometry(geom)
                newLayer.updateFeature(f)
        finally:
            newLayer.commitChanges()

        newLayer.setCrs(mask_crs)

        newLayer.setName(self.tr("NEW") + " {}".format(layer.name()))
        newLayer.setSubsetString(layer.subsetString())
        self.copyPasteStyle(layer, newLayer)

        self.addLayer(g, newLayer, visible=True)

        return newLayer

    def showProgress(self, text, percent):
        iface.statusBarIface().showMessage("{} {} %".format(text, int(100 * percent)))
        QApplication.processEvents()

    def message(self, text, level=Qgis.MessageLevel.Info, duration=5):
        iface.messageBar().pushMessage(
            self.tr("Tesselation"), text, level=level, duration=duration
        )
        QApplication.processEvents()

    def do(self):
        try:
            pname = self.pavage.typo["name"]
            gname = self.tr("Tesselation")

            group = QgsProject.instance().layerTreeRoot().findGroup(gname)
            if group is None:
                group = QgsProject.instance().layerTreeRoot().insertGroup(0, gname)

            # Add Points layer ------------------
            """points, pks = self.pavage.getAllControlsPointsXY()
            attrs = {"name": {"fieldtype": "str", "values": pks}}

            mouses, types = [], []
            for k in pks:
                mouse = ""
                typ = ""
                if k in self.pavage.typo["controls"]:
                    nodedict = self.pavage.typo["controls"][k]
                    if "mouse" in nodedict:
                        mouse = nodedict["mouse"]
                    if "visible" in nodedict:
                        typ = nodedict["visible"]

                mouses.append(mouse)
                types.append(typ)

            attrs["mouse"] = {"fieldtype": "str", "values": mouses}
            attrs["type"] = {"fieldtype": "str", "values": types}

            layerPoints = self.layerFromGeoms(
                [QgsGeometry.fromPointXY(p) for p in points],
                attrs=attrs,
                name=self.tr("Points"),
                typ="Point",
            )
            self.addLayer(group, layerPoints, visible=False)
            layerPoints.loadNamedStyle(str(DIR_PLUGIN_ROOT / "resources/node.qml"))
            # / Add Points layer"""

            # Tile Geom
            tileGeom = self.pavage.getTilePolygon()

            # mask
            attrs = {"name": {"fieldtype": "str", "value": pname}}
            layerMask = self.layerFromGeom(
                tileGeom, attrs=attrs, name=self.tr("Tile") + f" {pname}"
            )

            # pattern geoms
            patternGeoms, patternAttr = self.pavage.getPatternPolygons()
            patternAttr["name"] = {"fieldtype": "str", "value": pname}

            # pavage geoms limit to extent
            extent = self._canvas.extent()
            pavageGeoms, pavageTransfos, positions, pavageAttr = (
                self.pavage.getPavagePolygons(extent)
            )
            self.transformations = pavageTransfos
            self.patternPositions = positions

            layers = getLayers()
            self.message(self.tr("Initialization..."))
            newVectorLayers = []
            for layer in layers.values():
                self.message(f"- {layer.name()}")

                if isinstance(layer, QgsVectorLayer):
                    try:
                        newV = self.prepareNewVectorLayer(group, layer, layerMask)
                        newVectorLayers.append(newV)
                    except Exception:
                        self.message(
                            f"Traitement de la couche {layer.name()} impossible"
                        )

            self.showProgress("Cornelis", 0)
            for ilayer, layer in enumerate(newVectorLayers):
                self.showProgress("Cornelis", ilayer // len(newVectorLayers))

                pr = layer.dataProvider()
                layer.startEditing()
                toDelete = []
                feats = []
                self.message(f"- {layer.name()}")
                for _, f in enumerate(layer.getFeatures()):
                    QApplication.processEvents()
                    toDelete.append(f.id())
                    g = f.geometry()
                    images = self.pavage.getImagesGeomPavage(
                        g, self.transformations, self.patternPositions
                    )
                    newG = QgsGeometry.unaryUnion(images)
                    # for image in images:
                    feat = QgsFeature()
                    feat.setFields(f.fields())
                    feat.setGeometry(newG)  # or image
                    for atid in pr.attributeIndexes():
                        if atid not in pr.pkAttributeIndexes():
                            field = f.fields().at(atid)
                            feat.setAttribute(field.name(), f.attribute(atid))
                    feats.append(feat)

                self.message(f"- {layer.name()} {len(feats)} feats")
                pr.addFeatures(feats)
                pr.deleteFeatures(toDelete)
                layer.commitChanges()

            # Add Sketch layer
            if self.pavage.hasSketch():
                geom = self.pavage.getSketchGeom()
                images = self.pavage.getImagesGeomPavage(
                    geom, self.transformations, self.patternPositions
                )

                layersketch = self.layerFromGeoms(
                    images, name=self.tr("Sketch") + f" {pname}", typ="Linestring"
                )
                self.addLayer(group, layersketch, visible=False)
                layersketch.loadNamedStyle(
                    str(DIR_PLUGIN_ROOT / "resources/sketch.qml")
                )

            # Add pattern layer
            if len(patternGeoms) > 1:
                layerPattern = self.layerFromGeoms(
                    patternGeoms,
                    attrs=patternAttr,
                    name=self.tr("Pattern") + f" {pname}",
                )
                self.addLayer(group, layerPattern, visible=False)
                layerPattern.loadNamedStyle(
                    str(DIR_PLUGIN_ROOT / "resources/pattern.qml")
                )

            # Add tile layer
            self.addLayer(group, layerMask, visible=False)
            layerMask.loadNamedStyle(str(DIR_PLUGIN_ROOT / "resources/tile.qml"))

            # Add pavage layer
            pavageAttr["name"] = {"fieldtype": "str", "value": pname}
            layerPavage = self.layerFromGeoms(
                pavageGeoms,
                attrs=pavageAttr,
                name=self.tr("Tessellation") + f" {pname}",
            )
            self.addLayer(group, layerPavage, visible=False)
            layerPavage.loadNamedStyle(str(DIR_PLUGIN_ROOT / "resources/pavage.qml"))

            self.message(self.tr("End !"), level=Qgis.MessageLevel.Success)

        except Exception as e:
            self.message(self.tr("End !"), level=Qgis.MessageLevel.Critical)
            raise e

        finally:
            iface.statusBarIface().clearMessage()
            iface.mapCanvas().refreshAllLayers()
            iface.mapCanvas().waitWhileRendering()
            QgsApplication.restoreOverrideCursor()

    def buildSelectionRubberBand(self):
        """ """
        self.rbSamplePoly.reset()
        self.rbSampleLine.reset()
        self.rbSamplePoint.reset()

        if self.pavage is None:
            return

        if self.pavageVisible and self.pavage is not None:
            pav_crs = self._canvas.mapSettings().destinationCrs()

            tileGeom = self.pavage.getTilePolygon()
            layers = iface.layerTreeView().selectedLayers()
            geomsPoint = []
            geomsPoly = []
            geomsLine = []
            for layer in layers:
                if isinstance(layer, QgsVectorLayer):
                    layer_crs = QgsCoordinateReferenceSystem(layer.crs().authid())
                    for f in layer.selectedFeatures()[:10]:
                        g = f.geometry()
                        g.transform(
                            QgsCoordinateTransform(
                                layer_crs, pav_crs, QgsProject.instance()
                            )
                        )
                        g = g.intersection(tileGeom)
                        if (
                            layer.geometryType()
                            == QgsWkbTypes.GeometryType.PointGeometry
                        ):
                            geomsPoint.append(g)
                        if (
                            layer.geometryType()
                            == QgsWkbTypes.GeometryType.LineGeometry
                        ):
                            geomsLine.append(g)
                        if (
                            layer.geometryType()
                            == QgsWkbTypes.GeometryType.PolygonGeometry
                        ):
                            geomsPoly.append(g)

            for geoms, rbSample in zip(
                (geomsPoly, geomsPoint, geomsLine),
                (self.rbSamplePoly, self.rbSamplePoint, self.rbSampleLine),
            ):
                if len(geoms) > 0:
                    images = []
                    for g in geoms:
                        images = images + self.pavage.getImagesGeomPavage(
                            g, self.transformations, self.patternPositions
                        )
                    rbSample.setToGeometry(images[0])
                    for g in images[1:]:
                        rbSample.addGeometry(g)

    def buildCursorRubberBand(self, ptXY):
        geom = QgsGeometry.fromPointXY(ptXY)

        images = self.pavage.getImagesGeomPavage(
            geom, self.transformations, self.patternPositions
        )
        if len(images) > 1:
            self.rbCursors.setToGeometry(images[1])
            for g in images[2:]:
                self.rbCursors.addGeometry(g)

    def buildSketchRubberBand(self):
        if not self.pavage.hasSketch():
            self.rbSketch.reset()
            self.rbSketches.reset()
            return

        geom = self.pavage.getSketchGeom().simplify(self.x.mapUnitsPerPixel()).smooth()
        if geom.isNull():
            return

        try:
            self.sketch = geom.asMultiPolyline()
        except Exception:
            self.sketch = [geom.asPolyline()]

        self.rbSketch.setToGeometry(geom)

        images = self.pavage.getImagesGeomPavage(
            geom, self.transformations, self.patternPositions
        )
        if len(images) > 0:
            self.rbSketches.setToGeometry(images[0])
            for g in images[1:]:
                self.rbSketches.addGeometry(g)

    def buildRubberBand(self):
        """ """
        if self.pavage is None:
            return

        if self.pavageVisible:
            geom = self.pavage.getPControlsGeom()
            self.rbControls.setToGeometry(geom)

            geom = self.pavage.getTilePolygon()
            if geom:
                self.rbTile.setToGeometry(geom)

            geoms, _ = self.pavage.getPatternPolygons()
            if len(geoms) > 0:
                self.rbPattern.setToGeometry(geoms[0])
                for g in geoms[1:]:
                    self.rbPattern.addGeometry(g)

            extent = self._canvas.extent()
            geoms, transfos, positions, _ = self.pavage.getPavagePolygons(extent)
            self.transformations = transfos
            self.patternPositions = positions
            if len(geoms) > 0:
                self.rbPavage.setToGeometry(geoms[0])
                for g in geoms[1:]:
                    self.rbPavage.addGeometry(g)

            geom = self.pavage.getHandlesNodeGeom()
            self.rbNodes.setToGeometry(geom)

            geom = self.pavage.getOtherNodeGeom()
            self.rbOtherNodes.setToGeometry(geom)

            geom = self.pavage.getHandlesAddNodeGeom()
            self.rbAddNode.setToGeometry(geom)

            polysGeom = self.pavage.getInvalidTileGeom()
            if polysGeom is not None:
                self.rbInvalid.setToGeometry(polysGeom)
            else:
                self.rbInvalid.reset()

            self.buildSketchRubberBand()
        else:
            self.reset()

    def deltaRotation(self, c):
        if c is None:
            return None

        az_init = self.previousPointXY.azimuth(c)
        az_new = self.currentPointXY.azimuth(c)
        self.previousPointXY = self.currentPointXY

        if az_init > az_new:
            az_new = az_new + 360
        return az_new - az_init

    def canvasPressEvent(self, event):
        """ """
        self.pressedPointXY = self.x.toMapCoordinates(event.pos().x(), event.pos().y())
        self.currentPointXY = self.pressedPointXY
        self.previousPointXY = self.pressedPointXY

        self.currentNodeId = None
        self.mousePressed = True
        xpos, ypos, dist = (
            self.currentPointXY.x(),
            self.currentPointXY.y(),
            7 * self.x.mapUnitsPerPixel(),
        )

        self.mode = None

        if self.drawingMode:
            self.mode = Mode.DRAWING
            if not (self.keyModifier == Qt.KeyboardModifier.ControlModifier):
                self.pavage.sketch.append([self.currentPointXY])

        elif self.pavageVisible:
            snid = self.pavage.getIsHandleMoveNode(xpos, ypos, dist)
            if snid[0] is not None:
                (self.currentSegId, self.currentNodeId) = snid
                if self.keyModifier == Qt.KeyboardModifier.ControlModifier:
                    self.mode = Mode.DEL_NODE
                else:
                    self.mode = Mode.MOVE_NODE

            if self.mode is None:
                snid = self.pavage.getIsHandleAdd(xpos, ypos, dist)
                if snid[0] is not None:
                    # add node
                    (self.currentSegId, self.currentNodeId) = self.pavage.addNode(
                        snid[0], snid[1], self.currentPointXY
                    )
                    self.mode = Mode.MOVE_NODE

            if self.mode is None:
                idp = self.pavage.getIsHandleP(xpos, ypos, dist)
                if idp is not None:
                    self.currentNodeId = idp
                    self.mode = Mode.MOVE_P

    def setCursor(self, t):
        if Movement.MOVE_ALL in t:
            self._canvas.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        elif Movement.STRECH_X in t and Movement.ROTATION in t:
            self._canvas.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        elif Movement.STRECH_Y in t and Movement.ROTATION in t:
            self._canvas.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        elif Movement.STRECH_X in t and Movement.STRECH_Y in t:
            self._canvas.setCursor(self.cursorScale)
        elif Movement.STRECH_X in t:
            self._canvas.setCursor(QCursor(Qt.CursorShape.SplitHCursor))
        elif Movement.STRECH_Y in t:
            self._canvas.setCursor(QCursor(Qt.CursorShape.SplitVCursor))
        elif Movement.ROTATION in t:
            self._canvas.setCursor(self.cursorRotation)

    def canvasMoveEvent(self, event):
        """ """
        if self.pavage is None:
            return

        self.currentPointXY = self.x.toMapCoordinates(event.pos().x(), event.pos().y())

        xpos, ypos, dist = (
            self.currentPointXY.x(),
            self.currentPointXY.y(),
            7 * self.x.mapUnitsPerPixel(),
        )
        dx = dy = 0

        self._canvas.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        if self.pavageVisible:
            self.buildCursorRubberBand(self.currentPointXY)

        if not self.mousePressed:
            if self.pavageVisible and not self.drawingMode:
                idp = self.pavage.getIsHandleP(xpos, ypos, dist)

                (self.currentSegId, self.currentNodeId) = (
                    self.pavage.getIsHandleMoveNode(xpos, ypos, dist)
                )
                addId = self.pavage.getIsHandleAdd(xpos, ypos, dist)

                if addId[0] is not None:
                    self._canvas.setCursor(QCursor(Qt.CursorShape.CrossCursor))
                elif idp is not None:
                    t = self.pavage.getPMouseMovement(idp)
                    self.setCursor(t)

                elif self.currentNodeId is not None:
                    if self.keyModifier == Qt.KeyboardModifier.ControlModifier:
                        self._canvas.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
                    else:
                        self._canvas.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))

        else:
            if self.mode == Mode.DRAWING and not (
                (self.keyModifier == Qt.KeyboardModifier.ControlModifier)
            ):
                self.pavage.sketch[-1].append(self.currentPointXY)
                self.buildSketchRubberBand()

            if self.currentNodeId is None:
                return

            if self.mode == Mode.MOVE_NODE:
                if self.currentNodeId is not None:
                    self.pavage.setNodeXY(
                        self.currentSegId, self.currentNodeId, self.currentPointXY
                    )
                self.buildRubberBand()

            elif self.mode == Mode.MOVE_P:
                dx = self.currentPointXY.x() - self.pressedPointXY.x()
                dy = self.currentPointXY.y() - self.pressedPointXY.y()
                alpha = self.deltaRotation(self.pavage.getRotationPointXY())
                self.pressedPointXY = self.currentPointXY

                if self.currentNodeId is not None:
                    self.pavage.moveP(self.currentNodeId, dx, dy, alpha)

                self.buildRubberBand()

    def canvasReleaseEvent(self, event):
        """ """
        try:
            if self.keyModifier == Qt.KeyboardModifier.ControlModifier:
                if self.mode == Mode.DEL_NODE:
                    if self.currentNodeId is not None:
                        self.pavage.removeNode(self.currentSegId, self.currentNodeId)
                        self.buildRubberBand()

                if self.mode == Mode.DRAWING:
                    self.pavage.removeSketch(
                        self.currentPointXY, 7 * self.x.mapUnitsPerPixel()
                    )
                    self.buildSketchRubberBand()

            self.buildSelectionRubberBand()

            if self.mode == Mode.DRAWING and not (
                (self.keyModifier == Qt.KeyboardModifier.ControlModifier)
            ):
                self.buildSketchRubberBand()
        finally:
            self.mousePressed = False
            self.currentPointXY = None
            self.currentNodeId = None
            self.mode = None

            QgsApplication.restoreOverrideCursor()
            iface.mapCanvas().waitWhileRendering()

    def keyPressEvent(self, e):
        self.keyModifier = e.modifiers()

    def keyReleaseEvent(self, e):
        self.keyModifier = e.modifiers()

    def buildPavageGeometry(self, geom):

        if "globalPavage" not in globals() or globals()["globalPavage"] is None:
            return None
        try:
            tileGeom = globals()["globalPavage"].getTilePolygon()

            geom = geom.intersection(tileGeom)
            geoms = globals()["globalPavage"].getImagesGeomPavage(
                geom, self.transformations, self.patternPositions
            )
            newGeom = geoms[0]
            for g in geoms[1:]:
                newGeom.addPartGeometry(g)

            return newGeom
        except Exception:
            return None
