# src/data_processing/preprocess_data.py
import pandas as pd
import numpy as np
import logging

def preprocess_data(datasets):
    """
    Preprocess all datasets.

    Args:
    datasets (dict): Dictionary containing all loaded datasets.

    Returns:
    dict: Dictionary containing all preprocessed datasets.
    """
    preprocessed = {}

    for key, df in datasets.items():
        if df is not None:
            try:
                preprocessed[key] = preprocess_dataset(df, key)
            except Exception as e:
                logging.error(f"Error processing {key}: {e}")

    return preprocessed

def preprocess_dataset(df, dataset_name):
    """
    Preprocess a single dataset.

    Args:
    df (pandas.DataFrame): Dataset to preprocess.
    dataset_name (str): Name of the dataset.

    Returns:
    pandas.DataFrame: Preprocessed dataset.
    """
    df = df.copy()
    df = handle_missing_values(df)
    df = convert_date_columns(df)

    # Apply dataset-specific preprocessing
    preprocess_map = {
        'concussions': preprocess_concussions,
        'head_injuries': preprocess_head_injuries,
        'nfl_teams': preprocess_nfl_teams,
        'matches': preprocess_matches,
        'seasons': preprocess_seasons,
        'match_dates': preprocess_match_dates
    }

    if dataset_name in preprocess_map:
        df = preprocess_map[dataset_name](df)
    else:
        logging.warning(f"No specific preprocessing function for dataset: {dataset_name}")

    validate_preprocessed_data(df, dataset_name)

    return df

def handle_missing_values(df):
    """Handle missing values in the dataset."""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    categorical_columns = df.select_dtypes(include=['object']).columns
    df[categorical_columns] = df[categorical_columns].fillna('Unknown')

    return df

def convert_date_columns(df):
    """Convert date columns to datetime format."""
    date_columns = df.filter(like='Date').columns
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
    return df

def preprocess_concussions(df):
    """Preprocess the concussions dataset."""
    yes_no_columns = ['Pre-Season Injury?', 'Winning Team?', 'Unknown Injury?']
    for col in yes_no_columns:
        if col in df.columns:
            df[col] = df[col].str.capitalize()

    df['Severity'] = pd.cut(df['Weeks Injured'], bins=[0, 1, 2, 4, 8, np.inf],
                            labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

    df['Play Time After Injury'] = df['Play Time After Injury'].fillna('Unknown')
    df['Average Playtime Before Injury'] = df['Average Playtime Before Injury'].fillna('Unknown')

    return df

def preprocess_head_injuries(df):
    """Preprocess the head injuries dataset."""
    injury_columns = [
        '2012/2013 - Number of Injuries', '2012/2013 - Games Missed',
        '2013/2014 - Number of Injuries', '2013/2014 - Games Missed',
        '2014/2015 - Number of Injuries', '2014/2015 - Games Missed'
    ]

    for col in injury_columns:
        df[col] = df[col].fillna(0)

    df['Total Number of Injuries'] = df[[col for col in df.columns if 'Number of Injuries' in col]].sum(axis=1)
    df['Total Games Missed'] = df[[col for col in df.columns if 'Games Missed' in col]].sum(axis=1)

    if 'Roles during injuries' in df.columns:
        df['Roles during injuries'] = df['Roles during injuries'].str.title()

    # Create a list of seasons for each player based on non-zero injury counts
    df['Seasons'] = df.apply(lambda row: [
        '2012/2013' if row['2012/2013 - Number of Injuries'] > 0 else None,
        '2013/2014' if row['2013/2014 - Number of Injuries'] > 0 else None,
        '2014/2015' if row['2014/2015 - Number of Injuries'] > 0 else None
    ], axis=1)
    df['Seasons'] = df['Seasons'].apply(lambda x: [s for s in x if s is not None])

    return df

def preprocess_nfl_teams(df):
    """Preprocess the NFL teams dataset."""
    if 'Team' in df.columns:
        df['Team'] = df['Team'].str.upper()

    injury_columns = [
        '2012/2013 - Number of Injuries', '2012/2013 - Weeks of Injury, by all its players',
        '2013/2014 - Number of Injuries', '2013/2014 - Weeks of Injury, by all its players',
        '2014/2015 - Number of Injuries', '2014/2015 - Weeks of Injury, by all its players'
    ]

    for col in injury_columns:
        df[col] = df[col].fillna(0)

    return df

def preprocess_matches(df):
    """Preprocess the matches dataset."""
    if 'Team 1' in df.columns and 'Team 2' in df.columns:
        df['Match'] = df['Team 1'] + ' vs ' + df['Team 2']

    df['Score Team 1'] = df['Score Team 1'].fillna(0)
    df['Score Team 2'] = df['Score Team 2'].fillna(0)

    return df

def preprocess_seasons(df):
    """Preprocess the seasons dataset."""
    integer_columns = [
        'Total Number of Injuries', 'Total Games Missed, by all players',
        'Total Weeks of Injury, all its players'
    ]

    for col in integer_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df

def preprocess_match_dates(df):
    """Preprocess the match dates dataset."""
    integer_columns = ['Number of Injuries', 'Week']

    for col in integer_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df

def validate_preprocessed_data(df, dataset_name):
    """
    Validate the preprocessed dataset to ensure it contains the necessary columns.

    Args:
    df (pandas.DataFrame): Preprocessed dataset.
    dataset_name (str): Name of the dataset.
    """
    required_columns = {
        'concussions': ['ID', 'Player', 'Team', 'Date', 'Weeks Injured', 'Severity', 'Play Time After Injury', 'Average Playtime Before Injury'],
        'head_injuries': ['Player', 'Total Number of Injuries', 'Total Games Missed', 'Roles during injuries'],
        'match_dates': ['Date', 'Number of Injuries', 'Week', 'Season'],
        'nfl_teams': ['Team', 'Total Number of Injuries (2012-2014)', 'Total Weeks of Injury, by all its players (2012-2014)'],
        'matches': ['Match', 'Date', 'Team 1', 'Team 2', 'Score Team 1', 'Score Team 2'],
        'seasons': ['Season', 'Total Number of Injuries', 'Total Games Missed, by all players', 'Total Weeks of Injury, all its players']
    }

    if dataset_name in required_columns:
        missing_columns = set(required_columns[dataset_name]) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Dataset '{dataset_name}' is missing columns: {missing_columns}")
