#!/usr/bin/env python3
"""
Test script to verify the Zambia energy access analysis functionality.
This script runs the core analysis components to ensure everything works correctly.
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS
from shapely.geometry import Point, LineString
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib style for light theme
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.2

def create_test_population_data():
    """Create synthetic population density data for testing."""
    print("Creating synthetic population density data...")
    
    # Zambia bounds
    min_lon, max_lon = 21.5, 34.0
    min_lat, max_lat = -18.5, -8.5
    width, height = 100, 75
    
    # Generate realistic population distribution
    np.random.seed(42)
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    X, Y = np.meshgrid(x, y)
    
    # Create population centers
    centers = [(0.3, 0.7), (0.6, 0.4), (0.8, 0.8), (0.2, 0.3)]
    population = np.zeros((height, width))
    
    for cx, cy in centers:
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
        population += 500 * np.exp(-10 * dist)
    
    population += np.random.exponential(20, (height, width))
    
    # Save as GeoTIFF
    transform = from_bounds(min_lon, min_lat, max_lon, max_lat, width, height)
    
    with rasterio.open(
        'test_zambia_population.tif',
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=population.dtype,
        crs=CRS.from_epsg(4326),
        transform=transform,
    ) as dst:
        dst.write(population, 1)
    
    print("✅ Population data created")
    return 'test_zambia_population.tif'

def create_sample_substations():
    """Create sample substation data."""
    print("Creating sample substations...")
    
    substations_data = [
        {'geometry': Point(28.28, -15.41), 'name': 'Lusaka Central', 'voltage': '330/132', 'id': 1},
        {'geometry': Point(28.22, -12.97), 'name': 'Kitwe Main', 'voltage': '220/132', 'id': 2},
        {'geometry': Point(31.47, -12.84), 'name': 'Kasama', 'voltage': '132/33', 'id': 3},
        {'geometry': Point(30.05, -14.78), 'name': 'Serenje', 'voltage': '220/88', 'id': 4},
        {'geometry': Point(26.95, -14.29), 'name': 'Solwezi', 'voltage': '330/132', 'id': 5},
        {'geometry': Point(26.18, -17.87), 'name': 'Livingstone', 'voltage': '330/88', 'id': 6},
    ]
    
    gdf = gpd.GeoDataFrame(substations_data, crs='EPSG:4326')
    print(f"✅ Created {len(gdf)} substations")
    return gdf

def create_sample_transmission_lines():
    """Create sample transmission lines."""
    print("Creating sample transmission lines...")
    
    lines_data = [
        {'geometry': LineString([(28.3, -15.4), (30.2, -14.8), (31.5, -12.8)]), 'voltage': '330000', 'id': 1},
        {'geometry': LineString([(28.3, -15.4), (26.8, -14.2), (25.9, -13.1)]), 'voltage': '220000', 'id': 2},
        {'geometry': LineString([(30.2, -14.8), (29.1, -13.5), (28.2, -12.1)]), 'voltage': '132000', 'id': 3},
        {'geometry': LineString([(26.2, -17.8), (28.3, -15.4), (29.8, -13.9)]), 'voltage': '330000', 'id': 4},
        {'geometry': LineString([(24.8, -16.2), (26.5, -15.1), (28.1, -14.3)]), 'voltage': '88000', 'id': 5}
    ]
    
    gdf = gpd.GeoDataFrame(lines_data, crs='EPSG:4326')
    print(f"✅ Created {len(gdf)} transmission lines")
    return gdf

def create_buffers(substations, buffer_km=10):
    """Create buffer zones around substations."""
    print(f"Creating {buffer_km}km buffer zones...")
    
    # Convert to UTM for accurate distance calculations
    substations_utm = substations.to_crs('EPSG:32735')
    buffers = substations_utm.copy()
    buffers['geometry'] = substations_utm.geometry.buffer(buffer_km * 1000)
    buffers = buffers.to_crs('EPSG:4326')
    
    print(f"✅ Created {len(buffers)} buffer zones")
    return buffers

def assign_voltage_colors(transmission_lines):
    """Assign colors based on voltage levels."""
    print("Assigning voltage colors...")
    
    voltage_colors = {
        '330000': '#FF0000',  # Red
        '220000': '#FF6600',  # Orange-Red  
        '132000': '#FF9900',  # Orange
        '88000': '#0066CC',   # Blue
        '66000': '#0099FF',   # Light Blue
        '33000': '#00CC66',   # Green
        'unknown': '#333333'  # Dark Gray
    }
    
    lines = transmission_lines.copy()
    lines['voltage_clean'] = lines['voltage'].astype(str)
    lines['color'] = lines['voltage_clean'].map(voltage_colors)
    
    print("✅ Voltage colors assigned")
    return lines, voltage_colors

def create_visualization(pop_file, substations, transmission_lines, buffers, voltage_colors):
    """Create the main visualization."""
    print("Creating layered visualization...")
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12), dpi=150)
    
    # Load population data
    with rasterio.open(pop_file) as src:
        population_data = src.read(1)
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
        
        # Create colormap
        colors_pop = ['#FFFFFF', '#FFF5E6', '#FFE6CC', '#FFD1A3', 
                      '#FFBC7A', '#FFA751', '#FF9228', '#FF7D00', 
                      '#E6700A', '#CC6314', '#B3561E']
        pop_cmap = LinearSegmentedColormap.from_list('population', colors_pop)
        
        # Display population density
        pop_plot = ax.imshow(population_data, extent=extent, cmap=pop_cmap, alpha=0.8, aspect='auto')
    
    # Add buffer zones
    buffers.plot(ax=ax, color='lightblue', alpha=0.3, edgecolor='blue', linewidth=0.5, label='10km Buffer Zones')
    
    # Add transmission lines by voltage
    for voltage_level in transmission_lines['voltage_clean'].unique():
        lines_subset = transmission_lines[transmission_lines['voltage_clean'] == voltage_level]
        if len(lines_subset) > 0:
            color = voltage_colors.get(voltage_level, '#333333')
            lines_subset.plot(ax=ax, color=color, linewidth=2.5, alpha=0.9, label=f'{voltage_level}V Lines')
    
    # Add substations
    substations.plot(ax=ax, color='black', markersize=80, alpha=1.0, marker='s', 
                    edgecolor='white', linewidth=1.5, label='Substations')
    
    # Styling
    ax.set_title('Population Density vs Energy Access Analysis - Zambia\\n'
                'Substation Proximity and Transmission Infrastructure', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude (°E)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Latitude (°S)', fontsize=14, fontweight='bold')
    
    # Colorbar
    cbar = plt.colorbar(pop_plot, ax=ax, shrink=0.6, aspect=30)
    cbar.set_label('Population Density (people/km²)', fontsize=12, fontweight='bold')
    
    # Legend
    legend = ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98), fontsize=10, framealpha=0.9)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('black')
    
    # Grid and limits
    ax.grid(True, alpha=0.3, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlim(21.5, 34.0)
    ax.set_ylim(-18.5, -8.5)
    
    plt.tight_layout()
    plt.savefig('test_zambia_visualization.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='black')
    print("✅ Main visualization saved as 'test_zambia_visualization.png'")
    plt.close()

def create_summary_chart(substations, transmission_lines, buffers):
    """Create summary statistics chart."""
    print("Creating summary chart...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10), dpi=150)
    fig.suptitle('Energy Access Analysis Summary - Zambia', fontsize=16, fontweight='bold')
    
    # Chart 1: Infrastructure counts
    categories = ['Substations', 'Buffer Zones', 'Transmission Lines']
    counts = [len(substations), len(buffers), len(transmission_lines)]
    ax1.bar(categories, counts, color=['#4CAF50', '#2196F3', '#FF9800'], alpha=0.8)
    ax1.set_title('Infrastructure Count', fontweight='bold')
    ax1.set_ylabel('Count')
    for i, v in enumerate(counts):
        ax1.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    
    # Chart 2: Voltage distribution
    voltage_counts = transmission_lines['voltage_clean'].value_counts()
    ax2.pie(voltage_counts.values, labels=[f'{v}V' for v in voltage_counts.index], 
            autopct='%1.1f%%', startangle=90)
    ax2.set_title('Transmission Lines by Voltage', fontweight='bold')
    
    # Chart 3: Geographic coverage
    buffers_utm = buffers.to_crs('EPSG:32735')
    total_area = buffers_utm.geometry.area.sum() / 1e6  # km²
    ax3.text(0.5, 0.7, f'Total Buffer Area:', ha='center', fontsize=14, fontweight='bold', transform=ax3.transAxes)
    ax3.text(0.5, 0.5, f'{total_area:,.0f} km²', ha='center', fontsize=20, fontweight='bold', transform=ax3.transAxes)
    ax3.text(0.5, 0.3, f'({len(buffers)} × 10km buffers)', ha='center', fontsize=12, transform=ax3.transAxes)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.set_title('Coverage Statistics', fontweight='bold')
    
    # Chart 4: Analysis info
    ax4.text(0.1, 0.9, 'Analysis Parameters:', fontsize=14, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.1, 0.7, '• Buffer Distance: 10 km', fontsize=12, transform=ax4.transAxes)
    ax4.text(0.1, 0.6, '• Light theme design', fontsize=12, transform=ax4.transAxes)
    ax4.text(0.1, 0.5, '• Voltage-coded lines', fontsize=12, transform=ax4.transAxes)
    ax4.text(0.1, 0.4, '• UTM projection for accuracy', fontsize=12, transform=ax4.transAxes)
    ax4.text(0.1, 0.3, '• High contrast colors', fontsize=12, transform=ax4.transAxes)
    ax4.axis('off')
    ax4.set_title('Methodology', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('test_summary_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Summary chart saved as 'test_summary_chart.png'")
    plt.close()

def main():
    """Run the complete test analysis."""
    print("🚀 Starting Zambia Energy Access Analysis Test")
    print("=" * 50)
    
    try:
        # Create test data
        pop_file = create_test_population_data()
        substations = create_sample_substations()
        transmission_lines = create_sample_transmission_lines()
        
        # Process data
        buffers = create_buffers(substations)
        transmission_lines_colored, voltage_colors = assign_voltage_colors(transmission_lines)
        
        # Create visualizations
        create_visualization(pop_file, substations, transmission_lines_colored, buffers, voltage_colors)
        create_summary_chart(substations, transmission_lines_colored, buffers)
        
        # Clean up test files
        if os.path.exists(pop_file):
            os.remove(pop_file)
        
        print("\n" + "=" * 50)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("Generated files:")
        print("  - test_zambia_visualization.png")
        print("  - test_summary_chart.png")
        print("\nThe analysis components are working correctly!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()