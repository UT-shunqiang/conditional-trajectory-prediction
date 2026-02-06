# Conditional Trajectory Prediction

A demo for loading, processing, and visualizing ship encounter trajectory data from AIS (Automatic Identification Systems) data.

![Example crossing scenario](figs/cross_sample_9.png)

## Structure

```
conditional-trajectory-prediction/
├── api/
│   ├── AisPoint.py          # AIS point data structure and utilities
│   └── __init__.py
├── figs/                     # Generated visualization outputs
├── main.py                   # Main script for loading and visualizing data
├── samples.pkl               # Sample encounter data (pickle format)
├── samples.csv               # Sample encounter data (CSV format)
├── requirements.txt          
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher (tested on Python 3.11)
- NumPy
- Pandas
- Matplotlib

### Setup

1. Clone the repository:
```bash
git clone https://github.com/UT-shunqiang/conditional-trajectory-prediction.git
cd conditional-trajectory-prediction
```

2. Install dependencies:
```bash
pip install numpy pandas matplotlib
```

Or use a requirements file (recommended):
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the main script to convert, load, and visualize the sample data:

```bash
python main.py
```

This will:
1. Load encounter data from `samples.pkl`
2. Convert to `samples.csv` format
3. Generate trajectory plots for each encounter
4. Save high-resolution figures (300 DPI) to the `figs/` directory

### Working with AIS Points

The `AisPoint` class provides a structured way to work with AIS data:

```python
from api.AisPoint import AisPoint

# Create an AIS point
ais_point = AisPoint(
    mmsi=123456789,           # Ship identifier (Maritime Mobile Service Identity)
    timestamp=1234567890,     # Unix timestamp or relative time
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

### Working with Encounter Data from Pickle

```python
from main import export_to_csv
from pathlib import Path
import pickle

# Load encounter samples from pickle
pickle_file = Path("samples.pkl")
with open(pickle_file, 'rb') as f:
    encounters = pickle.load(f)

# Process first encounter
encounter = encounters[0]
gw_ship = encounter['GW']  # Give-way ship trajectory (list of AisPoint)
so_ship = encounter['SO']  # Stand-on ship trajectory (list of AisPoint)

print(f"GW ship has {len(gw_ship)} trajectory points")
print(f"SO ship has {len(so_ship)} trajectory points")

# Export to CSV for easier manipulation
export_to_csv(encounters, 'my_encounters.csv')
```

### Working with CSV Data

```python
import pandas as pd
from main import vis_samples_csv

# Load CSV data
df = pd.read_csv('samples.csv')

# View structure
print(df.head())
print(f"\nTotal encounters: {df['encounter_id'].nunique()}")
print(f"Total data points: {len(df)}")

# Filter specific encounter
encounter_0 = df[df['encounter_id'] == 0]
gw_data = encounter_0[encounter_0['ship_role'] == 'GW']
so_data = encounter_0[encounter_0['ship_role'] == 'SO']

# Visualize all encounters
vis_samples_csv(df, output_dir='figs')
```

## Data Format

### CSV Structure

The CSV file contains the following columns:

| Column        | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| encounter_id  | int     | Unique identifier for each encounter             |
| ship_role     | string  | 'GW' (Give-Way) or 'SO' (Stand-On)               |
| mmsi          | int     | Maritime Mobile Service Identity (ship ID)       |
| timestamp     | float   | Unix timestamp or relative time (seconds)        |
| lon           | float   | Longitude in decimal degrees (°E)                |
| lat           | float   | Latitude in decimal degrees (°N)                 |
| sog           | float   | Speed Over Ground in knots                       |
| cog           | float   | Course Over Ground in degrees (0-360°)           |
| heading       | float   | True heading in degrees(not used)                |
| rot           | float   | Rate of Turn in degrees/minute(not used)         |
| status        | int     | Navigation status code(not used)                 |
| shiptype      | int     | Ship type according to AIS specification         |

### Pickle Structure

Each encounter in `samples.pkl` is a dictionary containing:
- `'GW'`: List of AisPoint objects for the Give-Way vessel
- `'SO'`: List of AisPoint objects for the Stand-On vessel

### AIS Point Attributes

- **mmsi**: Maritime Mobile Service Identity - unique 9-digit ship identifier
- **timestamp**: Unix timestamp (seconds) or relative time
- **lon**: Longitude in decimal degrees (°E)
- **lat**: Latitude in decimal degrees (°N)
- **sog**: Speed Over Ground in knots
- **cog**: Course Over Ground in degrees (0-360°)
- **heading**: True heading in degrees (not used)
- **rot**: Rate of Turn in degrees per minute(not used)
- **statu**: Navigation status code(not used)
- **shiptype**: Ship type code per AIS specification (e.g., 84=cargo, 77=tanker)


## API Reference

### main.py Functions

#### `export_to_csv(encounters: list, output_path: str)`
Convert encounter data from pickle format to CSV.

**Parameters:**
- `encounters`: List of encounter dictionaries with 'GW' and 'SO' keys
- `output_path`: Path to save the CSV file

**Example:**
```python
export_to_csv(encounters, 'output.csv')
```

#### `vis_samples_csv(df, output_dir='figs')`
Generate visualization plots from CSV data.

**Parameters:**
- `df`: Pandas DataFrame containing encounter data
- `output_dir`: Directory to save figures (default: 'figs')

**Example:**
```python
import pandas as pd
df = pd.read_csv('samples.csv')
vis_samples_csv(df, output_dir='my_figures')
```

### AisPoint Class Methods

- `get_mmsi()`: Get ship MMSI
- `get_timestamp()`: Get timestamp
- `get_lon()`: Get longitude
- `get_lat()`: Get latitude
- `get_sog()`: Get speed over ground
- `get_cog()`: Get course over ground
- `get_heading()`: Get true heading
- `get_rot()`: Get rate of turn
- `get_statu()`: Get navigation status
- `get_shiptype()`: Get ship type code
- `to_string()`: Convert to comma-separated string
- `to_dict()`: Convert to dictionary
- `from_string(ais_str)`: Create AisPoint from string (static method)
- `list_to_string(ais_points)`: Convert list to string (static method)
- `list_from_string(ais_str)`: Parse string to list (static method)



## Data Source

The sample data in this repository is derived from HELCOM AIS dataset(https://www.dma.dk/safety-at-sea/navigational-information/ais-data).

## Contact
Email: Send your inquiries or support requests to s.xu-1@utwente.nl.