# Conditional Trajectory Prediction - Samples of encounter data

A demo for loading and visualizing ship encounter trajectory data.

![Example crossing scenario](figs/cross_sample_9.png)

## Structure

```
conditional-trajectory-prediction/
├── api/
│   ├── AisPoint.py          # AIS point data structure and utilities
│   └── __init__.py
├── figs/                     # Generated visualization outputs
├── load_samples.py           # Main script for loading and visualizing data
├── samples.pkl               # Sample encounter data
└── README.md
```

## Installation

### Dependencies

- Python 3.11
- NumPy
- Matplotlib
- Pickle (standard library)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/UT-shunqiang/conditional-trajectory-prediction.git
cd conditional-trajectory-prediction
```

2. Install dependencies:
```bash
pip install numpy matplotlib
```

## Usage

### Loading and Visualizing Sample Data

Run the main script to load sample encounters and generate visualizations:

```bash
python load_samples.py
```

This will:
1. Load encounter data from `samples.pkl`
2. Generate trajectory plots for each encounter
3. Save high-resolution figures (300 DPI) to the `figs/` directory

### Working with AIS Points

```python
from api.AisPoint import AisPoint

# Create an AIS point
ais_point = AisPoint(
    mmsi=123456789,           # Ship MMSI
    timestamp=1234567890,     # Unix timestamp
    lon=12.345,               # Longitude (°E)
    lat=56.789,               # Latitude (°N)
    sog=10.5,                 # Speed over ground (knots)
    cog=45.0,                 # Course over ground (degrees)
    heading=47.0,             # True heading
    rot=0.5,                  # Rate of turn
    statu=0,                  # Navigation status
    shiptype=70               # Ship type code
)

# Access properties
print(f"Position: {ais_point.get_lat()}°N, {ais_point.get_lon()}°E")
print(f"Speed: {ais_point.get_sog()} knots")
print(f"Course: {ais_point.get_cog()}°")
```

### Working with Encounter Data

```python
from load_samples import load_data, get_lons, get_lats
from pathlib import Path

# Load encounter samples
file_path = Path("samples.pkl")
encounters = load_data(file_path)

# Process first encounter
encounter = encounters[0]
gw_ship = encounter['GW']  # Give-way ship trajectory
so_ship = encounter['SO']  # Stand-on ship trajectory

# Extract coordinates
gw_lons = get_lons(gw_ship)
gw_lats = get_lats(gw_ship)
so_lons = get_lons(so_ship)
so_lats = get_lats(so_ship)
```

## Data Format

### Encounter Dictionary Structure

Each encounter in `samples.pkl` contains:
- `'GW'`: List of AisPoint objects for the Give-Way vessel
- `'SO'`: List of AisPoint objects for the Stand-On vessel

### AIS Point Attributes

- `mmsi`: Maritime Mobile Service Identity
- `timestamp`: Unix timestamp
- `lon`: Longitude in decimal degrees (°E)
- `lat`: Latitude in decimal degrees (°N)
- `sog`: Speed Over Ground in knots
- `cog`: Course Over Ground in degrees (0-360°)
- `heading`: True heading in degrees
- `rot`: Rate of Turn in degrees per minute
- `statu`: Navigation status code
- `shiptype`: Ship type code

## API Reference

### load_samples.py Functions

- `load_data(file_path: str)`: Load pickled encounter data
- `get_timestamps(ais_points: list)`: Extract timestamps as numpy array
- `get_lons(ais_points: list)`: Extract longitudes as numpy array
- `get_lats(ais_points: list)`: Extract latitudes as numpy array
- `get_cogs(ais_points: list)`: Extract courses as numpy array
- `get_sogs(ais_points: list)`: Extract speeds as numpy array
- `vis_samples(encounters_samples)`: Generate and save visualization plots


## Contact

Email: Send your inquiries or support requests to s.xu-1@utwente.nl.

