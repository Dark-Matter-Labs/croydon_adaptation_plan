import os
import csv
from collections import defaultdict
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsFeatureRequest, QgsPrintLayout,
    QgsLayoutItemMap, QgsLayoutSize, QgsLayoutPoint, QgsLayoutExporter,
    QgsLayoutItemPage, QgsUnitTypes, QgsSymbol, QgsSimpleFillSymbolLayer,
    QgsPalLayerSettings, QgsTextFormat, QgsVectorLayerSimpleLabeling
)
from PyQt5.QtGui import QColor, QFont
from qgis.utils import iface

# === CONFIGURATION ===
lsoa_name = "Croydon 022D"
oa_layer_name = "Croydon_OA_Raw data_Quintiles_AdaptMeasures"
lsoa_layer_name = "LSOAs Croydon"
borough_layer_name = "Croydon_borough"
basemap_group_name = "Adaptation Maps Export"
output_base = r"C:\Users\ledwards\Documents\DML\Outputs\Adaptation Group Maps" # PASTE FILE LOCATION HERE <<<<<<<<< #
output_folder = os.path.join(output_base, lsoa_name.replace(" ", ""))
os.makedirs(output_folder, exist_ok=True)

# === ADAPTATION GROUPS AND THRESHOLDS ===
adaptation_groups = {
    "AdaptiveSpaces": ['Adapt_A', 'Adapt_B', 'Adapt_C', 'Adapt_D', 'Adapt_E', 'Adapt_F', 'Adapt_G'],
    "BuildingRetrofit": ['Adapt_H', 'Adapt_I', 'Adapt_J', 'Adapt_K',],
    "TransportInterventions": ['Adapt_L', 'Adapt_M', 'Adapt_N', 'Adapt_O', 'Adapt_P'],
    "CommunityLearning": ['Adapt_Q', 'Adapt_R', 'Adapt_S', 'Adapt_T', 'Adapt_U']
}
group_colors = {
    "AdaptiveSpaces": "#f1c232",
    "BuildingRetrofit": "#cc0000",
    "TransportInterventions": "#9900ff",
    "CommunityLearning": "#3c78d8"
}
thresholds = {

    'Adapt_A': 31,
    'Adapt_B': 24,
    'Adapt_C': 28,
    'Adapt_D': 16,
    'Adapt_E': 25,
    'Adapt_F': 12,
    'Adapt_G': 16,
    'Adapt_H': 12,
    'Adapt_I': 16,
    'Adapt_J': 12,
    'Adapt_K': 14,
    'Adapt_L': 21,
    'Adapt_M': 21,
    'Adapt_N': 16,
    'Adapt_O': 11,
    'Adapt_P': 15,
    'Adapt_Q': 25,
    'Adapt_R': 22,
    'Adapt_S': 17,
    'Adapt_T': 18,
    'Adapt_U': 14
}

# === LOAD LAYERS ===
oa_layer = QgsProject.instance().mapLayersByName(oa_layer_name)[0]
lsoa_layer = QgsProject.instance().mapLayersByName(lsoa_layer_name)[0]
borough_layer = QgsProject.instance().mapLayersByName(borough_layer_name)[0]
basemap_layers = [lyr.layer() for lyr in QgsProject.instance().layerTreeRoot().findGroup(basemap_group_name).findLayers()]

# === FILTER OA FEATURES BY LSOA ===
oa_features = [f for f in oa_layer.getFeatures() if f['LSOA11NM'] == lsoa_name]
oa_ids = [f['OA11CD'] for f in oa_features]

# === CREATE LSOA BOUNDARY LAYER ===
lsoa_boundary_layer = QgsVectorLayer("Polygon?crs=" + lsoa_layer.crs().authid(), "LSOA_Boundary", "memory")
lsoa_boundary_data = lsoa_boundary_layer.dataProvider()
lsoa_boundary_data.addAttributes(lsoa_layer.fields())
lsoa_boundary_layer.updateFields()
lsoa_boundary_layer.startEditing()
for f in lsoa_layer.getFeatures(QgsFeatureRequest().setFilterExpression(f'"LSOA11NM" = \'{lsoa_name}\'')):
    new_feat = QgsFeature(lsoa_boundary_layer.fields())
    new_feat.setGeometry(f.geometry())
    new_feat.setAttributes(f.attributes())
    lsoa_boundary_layer.addFeature(new_feat)
