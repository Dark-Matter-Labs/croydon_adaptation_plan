from qgis.core import (
    QgsProject, QgsField, QgsVectorLayer, QgsFeature, QgsGeometry, QgsWkbTypes
)
from PyQt5.QtCore import QVariant

# Load the base layer
base_layer = QgsProject.instance().mapLayersByName('Croydon_OA_Raw data_Quintiles_AdaptMeasures')[0]

# Define relevant fields for each adaptation measure
adapt_fields = {  
    'Adapt_A': ['MaxAvLST_q', 'VM5_q', 'Poll_q', 'VM1_q','RENT_q','VM7_q', 'VM6_q', 'Education_', 'Nursing_5', 'Hospital_5'],
    'Adapt_B': ['MaxAvLST_q', 'VM5_q', 'Poll_q', 'VM7_q', 'VM6_q', 'Education_'],
    'Adapt_C': ['MaxAvLST_q', 'VM5_q', 'Poll_q','VM1_q', 'VM7_q', 'VM6_q','Education_'],
    'Adapt_D': ['VM5_q','VM1_q','VM6_q','Basement_5'],
    'Adapt_E': ['MaxAvLST_q', 'VM5_q','VM1_q', 'VM7_q', 'VM6_q','Q_CanopyOu', 'Education_'],
    'Adapt_F': ['MaxAvLST_q', 'PU5_q', 'PO75_q'],
    'Adapt_G': ['MaxAvLST_q','VM1_q', 'PU5_q', 'PO75_q'],
    'Adapt_H': ['MaxAvLST_q', 'VM5_q', 'Q_Roof_Cou'],
    'Adapt_I': ['MaxAvLST_q', 'VM5_q','VM1_q', 'Q_Roof_Cou'],
    'Adapt_J': ['MaxAvLST_q', 'VM1_q','RENT_q'],
    'Adapt_K': ['VM1_q','RENT_q', 'PU5_q', 'PO75_q'],
    'Adapt_L': ['MaxAvLST_q','PU5_q', 'PO75_q','VM6_q','RailBuffer'],
    'Adapt_M': ['MaxAvLST_q','VM5_q','PU5_q', 'PO75_q','Station_5'],
    'Adapt_N': ['VM5_q', 'VM6_q', 'Q_CanopyOu','Roads_comb'],
    'Adapt_O': ['MaxAvLST_q','VM6_q','Roads_comb'],
    'Adapt_P': ['MaxAvLST_q','Poll_q','VM6_q','Roads_comb'],
    'Adapt_Q': ['MaxAvLST_q', 'VM5_q', 'Poll_q', 'VM1_q','PU5_q', 'Education_'],
    'Adapt_R': ['MaxAvLST_q', 'VM5_q', 'Poll_q', 'VM1_q','PU5_q','Education_', 'Nursing_5'],
    'Adapt_S': ['MaxAvLST_q', 'VM5_q', 'Poll_q', 'VM1_q','Education_'],
    'Adapt_T': ['MaxAvLST_q', 'VM5_q', 'Poll_q', 'VM1_q','Education_', 'Nursing_5'],
    'Adapt_U': ['MaxAvLST_q','VM1_q','PO75_q', 'Education_', 'Nursing_5'],
    }

# Get existing field names from base layer
existing_fields = [field.name() for field in base_layer.fields()]

# Create a scratch layer with same geometry and CRS
scratch_layer = QgsVectorLayer(
    f"{QgsWkbTypes.displayString(base_layer.wkbType())}?crs={base_layer.crs().authid()}",
    "OA_Data_Recalc",
    "memory"
)

# Add base fields
scratch_layer_data = scratch_layer.dataProvider()
scratch_layer_data.addAttributes(base_layer.fields().toList())

# Add only new adaptation fields
for adapt in adapt_fields:
    if adapt not in existing_fields:
        scratch_layer_data.addAttributes([QgsField(adapt, QVariant.Int)])

scratch_layer.updateFields()

# Start editing
scratch_layer.startEditing()

# Process features
total_oas = base_layer.featureCount()
hazard_count = 0
print(f"🔄 Starting adaptation score update for {total_oas} OA features...")

for i, feat in enumerate(base_layer.getFeatures()):
    new_feat = QgsFeature(scratch_layer.fields())
    new_feat.setGeometry(feat.geometry())

    # Copy base attributes
    attrs = feat.attributes()

    # Prepare a dictionary for field values
    attr_dict = {field.name(): val for field, val in zip(base_layer.fields(), attrs)}

    # Check hazard condition
    hazard_triggered = False
    for field in ['MaxAvLST_q', 'VM5_q', 'Poll_q']:
        try:
            val = feat[field]
            if val is not None and int(str(val).strip()) >= 4:
                hazard_triggered = True
                break
        except:
            continue

    if hazard_triggered:
        hazard_count += 1

    # Calculate and assign adaptation scores
    for adapt, fields in adapt_fields.items():
        score = 0
        if hazard_triggered:
            for field in fields:
                try:
                    val = feat[field]
                    if val is not None:
                        score += int(str(val).strip())
                except:
                    continue
        attr_dict[adapt] = score  # overwrite or add

    # Set attributes in correct order
    ordered_attrs = [attr_dict.get(field.name(), None) for field in scratch_layer.fields()]
    new_feat.setAttributes(ordered_attrs)
    scratch_layer.addFeature(new_feat)

    if (i + 1) % 50 == 0 or (i + 1) == total_oas:
        print(f"✅ Updated {i + 1} of {total_oas} OAs")

# Finalize
scratch_layer.commitChanges()
QgsProject.instance().addMapLayer(scratch_layer)
print(f"✅ Finished. {hazard_count} OAs met the hazard condition.")
print("✅ Adaptation scores added to 'OA_Data_Recalc'.")