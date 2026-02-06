import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from api.AisPoint import AisPoint
from pathlib import Path
import pickle

def export_to_csv(encounters: list, output_path: str):
    """
    Export encounter data to CSV format
    
    Args:
        encounters: List of encounter dictionaries with 'GW' and 'SO' keys
        output_path: Path to save the CSV file
    """
    print(f"Exporting data to CSV: {output_path}")
    
    rows = []
    
    for encounter_id, encounter in enumerate(encounters):
        # Process GW ship
        for point in encounter['GW']:
            rows.append({
                'encounter_id': encounter_id,
                'ship_role': 'GW',
                'mmsi': point.get_mmsi(),
                'timestamp': point.get_timestamp(),
                'lon': point.get_lon(),
                'lat': point.get_lat(),
                'sog': point.get_sog(),
                'cog': point.get_cog(),
                'heading': point.get_heading(),
                'rot': point.get_rot(),
                'status': point.get_statu(),
                'shiptype': point.get_shiptype()
            })
        
        # Process SO ship
        for point in encounter['SO']:
            rows.append({
                'encounter_id': encounter_id,
                'ship_role': 'SO',
                'mmsi': point.get_mmsi(),
                'timestamp': point.get_timestamp(),
                'lon': point.get_lon(),
                'lat': point.get_lat(),
                'sog': point.get_sog(),
                'cog': point.get_cog(),
                'heading': point.get_heading(),
                'rot': point.get_rot(),
                'status': point.get_statu(),
                'shiptype': point.get_shiptype()
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Successfully exported {len(rows)} rows to {output_path}")


def vis_samples_csv(df, output_dir='figs'):
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']

    # Read CSV file
    
    for encounter_id in df['encounter_id'].unique():
        encounter_df = df[df['encounter_id'] == encounter_id]

        # Separate GW and SO ships
        gw_df = encounter_df[encounter_df['ship_role'] == 'GW'].sort_values('timestamp')
        so_df = encounter_df[encounter_df['ship_role'] == 'SO'].sort_values('timestamp')

        plt.figure(figsize=(6, 4))
        # Extract coordinates
        lon1 = gw_df["lon"].values
        lat1 = gw_df["lat"].values
        lon2 = so_df["lon"].values
        lat2 = so_df["lat"].values
        ax = plt.gca()
        # Draw arrow for GW ship showing initial direction
        if len(lon1) >= 4:
            ax.annotate(
                '',
                xy=(lon1[3], lat1[3]),          # arrow tip
                xytext=(lon1[0], lat1[0]),      # first point
                arrowprops=dict(
                    headwidth=10,
                    width=2,
                    linewidth=2,
                    color='black'
                )
            )
        # Draw arrow for SO ship showing initial direction
        if len(lon2) >= 4:
            ax.annotate(
                '',
                xy=(lon2[3], lat2[3]),          # arrow tip
                xytext=(lon2[0], lat2[0]),      # first point
                arrowprops=dict(
                    headwidth=10,
                    width=2,
                    linewidth=2,
                    color='black'
                )
            ) 
        # Plot trajectories
        plt.plot(lon1, lat1, marker='o', markersize=5, label='GW ship', linewidth=2)
        plt.plot(lon2, lat2, marker='o', markersize=5, label='SO ship', linewidth=2)
        # Draw lines connecting corresponding time points
        min_len = min(len(lon1), len(lon2))
        for i in range(min_len):
            plt.plot([lon1[i], lon2[i]], [lat1[i], lat2[i]], 
                    color='gray', linestyle='--', linewidth=1, alpha=0.5)
        plt.xlabel('Longitude [°E]', fontsize=12)
        plt.ylabel('Latitude [°N]', fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.title(f'Cross sample {encounter_id}', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        # Save figure
        output_file = Path(output_dir) / f'cross_sample_{encounter_id}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    # Set up file paths
    script_dir = Path(__file__).resolve().parent
    pickle_file = script_dir / "samples.pkl"
    csv_file = script_dir / "samples.csv"
    
    print("="*60)
    print("Ship Encounter Data - CSV Converter and Visualizer")
    print("="*60)
    
    # Step 1: Convert pickle to CSV
    print(f"\nStep 1: Converting pickle to CSV")
    print(f"Input:  {pickle_file}")
    print(f"Output: {csv_file}")
    
    with open(pickle_file, 'rb') as f:
        encounters_from_pickle = pickle.load(f)
    
    export_to_csv(encounters_from_pickle, csv_file)
    
    # Step 2: Load from CSV
    df = pd.read_csv(csv_file)
    
    # Step 3: Visualize
    print(f"\nStep 3: Visualizing encounters")
    vis_samples_csv(df, output_dir='figs')
    
    
    print("\n" + "="*60)
    print("Process completed successfully!")
    print("="*60)
    print(f"\nGenerated files:")
    print(f"  - CSV data: {csv_file}")
    print(f"  - Figures:  {script_dir / 'figs'}/")
    print("="*60)