lsoa_boundary_layer.commitChanges()

# === STYLE LSOA BOUNDARY ===
symbol = QgsSymbol.defaultSymbol(lsoa_boundary_layer.geometryType())
fill_layer = symbol.symbolLayer(0)
if isinstance(fill_layer, QgsSimpleFillSymbolLayer):
    fill_layer.setFillColor(QColor(255, 255, 255, 0))  # transparent
    fill_layer.setStrokeColor(QColor("#6a00ff"))
    fill_layer.setStrokeWidth(2)
lsoa_boundary_layer.renderer().setSymbol(symbol)
lsoa_boundary_layer.triggerRepaint()

# === CREATE OA BOUNDARY LAYER ===
oa_boundary_layer = QgsVectorLayer("Polygon?crs=" + oa_layer.crs().authid(), "OA_Boundaries", "memory")
oa_boundary_data = oa_boundary_layer.dataProvider()
oa_boundary_data.addAttributes(oa_layer.fields())
oa_boundary_layer.updateFields()
oa_boundary_layer.startEditing()
for f in oa_features:
    new_feat = QgsFeature(oa_boundary_layer.fields())
    new_feat.setGeometry(f.geometry())
    new_feat.setAttributes(f.attributes())
    oa_boundary_layer.addFeature(new_feat)
oa_boundary_layer.commitChanges()

# === STYLE OA BOUNDARIES ===
oa_symbol = QgsSymbol.defaultSymbol(oa_boundary_layer.geometryType())
oa_fill = oa_symbol.symbolLayer(0)
if isinstance(oa_fill, QgsSimpleFillSymbolLayer):
    oa_fill.setFillColor(QColor(255, 255, 255, 0))  # transparent
    oa_fill.setStrokeColor(QColor("#6a00ff"))
    oa_fill.setStrokeWidth(0.8)
oa_boundary_layer.renderer().setSymbol(oa_symbol)
oa_boundary_layer.triggerRepaint()

# === CREATE MASK LAYER ===
mask_layer = QgsVectorLayer("Polygon?crs=" + borough_layer.crs().authid(), "Mask", "memory")
mask_data = mask_layer.dataProvider()
mask_layer.startEditing()
for f in borough_layer.getFeatures():
    geom = f.geometry().difference(lsoa_boundary_layer.getFeatures().__next__().geometry())
    new_feat = QgsFeature()
    new_feat.setGeometry(geom)
    mask_data.addFeature(new_feat)
mask_layer.commitChanges()
mask_symbol = QgsSymbol.defaultSymbol(mask_layer.geometryType())
mask_symbol.setColor(QColor(0, 0, 0))
mask_symbol.setOpacity(0.25)
mask_layer.renderer().setSymbol(mask_symbol)
mask_layer.triggerRepaint()

# === CSV DATA STRUCTURES ===
csv_scores = {}
grouped_csv_data = defaultdict(lambda: defaultdict(list))

