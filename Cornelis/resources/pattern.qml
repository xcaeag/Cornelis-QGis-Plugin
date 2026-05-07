<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis autoRefreshMode="Disabled" autoRefreshTime="0" simplifyMaxScale="1" simplifyAlgorithm="0" simplifyDrawingTol="1" symbologyReferenceScale="-1" simplifyDrawingHints="1" minScale="0" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" styleCategories="Symbology|Labeling|Rendering" version="3.40.8-Bratislava" maxScale="0" simplifyLocal="1">
  <renderer-v2 referencescale="-1" type="RuleRenderer" symbollevels="0" forceraster="0" enableorderby="0">
    <rules key="{9ed62621-ad90-4c6f-b3eb-9b2688d32417}">
      <rule key="{f4be0ea7-9767-4b97-9903-e753bdab5cad}" symbol="0"/>
      <rule label="sens" checkstate="0" key="{d6a1ce7e-df29-4a30-babd-1294da2c2932}" symbol="1"/>
    </rules>
    <symbols>
      <symbol name="0" type="fill" alpha="0.8" frame_rate="10" is_animated="0" force_rhr="0" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer id="{c0edee7d-940d-4974-83c6-194fa61eeffc}" locked="0" class="SimpleFill" pass="0" enabled="1">
          <Option type="Map">
            <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="color" value="166,225,89,255,rgb:0.65098039215686276,0.88235294117647056,0.34901960784313724,1" type="QString"/>
            <Option name="joinstyle" value="round" type="QString"/>
            <Option name="offset" value="0,0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="outline_color" value="47,30,22,255,hsv:0.05191666666666667,0.52864881361104754,0.18455786984054323,1" type="QString"/>
            <Option name="outline_style" value="solid" type="QString"/>
            <Option name="outline_width" value="1" type="QString"/>
            <Option name="outline_width_unit" value="MM" type="QString"/>
            <Option name="style" value="no" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" type="fill" alpha="1" frame_rate="10" is_animated="0" force_rhr="0" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer id="{26655f84-d03c-43bd-a0c1-2b0cb7a3d103}" locked="0" class="GeometryGenerator" pass="0" enabled="1">
          <Option type="Map">
            <Option name="SymbolType" value="Line" type="QString"/>
            <Option name="geometryModifier" value="with_variable('d',  bounds_width(minimal_circle($geometry))/6, &#xd;&#xa;with_variable('c0', centroid($geometry), &#xd;&#xa;with_variable('p0', project(@c0, -@d/2, &quot;flip&quot; *radians(&quot;rotation&quot;)), &#xd;&#xa;with_variable('p1', project(@p0, @d,  &quot;flip&quot; *radians(&quot;rotation&quot;) ), &#xd;&#xa;with_variable('p2', project(@p1, @d/2, &quot;flip&quot; *radians(&quot;rotation&quot;+120)), &#xd;&#xa;with_variable('p3', project(@p2, @d/2, &quot;flip&quot; *radians(&quot;rotation&quot;+240)), &#xd;&#xa;&#x9;make_line(@p0, @p1, @p2, @p3)&#xd;&#xa;)))))) " type="QString"/>
            <Option name="units" value="MapUnit" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@0" type="line" alpha="1" frame_rate="10" is_animated="0" force_rhr="0" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer id="{c716b907-2b0a-4da9-9a4d-247d69292bbf}" locked="0" class="SimpleLine" pass="0" enabled="1">
              <Option type="Map">
                <Option name="align_dash_pattern" value="0" type="QString"/>
                <Option name="capstyle" value="square" type="QString"/>
                <Option name="customdash" value="5;2" type="QString"/>
                <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="customdash_unit" value="MM" type="QString"/>
                <Option name="dash_pattern_offset" value="0" type="QString"/>
                <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
                <Option name="draw_inside_polygon" value="0" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="line_color" value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString"/>
                <Option name="line_style" value="solid" type="QString"/>
                <Option name="line_width" value="0.66" type="QString"/>
                <Option name="line_width_unit" value="MM" type="QString"/>
                <Option name="offset" value="0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="ring_filter" value="0" type="QString"/>
                <Option name="trim_distance_end" value="0" type="QString"/>
                <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="trim_distance_end_unit" value="MM" type="QString"/>
                <Option name="trim_distance_start" value="0" type="QString"/>
                <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="trim_distance_start_unit" value="MM" type="QString"/>
                <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
                <Option name="use_custom_dash" value="0" type="QString"/>
                <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <data-defined-properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </data-defined-properties>
  </renderer-v2>
  <selection mode="Default">
    <selectionColor invalid="1"/>
    <selectionSymbol>
      <symbol name="" type="fill" alpha="1" frame_rate="10" is_animated="0" force_rhr="0" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer id="{9fdaa89b-24f8-49db-bb3a-0e4fa56850e4}" locked="0" class="SimpleFill" pass="0" enabled="1">
          <Option type="Map">
            <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="color" value="0,0,255,255,rgb:0,0,1,1" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="offset" value="0,0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="outline_color" value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString"/>
            <Option name="outline_style" value="solid" type="QString"/>
            <Option name="outline_width" value="0.26" type="QString"/>
            <Option name="outline_width_unit" value="MM" type="QString"/>
            <Option name="style" value="solid" type="QString"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </selectionSymbol>
  </selection>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" textOpacity="1" useSubstitutions="0" blendMode="0" allowHtml="0" fontSize="20" fontSizeUnit="Point" fontWordSpacing="0" textColor="50,50,50,255,rgb:0.19607843137254902,0.19607843137254902,0.19607843137254902,1" stretchFactor="100" fontStrikeout="0" tabStopDistance="80" forcedItalic="0" fieldName="'F'" previewBkgrdColor="255,255,255,255,rgb:1,1,1,1" textOrientation="rotation-based" multilineHeightUnit="Percentage" fontWeight="50" capitalization="0" fontLetterSpacing="0" isExpression="1" namedStyle="Regular" fontFamily="Liberation Sans" fontItalic="0" tabStopDistanceMapUnitScale="3x:0,0,0,0,0,0" tabStopDistanceUnit="Point" fontUnderline="0" fontKerning="1" multilineHeight="1" forcedBold="0" legendString="Aa">
        <families/>
        <text-buffer bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="1" bufferNoFill="1" bufferBlendMode="0" bufferJoinStyle="128" bufferSizeUnits="MM" bufferOpacity="1" bufferDraw="0" bufferColor="250,250,250,255,rgb:0.98039215686274506,0.98039215686274506,0.98039215686274506,1"/>
        <text-mask maskSize="1.5" maskSizeUnits="MM" maskOpacity="1" maskSize2="1.5" maskJoinStyle="128" maskType="0" maskedSymbolLayers="" maskEnabled="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <background shapeBorderWidth="0" shapeRadiiX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeOffsetY="0" shapeSizeType="0" shapeDraw="0" shapeType="0" shapeSVGFile="" shapeFillColor="255,255,255,255,rgb:1,1,1,1" shapeRadiiY="0" shapeRotation="0" shapeOffsetUnit="Point" shapeOffsetX="0" shapeBlendMode="0" shapeSizeX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="Point" shapeRotationType="0" shapeBorderColor="128,128,128,255,rgb:0.50196078431372548,0.50196078431372548,0.50196078431372548,1" shapeSizeY="0" shapeOpacity="1" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="Point" shapeRadiiUnit="Point" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0">
          <symbol name="markerSymbol" type="marker" alpha="1" frame_rate="10" is_animated="0" force_rhr="0" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer id="" locked="0" class="SimpleMarker" pass="0" enabled="1">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="125,139,143,255,rgb:0.49019607843137253,0.54509803921568623,0.5607843137254902,1" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="circle" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="diameter" type="QString"/>
                <Option name="size" value="2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol name="fillSymbol" type="fill" alpha="1" frame_rate="10" is_animated="0" force_rhr="0" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer id="" locked="0" class="SimpleFill" pass="0" enabled="1">
              <Option type="Map">
                <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="color" value="255,255,255,255,rgb:1,1,1,1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="128,128,128,255,rgb:0.50196078431372548,0.50196078431372548,0.50196078431372548,1" type="QString"/>
                <Option name="outline_style" value="no" type="QString"/>
                <Option name="outline_width" value="0" type="QString"/>
                <Option name="outline_width_unit" value="Point" type="QString"/>
                <Option name="style" value="solid" type="QString"/>
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOffsetDist="1" shadowRadiusUnit="MM" shadowDraw="0" shadowUnder="0" shadowRadiusAlphaOnly="0" shadowRadius="0" shadowColor="0,0,0,255,rgb:0,0,0,1" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0" shadowOffsetUnit="MM" shadowScale="100" shadowBlendMode="6"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format reverseDirectionSymbol="0" decimals="3" useMaxLineLengthForAutoWrap="1" multilineAlign="3" addDirectionSymbol="0" rightDirectionSymbol=">" formatNumbers="0" leftDirectionSymbol="&lt;" placeDirectionSymbol="0" wrapChar="" plussign="0" autoWrapLength="0"/>
      <placement labelOffsetMapUnitScale="3x:0,0,0,0,0,0" lineAnchorTextPoint="FollowPlacement" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" allowDegraded="0" yOffset="0" prioritization="PreferCloser" centroidInside="0" maxCurvedCharAngleIn="25" overrunDistance="0" fitInPolygonOnly="0" maxCurvedCharAngleOut="-25" offsetUnits="MM" distUnits="MM" rotationAngle="0" centroidWhole="0" lineAnchorPercent="0.5" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" quadOffset="4" polygonPlacementFlags="2" maximumDistanceMapUnitScale="3x:0,0,0,0,0,0" dist="0" priority="5" geometryGeneratorEnabled="0" distMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" placement="0" xOffset="0" preserveRotation="1" geometryGenerator="" maximumDistance="0" overlapHandling="PreventOverlap" repeatDistance="0" repeatDistanceUnits="MM" placementFlags="10" maximumDistanceUnit="MM" lineAnchorType="0" lineAnchorClipping="0" overrunDistanceUnit="MM" rotationUnit="AngleDegrees" layerType="PolygonGeometry"/>
      <rendering maxNumLabels="2000" fontMinPixelSize="3" labelPerPart="0" scaleMax="0" scaleVisibility="0" minFeatureSize="0" unplacedVisibility="0" fontMaxPixelSize="10000" drawLabels="1" mergeLines="0" fontLimitPixelSize="0" zIndex="1" obstacleFactor="1" upsidedownLabels="0" scaleMin="0" limitNumLabels="0" obstacleType="1" obstacle="1"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties"/>
          <Option name="type" value="collection" type="QString"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
          <Option name="blendMode" value="0" type="int"/>
          <Option name="ddProperties" type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
          <Option name="drawToAllParts" value="false" type="bool"/>
          <Option name="enabled" value="0" type="QString"/>
          <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
          <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; alpha=&quot;1&quot; frame_rate=&quot;10&quot; is_animated=&quot;0&quot; force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer id=&quot;{431dece8-07d4-476e-b63a-9647f5226b8b}&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255,rgb:0.23529411764705882,0.23529411764705882,0.23529411764705882,1&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
          <Option name="minLength" value="0" type="double"/>
          <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="minLengthUnit" value="MM" type="QString"/>
          <Option name="offsetFromAnchor" value="0" type="double"/>
          <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
          <Option name="offsetFromLabel" value="0" type="double"/>
          <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
          <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <blendMode>6</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>0.8</layerOpacity>
  <layerGeometryType>2</layerGeometryType>
</qgis>
