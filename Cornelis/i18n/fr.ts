<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr" sourcelanguage="en">
<context>
    <name>CornelisGeometryFunction</name>
    <message>
        <location filename="../cornelisPlugin.py" line="48"/>
        <source>&lt;h1&gt;cornelis&lt;/h1&gt;
Expression function added by Cornelis plugin.&lt;br&gt;
&lt;br&gt;
Duplicates the geometry according to the transformation rules of the current tessellation scheme.
&lt;br&gt;
&lt;h2&gt;Return value&lt;/h2&gt;
Geom&lt;br/&gt;
&lt;h2&gt;Usage&lt;/h2&gt;
cornelis($geometry)&lt;br&gt;
&lt;br&gt;
or if a transformation is necessary (Here 2154 is the map projection, 4326 the layer projection) :&lt;br&gt;
&lt;br&gt;
transform(&lt;br&gt;
	cornelis(transform($geometry, &apos;EPSG:4326&apos;, &apos;EPSG:2154&apos;)),&lt;br&gt;
	&apos;EPSG:2154&apos;,&apos;EPSG:4326&apos;&lt;br&gt;
)&lt;br&gt;
...
        </source>
        <translation>&lt;h1&gt;cornelis&lt;/h1&gt;
Expression ajoutée par l&apos;extension Cornelis.&lt;br&gt;
&lt;br&gt;
Pave le plan en dupliquant les géométries contenues dans la tuile de base, selon les règles de transformation du pavage courant.
&lt;br&gt;
&lt;h2&gt;Valeur retournée&lt;/h2&gt;
Geométrie (multiple)&lt;br/&gt;
&lt;h2&gt;Utilisation&lt;/h2&gt;
cornelis($geometry)&lt;br&gt;
&lt;br&gt;
ou si une transformation est nécessaire : (ici 2154 correspond à la projection de la carte, 4326 à celle de la couche) :&lt;br&gt;
&lt;br&gt;
transform(&lt;br&gt;
	cornelis(transform($geometry, &apos;EPSG:4326&apos;, &apos;EPSG:2154&apos;)),&lt;br&gt;
	&apos;EPSG:2154&apos;,&apos;EPSG:4326&apos;&lt;br&gt;
)</translation>
    </message>
</context>
<context>
    <name>CornelisPlugin</name>
    <message>
        <location filename="../cornelisPlugin.py" line="264"/>
        <source>&amp;CornelisPlugin</source>
        <translation>&amp;CornelisPlugin</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="114"/>
        <source>&amp;Cornelis</source>
        <translation>&amp;Cornelis</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="192"/>
        <source>New pattern</source>
        <translation>Nouveau pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="201"/>
        <source>Show/Hide pattern</source>
        <translation>Montrer/Masquer le pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="223"/>
        <source>Build tesselation</source>
        <translation>Construire le pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="232"/>
        <source>Load a existing pattern</source>
        <translation>Charger un modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="241"/>
        <source>Save pattern</source>
        <translation>Sauver le modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="314"/>
        <source>Load Pattern</source>
        <translation>Charger un modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="334"/>
        <source>Save Pattern</source>
        <translation>Sauver le modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="360"/>
        <source>Error during process</source>
        <translation>Erreur pendant le traitement</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="154"/>
        <source>Tiles</source>
        <translation>Tuiles</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="212"/>
        <source>Draw a sketch</source>
        <translation>Dessiner</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="299"/>
        <source>New pavage</source>
        <translation>Nouveau pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="299"/>
        <source>Abandon the current tessellation ?</source>
        <translation>Abandonner le pavage courant ?</translation>
    </message>
</context>
<context>
    <name>TDMapTool</name>
    <message>
        <location filename="../TDMapTool.py" line="493"/>
        <source>Initialization...</source>
        <translation>Initialisations...</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="576"/>
        <source>End !</source>
        <translation>Fin !</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="549"/>
        <source>Pattern</source>
        <translation>Modèle</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="477"/>
        <source>Tile</source>
        <translation>Tuile</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="565"/>
        <source>Tessellation</source>
        <translation>Pavage</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="434"/>
        <source>Tesselation</source>
        <translation>Pavage</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="541"/>
        <source>Sketch</source>
        <translation>Croquis</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="210"/>
        <source>New pavage</source>
        <translation>Nouveau pavage</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="462"/>
        <source>Points</source>
        <translation>Noeuds</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="210"/>
        <source>Abandon the current tessellation ?</source>
        <translation>Abandonner le pavage courant ?</translation>
    </message>
</context>
</TS>
