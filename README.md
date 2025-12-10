# Croydon Adaptation Plan

A geospatial data processing and visualization project for TreesAI's climate adaptation planning in Croydon, analyzing adaptation measures across Output Areas (OAs) and Lower Super Output Areas (LSOAs).

## Overview

This project processes and exports geospatial data related to climate adaptation measures for the London Borough of Croydon. It generates interactive maps and datasets that help visualize adaptation priorities and vulnerability assessments at different geographic scales.

## Project Structure

```
croydon_adaptation_plan/
├── Adaptation Maps Export.gpkg          # Main GeoPackage with all spatial layers
├── Final OA and LSOA Outputs.gpkg      # Processed Output Area and LSOA geometries
├── Croydon_OA_Raw data...tiles_AdaptMeasures.csv
├── Croydon_LSOA_Raw data and Quintiles.csv
├── Croydon_LSOA_Raw data and Quintiles.xlsx
├── Scr2_Exporting Adaptat...group maps and CSVs.py
└── Scr1_Recalculating ada...asure scores for OAs.py
```

## Data Files

### GeoPackages

- **`Adaptation Maps Export.gpkg`** (65.7 MB)
  - Primary spatial database containing all map layers
  - Includes adaptation measure geometries and attributes
  - Ready for import into QGIS, ArcGIS, or other GIS software

- **`Final OA and LSOA Outputs.gpkg`** (2.8 MB)
  - Processed boundary data for Output Areas and Lower Super Output Areas
  - Contains calculated scores and classifications

### CSV/Excel Files

- **`Croydon_OA_Raw data...tiles_AdaptMeasures.csv`** (599 KB)
  - Raw data for Output Areas with adaptation measure scores
  - Includes quintile classifications for vulnerability assessment

- **`Croydon_LSOA_Raw data and Quintiles.csv`** (79 KB)
  - Aggregated data at LSOA level
  - Statistical summaries and quintile breakdowns

- **`Croydon_LSOA_Raw data and Quintiles.xlsx`** (50 KB)
  - Excel version with formatted tables and potential additional sheets

## Scripts

### Script 1: Recalculating Adaptation Measure Scores for OAs
**`Scr1_Recalculating ada...asure scores for OAs.py`** (4 KB)

Processes raw adaptation measure data and calculates vulnerability scores for Output Areas.

**Key functions:**
- Loads OA-level raw data
- Recalculates adaptation measure scores based on updated criteria
- Generates quintile classifications for visualization
- Exports processed data to CSV and GeoPackage formats

**Usage:**
```bash
python Scr1_Recalculating_adaptation_measure_scores_for_OAs.py
```

### Script 2: Exporting Adaptation Group Maps and CSVs
**`Scr2_Exporting Adaptat...group maps and CSVs.py`** (11 KB)

Generates map exports and aggregated datasets for different adaptation measure groups.

**Key functions:**
- Groups adaptation measures by category
- Creates thematic map layers for each adaptation group
- Aggregates OA data to LSOA level
- Exports final GeoPackages and CSV files for analysis

**Usage:**
```bash
python Scr2_Exporting_Adaptation_group_maps_and_CSVs.py
```

## Requirements

### Python Dependencies

```bash
pip install geopandas pandas numpy fiona shapely
```

### Required Libraries

- **geopandas** - Geospatial data processing
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **fiona** - GeoPackage I/O operations
- **shapely** - Geometric operations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/treesai/croydon-adaptation-plan.git
cd croydon-adaptation-plan
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Complete Workflow

1. **Recalculate OA scores:**
```bash
python Scr1_Recalculating_adaptation_measure_scores_for_OAs.py
```

2. **Generate exports:**
```bash
python Scr2_Exporting_Adaptation_group_maps_and_CSVs.py
```

### Loading Data in GIS Software

**QGIS:**
1. Open QGIS
2. Layer → Add Layer → Add Vector Layer
3. Select `Adaptation Maps Export.gpkg`
4. Choose the layers you want to display

**Python/GeoPandas:**
```python
import geopandas as gpd

# Load the main GeoPackage
gdf = gpd.read_file('Adaptation Maps Export.gpkg', layer='adaptation_measures')

# Load LSOA data
lsoa = gpd.read_file('Final OA and LSOA Outputs.gpkg', layer='lsoa_boundaries')

# Display basic statistics
print(gdf.describe())
```

## Data Dictionary

### Adaptation Measures
- **Quintile classifications:** Areas divided into 5 groups (Q1-Q5) based on vulnerability
- **Output Areas (OAs):** Small geographic areas containing ~300 residents
- **LSOAs:** Larger areas containing 1,000-3,000 residents

### Score Calculations
Adaptation measure scores typically combine factors such as:
- Climate vulnerability indicators
- Socioeconomic factors
- Environmental characteristics
- Infrastructure capacity
- Green space availability

## Output Files

After running the scripts, you'll have:
- Updated GeoPackage files with calculated scores
- CSV exports for tabular analysis
- Map-ready layers for visualization
- Quintile classifications for policy prioritization

## Contributing

This is a TreesAI project for Croydon climate adaptation planning. For questions or contributions, please contact the project team.

## License

[Specify your license here - e.g., MIT, Apache 2.0, or Proprietary]

## Contact

**Project:** TreesAI Croydon Adaptation Plan  
**Organization:** [TreesAI / Dark Matter Labs]  
**Email:** [contact email]

## Acknowledgments

- London Borough of Croydon for geographic boundary data
- ONS for Output Area and LSOA definitions
- Laurence Edwards

## Changelog

### Version 1.0 (October 2025)
- Initial release with OA and LSOA adaptation measure calculations
- GeoPackage exports for mapping
- Quintile classification system implemented

