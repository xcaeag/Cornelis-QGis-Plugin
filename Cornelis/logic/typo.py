# -*- coding: utf-8 -*-

from enum import Enum


class Typo1(Enum):
    T1 = "1"
    T1G = "1G"
    T1S = "1S"
    T2 = "2"
    T2G = "2G"
    T2S = "2S"
    T3 = "3"
    T3S = "3S"
    T4 = "4"
    T4S = "4S"
    T6 = "6"


class Typo(Enum):
    """Type de pavage

    Nomenclature : https://fr.tessellations-nicolas.com/methode.php
    """

    # TYPE 1 (p1) Translations
    T1a = "1a"
    T1b = "1b"

    # TYPE 1G (pg) Réflexion glissée + translations
    T1Ga = "1Ga"
    T1Gb = "1Gb"
    T1Gc = "1Gc"
    T1Gd = "1Gd"

    # TYPE 1S (cm) Translations
    T1Sa = "1Sa"
    T1Sb = "1Sb"

    # TYPE 2 (p2) Rotation 180° + translations
    T2a = "2a"
    T2b = "2b"
    T2c = "2c"
    T2d = "2d"
    T2e = "2e"

    # TYPE 2G (pgg) Rotation 180° + réflexion glissée + translations
    T2Ga = "2Ga"
    T2Gb = "2Gb"
    T2Gc = "2Gc"
    T2Gd = "2Gd"
    T2Ge = "2Ge"
    T2Gf = "2Gf"
    T2Gg = "2Gg"
    T2Gh = "2Gh"

    # TYPE 2S (pmg) Rotation 180° + translations
    T2Sa = "2Sa"
    T2Sb = "2Sb"
    T2Sc = "2Sc"

    # TYPE 3 (p3) 2 rotations 120° + translations
    T3a = "3a"
    T3b = "3b"

    # TYPE 3S (p31m) 2 rotations 120° + translations
    T3Sa = "3Sa"

    # TYPE 4 (p4) 3 rotations 90° + translations
    T4a = "4a"
    T4b = "4b"
    T4c = "4c"

    # TYPE 4S (p4g) 3 rotations 90° + translations
    T4Sa = "4Sa"

    # TYPE 6 (p6) Rotations 180° + 2 rotations 120° + translation
    T6a = "6a"
    T6b = "6b"
    T6c = "6c"
    T6d = "6d"


TypoTree = {
    Typo1.T1: {"name": "1. Translations", "types": [Typo.T1a, Typo.T1b]},
    Typo1.T1G: {
        "name": "1G. Réflexion glissée + translations",
        "types": [Typo.T1Ga, Typo.T1Gb, Typo.T1Gc, Typo.T1Gd],
    },
    Typo1.T1S: {"name": "1S. Translations", "types": [Typo.T1Sa, Typo.T1Sb]},
    Typo1.T2: {
        "name": "2. Rotation 180° + translations",
        "types": [Typo.T2a, Typo.T2b, Typo.T2c, Typo.T2d, Typo.T2e],
    },
    Typo1.T2G: {
        "name": "2G. Rotation 180° + réflexion glissée + translations",
        "types": [
            Typo.T2Ga,
            Typo.T2Gb,
            Typo.T2Gc,
            Typo.T2Gd,
            Typo.T2Ge,
            Typo.T2Gf,
            Typo.T2Gg,
            Typo.T2Gh,
        ],
    },
    Typo1.T2S: {
        "name": "2S. Rotation 180° + translations",
        "types": [Typo.T2Sa, Typo.T2Sb, Typo.T2Sc],
    },
    Typo1.T3: {
        "name": "3. 2 rotations 120° + translations",
        "types": [Typo.T3a, Typo.T3b],
    },
    Typo1.T3S: {"name": "3S. 2 rotations 120° + translations", "types": [Typo.T3Sa]},
    Typo1.T4: {
        "name": "4. 3 rotations 90° + translations",
        "types": [Typo.T4a, Typo.T4b, Typo.T4c],
    },
    Typo1.T4S: {"name": "4S. 3 rotations 90° + translations", "types": [Typo.T4Sa]},
    Typo1.T6: {
        "name": "6. Rotations 180° + 2 rotations 120° + translation",
        "types": [Typo.T6a, Typo.T6b, Typo.T6c, Typo.T6d],
    },
}

"""

    "name": Nom du type de pavage
    "type": Le type de pavage selon la nomenclature
    "subtype": Le sous-type,
    "form": La forme de la tuile,
    "controls": {  Les points de contrôles
        "pn": {    Un nom de point  (p0=(0,0) est implicite, à ne pas utiliser)
            "pos": Un tuple de coordonnées ou une transformation textuelle
            "mouse":  Actions a effectuer sur le mouvement de la souris : affecte le pavage, ou un point donné
        },
        ...
    },
    "seeds": {  Les segments initiaux (éditables)
        "s1": ["p0", "p1"],  Le premier segment constitué des deux points prédéfinis p0 et p1
        ...
    },
    "images": {  Les images des segments initiaux (non éditables)
        "i1": {"s1":"T(p0,p2)"}
        ...
    },
    "tile": ["-s1", "+s2", "+i1", "-i2"],
    "pattern": {},
    "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
"""

