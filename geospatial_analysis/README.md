# Population Density vs Energy Access Analysis - Zambia

This project performs a comprehensive geospatial analysis of population density versus energy access in Zambia by examining the proximity of electrical substations and transmission infrastructure within a 10km buffer zone.

## Overview

The analysis combines population density data from WorldPop with electrical infrastructure data from OpenStreetMap to create layered visualizations that reveal the relationship between population distribution and energy access.

## Analysis Components

### 1. Population Density Layer (Base Layer)
- **Source**: WorldPop (worldpop.org)
- **Data Type**: Population density raster (GeoTIFF)
- **Coverage**: Zambia nationwide
- **Visualization**: Light theme color gradient (white to orange/brown)

### 2. Transmission Lines Layer (Second Layer)
- **Source**: OpenStreetMap via Overpass API
- **Data Type**: Vector lines with voltage attributes
- **Color Coding**: Voltage-based with high contrast colors:
  - 330kV: Red (High voltage)
  - 220kV: Orange-Red
  - 132kV: Orange
  - 88kV: Blue
  - 66kV: Light Blue
  - 33kV: Green
  - 22kV: Light Green
  - 11kV: Gray
  - Unknown: Dark Gray

### 3. Substations Layer (Top Layer)
- **Source**: OpenStreetMap via Overpass API
- **Data Type**: Point features
- **Visualization**: Black squares with white borders (opacity 1.0)
- **Buffer Zones**: 10km radius circles for proximity analysis

## Methodology

### Data Acquisition
1. **Population Data**: Download from WorldPop using Python requests
2. **Infrastructure Data**: Query OpenStreetMap using the overpy package
3. **Fallback**: Synthetic data generation for demonstration purposes

### Spatial Analysis
1. **Coordinate System**: WGS84 (EPSG:4326) for display, UTM Zone 35S (EPSG:32735) for distance calculations
2. **Buffer Creation**: 10km radius around each substation
3. **Population Analysis**: Calculate population within/outside buffer zones
4. **Statistical Metrics**: Density ratios and coverage percentages

### Visualization Design
- **Theme**: Light background with high contrast colors
- **Layer Order**: Population density → Transmission lines → Substations
- **Accessibility**: Color choices ensure readability and contrast
- **Export**: High-resolution PNG files (300 DPI)

## Requirements

### Python Dependencies
```
jupyter==1.0.0
notebook==7.0.6
overpy==0.7
rasterio==1.3.9
geopandas==0.14.1
matplotlib==3.8.2
contextily==1.4.0
requests==2.31.0
folium==0.15.1
shapely==2.0.2
pandas==2.1.4
numpy==1.26.2
pillow==10.1.0
```

### System Requirements
- Python 3.8+
- Jupyter Notebook environment
- Internet connection for data download (or use synthetic data)

## Installation and Usage

### 1. Setup Environment
```bash
# Navigate to the geospatial_analysis directory
cd geospatial_analysis

# Install required packages
pip install -r requirements.txt

# Start Jupyter Notebook
jupyter notebook
```

### 2. Run Analysis
1. Open `zambia_energy_access_analysis.ipynb`
2. Run all cells sequentially
3. The notebook will:
   - Download/create population data
   - Extract infrastructure data from OpenStreetMap
   - Create buffer zones around substations
   - Generate layered visualizations
   - Perform statistical analysis

### 3. Output Files
- `zambia_energy_access_analysis.png`: Main layered visualization
- `zambia_energy_analysis_summary.png`: Statistical summary charts
- `zambia_population_density.tif`: Population density raster data

## Analysis Results

### Key Metrics
- **Population Distribution**: Percentage within/outside 10km of substations
- **Density Comparison**: Average population density in buffer zones vs. outside
- **Infrastructure Coverage**: Total area covered by buffer zones
- **Voltage Distribution**: Breakdown of transmission lines by voltage level

### Energy Access Indicators
- **Access Ratio**: Population density within buffers / density outside buffers
- **Coverage Percentage**: Proportion of population with proximity to substations
- **Infrastructure Gaps**: Areas with high population but limited electrical infrastructure

## Data Sources and Attribution

### Population Data
- **Source**: WorldPop (https://www.worldpop.org/)
- **License**: Creative Commons Attribution 4.0 International
- **Citation**: "WorldPop Global Population Datasets"

### Infrastructure Data
- **Source**: OpenStreetMap (https://www.openstreetmap.org/)
- **License**: Open Database License (ODbL)
- **API**: Overpass API for querying OSM data
- **Attribution**: © OpenStreetMap contributors

## Technical Implementation

### Overpass Queries
```javascript
// Transmission Lines Query
[out:json][timeout:60];
(
    way["power"="line"]["voltage"](bbox:-18.5,21.5,-8.5,34.0);
    relation["power"="line"]["voltage"](bbox:-18.5,21.5,-8.5,34.0);
);
out geom;

// Substations Query
[out:json][timeout:60];
(
    node["power"="substation"](bbox:-18.5,21.5,-8.5,34.0);
    way["power"="substation"](bbox:-18.5,21.5,-8.5,34.0);
);
out center;
```

### Coordinate Reference Systems
- **Display CRS**: WGS84 (EPSG:4326)
- **Analysis CRS**: UTM Zone 35S (EPSG:32735)
- **Rationale**: UTM for accurate distance calculations, WGS84 for web compatibility

## Visualization Features

### Design Principles
1. **Light Theme**: White background for professional presentation
2. **High Contrast**: Colors chosen for accessibility and clarity
3. **Layer Hierarchy**: Logical stacking order for data interpretation
4. **Scale Awareness**: Appropriate symbol sizes and line weights

### Color Palette
- **Population Density**: White to orange gradient
- **Buffer Zones**: Light blue with transparency
- **Transmission Lines**: Voltage-coded spectrum
- **Substations**: Black with white outlines

## Applications

### Energy Planning
- Identify underserved population areas
- Plan new substation locations
- Assess transmission line adequacy
- Prioritize infrastructure investments

### Research Applications
- Energy access studies
- Rural electrification analysis
- Infrastructure-population relationships
- Geospatial data science methods

### Policy Support
- Evidence-based energy policy
- Rural development planning
- Infrastructure gap analysis
- Sustainable development goals (SDG 7)

## Limitations and Considerations

### Data Limitations
1. **OpenStreetMap Coverage**: May not include all infrastructure
2. **Population Data**: Based on modeled estimates
3. **Temporal Alignment**: Data from different time periods
4. **Infrastructure Details**: Limited attribute information

### Analysis Limitations
1. **10km Buffer**: Simplified proximity metric
2. **Linear Distance**: Doesn't account for terrain or access roads
3. **Energy Access**: Proximity doesn't guarantee actual access
4. **Grid Connection**: Doesn't show actual electrical connections

## Future Enhancements

### Data Integration
- Real-time infrastructure data
- Household electrification surveys
- Economic development indicators
- Geographic accessibility models

### Analysis Extensions
- Network analysis of transmission systems
- Cost-distance modeling
- Multi-criteria decision analysis
- Temporal change analysis

### Visualization Improvements
- Interactive web maps
- 3D terrain visualization
- Animation of infrastructure development
- Mobile-responsive dashboards

## Contributing

Contributions to improve the analysis are welcome:
1. Fork the repository
2. Create a feature branch
3. Make improvements
4. Submit a pull request

## License

This project is available under the MIT License. See LICENSE file for details.

## Contact

For questions or collaboration opportunities, please open an issue in the repository.

---

**Note**: This analysis is for educational and research purposes. For official energy planning, consult with relevant authorities and use authoritative data sources.