---

*Last updated: October 31, 2025*# Croydon Adaptation Plan

A geospatial data processing and visualization project for TreesAI's climate adaptation planning in Croydon, analyzing adaptation measures across Output Areas (OAs) and Lower Super Output Areas (LSOAs).

## Overview

This project processes and exports geospatial data related to climate adaptation measures for the London Borough of Croydon. It generates interactive maps and datasets that help visualize adaptation priorities and vulnerability assessments at different geographic scales.

## Project Structure

```
croydon_adaptation_plan/
├── Adaptation Maps Export.gpkg          # Main GeoPackage with all spatial layers
├── Final OA and LSOA Outputs.gpkg      # Processed Output Area and LSOA geometries
├── Croydon_OA_Raw data...tiles_AdaptMeasures.csv
├── Croydon_LSOA_Raw data and Quintiles.csv
├── Croydon_LSOA_Raw data and Quintiles.xlsx
├── Scr2_Exporting Adaptat...group maps and CSVs.py
└── Scr1_Recalculating ada...asure scores for OAs.py
```

## Data Files

### GeoPackages

- **`Adaptation Maps Export.gpkg`** (65.7 MB)
  - Primary spatial database containing all map layers
  - Includes adaptation measure geometries and attributes
  - Ready for import into QGIS, ArcGIS, or other GIS software

- **`Final OA and LSOA Outputs.gpkg`** (2.8 MB)
  - Processed boundary data for Output Areas and Lower Super Output Areas
  - Contains calculated scores and classifications

### CSV/Excel Files

- **`Croydon_OA_Raw data...tiles_AdaptMeasures.csv`** (599 KB)
  - Raw data for Output Areas with adaptation measure scores
  - Includes quintile classifications for vulnerability assessment

- **`Croydon_LSOA_Raw data and Quintiles.csv`** (79 KB)
  - Aggregated data at LSOA level
  - Statistical summaries and quintile breakdowns

- **`Croydon_LSOA_Raw data and Quintiles.xlsx`** (50 KB)
  - Excel version with formatted tables and potential additional sheets

## Scripts

### Script 1: Recalculating Adaptation Measure Scores for OAs
**`Scr1_Recalculating ada...asure scores for OAs.py`** (4 KB)

Processes raw adaptation measure data and calculates vulnerability scores for Output Areas.

**Key functions:**
- Loads OA-level raw data
- Recalculates adaptation measure scores based on updated criteria
- Generates quintile classifications for visualization
- Exports processed data to CSV and GeoPackage formats

**Usage:**
```bash
python Scr1_Recalculating_adaptation_measure_scores_for_OAs.py
```

### Script 2: Exporting Adaptation Group Maps and CSVs
**`Scr2_Exporting Adaptat...group maps and CSVs.py`** (11 KB)

Generates map exports and aggregated datasets for different adaptation measure groups.

**Key functions:**
- Groups adaptation measures by category
- Creates thematic map layers for each adaptation group
- Aggregates OA data to LSOA level
- Exports final GeoPackages and CSV files for analysis

**Usage:**
```bash
python Scr2_Exporting_Adaptation_group_maps_and_CSVs.py
```

## Requirements

### Python Dependencies

```bash
pip install geopandas pandas numpy fiona shapely
```

### Required Libraries

- **geopandas** - Geospatial data processing
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **fiona** - GeoPackage I/O operations
- **shapely** - Geometric operations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/treesai/croydon-adaptation-plan.git
cd croydon-adaptation-plan
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Complete Workflow

1. **Recalculate OA scores:**
```bash
python Scr1_Recalculating_adaptation_measure_scores_for_OAs.py
```

2. **Generate exports:**
```bash
python Scr2_Exporting_Adaptation_group_maps_and_CSVs.py
```

### Loading Data in GIS Software

**QGIS:**
1. Open QGIS
2. Layer → Add Layer → Add Vector Layer
3. Select `Adaptation Maps Export.gpkg`
4. Choose the layers you want to display

**Python/GeoPandas:**
```python
import geopandas as gpd

# Load the main GeoPackage
gdf = gpd.read_file('Adaptation Maps Export.gpkg', layer='adaptation_measures')

# Load LSOA data
lsoa = gpd.read_file('Final OA and LSOA Outputs.gpkg', layer='lsoa_boundaries')

# Display basic statistics
print(gdf.describe())
```

## Data Dictionary

### Adaptation Measures
- **Quintile classifications:** Areas divided into 5 groups (Q1-Q5) based on vulnerability
- **Output Areas (OAs):** Small geographic areas containing ~300 residents
- **LSOAs:** Larger areas containing 1,000-3,000 residents

### Score Calculations
Adaptation measure scores typically combine factors such as:
- Climate vulnerability indicators
- Socioeconomic factors
- Environmental characteristics
- Infrastructure capacity
- Green space availability

## Output Files

After running the scripts, you'll have:
- Updated GeoPackage files with calculated scores
- CSV exports for tabular analysis
- Map-ready layers for visualization
- Quintile classifications for policy prioritization

## Contact

**Project:** TreesAI Croydon Adaptation Plan  
**Organization:** Dark Matter Labs
**Email:** treesai@darkmatterlabs.org

## Acknowledgments

- London Borough of Croydon for geographic boundary data
- ONS for Output Area and LSOA definitions
- Laurence Edwards

## Changelog

### Version 1.0 (October 2025)
- Initial release with OA and LSOA adaptation measure calculations
- GeoPackage exports for mapping
- Quintile classification system implemented

---

*Last updated: October 31, 2025*
