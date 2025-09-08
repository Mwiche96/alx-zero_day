#!/usr/bin/env python3
"""
Test script to verify basic functionality of the Zambia geospatial visualization
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import requests
        print("✓ requests")
    except ImportError as e:
        print(f"✗ requests: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas")
    except ImportError as e:
        print(f"✗ pandas: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib")
    except ImportError as e:
        print(f"✗ matplotlib: {e}")
        return False
    
    # Optional packages (graceful fallback)
    try:
        import rasterio
        print("✓ rasterio (optional - will create sample data if missing)")
    except ImportError:
        print("! rasterio not available - will create sample data")
    
    try:
        import overpy
        print("✓ overpy (optional - will create sample data if missing)")
    except ImportError:
        print("! overpy not available - will create sample data")
    
    try:
        import geopandas as gpd
        print("✓ geopandas (optional - will use alternative approach if missing)")
    except ImportError:
        print("! geopandas not available - will use alternative approach")
    
    return True

def create_sample_visualization():
    """Create a simple sample visualization to test basic functionality"""
    print("\nCreating sample visualization...")
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Create sample data
    np.random.seed(42)
    
    # Sample coordinates for Zambia
    lons = np.linspace(22, 34, 100)
    lats = np.linspace(-18, -8, 100)
    
    # Create sample population density data
    pop_density = np.random.exponential(scale=50, size=(100, 100))
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig.patch.set_facecolor('white')
    
    # Plot population density
    im = ax.imshow(pop_density, extent=[22, 34, -18, -8], 
                   cmap='YlOrRd', alpha=0.7, aspect='auto')
    
    # Add sample transmission lines
    line_coords = [
        ([28.28, 28.64, 29.12], [-15.42, -15.13, -14.85]),  # High voltage
        ([28.28, 28.73, 29.12], [-12.97, -12.84, -12.71]),  # Medium voltage
        ([25.85, 26.73, 27.85], [-17.85, -16.92, -15.98]),  # Lower voltage
    ]
    
    colors = ['#8B0000', '#FF8C00', '#32CD32']
    labels = ['≥300kV', '130-199kV', '60-79kV']
    
    for i, (lons_line, lats_line) in enumerate(line_coords):
        ax.plot(lons_line, lats_line, color=colors[i], linewidth=3, 
                alpha=0.8, label=f'Transmission {labels[i]}')
    
    # Add sample substations
    substation_lons = [28.28, 28.25, 28.64, 27.85, 25.85]
    substation_lats = [-15.42, -12.97, -12.84, -15.98, -17.85]
    
    ax.scatter(substation_lons, substation_lats, color='black', s=100, 
               marker='s', edgecolors='white', linewidth=2, 
               label='Substations', alpha=1.0)
    
    # Customize plot
    ax.set_title('Zambia: Population Density with Power Infrastructure (Sample)\\n' +
                 'Base: Population Density | Lines: Transmission by Voltage | Points: Substations',
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), 
              frameon=True, fancybox=True, shadow=True)
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.6, aspect=30)
    cbar.set_label('Population Density (sample data)', fontsize=10, fontweight='bold')
    
    # Save the plot
    plt.tight_layout()
    output_file = 'test_visualization.png'
    fig.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Sample visualization created: {output_file}")
    return True

def main():
    """Main test function"""
    print("=" * 60)
    print("ZAMBIA GEOSPATIAL VISUALIZATION - FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n✗ Import test failed!")
        return False
    
    print("\n✓ All critical imports successful!")
    
    # Test basic visualization
    try:
        if create_sample_visualization():
            print("\n✓ Sample visualization test passed!")
        else:
            print("\n✗ Sample visualization test failed!")
            return False
    except Exception as e:
        print(f"\n✗ Sample visualization test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("The notebook should work with your environment.")
    print("Note: Full functionality requires internet access for downloading")
    print("WorldPop data and querying OpenStreetMap.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)