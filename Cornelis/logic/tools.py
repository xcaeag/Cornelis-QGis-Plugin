import processing
from qgis.utils import iface

from qgis.core import (
    QgsLayerTreeLayer,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsProcessingUtils,
)

def getRecursiveLayers(layers: dict, node, checkedOnly: bool = True):
    """Get layers dict from group, only checked ones possibly

    :param layers: dict to append
    :type layers: dict
    :param node: group to explore
    :type node: QgsLayerTree
    :return: None (layers updated)
    """
    for c in node.children():
        if not checkedOnly or (checkedOnly and c.itemVisibilityChecked()):
            if isinstance(c, QgsLayerTreeLayer) and (
                isinstance(c.layer(), QgsVectorLayer)
                or isinstance(c.layer(), QgsRasterLayer)
            ):
                layers[c.layer().id()] = c.layer()

            else:
                getRecursiveLayers(layers, c, checkedOnly)


def getLayers(checkedOnly: bool = True) -> dict:
    """Get layers dict from legend root, only checked ones possibly

    :return: layers dict (layer id is the key)
    :rtype: dict
    """
    layers = {}
    node = QgsProject.instance().layerTreeRoot()
    getRecursiveLayers(layers, node, checkedOnly)
    return layers


def cliprasterbyextent(rasterLayer, extent):
    crs = iface.mapCanvas().mapSettings().destinationCrs()
    extentStr = "{},{},{},{} [{}]".format(
        extent.xMinimum(),
        extent.xMaximum(),
        extent.yMinimum(),
        extent.yMaximum(),
        crs.authid(),
    )

    r = processing.run(
        "gdal:cliprasterbyextent",
        {
            "INPUT": rasterLayer,
            "PROJWIN": extentStr,
            "OVERCRS": False,
            "NODATA": None,
            "OPTIONS": None,
            "DATA_TYPE": 0,
            "EXTRA": "",
            "OUTPUT": QgsProcessingUtils.generateTempFilename("clip.tif"),
        },
    )

    return r["OUTPUT"]


def warpreproject(r, crs):
    r = processing.run(
        "gdal:warpreproject",
        {
            "INPUT": r,
            "SOURCE_CRS": None,
            "TARGET_CRS": crs,
            "RESAMPLING": 0,
            "NODATA": None,
            "TARGET_RESOLUTION": None,
            "OPTIONS": "",
            "DATA_TYPE": 0,
            "TARGET_EXTENT": None,
            "TARGET_EXTENT_CRS": None,
            "MULTITHREADING": False,
            "EXTRA": "",
            "OUTPUT": QgsProcessingUtils.generateTempFilename("project.tif"),
        },
    )

    return r["OUTPUT"]