TYPES_PAVAGES = {
    # -------------------- TYPE 1 (p1) Translations ----------------------------
    Typo.T1a: {
        "name": "Type 1a",
        "type": "1",
        "subtype": "a",
        "form": "Parallélogramme",
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2)"},
            "p3": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
        },
        "seeds": {"s1": ["p0", "p1"], "s2": ["p0", "p2"]},
        "images": {"i1": ["s1", "T(p0,p2)"], "i2": ["s2", "T(p0,p1)"]},
        "tile": ["-s1", "+s2", "+i1", "-i2"],
        "pattern": {},
        "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T1b: {
        "name": "Type 1b",
        "type": "1",
        "subtype": "b",
        "form": "Hexagone",
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);ph=T(p1,pb,p2)",
            },
            "pb": {"pos": (0.5, -0.2), "mouse": "move(pb);ph=T(p1,pb,p2)"},
            "p2": {
                "pos": (0, 0.7),
                "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2);ph=T(p1,pb,p2)",
            },
            "p3": {"pos": (1, 0.7), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "ph": {"pos": (0.5, 0.9)},
        },
        "seeds": {"s1": ["p1", "pb"], "s2": ["pb", "p0"], "s3": ["p0", "p2"]},
        "images": {
            "i1": ["s1", "T(pb,p2)"],
            "i2": ["s2", "T(p0,ph)"],
            "i3": ["s3", "T(p0,p1)"],
        },
        "tile": ["+s1", "+s2", "+s3", "-i1", "-i2", "-i3"],
        "pattern": {},
        "pavage": {"x": "T(p0,p1)", "y": "T(p0,ph)"},
    },
    # -------------------- TYPE 1G (pg) Réflexion glissée + translations ----------------------------
    Typo.T1Ga: {
        "name": "Type 1Ga",
        "type": "1G",
        "subtype": "a",
        "form": "Parallélogramme",
        "fxy": (0.8, 0.8),
        "controls": {
            "p1": {
                "pos": (1.5, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2)",
            },
            "p3": {
                "pos": (-0.3, 0.75),
                "mouse": "move(p3)",
                "constraints": "ontheline(p0,p1,p3)",
            },
            "p2": {"pos": (0, 1.5), "mouse": "stretch_y(p0,p2,p1)"},
            "ps": {
                "pos": (1.5, 1.5),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
        },
        "seeds": {"s1": ["p1", "p0"], "s2": ["p0", "p3"]},
        "images": {
            "i1": ["s1", "F(p0,p2,p0);T(p0,p3);T(p0,p1)"],
            "i2": ["s2", "T(p0,p1)"],
        },
        "tile": ["+s1", "+s2", "+i1", "-i2"],
        "pattern": {"1": "Fv(p0,p2,p3);T(p0,p1);T(p3,p2)"},
        "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T1Gb: {
        "name": "Type 1Gb",
        "type": "1G",
        "subtype": "b",
        "form": "Losange",
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2)",
            },
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {"pos": (0, 0.5)},
            "p5": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "p6": {
                "pos": (1.2, 0.5),
                "mouse": "move(p6)",
                "constraints": "ontheline(p0,p1,p6)",
            },
        },
        "seeds": {"s1": ["p6", "p1"], "s2": ["p1", "p3"]},
        "images": {
            "i1": ["s1", "F(p0,p2,p6);T(p6,p5)"],
            "i2": ["s2", "F(p0,p2,p0);T(p3,p5)"],
        },
        "tile": ["+s1", "+s2", "+i2", "+i1"],
        "pattern": {"1": "Fv(p0,p2,p3);T(p3,p1)"},
        "pavage": {"x": "T(p3,p6)", "y": "T(p1,p5)"},
    },
    Typo.T1Gc: {
        "name": "Type 1Gc",
        "type": "1G",
        "subtype": "c",
        "form": "Hexagone",
        "fxy": (1.5, 1.5),
        "controls": {
            "p1": {"pos": (0.9, 0)},
            "p2": {"pos": (0, 0.8), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {
                "pos": (0.3, 0),
                "mouse": "move(s1);p9=T(p3,p4,p8);p9=F(p9,p0,p1,p8);ps=F(p3,p0,p1,p8)",
            },
            "p4": {"pos": (0, 0), "mouse": "move_all()"},
            "p5": {
                "pos": (-0.3, 0.4),
                "mouse": "move(p5)",
                "constraints": "ontheline(p0,p1,p5)",
            },
            "p8": {"pos": (0.6, 0.4), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p9": {"pos": (0.9, 0.4)},
            "ps": {
                "pos": (0.3, 0.8),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
        },
        "seeds": {"s1": ["p8", "p3"], "s2": ["p3", "p4"], "s3": ["p4", "p5"]},
        "images": {
            "i1": ["s1", "F(p0,p2,p3);T(p3,p8)"],
            "i2": ["s2", "T(p4,p2)"],
            "i3": ["s3", "F(p0,p2,p4);T(p4,p5)"],
        },
        "tile": ["+s1", "+s2", "+s3", "+i3", "-i2", "+i1"],
        "pattern": {"1": "Fv(p0,p2,p3);T(p3,p8)"},
        "pavage": {"x": "T(p5,p9)", "y": "T(p4,p2)"},
    },
    Typo.T1Gd: {
        "name": "Type 1Gd",
        "type": "1G",
        "subtype": "d",
        "form": "Hexagone",
        "controls": {
            "p2": {"pos": (0, 0.6), "mouse": "stretch_y(p0,p2,p1)"},
            "pb": {
                "pos": "R3(p2,p0)",
                "mouse": "move(pb);ph=F(pb,p0,p1,p0);ph=T(ph,p0,p2)",
            },
            "p1": {"pos": "R3(p0,pb)", "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p3": {
                "pos": "R3(pb,p1)",
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {"pos": "R3(p1,p3)"},
        },
        "seeds": {"s1": ["p1", "pb"], "s2": ["pb", "p0"], "s3": ["p0", "p2"]},
        "images": {
            "i1": ["s1", "F(p0,p2,pb);T(pb,p3)"],
            "i2": ["s2", "F(p0,p2,pb);T(pb,p2)"],
            "i3": ["s3", "T(p2,p3)"],
        },
        "tile": ["+s1", "+s2", "+s3", "+i2", "+i1", "-i3"],
        "pattern": {"1": "Fv(p0,p2,p0);T(p2,pb)"},
        "pavage": {"x": "T(p0,p1)", "y": "T(ph,pb);T(p2,p0)"},
    },
    # -------------------- TYPE 1S (cm) Translations ----------------------------
    Typo.T1Sa: {
        "name": "Type 1Sa",
        "type": "1S",
        "subtype": "a",
        "form": "Losange",
        "fxy": (1.3, 1.3),
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "ps": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "pq14": {"pos": (0.25, 0)},
            "pq34": {"pos": (0.75, 0)},
            "p3": {"pos": (0.5, 0)},
            "p4": {"pos": (0, 0.5)},
            "p5": {"pos": (0.5, 1)},
        },
        "seeds": {"s1": ["p3", "p4"]},
        "images": {
            "i1": ["s1", "F(p0,p2,pq14);T(p0,p4)"],
            "i2": ["s1", "F(p3,p5,p3)"],
            "i3": ["i2", "F(p0,p2,pq34);T(p0,p4)"],
        },
        "tile": ["+s1", "+i1", "-i3", "-i2"],
        "pattern": {},
        "pavage": {"x": "T(p3,p4)", "y": "T(p4,p5)"},
    },
    Typo.T1Sb: {
        "name": "Type 1Sb",
        "type": "1S",
        "subtype": "b",
        "form": "Hexagone",
        "controls": {
            "p1": {"pos": (0.6, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "p01": {"pos": (0.3, 0)},
            "p3": {"pos": (0.6, 0.5)},
            "p4": {"pos": (-0.6, 0.5)},
            "p5": {"pos": (0.3, 1)},
            "ps": {"pos": (0.6, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
        },
        "seeds": {"s1": ["p3", "p01"], "s2": ["p01", "p0"]},
        "images": {
            "i1": ["s1", "F(p0,p2,p01);T(p01,p3)"],
            "i2": ["s2", "T(p0,p2)"],
            "i3": ["s2", "F(p0,p2,p0)"],
            "i4": ["s1", "F(p0,p2,p0)"],
            "i5": ["i1", "F(p0,p2,p0)"],
            "i6": ["i2", "F(p0,p2,p0)"],
        },
        "tile": ["+s1", "+s2", "-i3", "-i4", "-i5", "+i6", "-i2", "+i1"],
        "pattern": {},
        "pavage": {"x": "T(p4,p01)", "y": "T(p4,p5)"},
    },
    # -------------------- TYPE 2 (p2) Rotation 180° + translations ----------------------------
    Typo.T2a: {
        "name": "Type 2a",
        "type": "2",
        "subtype": "a",
        "form": "Triangle",
        "fxy": (1.2, 1.2),
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2)"},
            "ps": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "p01": {"pos": (0.5, 0), "visible": "R"},
            "p02": {"pos": (0, 0.5), "visible": "R"},
            "p12": {"pos": (0.5, 0.5), "visible": "R"},
        },
        "seeds": {
            "s1": ["p1", "p01"],
            "s2": ["p0", "p02"],
            "s3": ["p2", "p12"],
        },
        "images": {
            "i1": ["s1", "R2(p01)"],
            "i2": ["s2", "R2(p02)"],
            "i3": ["s3", "R2(p12)"],
        },
        "tile": ["+s1", "-i1", "+s2", "-i2", "+s3", "-i3"],
        "pattern": {"1": "R2(p12)"},
        "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T2b: {
        "name": "Type 2b",
        "type": "2",
        "subtype": "b",
        "form": "Quadrilatère",
        "fxy": (0.8, 0.8),
        "controls": {
            "p1": {
                "pos": (0.8, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2)",
            },
            "p2": {"pos": (0, 0.8), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {
                "pos": (0.8, 0.8),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "pb": {"pos": (0.4, -0.4)},
            "ph": {"pos": (0.4, 1.2)},
            "pg": {"pos": (-0.4, 0.4)},
            "pd": {"pos": (1.2, 0.4)},
        },
        "seeds": {
            "s1": ["pb", "p0"],
            "s2": ["pg", "p2"],
            "s3": ["ph", "p3"],
            "s4": ["pd", "p1"],
        },
        "images": {
            "i1": ["s1", "R2(p0)"],
            "i2": ["s2", "R2(p2)"],
            "i3": ["s3", "R2(p3)"],
            "i4": ["s4", "R2(p1)"],
        },
        "tile": ["+s1", "-i1", "+s2", "-i2", "+s3", "-i3", "+s4", "-i4"],
        "pattern": {"1": "R2(p0)"},
        "pavage": {"x": "T(pg,pd)", "y": "2xT(p0,p3)"},
    },
    Typo.T2c: {
        "name": "Type 2c",
        "type": "2",
        "subtype": "c",
        "form": "Parallélogramme",
        "controls": {
            "p1": {
                "pos": (1.5, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2)",
            },
            "p2": {"pos": (0, 0.75), "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2)"},
            "pb": {"pos": (0.75, 0), "visible": "R"},
            "ph": {"pos": (0.75, 0.75), "visible": "R"},
            "ps": {
                "pos": (1.5, 0.75),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
        },
        "seeds": {
            "s1": ["pb", "p0"],
            "s2": ["p0", "p2"],
            "s3": ["p2", "ph"],
        },
        "images": {
            "i1": ["s1", "R2(pb)"],
            "i2": ["s2", "T(p0,p1)"],
            "i3": ["s3", "R2(ph)"],
        },
        "tile": ["+s1", "+s2", "+s3", "-i3", "-i2", "-i1"],
        "pattern": {"1": "R2(pb)"},
        "pavage": {"x": "T(p0,p1)", "y": "2xT(p0,p2)"},
    },
    Typo.T2d: {
        "name": "Type 2d",
        "type": "2",
        "subtype": "d",
        "form": "Pentagone",
        "controls": {
            "p1": {
                "pos": (0.5, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2)",
            },
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2)"},
            "p3": {"pos": (0.5, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "p4": {"pos": (0.7, 0.5)},
            "p02": {"pos": (0, 0.5), "visible": "R"},
            "p34": {"pos": (0.6, 0.75), "visible": "R"},
            "p14": {"pos": (0.6, 0.25), "visible": "R"},
        },
        "seeds": {
            "s1": ["p1", "p0"],
            "s2": ["p0", "p02"],
            "s3": ["p3", "p34"],
            "s4": ["p4", "p14"],
        },
        "images": {
            "i1": ["s1", "T(p0,p2)"],
            "i2": ["s2", "R2(p02)"],
            "i3": ["s3", "R2(p34)"],
            "i4": ["s4", "R2(p14)"],
        },
        "tile": ["+s1", "+s2", "-i2", "-i1", "+s3", "-i3", "+s4", "-i4"],
        "pattern": {"1": "R2(p02)"},
        "pavage": {"x": "T(p3,p4);2xT(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T2e: {
        "name": "Type 2e",
        "type": "2",
        "subtype": "e",
        "form": "Hexagone",
        "controls": {
            "p2": {"pos": (0, 0.6), "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2)"},
            "pb": {"pos": "R3(p2,p0)"},
            "p1": {
                "pos": "R3(p0,pb)",
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "p3": {
                "pos": "R3(pb,p1)",
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {"pos": "R3(p1,p3)"},
            "p02": {"pos": "M(p0,p2)", "visible": "R"},
            "p3h": {"pos": "M(p3,ph)", "visible": "R"},
            "p13": {"pos": "M(p1,p3)", "visible": "R"},
            "p0b": {"pos": "M(p0,pb)", "visible": "R"},
        },
        "seeds": {
            "s1": ["p1", "pb"],
            "s2": ["pb", "p0b"],
            "s3": ["p0", "p02"],
            "s4": ["ph", "p3h"],
            "s5": ["p3", "p13"],
        },
        "images": {
            "i1": ["s1", "T(pb,p2)"],
            "i2": ["s2", "R2(p0b)"],
            "i3": ["s3", "R2(p02)"],
            "i4": ["s4", "R2(p3h)"],
            "i5": ["s5", "R2(p13)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+s3", "-i3", "-i1", "+s4", "-i4", "+s5", "-i5"],
        "pattern": {"1": "R2(p02)"},
        "pavage": {"x": "T(p0,p1);T(p0,ph)", "y": "T(pb,p2)"},
    },
    # -------------------- TYPE 2G (pgg) Rotation 180° + réflexion glissée + translations --------------------
    Typo.T2Ga: {
        "name": "Type 2Ga",
        "type": "2G",
        "subtype": "a",
        "form": "Triangle isocèle",
        "fxy": (1.5, 1.5),
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "ps": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "p01": {"pos": (0.5, 0), "visible": "R"},
            "p02": {"pos": (0, 0.5)},
            "ph": {"pos": (0.5, 0.5), "visible": "R"},
            "pb": {"pos": (0.5, -0.5)},
        },
        "seeds": {
            "s1": ["p1", "pb"],
            "s2": ["pb", "p01"],
        },
        "images": {
            "i1": ["s1", "F(p0,p1,p0);R2(p1,ph)"],
            "i2": ["s2", "R2(p01)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+i1"],
        "pattern": {
            "1": "R2(p01)",
            "2": "R2(p01);Fh(p0,p1,p0);T(pb,p0)",
            "3": "R2(p02)",
        },
        "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T2Gb: {
        "name": "Type 2Gb",
        "type": "2G",
        "subtype": "b",
        "form": "Quadrilatère",
        "fxy": (1.3, 1.3),
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "pb": {"pos": "M(p0,p1)"},
            "pg": {"pos": "M(p0,p2)"},
            "ph": {"pos": "M(p2,p3)"},
            "pd": {"pos": "M(p1,p3)"},
            "pbg": {"pos": "M(pb,pg)", "visible": "R"},
            "pgh": {"pos": "M(pg,ph)", "visible": "R"},
            "pbg2": {"pos": "T(pbg,pd,p0)"},
        },
        "seeds": {"s1": ["pd", "pb"], "s2": ["pb", "pbg"], "s3": ["pg", "pgh"]},
        "images": {
            "i1": ["s1", "F(p0,p2,pd);A(ph)"],
            "i2": ["s2", "R2(pbg)"],
            "i3": ["s3", "R2(pgh)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+s3", "-i3", "+i1"],
        "pattern": {"1": "R2(pbg)", "2": "T(pbg,pbg2);Fv(p0,p2,pbg2)", "3": "R2(pbg2)"},
        "pavage": {"x": "2xT(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T2Gc: {
        "name": "Type 2Gc",
        "type": "2G",
        "subtype": "c",
        "form": "Quadrilatère",
        "fxy": (1, 1.5),
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 0.5), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {"pos": (1, 0.5), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "pg": {
                "pos": (-0.2, 0.2),
                "mouse": "move(pg);ph=R2(pg,p2);pg2=R2(pg,p0);pd=F(pg,p0,p2,p0);pd=T(pd,p0,p3);pb=R2(pd,p3)",
            },
            "ph": {"pos": "R2(pg,p2)"},
            "pg2": {"pos": "R2(pg,p0)"},
            "pd": {"pos": "F(pg,p0,p2,p0);T(pd,p0,p3)"},
            "pb": {"pos": "R2(pd,p3)"},
        },
        "seeds": {"s1": ["pb", "pg"], "s2": ["pg", "p2"], "s3": ["pd", "p3"]},
        "images": {
            "i1": ["s1", "F(p0,p2,pb);T(pb,ph)"],
            "i2": ["s2", "R2(p2)"],
            "i3": ["s3", "R2(p3)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+i1", "+s3", "-i3"],
        "pattern": {"1": "R2(p2)", "2": "F(p0,p2,p2);T(p3,p0)", "3": "R2(p0)"},
        "pavage": {"x": "2xT(p0,p1)", "y": "2xT(p0,p2)"},
    },
    Typo.T2Gd: {
        "name": "Type 2Gd",
        "type": "2G",
        "subtype": "d",
        "form": "Rectangle",
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {"pos": (1, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
        },
        "seeds": {"s1": ["p1", "p0"], "s2": ["p0", "p2"]},
        "images": {
            "i1": ["s1", "F(p0,p2,p0);T(p0,p3)"],
            "i2": ["s2", "F(p0,p1,p0);T(p0,p3)"],
        },
        "tile": ["+s1", "+s2", "+i1", "+i2"],
        "pattern": {
            "1": "Fh(p0,p1,p0);T(p1,p2)",
            "2": "Fv(p0,p2,p0);T(p3,p0)",
            "3": "Fh(p0,p1,p0);T(p2,p1)",
        },
        "pavage": {"x": "2xT(p0,p1)", "y": "2xT(p0,p2)"},
    },
    Typo.T2Ge: {
        "name": "Type 2Ge",
        "type": "2G",
        "subtype": "e",
        "form": "Pentagone",
        "fxy": (1.4, 1.4),
        "controls": {
            "p1": {"pos": (0.8, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p1g": {"pos": (-0.8, 0)},
            "p2": {"pos": (0, 0.8), "mouse": "stretch_y(p0,p2,p1)"},
            "ps": {
                "pos": (0.8, 0.8),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {
                "pos": (0.3, 0.9),
                "mouse": "move(s3,pb,pdh,pdb)",  # ;move(pb);move(pdh);move(pdb)",
                "constraints": "ontheline(p0,p2,pb)",
            },
            "pb": {"pos": (0.3, 0.1)},
            "pd": {
                "pos": (0.5, 0.5),
                "mouse": "move(pd);ph=R2(pd,pdh);pb=R2(pd,pdb)",
                "constraints": "ontheline(p0,p1,pd)",
            },
            "p02": {"pos": "M(p0,p2)", "visible": "R"},
            "pdh": {"pos": "M(pd,ph)"},
            "pdb": {"pos": "M(pd,pb)"},
            "pg": {"pos": "R2(pd,p02)"},
            "pb2": {"pos": "R2(pb,p0)"},
        },
        "seeds": {"s1": ["pb", "p0"], "s2": ["p0", "p02"], "s3": ["ph", "pd"]},
        "images": {
            "i1": ["s1", "T(p0,p2)"],
            "i2": ["s2", "R2(p02)"],
            "i3": ["s3", "F(p0,p2,pd);T(pd,pb)"],
        },
        "tile": ["+s1", "+s2", "-i2", "-i1", "+s3", "+i3"],
        "pattern": {
            "1": "R2(p02)",
            "2": "Fv(p0,p2,pg);T(pg,pb2)",
            "3": "R2(p1g)",
        },
        "pavage": {"x": "2xT(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T2Gf: {
        "name": "Type 2Gf",
        "type": "2G",
        "subtype": "f",
        "form": "Pentagone",
        "controls": {
            "p1": {"pos": (0.8, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 0.8), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {
                "pos": (0.8, 0.8),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {
                "pos": (0.2, 1.0),
                "mouse": "move(ph);pg=R2(ph,p2);px=F(p3,p2,p3,ph);px=T(px,ph,p0)",
            },
            "pg": {"pos": "R2(ph,p2)"},
            "px": {"pos": "F(p3,p2,p3,ph);T(px,ph,p0)"},
        },
        "seeds": {
            "s1": ["px", "p0"],
            "s2": ["p0", "pg"],
            "s3": ["p2", "ph"],
        },
        "images": {
            "i1": ["s1", "F(p0,p2,p0);T(p0,p3)"],
            "i2": ["s2", "F(p0,p1,p0);T(p0,p3)"],
            "i3": ["s3", "R2(p2)"],
        },
        "tile": ["+s1", "+s2", "-i3", "+s3", "+i1", "+i2"],
        "pattern": {
            "1": "Fv(p0,p2,p3);T(p3,p0)",
            "2": "R2(p1)",
            "3": "Fv(p0,p2,p1);T(p2,p1)",
        },
        "pavage": {"x": "2xT(p0,p1)", "y": "2xT(p0,p2)"},
    },
    Typo.T2Gg: {
        "name": "Type 2Gg",
        "type": "2G",
        "subtype": "g",
        "form": "Hexagone",
        "fxy": (0.8, 0.8),
        "controls": {
            "p1": {"pos": (1.6, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p4": {"pos": (-1.6, 0.8), "visible": "R"},
            "p2": {"pos": (0, 0.8), "mouse": "stretch_y(p0,p2,p1)"},
            "ps": {
                "pos": (1.6, 0.8),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "pb": {"pos": (0.2, -0.6)},
            "px": {
                "pos": (0.6, -0.7),
                "mouse": "move(px);pz=T(px,pb,ph);py=R2(px,p0);py=F(py,p0,p1,p4);py=T(py,p4,p0)",
            },
            "pg": {"pos": "R2(pb,p0)", "mouse": "move(pg);ph=R2(pg,p2);pb=R2(pg,p0)"},
            "ph": {"pos": "R2(pg,p2)"},
            "pz": {"pos": "T(px,pb,ph)"},
            "py": {"pos": "R2(px,p0);F(py,p0,p1,p4);T(py,p4,p0)"},
        },
        "seeds": {
            "s1": ["px", "pb"],
            "s2": ["pb", "p0"],
            "s3": ["pg", "p2"],
            "s4": ["py", "px"],
        },
        "images": {
            "i1": ["s1", "T(pb,ph)"],
            "i2": ["s2", "R2(p0)"],
            "i3": ["s3", "R2(p2)"],
            "i4": ["s4", "F(p0,p2,py);T(py,pz)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+s3", "-i3", "-i1", "+i4", "+s4"],
        "pattern": {"1": "R2(p0)", "2": "Fv(p0,p2,p0);T(p0,p4)", "3": "R2(p4)"},
        "pavage": {"x": "2xT(p0,p1)", "y": "2xT(p0,p2)"},
    },
    Typo.T2Gh: {
        "name": "Type 2Gh",
        "type": "2G",
        "subtype": "h",
        "form": "Hexagone",
        "controls": {
            "p1": {"pos": (0.9, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 0.9), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {  # -> p8, p6
                "pos": (0.6, -0.3),
                "mouse": "move(p3);p6=F(p4,p0,p1,p3);p6=T(p6,p3,p7)",
            },
            "p4": {
                "pos": (0, -0.3),
                "mouse": "move(p4);p5=R2(p4,p0);p7=Z(p7,i2)",  # attention p7 dépend de i2... i2 ne doit pas dépendre de p7
            },
            "p5": {"pos": (0, 0.3), "visible": "R"},
            "p6": {"pos": (0.3, 0.6)},
            "p7": {
                "pos": (0.9, 0.6),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
        },
        "seeds": {
            "s1": ["p1", "p3"],
            "s2": ["p3", "p4"],
            "s3": ["p4", "p0"],
            "s4": ["p5", "p6"],
        },
        "images": {
            "i1": ["s1", "R2(p1)"],
            "i2": ["s2", "F(p0,p1,p4);R2(p3);A(p6)"],
            "i3": ["s3", "R2(p0)"],
            "i4": ["s4", "F(p0,p2,p5);R2(p5);A(p7)"],
        },
        "tile": ["+s1", "+s2", "+s3", "-i3", "+s4", "+i2", "+i4", "-i1"],
        "conf": ["patternfromsource"],
        "pattern": {
            "1": "R2(p0)",
            "2": "T(p3,p6);Fv(p0,p2,p6)",
            "3": "T(p1,p2);Fh(p0,p1,p2)",
        },
        "pavage": {"x": "2xT(p0,p1)", "y": "2xT(p0,p2)"},
    },
    # -------------------- TYPE 2S (pmg) Rotation 180° + translations --------------------
    Typo.T2Sa: {
        "name": "Type 2Sa",
        "type": "2S",
        "subtype": "a",
        "form": "Rectangle",
        "fxy": (1.3, 1.3),
        "controls": {
            "p1": {"pos": (0.5, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1)"},
            "ps": {"pos": (0.5, 1), "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)"},
            "p01": {
                "pos": (0.25, 0),
                "mouse": "move(p01)",
                "constraints": "ontheline(p0,p2,p01)",
            },
            "p3": {"pos": (0.5, 0.5), "visible": "R"},
        },
        "seeds": {"s1": ["p3", "p1"], "s2": ["p1", "p01"]},
        "images": {
            "i6": ["s1", "R2(p3)"],
            "i1": ["s2", "F(p0,p2,p01)"],
            "i2": ["s1", "F(p0,p2,p01)"],
            "i3": ["i6", "F(p0,p2,p01)"],
            "i4": ["i1", "T(p0,p2)"],
            "i5": ["s2", "T(p0,p2)"],
        },
        "tile": ["+s1", "+s2", "-i1", "-i2", "+i3", "+i4", "-i5", "-i6"],
        "pattern": {"1": "R2(p3)"},
        "pavage": {"x": "2xT(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T2Sb: {
        "name": "Type 2Sb",
        "type": "2S",
        "subtype": "b",
        "form": "Losange",
        "fxy": (1.8, 1.8),
        "controls": {
            "p1": {"pos": (0.4, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 0.4), "mouse": "stretch_y(p0,p2,p1)"},
            "p3": {
                "pos": (0.4, 0.4),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {
                "pos": (0.2, 0.7),
                "mouse": "move(ph);pg=R2(ph,p2);pb=R2(pg,p0);pd=R2(pb,p1)",
                "constraints": "ontheline(p0,p2,ph)",
            },
            "pb": {
                "pos": (0.2, -0.1),
                "mouse": "move(pb);pg=R2(pb,p0);ph=R2(pg,p2);pd=R2(ph,p3)",
                "constraints": "ontheline(p0,p2,pb)",
            },
            "pg": {"pos": "R2(ph,p2)"},
            "pd": {"pos": "R2(pb,p1)"},
        },
        "seeds": {
            "s1": ["pb", "p0"],
            "s2": ["p2", "ph"],
        },
        "images": {
            "i1": ["s1", "R2(p0)"],
            "i2": ["s2", "R2(p2)"],
            "i3": ["s1", "F(pb,ph,pb)"],
            "i4": ["i1", "F(pb,ph,pb)"],
            "i5": ["s2", "F(pb,ph,ph)"],
            "i6": ["i2", "F(pb,ph,ph)"],
        },
        "tile": ["+s1", "-i1", "-i2", "+s2", "-i5", "+i6", "+i4", "-i3"],
        "pattern": {"1": "R2(p0)"},
        "pavage": {"x": "T(pg,pd)", "y": "T(ph,pb)"},
    },
    Typo.T2Sc: {
        "name": "Type 2Sc",
        "type": "2S",
        "subtype": "c",
        "form": "Hexagone",
        "fxy": (1.4, 1.4),
        "controls": {
            "p1": {"pos": (0.6, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
            "p2": {"pos": (0, 0.4), "mouse": "stretch_y(p0,p2,p1)"},
            "pm": {"pos": (0.3, 0.2)},
            "p3": {
                "pos": (0.6, 0.4),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "pg": {"pos": (-0.15, 0.2)},
            "pd": {"pos": (0.75, 0.2)},
            "ph1": {
                "pos": "R2(pg,p2)",
                "mouse": "move(ph1);ph2=F(ph1,p0,p2,pm);pg=R2(ph1,p2);pb1=R2(pg,p0);pd=R2(ph2,p3);pb2=R2(pd,p1)",
            },
            "ph2": {"pos": "R2(pd,p3)"},
            "pb1": {"pos": "R2(pg,p0)"},
            "pb2": {"pos": "R2(pd,p1)"},
        },
        "seeds": {
            "s1": ["pb2", "pb1"],
            "s2": ["pb1", "p0"],
            "s3": ["pg", "p2"],
        },
        "images": {
            "i1": ["s1", "T(pb1,ph1)"],
            "i2": ["s2", "R2(p0)"],
            "i3": ["s3", "R2(p2)"],
            "i4": ["i3", "F(p0,p2,pm)"],
            "i5": ["s3", "F(p0,p2,pm)"],
            "i6": ["i2", "F(p0,p2,pm)"],
            "i7": ["s2", "F(p0,p2,pm)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+s3", "-i3", "-i1", "+i4", "-i5", "+i6", "-i7"],
        "pattern": {"1": "R2(p0)"},
        "pavage": {"x": "T(pg,pd);T(pb1,pb2)", "y": "T(ph1,pb1)"},
    },
    # -------------------- TYPE 3 (p3) 2 rotations 120° + translations --------------------
    Typo.T3a: {
        "name": "Type 3a",
        "type": "3",
        "subtype": "a",
        "form": "Losange",
        "controls": {
            "p1": {"pos": (1, 0), "mouse": "rotation(p0)"},
            "p3": {
                "pos": "-R6(p1,p0)",
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "p2": {"pos": "T(p3,p1,p3)"},
        },
        "seeds": {"s1": ["p1", "p0"], "s2": ["p0", "p3"]},
        "images": {"i1": ["s1", "R3(p1)"], "i2": ["s2", "R3(p3);R3(p3)"]},
        "tile": ["+s1", "+s2", "-i2", "-i1"],
        "pattern": {"1": "R3(p3)", "2": "R3(p3)"},
        "pavage": {"x": "T(p0,p1);T(p3,p1)", "y": "T(p0,p1);T(p0,p3)"},
    },
    Typo.T3b: {
        "name": "Type 3b",
        "type": "3",
        "subtype": "b",
        "form": "Hexagone",
        "controls": {  # rotations en p0, p1, ph
            "p2": {"pos": (0, 0.6), "visible": "R"},
            "pb": {"pos": "R3(p2,p0)"},
            "p1": {
                "pos": "R3(p0,pb)",
                "mouse": "rotation(p0)",
            },
            "p3": {
                "pos": "R3(pb,p1)",
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {
                "pos": "R3(p1,p3)",
                "mouse": "move(ph);p0=R3(ph,p2);p1=R3(p0,pb);py=-R3(p1,p2);px=-R3(ph,p2)",
            },
            "py": {"pos": "-R3(p1,p2)"},
            "px": {"pos": "-R3(ph,p2)"},
        },
        "seeds": {"s1": ["p1", "pb"], "s2": ["p0", "p2"], "s3": ["ph", "p3"]},
        "images": {
            "i1": ["s1", "-R3(pb)"],
            "i2": ["s2", "-R3(p2)"],
            "i3": ["s3", "-R3(p3)"],
        },
        "tile": ["+s1", "-i1", "+s2", "-i2", "+s3", "-i3"],
        "pattern": {"1": "R3(p2)", "2": "R3(p2)"},
        "pavage": {"x": "T(px,p1)", "y": "T(py,p0)"},
    },
    # -------------------- TYPE 3S (p31m) 2 rotations 120° + translations --------------------
    Typo.T3Sa: {
        "name": "Type 3Sa",
        "type": "3S",
        "subtype": "a",
        "form": "Losange",
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0)",
            },
            "p3": {
                "pos": "-R6(p1,p0)",
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "p2": {"pos": "T(p3,p1,p3)"},
        },
        "seeds": {"s1": ["p1", "p0"]},
        "images": {
            "i1": ["s1", "-R6(p0)"],
            "i2": ["i1", "-R3(p3)"],
            "i3": ["s1", "R3(p1)"],
        },
        "tile": ["+s1", "-i1", "+i2", "-i3"],
        "pattern": {"1": "R3(p3)", "2": "R3(p3)"},
        "pavage": {"x": "T(p0,p1);T(p3,p1)", "y": "T(p0,p1);T(p0,p3)"},
    },
    # -------------------- TYPE 4 (p4) 3 rotations 90° + translations --------------------
    Typo.T4a: {
        "name": "Type 4a",
        "type": "4",
        "subtype": "a",
        "form": "Triangle rectangle isocèle",
        "fxy": (1.5, 1.5),
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "p2": {"pos": (0, 1), "mouse": "rotation(p0)"},
            "p01": {"pos": (0.5, 0), "visible": "R"},
            "pm": {"pos": (0.5, 0.5), "visible": "R"},
        },
        "seeds": {"s1": ["p01", "p0"], "s2": ["p0", "pm"]},
        "images": {"i1": ["s1", "R2(p01)"], "i2": ["s2", "-R4(pm)"]},
        "tile": ["+s1", "+s2", "-i2", "-i1"],
        "pattern": {"1": "R4(pm)", "2": "R4(pm)", "3": "R4(pm)"},
        "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
    },
    Typo.T4b: {
        "name": "Type 4b",
        "type": "4",
        "subtype": "b",
        "form": "Carré",
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "p2": {"pos": (0, 1), "mouse": "rotation(p0)"},
            "p3": {"pos": (1, 1), "visible": "R"},
        },
        "seeds": {"s1": ["p1", "p0"], "s2": ["p2", "p3"]},
        "images": {
            "i1": ["s1", "-R4(p0)"],
            "i2": ["s2", "-R4(p3)"],
        },
        "tile": ["+s1", "-i1", "+s2", "-i2"],
        "pattern": {"1": "R4(p0)", "2": "R4(p0)", "3": "R4(p0)"},
        "pavage": {"x": "2xT(p0,p1)", "y": "2xT(p0,p2)"},
    },
    Typo.T4c: {
        "name": "Type 4c",
        "type": "4",
        "subtype": "c",
        "form": "Pentagone",
        "controls": {
            "p1": {
                "pos": (0.6, 0.2, 0),
                "mouse": "move(p1);pg=-R4(p1,p0);ph=R2(pg,p2);dx=-R4(ph,p0);dy=R4(p1,p0)",
            },
            "p2": {"pos": (0, 0.8), "mouse": "rotation(p0)"},
            "p3": {
                "pos": (0.8, 0.8, 0),
                "mouse": "stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "pg": {"pos": "-R4(p1,p0)"},
            "ph": {"pos": "R2(pg,p2)"},
            "dx": {"pos": "-R4(ph,p0)"},
            "dy": {"pos": "R4(p1,p0)"},
        },
        "seeds": {"s1": ["p1", "p0"], "s2": ["pg", "p2"], "s3": ["ph", "p3"]},
        "images": {
            "i1": ["s1", "-R4(p0)"],
            "i2": ["s2", "R2(p2)"],
            "i3": ["s3", "-R4(p3)"],
        },
        "tile": ["+s1", "-i1", "+s2", "-i2", "+s3", "-i3"],
        "pattern": {"1": "R4(p0)", "2": "R4(p0)", "3": "R4(p0)"},
        "pavage": {"x": "T(dx,p1)", "y": "T(ph,dy)"},
    },
    # -------------------- TYPE 4S (p4g) 3 rotations 90° + translations --------------------
    Typo.T4Sa: {
        "name": "Type 4Sa",
        "type": "4S",
        "subtype": "a",
        "form": "Carré",
        "fxy": (1.3, 1.3),
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "p2": {"pos": (0, 1), "mouse": "rotation(p0)"},
            "pm": {"pos": (0.5, 0.5), "visible": "R"},
            "pb": {"pos": (0.5, -0.5), "visible": "R"},
        },
        "seeds": {"s1": ["p1", "pm"]},
        "images": {
            "i1": ["s1", "R4(pm)"],
            "i2": ["i1", "R4(p0)"],
            "i3": ["i2", "R4(pb)"],
        },
        "tile": ["+s1", "-i1", "+i2", "-i3"],
        "pattern": {"1": "R4(pm)", "2": "R4(pm)", "3": "R4(pm)"},
        "pavage": {"x": "T(p0,p1);T(p0,p2)", "y": "T(p0,p1);T(p2,p0)"},
    },
    # -------------------- TYPE 6 (p6) Rotations 180° + 2 rotations 120° + translat. --------------------
    Typo.T6a: {
        "name": "Type 6a",
        "type": "6",
        "subtype": "a",
        "form": "Triangle équilatéral",
        "controls": {
            "p01": {"pos": (0.5, 0), "visible": "R"},
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "ph": {"pos": "-R6(p1,p0)", "visible": "R"},
            "p2": {"pos": "T(ph,p01,p0)", "mouse": "rotation(p0)"},
        },
        "seeds": {"s1": ["p01", "p0"], "s2": ["ph", "p1"]},
        "images": {"i1": ["s1", "R2(p01)"], "i2": ["s2", "R6(ph)"]},
        "tile": ["+s1", "-i2", "+s2", "-i1"],
        "pattern": {
            "1": "R6(ph)",
            "2": "R6(ph)",
            "3": "R6(ph)",
            "4": "R6(ph)",
            "5": "R6(ph)",
        },
        "pavage": {"x": "T(p0,p1);T(ph,p1)", "y": "T(p0,p1);T(p0,ph)"},
    },
    Typo.T6b: {
        "name": "Type 6b",
        "type": "6",
        "subtype": "b",
        "form": "Triangle isocèle",
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "pg": {"pos": "-R3(p1,p0)"},
            "p2": {
                "pos": "-R3(p0,pg)",
                "mouse": "rotation(p0)",
            },
            "p3": {"pos": "-R3(pg,p2)"},
            "pd": {"pos": "-R3(p2,p3)"},
            "p0d": {"pos": "M(p0,pd)", "visible": "R"},
            "p02": {"pos": "M(p0,p2)"},
            "p2d": {"pos": "M(p2,pd)"},
            "pm": {"pos": "M(p0,p3)"},
        },
        "seeds": {"s1": ["p1", "p0"], "s2": ["p0", "p0d"]},
        "images": {"i1": ["s1", "R3(p1)"], "i2": ["s2", "R2(p0d)"]},
        "tile": ["+s1", "+s2", "-i2", "-i1"],
        "pattern": {
            "1": "R2(p0d)",
            "2": "R3(pm)",
            "3": "R2(p02)",
            "4": "R2(p02);R3(pm)",
            "5": "R2(p2d)",
        },
        "pavage": {"x": "T(pg,p3)", "y": "T(pg,p1)"},
    },
    Typo.T6c: {
        "name": "Type 6c",
        "type": "6",
        "subtype": "c",
        "form": "Losange",
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p01,p1,pm);stretch_y(p01,pm,p1)",
            },
            "pg": {
                "pos": "-R3(p1,p0)",
                "mouse": "rotation(p0)",
            },
            "pd": {"pos": "R3(p0,p1)"},
            "p1d": {"pos": "M(p1,pd)"},
            "pm": {"pos": "M(pg,pd)", "visible": "R"},
            "p01": {"pos": "M(p0,p1)"},
            "p0g": {"pos": "M(p0,pg)"},
        },
        "seeds": {"s1": ["p1", "p01"], "s2": ["p01", "pm"]},
        "images": {"i1": ["s1", "R3(p1)"], "i2": ["s2", "-R6(pm)"]},
        "tile": ["+s1", "+s2", "-i2", "-i1"],
        "pattern": {
            "1": "R3(p1)",
            "2": "R3(p1)",
            "3": "R2(p01)",
            "4": "R3(p0)",
            "5": "R3(p0)",
        },
        "pavage": {"x": "2xT(p0g,pm)", "y": "2xT(pm,p1d)"},
    },
    Typo.T6d: {
        "name": "Type 6d",
        "type": "6",
        "subtype": "d",
        "form": "Pentagone",
        "fxy": (1.3, 1.3),
        "controls": {
            "p1": {
                "pos": (1, 0),
                "mouse": "rotation(p0);stretch_x(p0,p1,p2);stretch_y(p0,p2,p1)",
            },
            "px": {"pos": (0, 1.1), "mouse": "move(px);p3=R2(px,pg2);p4=R6(px,pm)"},
            "pg": {"pos": "-R3(p1,p0)"},
            "p2": {
                "pos": "-R3(p0,pg)",
                "mouse": "rotation(p0)",
            },
            "p0g": {"pos": "M(p0,pg)"},
            "pg2": {"pos": "M(pg,p2)", "visible": "R"},
            "pm": {"pos": "M(p1,p2)", "visible": "R"},
            "pm1": {"pos": "R2(pm,pg2)"},
            "pm2": {"pos": "R2(pm,p0g)"},
            "p3": {"pos": "R2(px,pg2)"},
            "p4": {"pos": "R6(px,pm)"},
            "pr2": {"pos": "R3(p0g,pg)"},
        },
        "seeds": {"s1": ["pm", "px"], "s2": ["px", "pg2"], "s3": ["p3", "p2"]},
        "images": {
            "i1": ["s1", "R6(pm)"],
            "i2": ["s2", "R2(pg2)"],
            "i3": ["s3", "-R3(p2)"],
        },
        "tile": ["+s1", "+s2", "-i2", "+s3", "-i3", "-i1"],
        "pattern": {
            "1": "-R6(pm)",
            "2": "R2(p0g)",
            "3": "-R6(pm2)",
            "4": "R2(pr2)",
            "5": "-R6(pm1)",
        },
        "pavage": {"x": "T(pm2,pm)", "y": "T(pm1,pm)"},
    },
}


"""
TYPES_PAVAGES[Typo.xxx] = {
    "name": "Type xxx",
    "type": "xx",
    "subtype": "x",
    "form": "",
    "controls": {
        "p1": {"pos": (1, 0), "mouse": "rotation(p0);stretch_x(p0,p1,p2)"},
        "p2": {"pos": (0, 1), "mouse": "stretch_y(p0,p2,p1);shear(p0,p1,p2)"},
    },
    "seeds": {"s1": ["p0", "p1"]},
    "images": {
        "i1": ["s1", "T(p0,p1)"],
    },
    "tile": ["+s1", "+i1"],
    "pattern": {"1": "T(p0,p1)"},
    "pavage": {"x": "T(p0,p1)", "y": "T(p0,p2)"},
}
"""
