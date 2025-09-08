# Zambia Geospatial Visualization Project

This project creates a comprehensive geospatial visualization of Zambia combining population density data with power infrastructure information.

## Overview

The visualization includes three layers:
1. **Base Layer**: Population density map from WorldPop (TIFF format)
2. **Second Layer**: Transmission lines from OpenStreetMap with voltage-based color coding
3. **Third Layer**: Substations from OpenStreetMap (black with full opacity)

## Features

- 🗺️ **Population Density Mapping**: High-resolution data from WorldPop
- ⚡ **Power Infrastructure**: Transmission lines and substations from OpenStreetMap
- 🎨 **Voltage Color Coding**: Clear visual distinction between different voltage levels
- 📊 **Professional Visualization**: Light theme with excellent contrast
- 📓 **Interactive Notebook**: Well-documented Jupyter notebook for learning

## Installation

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open the Jupyter notebook:
   ```bash
   jupyter notebook zambia_geospatial_visualization.ipynb
   ```

2. Run all cells to:
   - Download WorldPop data for Zambia
   - Query OpenStreetMap for power infrastructure
   - Create the layered visualization

## Data Sources

- **Population Density**: [WorldPop](https://www.worldpop.org/)
- **Power Infrastructure**: [OpenStreetMap](https://www.openstreetmap.org/) via Overpass API

## Output

The notebook generates:
- High-resolution PNG visualization (`zambia_geospatial_visualization.png`)
- Population density TIFF file
- Detailed summary statistics

## Color Scheme

### Transmission Lines (by voltage):
- **≥300kV**: Dark Red (#8B0000)
- **200-299kV**: Orange Red (#FF4500)
- **130-199kV**: Dark Orange (#FF8C00)
- **80-129kV**: Gold (#FFD700)
- **60-79kV**: Lime Green (#32CD32)
- **30-59kV**: Royal Blue (#4169E1)
- **<30kV**: Dark Orchid (#9932CC)
- **Unknown**: Gray (#808080)

### Substations:
- **Color**: Black with white borders
- **Opacity**: 100% (full opacity)

## Technical Details

- **Coordinate System**: WGS84 (EPSG:4326)
- **Population Data**: WorldPop constrained population counts
- **Infrastructure Data**: OpenStreetMap via Overpass API
- **Visualization**: Matplotlib with light theme optimization

## Dependencies

See `requirements.txt` for full list of dependencies including:
- `jupyter` - Interactive notebook environment
- `rasterio` - Geospatial raster data processing
- `overpy` - OpenStreetMap Overpass API client
- `geopandas` - Geospatial data manipulation
- `matplotlib` - Plotting and visualization
- `folium` - Interactive mapping (optional)

## Author

Created for the ALX learning program - demonstrating geospatial data visualization techniques.

## License

This project is for educational purposes as part of the ALX curriculum.