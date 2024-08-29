# src/utils/helpers.py
import logging

# Configure logging for the utility module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_injury_rate(injuries, games_played):
    """
    Calculate the injury rate based on the number of injuries and games played.

    Args:
    injuries (int): Number of injuries.
    games_played (int): Number of games played.

    Returns:
    float: Injury rate, or 0 if games_played is 0.
    """
    try:
        return injuries / games_played if games_played > 0 else 0
    except TypeError as e:
        logging.error(f"Invalid input types for calculate_injury_rate: {e}")
        return 0

def format_percentage(value, total):
    """
    Format a value as a percentage of a total.

    Args:
    value (int or float): The part value.
    total (int or float): The total value.

    Returns:
    str: The formatted percentage string, or '0.00%' if total is 0.
    """
    try:
        percentage = (value / total) * 100 if total > 0 else 0
        return f"{percentage:.2f}%"
    except TypeError as e:
        logging.error(f"Invalid input types for format_percentage: {e}")
        return "0.00%"

def format_number(num):
    """
    Format a number into a more readable string (e.g., 1000 -> '1K', 1000000 -> '1M').

    Args:
    num (int or float): The number to format.

    Returns:
    str: The formatted number string.
    """
    try:
        if num >= 1000000:
            return f'{num // 1000000}M'
        elif num >= 1000:
            return f'{num // 1000}K'
        else:
            return str(num)
    except TypeError as e:
        logging.error(f"Invalid input type for format_number: {e}")
        return str(num)

def calculate_avg_injuries_per_season(total_injuries, num_seasons):
    """
    Calculate the average number of injuries per season.

    Args:
    total_injuries (int): Total number of injuries over multiple seasons.
    num_seasons (int): Number of seasons.

    Returns:
    float: Average injuries per season, or 0 if num_seasons is 0.
    """
    try:
        return total_injuries / num_seasons if num_seasons > 0 else 0
    except TypeError as e:
        logging.error(f"Invalid input types for calculate_avg_injuries_per_season: {e}")
        return 0

def calculate_injury_severity(weeks_injured):
    """
    Categorize the severity of an injury based on the number of weeks injured.

    Args:
    weeks_injured (int): Number of weeks the player was injured.

    Returns:
    str: Severity level ('Minor', 'Moderate', 'Severe').
    """
    try:
        if weeks_injured <= 1:
            return "Minor"
        elif weeks_injured <= 4:
            return "Moderate"
        else:
            return "Severe"
    except TypeError as e:
        logging.error(f"Invalid input type for calculate_injury_severity: {e}")
        return "Unknown"

def calculate_team_injury_impact(games_missed, total_games, roster_size=53):
    """
    Calculate the impact of injuries on a team based on games missed and total games.

    Args:
    games_missed (int): Total games missed due to injuries.
    total_games (int): Total games played.
    roster_size (int, optional): The size of the team roster. Default is 53.

    Returns:
    float: Impact score, or 0 if total_games is 0.
    """
    try:
        return games_missed / (total_games * roster_size) if total_games > 0 else 0
    except TypeError as e:
        logging.error(f"Invalid input types for calculate_team_injury_impact: {e}")
        return 0
