<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr_FR" sourcelanguage="en_US">
<context>
    <name>CornelisGeometryFunction</name>
    <message>
        <location filename="../cornelisPlugin.py" line="53"/>
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
fonction d&apos;expression apportée par l&apos;extension Cornelis.&lt;br&gt;
&lt;br&gt;
Duplique la géométrie selon les règle de transformation du pavage courant.
&lt;br&gt;
&lt;h2&gt;Valeur de retour&lt;/h2&gt;
Geométrie&lt;br/&gt;
&lt;h2&gt;Exemple&lt;/h2&gt;
cornelis($geometry)&lt;br&gt;
&lt;br&gt;
ou...  :&lt;br&gt;
&lt;br&gt;
transform(&lt;br&gt;
    cornelis(transform($geometry, &apos;EPSG:4326&apos;, &apos;EPSG:2154&apos;)),&lt;br&gt;
    &apos;EPSG:2154&apos;,&apos;EPSG:4326&apos;&lt;br&gt;
)&lt;br&gt;</translation>
    </message>
</context>
<context>
    <name>CornelisPlugin</name>
    <message>
        <location filename="../cornelisPlugin.py" line="263"/>
        <source>&amp;CornelisPlugin</source>
        <translation>&amp;CornelisPlugin</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="110"/>
        <source>&amp;Cornelis</source>
        <translation>&amp;Cornelis</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="187"/>
        <source>New pattern</source>
        <translation>Nouveau pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="198"/>
        <source>Show/Hide pattern</source>
        <translation>Montrer/Masquer le pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="222"/>
        <source>Build tesselation</source>
        <translation>Construire le pavage</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="231"/>
        <source>Load a existing pattern</source>
        <translation>Charger un modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="240"/>
        <source>Save pattern</source>
        <translation>Sauver le modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="313"/>
        <source>Load Pattern</source>
        <translation>Charger un modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="333"/>
        <source>Save Pattern</source>
        <translation>Sauver le modèle</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="359"/>
        <source>Error during process</source>
        <translation>Erreur pendant le traitement</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="150"/>
        <source>Tiles</source>
        <translation>Tuiles</translation>
    </message>
    <message>
        <location filename="../cornelisPlugin.py" line="209"/>
        <source>Draw a sketch (+ctrl to erase)</source>
        <translation>Dessiner (+ctrl pour effacer)</translation>
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
        <location filename="../TDMapTool.py" line="616"/>
        <source>Initialization...</source>
        <translation>Initialisations...</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="685"/>
        <source>End !</source>
        <translation>Fin !</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="643"/>
        <source>Pattern</source>
        <translation>Modèle</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="603"/>
        <source>Tile</source>
        <translation>Tuile</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="659"/>
        <source>Tessellation</source>
        <translation>Pavage</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="592"/>
        <source>Tesselation</source>
        <translation>Pavage</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="674"/>
        <source>Sketch</source>
        <translation>Croquis</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="235"/>
        <source>New pavage</source>
        <translation>Nouveau pavage</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="235"/>
        <source>Abandon the current tessellation ?</source>
        <translation>Abandonner le pavage courant ?</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="435"/>
        <source>NEW</source>
        <translation>COPIE</translation>
    </message>
    <message>
        <location filename="../TDMapTool.py" line="631"/>
        <source>Raster support needs install &apos;skimage&apos; and &apos;scipy&apos; libraries</source>
        <translation>Le support des raster nécessite l&apos;installation des librairies python &apos;skimage&apos; et &apos;scipy&apos; </translation>
    </message>
</context>
</TS>
