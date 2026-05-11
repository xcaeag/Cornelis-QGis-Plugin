import numpy as np
import processing
from qgis.utils import iface


try:
    from skimage.draw import polygon
    from scipy.interpolate import RegularGridInterpolator

    SUPPORT_RASTER = True
except ImportError:
    SUPPORT_RASTER = False

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


def updateGeotiff(ds, arr, nodatavalue=None):
    """Update tif file (gdal GDALDataset)

    :param ds: Gdal dataset
    :type ds: GDALDataset
    :return: None
    """
    if len(arr.shape) == 3:
        Z, _, _ = arr.shape
    if len(arr.shape) == 2:
        Z = 1

    for b in range(Z):
        data = arr if (len(arr.shape) == 2) else arr[b]
        band = ds.GetRasterBand(b + 1)
        if nodatavalue is not None:
            band.SetNoDataValue(nodatavalue)
        band.WriteArray(data)
        band.FlushCache()
        band.ComputeStatistics(False)


def toPix(raster, pts):
    """Transforme un tableau de coordonnées carte (xy) en un tableau de coordonnées en pixels (raster)"""
    xmin, _, _, ymax = raster.extent().toRectF().getCoords()
    r = []
    xpixmin = ypixmin = xpixmax = ypixmax = None
    for pt in pts:
        xpix = round((pt[0] - xmin) / raster.rasterUnitsPerPixelX())
        ypix = round((ymax - pt[1]) / raster.rasterUnitsPerPixelY())
        r.append((xpix, ypix))

    allx, ally = list(zip(*r))
    xpixmin, ypixmin = (min(allx), min(ally))
    xpixmax, ypixmax = (max(allx), max(ally))

    return (r, xpixmin, ypixmin, xpixmax, ypixmax)


def calculer_transformation_affine(poly_source, poly_cible):
    """
    Calcule la matrice de transformation affine entre deux polygones.

    Args:
        poly_source: array Nx2 de coordonnées (x, y) du polygone source
        poly_cible: array Nx2 de coordonnées (x, y) du polygone cible

    Returns:
        matrice de transformation 2x3
    """
    if len(poly_source) < 3 or len(poly_cible) < 3:
        raise ValueError("Les polygones doivent avoir au moins 3 points")

    # Utiliser les 3 premiers points pour calculer la transformation affine
    src_pts = np.float32(poly_source[:3])
    dst_pts = np.float32(poly_cible[:3])

    # Résoudre le système d'équations pour la transformation affine
    # [x']   [a b c] [x]
    # [y'] = [d e f] [y]
    #                [1]

    # Construire le système d'équations linéaires
    A = np.zeros((6, 6))
    b = np.zeros(6)

    for i in range(3):
        # Équation pour x'
        A[2 * i, 0] = src_pts[i, 0]  # a
        A[2 * i, 1] = src_pts[i, 1]  # b
        A[2 * i, 2] = 1  # c
        b[2 * i] = dst_pts[i, 0]

        # Équation pour y'
        A[2 * i + 1, 3] = src_pts[i, 0]  # d
        A[2 * i + 1, 4] = src_pts[i, 1]  # e
        A[2 * i + 1, 5] = 1  # f
        b[2 * i + 1] = dst_pts[i, 1]

    # Résoudre le système
    params = np.linalg.solve(A, b)

    # Construire la matrice de transformation 2x3
    matrice = np.array(
        [[params[0], params[1], params[2]], [params[3], params[4], params[5]]]
    )

    return matrice


def inverser_transformation_affine(matrice):
    """
    Inverse une matrice de transformation affine 2x3.

    Args:
        matrice: array 2x3 de transformation affine

    Returns:
        matrice inverse 2x3
    """
    # Extraire la partie linéaire (2x2) et le vecteur de translation
    A = matrice[:, :2]
    t = matrice[:, 2]

    # Inverser la partie linéaire
    A_inv = np.linalg.inv(A)

    # Calculer le nouveau vecteur de translation
    t_inv = -A_inv @ t

    # Construire la matrice inverse
    matrice_inv = np.hstack([A_inv, t_inv.reshape(-1, 1)])

    return matrice_inv


