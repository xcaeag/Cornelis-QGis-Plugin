from qgis.core import (QgsLayerTreeLayer, QgsProject,
                       QgsRasterLayer, QgsVectorLayer)


def getRecursiveLayers(layers: dict, node, checkedOnly: bool = True):
    """Get layers dict from group, only checked ones possibly

    :param layers: dict to append
    :type layers: dict
    :param node: group to explore
    :type node: QgsLayerTree
    :return: None (layers updated)
    """
    for c in node.children():
        if isinstance(c, QgsLayerTreeLayer) and (
            isinstance(c.layer(), QgsVectorLayer)
            or isinstance(c.layer(), QgsRasterLayer)
        ):
            if not checkedOnly or (checkedOnly and c.itemVisibilityChecked()):
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

