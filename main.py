import numpy as np
import pickle
import matplotlib.pyplot as plt
from api.AisPoint import AisPoint
from pathlib import Path
import os

def load_data(
        file_path: str
        ):
    """
    Load data from a pickle file
    """
    with open(file_path, 'rb') as f:
        file = pickle.load(f)
    return file

def get_timestamps(
        ais_points: list
        ) -> np.ndarray:
    """
    get all timestamps of an ais points list
    """
    return np.array([point.get_timestamp() for point in ais_points])

def get_lons(
        ais_points: list
        ) -> np.ndarray:
    return np.array([point.get_lon() for point in ais_points])

def get_lats(
        ais_points: list
        ) -> np.ndarray:
    return np.array([point.get_lat() for point in ais_points])

def get_cogs(
        ais_points: list
        ) -> np.ndarray:
    return np.array([point.get_cog() for point in ais_points])

def get_sogs(
        ais_points: list
        ) -> np.ndarray:
    return np.array([point.get_sog() for point in ais_points])

def vis_samples(
        encounters_samples):
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    
    for index, encounter in enumerate(encounters_samples):
        plt.figure()
        lon1 = get_lons(encounter['GW'])
        lat1 = get_lats(encounter['GW'])

        lon2 = get_lons(encounter['SO'])
        lat2 = get_lats(encounter['SO'])

        ax = plt.gca()
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

        plt.plot(lon1, lat1, marker='o', markersize=5, label='GW ship')
        plt.plot(lon2, lat2, marker='o', markersize=5, label='SO ship')
        for i in range(len(lon1)):
            plt.plot([lon1[i], lon2[i]], [lat1[i], lat2[i]], color='gray', linestyle='--', linewidth=1, alpha=0.5)
        plt.xlabel('Longitude [°E]', fontsize=12)
        plt.ylabel('Latitude [°N]', fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.title(f'Cross sample {index}', fontsize=12)
        plt.legend(loc=3, fontsize=12)

        figs_dir = Path(__file__).resolve().parent / "figs"
        figs_dir.mkdir(parents=True, exist_ok=True)

        plt.savefig(figs_dir / f'cross_sample_{index}.png', dpi=300)

if __name__ == "__main__":
    file_path = Path(__file__).resolve().parent / "samples.pkl"
    encounter_samples = load_data(file_path)
    print(f"Number of encounters: {len(encounter_samples)}")
    vis_samples(encounter_samples)