def copyPasteRasterTile(image, poly_source, poly_cible, methode_interpolation="linear"):
    """
    Copie une région polygonale vers une autre position avec transformation.

    Args:
        image: array numpy (H, W) ou (H, W, C)
        poly_source: array Nx2 de coordonnées (x, y) en pixels
        poly_cible: array Nx2 de coordonnées (x, y) en pixels
        methode_interpolation: 'nearest', 'linear', 'cubic'

    Returns:
        image_resultat: array numpy avec la région copiée
    """
    poly_source = np.array(poly_source, dtype=np.float32)
    poly_cible = np.array(poly_cible, dtype=np.float32)

    image_resultat = image.copy()

    matrice_transform = calculer_transformation_affine(poly_source, poly_cible)

    min_x_c = int(np.floor(poly_cible[:, 0].min()))
    max_x_c = int(np.ceil(poly_cible[:, 0].max()))
    min_y_c = int(np.floor(poly_cible[:, 1].min()))
    max_y_c = int(np.ceil(poly_cible[:, 1].max()))

    min_x_c = max(0, min_x_c)
    min_y_c = max(0, min_y_c)
    max_x_c = min(image.shape[1], max_x_c)
    max_y_c = min(image.shape[0], max_y_c)

    poly_cible_relatif = poly_cible.copy()
    poly_cible_relatif[:, 0] -= min_x_c
    poly_cible_relatif[:, 1] -= min_y_c

    rr_c, cc_c = polygon(
        poly_cible_relatif[:, 1],
        poly_cible_relatif[:, 0],
        shape=(max_y_c - min_y_c, max_x_c - min_x_c),
    )

    if max_y_c <= min_y_c or max_x_c <= min_x_c:
        return image

    masque_cible = np.zeros((max_y_c - min_y_c, max_x_c - min_x_c), dtype=bool)
    masque_cible[rr_c, cc_c] = True

    matrice_inv = inverser_transformation_affine(matrice_transform)

    h_cible, w_cible = max_y_c - min_y_c, max_x_c - min_x_c

    if len(image.shape) == 2:
        region_transformee = np.zeros((h_cible, w_cible))
    else:
        region_transformee = np.zeros((h_cible, w_cible, image.shape[2]))

    yy, xx = np.meshgrid(np.arange(h_cible), np.arange(w_cible), indexing="ij")
    coords_cible = np.stack([xx.ravel() + min_x_c, yy.ravel() + min_y_c], axis=1)

    coords_cible_homogene = np.hstack([coords_cible, np.ones((len(coords_cible), 1))])

    coords_source = (matrice_inv @ coords_cible_homogene.T).T

    x_src = coords_source[:, 0]
    y_src = coords_source[:, 1]

    if len(image.shape) == 2:
        interpolateur = RegularGridInterpolator(
            (np.arange(image.shape[0]), np.arange(image.shape[1])),
            image,
            method=methode_interpolation,
            bounds_error=False,
            fill_value=0,
        )
        valeurs = interpolateur(np.column_stack([y_src, x_src]))
        region_transformee = valeurs.reshape(h_cible, w_cible)
    else:
        for canal in range(image.shape[2]):
            interpolateur = RegularGridInterpolator(
                (np.arange(image.shape[0]), np.arange(image.shape[1])),
                image[:, :, canal],
                method=methode_interpolation,
                bounds_error=False,
                fill_value=0,
            )
            valeurs = interpolateur(np.column_stack([y_src, x_src]))
            region_transformee[:, :, canal] = valeurs.reshape(h_cible, w_cible)

    if len(image.shape) == 2:
        image_resultat[min_y_c:max_y_c, min_x_c:max_x_c][masque_cible] = (
            region_transformee[masque_cible]
        )
    else:
        for canal in range(image.shape[2]):
            image_resultat[min_y_c:max_y_c, min_x_c:max_x_c, canal][masque_cible] = (
                region_transformee[:, :, canal][masque_cible]
            )

    return image_resultat
