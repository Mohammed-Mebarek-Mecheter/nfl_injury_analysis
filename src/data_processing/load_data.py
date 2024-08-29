import pandas as pd
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_dataset(filename, data_dir=None):
    if data_dir is None:
        data_dir = Path(__file__).parent.parent.parent / 'data'
    else:
        data_dir = Path(data_dir)

    file_path = data_dir / filename

    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded {filename}")
        return df
    except FileNotFoundError:
        logging.error(f"File {filename} not found in {data_dir}")
        return None

def load_all_datasets(data_dir=None):
    """
    Load all datasets from the data directory.

    Returns:
    dict: A dictionary containing all loaded datasets.
    """
    datasets = {
        'concussions': load_dataset('Concussion_Injuries_2012_2014.csv', data_dir),
        'head_injuries': load_dataset('Head_Injured_Players.csv', data_dir),
        'match_dates': load_dataset('Match_Dates.csv', data_dir),
        'matches': load_dataset('Matches_2012_2015.csv', data_dir),
        'nfl_teams': load_dataset('NFL_Teams.csv', data_dir),
        'seasons': load_dataset('Seasons.csv', data_dir)
    }

    return {k: v for k, v in datasets.items() if v is not None}