# === PROCESS EACH GROUP ===
for group_name, measures in adaptation_groups.items():
    group_layers = []
    for measure in measures:
        threshold = thresholds[measure]
        selected_feats = []
        for f in oa_features:
            score = f[measure]
            if score is not None and int(score) >= threshold:
                selected_feats.append(f)
                oa_id = f['OA11CD']
                csv_scores.setdefault(oa_id, {})[measure] = int(score)
                grouped_csv_data[group_name][measure].append(oa_id)
        if selected_feats:
            mem_layer = QgsVectorLayer("Polygon?crs=" + oa_layer.crs().authid(), f"{measure}", "memory")
            mem_layer_data = mem_layer.dataProvider()
            mem_layer_data.addAttributes(oa_layer.fields())
            mem_layer.updateFields()
            mem_layer.startEditing()
            for f in selected_feats:
                new_feat = QgsFeature(mem_layer.fields())
                new_feat.setGeometry(f.geometry())
                new_feat.setAttributes(f.attributes())
                mem_layer.addFeature(new_feat)
            mem_layer.commitChanges()
            color = group_colors[group_name]
            symbol = QgsSymbol.defaultSymbol(mem_layer.geometryType())
            symbol.setColor(QColor(color))
            symbol.setOpacity(0.5)
            mem_layer.renderer().setSymbol(symbol)
            label_settings = QgsPalLayerSettings()
            label_settings.fieldName = "OA11CD"
            text_format = QgsTextFormat()
            text_format.setFont(QFont("Arial"))
            text_format.setSize(10)
            text_format.setColor(QColor("black"))
            buffer = text_format.buffer()
            buffer.setEnabled(True)
            buffer.setSize(1.5)
            buffer.setColor(QColor("white"))
            text_format.setBuffer(buffer)
            label_settings.setFormat(text_format)
            mem_layer.setLabelsEnabled(True)
            mem_layer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
            mem_layer.triggerRepaint()
            QgsProject.instance().addMapLayer(mem_layer)
            group_layers.append(mem_layer)

    QgsProject.instance().addMapLayer(lsoa_boundary_layer)
    QgsProject.instance().addMapLayer(oa_boundary_layer)
    QgsProject.instance().addMapLayer(mask_layer)

    layout_name = f"{group_name}_Layout"
    project = QgsProject.instance()
    manager = project.layoutManager()
    existing_layout = manager.layoutByName(layout_name)
    if existing_layout:
        manager.removeLayout(existing_layout)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layout_name)
    manager.addLayout(layout)

    page = layout.pageCollection().pages()[0]
    page.setPageSize('A4', QgsLayoutItemPage.Orientation.Landscape)

    map_item = QgsLayoutItemMap(layout)
    map_item.setRect(20, 20, 200, 100)
    map_item.setLayers([oa_boundary_layer] + group_layers + [lsoa_boundary_layer, mask_layer] + basemap_layers)
    map_item.zoomToExtent(lsoa_boundary_layer.extent())
    layout.addLayoutItem(map_item)
    map_item.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutMillimeters))
    map_item.attemptResize(QgsLayoutSize(277, 190, QgsUnitTypes.LayoutMillimeters))
    iface.mapCanvas().refresh()

    exporter = QgsLayoutExporter(layout)
    png_path = os.path.join(output_folder, f"{lsoa_name.replace(' ', '')}_{group_name}.png")
    pdf_path = os.path.join(output_folder, f"{lsoa_name.replace(' ', '')}_{group_name}.pdf")
    exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
    exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())
    print(f"✅ Exported map for {group_name} to PNG and PDF.")

    for lyr in group_layers:
        QgsProject.instance().removeMapLayer(lyr)
        

# Remove temporary layers after export
for temp_layer_name in ["LSOA_Boundary", "OA_Boundaries", "Mask"]:
    layer = QgsProject.instance().mapLayersByName(temp_layer_name)
    if layer:
        QgsProject.instance().removeMapLayer(layer[0])

print("✅ Temporary layers removed from project.")


# === EXPORT CSVs ===
csv1_path = os.path.join(output_folder, f"{lsoa_name.replace(' ', '')}_AdaptationScores.csv")
with open(csv1_path, 'w', newline='') as f:
    writer = csv.writer(f)
    header = ['OA11CD'] + list(thresholds.keys())
    writer.writerow(header)
    for oa_id in oa_ids:
        row = [oa_id]
        for measure in thresholds.keys():
            row.append(csv_scores.get(oa_id, {}).get(measure, ''))
        writer.writerow(row)
print(f"✅ Exported CSV of adaptation scores: {csv1_path}")

csv2_path = os.path.join(output_folder, f"{lsoa_name.replace(' ', '')}_AdaptationGroups.csv")
with open(csv2_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['AdaptationGroup', 'AdaptationMeasure', 'OA11CDs'])
    for group, measures in grouped_csv_data.items():
        for measure, oas in measures.items():
            writer.writerow([group, measure, ",".join(oas)])
print(f"✅ Exported CSV of adaptation groups: {csv2_path}")
