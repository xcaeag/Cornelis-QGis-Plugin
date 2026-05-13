import numpy as np
import processing
from qgis.utils import iface


try:
    from skimage.draw import polygon
    from scipy.interpolate import RegularGridInterpolator

    from skimage.draw import polygon
    from scipy.linalg import orthogonal_procrustes

    SUPPORT_RASTER = True
except ImportError:
    SUPPORT_RASTER = False

from qgis.core import (
    QgsLayerTreeLayer,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsProcessingUtils,
    QgsCoordinateReferenceSystem,
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


def newRaster(rmodel, extent):
    crs = iface.mapCanvas().mapSettings().destinationCrs()
    extentStr = "{},{},{},{} [{}]".format(
        extent.xMinimum(),
        extent.xMaximum(),
        extent.yMinimum(),
        extent.yMaximum(),
        crs.authid(),
    )
    r = processing.run(
        "native:createconstantrasterlayer",
        {
            "EXTENT": extentStr,
            "TARGET_CRS": QgsCoordinateReferenceSystem(crs.authid()),
            "PIXEL_SIZE": rmodel.rasterUnitsPerPixelX(),
            "NUMBER": 0,
            "OUTPUT_TYPE": 5,
            "CREATE_OPTIONS": None,
            "OUTPUT": QgsProcessingUtils.generateTempFilename("new.tif"),
        },
    )
    return r["OUTPUT"]


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


def copier_region_avec_transformation(
    image,
    poly_source,
    poly_cible,
    methode_interpolation="linear",
    autoriser_reflexion=True,
):
    """
    Copie une région polygonale vers une autre position avec transformation RIGIDE.

    Args:
        image: array numpy (H, W) ou (H, W, C)
        poly_source: array Nx2 de coordonnées (x, y) en pixels
        poly_cible: array Nx2 de coordonnées (x, y) en pixels
        methode_interpolation: 'nearest', 'linear', 'cubic'
        autoriser_reflexion: si True, autorise les symétries

    Returns:
        image_resultat: array numpy avec la région copiée
    """
    poly_source = np.array(poly_source, dtype=np.float32)
    poly_cible = np.array(poly_cible, dtype=np.float32)

    # Analyser la transformation
    # info_transform = analyser_transformation(poly_source, poly_cible)

    """print(f"\n📊 Analyse de la transformation:")
    print(f"   Translation: {info_transform['translation_norme']:.2f} pixels")
    print(f"   Rotation: {info_transform['rotation_degres']:.2f}°")
    print(f"   Échelle moyenne: {info_transform['echelle_moyenne']:.4f}")
    print(f"   Variance d'échelle: {info_transform['echelle_variance']:.6f}")
    print(f"   Réflexion: {'Oui' if info_transform['a_reflexion'] else 'Non'}")
    print(
        f"   Transformation rigide: {'✓' if info_transform['est_rigide'] else '✗ ATTENTION: déformation détectée!'}"
    )"""

    image_resultat = image.copy()

    # Calculer la transformation rigide
    if autoriser_reflexion:
        matrice_transform = calculer_transformation_rigide(poly_source, poly_cible)
    else:
        matrice_transform = calculer_transformation_rigide_sans_reflexion(
            poly_source, poly_cible
        )

    # Calculer la bounding box de la région cible
    min_x_c = int(np.floor(poly_cible[:, 0].min()))
    max_x_c = int(np.ceil(poly_cible[:, 0].max()))
    min_y_c = int(np.floor(poly_cible[:, 1].min()))
    max_y_c = int(np.ceil(poly_cible[:, 1].max()))

    # Clipper aux dimensions
    min_x_c = max(0, min_x_c)
    min_y_c = max(0, min_y_c)
    max_x_c = min(image.shape[1], max_x_c)
    max_y_c = min(image.shape[0], max_y_c)

    # Créer le masque de la région cible
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

    # Inverser la transformation
    matrice_inv = inverser_transformation_affine(matrice_transform)

    h_cible, w_cible = max_y_c - min_y_c, max_x_c - min_x_c

    if len(image.shape) == 2:
        region_transformee = np.zeros((h_cible, w_cible))
    else:
        region_transformee = np.zeros((h_cible, w_cible, image.shape[2]))

    # Créer une grille de coordonnées pour la région cible
    yy, xx = np.meshgrid(np.arange(h_cible), np.arange(w_cible), indexing="ij")
    coords_cible = np.stack([xx.ravel() + min_x_c, yy.ravel() + min_y_c], axis=1)

    # Ajouter colonne de 1 pour transformation affine
    coords_cible_homogene = np.hstack([coords_cible, np.ones((len(coords_cible), 1))])

    # Appliquer la transformation inverse
    coords_source = (matrice_inv @ coords_cible_homogene.T).T

    # Interpoler les valeurs
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

    # Appliquer le masque et copier dans l'image résultat
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


def analyser_transformation(poly_source, poly_cible):
    """
    Analyse le type de transformation entre deux polygones.

    Args:
        poly_source: array Nx2 de coordonnées (x, y)
        poly_cible: array Nx2 de coordonnées (x, y)

    Returns:
        dict avec les informations sur la transformation
    """
    src = np.array(poly_source, dtype=np.float64)
    dst = np.array(poly_cible, dtype=np.float64)

    # Calculer les centres de masse
    src_centroid = np.mean(src, axis=0)
    dst_centroid = np.mean(dst, axis=0)

    # Translation
    translation = dst_centroid - src_centroid

    # Centrer les polygones
    src_centered = src - src_centroid
    dst_centered = dst - dst_centroid

    # Calculer l'angle de rotation moyen
    angles = []
    for i in range(len(src)):
        angle_src = np.arctan2(src_centered[i, 1], src_centered[i, 0])
        angle_dst = np.arctan2(dst_centered[i, 1], dst_centered[i, 0])
        angles.append(angle_dst - angle_src)

    angle_moyen = np.mean(angles)
    angle_degres = np.degrees(angle_moyen)

    # Calculer les échelles (pour détecter les déformations)
    dist_src = np.sqrt(np.sum(src_centered**2, axis=1))
    dist_dst = np.sqrt(np.sum(dst_centered**2, axis=1))

    echelles = dist_dst / (dist_src + 1e-10)
    echelle_moyenne = np.mean(echelles)
    echelle_variance = np.var(echelles)

    # Vérifier s'il y a une réflexion
    # Calculer l'aire signée du polygone
    def aire_signee(poly):
        x, y = poly[:, 0], poly[:, 1]
        return 0.5 * np.sum(
            x[:-1] * y[1:] - x[1:] * y[:-1] + x[-1] * y[0] - x[0] * y[-1]
        )

    aire_src = aire_signee(src)
    aire_dst = aire_signee(dst)
    reflexion = (aire_src * aire_dst) < 0

    info = {
        "translation": translation,
        "translation_norme": np.linalg.norm(translation),
        "rotation_radians": angle_moyen,
        "rotation_degres": angle_degres,
        "echelle_moyenne": echelle_moyenne,
        "echelle_variance": echelle_variance,
        "a_reflexion": reflexion,
        "est_rigide": echelle_variance < 0.01 and abs(echelle_moyenne - 1.0) < 0.1,
    }

    return info


def calculer_transformation_rigide(poly_source, poly_cible):
    """
    Calcule la transformation rigide (rotation + translation + réflexion éventuelle)
    entre deux polygones SANS déformation ni étirement.

    Args:
        poly_source: array Nx2 de coordonnées (x, y) du polygone source
        poly_cible: array Nx2 de coordonnées (x, y) du polygone cible

    Returns:
        matrice de transformation 2x3
    """
    if len(poly_source) < 3 or len(poly_cible) < 3:
        raise ValueError("Les polygones doivent avoir au moins 3 points")

    # Utiliser tous les points disponibles pour une meilleure estimation
    src = np.array(poly_source, dtype=np.float64)
    dst = np.array(poly_cible, dtype=np.float64)

    # Centrer les points (retirer la moyenne)
    src_centroid = np.mean(src, axis=0)
    dst_centroid = np.mean(dst, axis=0)

    src_centered = src - src_centroid
    dst_centered = dst - dst_centroid

    # Calculer la matrice de rotation optimale (Procrustes)
    # Cette méthode préserve les distances et les angles
    R, _ = orthogonal_procrustes(src_centered, dst_centered)

    # Vérifier si c'est une réflexion (déterminant négatif)
    if np.linalg.det(R) < 0:
        # C'est une réflexion, on la garde
        pass

    # Calculer la translation
    t = dst_centroid - R @ src_centroid

    # Construire la matrice de transformation 2x3
    matrice = np.hstack([R, t.reshape(-1, 1)])

    return matrice


def calculer_transformation_rigide_sans_reflexion(poly_source, poly_cible):
    """
    Calcule la transformation rigide (rotation + translation uniquement)
    SANS réflexion, SANS déformation.

    Args:
        poly_source: array Nx2 de coordonnées (x, y) du polygone source
        poly_cible: array Nx2 de coordonnées (x, y) du polygone cible

    Returns:
        matrice de transformation 2x3
    """
    src = np.array(poly_source, dtype=np.float64)
    dst = np.array(poly_cible, dtype=np.float64)

    # Centrer les points
    src_centroid = np.mean(src, axis=0)
    dst_centroid = np.mean(dst, axis=0)

    src_centered = src - src_centroid
    dst_centered = dst - dst_centroid

    # Méthode SVD pour trouver la rotation optimale
    H = src_centered.T @ dst_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # Forcer le déterminant à être positif (rotation pure, pas de réflexion)
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # Calculer la translation
    t = dst_centroid - R @ src_centroid

    # Construire la matrice de transformation 2x3
    matrice = np.hstack([R, t.reshape(-1, 1)])

    return matrice
