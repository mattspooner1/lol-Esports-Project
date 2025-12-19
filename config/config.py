"""
Configuration file for LoL Esports Data Analysis Project.

This module contains all configuration parameters, URLs, and constants
used throughout the data pipeline and analysis.

Returns:
    dict: Configuration parameters accessible throughout the project.
"""

# Google Drive file IDs for Oracle's Elixir datasets
# These IDs map to specific years of professional LoL esports data
ORACLE_ELIXIR_FILE_IDS = {
    2025: "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH",  # User-provided folder ID
    2024: "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH",  # Placeholder - update with actual file ID
    # Add more years as needed
}

# Google Drive base URL for direct CSV download
GOOGLE_DRIVE_DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id={file_id}"

# Data directory paths
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"

# Output directory paths
OUTPUT_DIR = "output"
FIGURES_DIR = f"{OUTPUT_DIR}/figures"
REPORTS_DIR = f"{OUTPUT_DIR}/reports"

# Visualization settings
FIGURE_SIZE = (12, 6)
DPI = 300
STYLE = 'seaborn-v0_8-darkgrid'

# Analysis parameters
CURRENT_YEAR = 2025
MIN_GAMES_THRESHOLD = 5  # Minimum games for player statistics

# Column mappings and data types
EXPECTED_COLUMNS = [
    'gameid', 'datacompleteness', 'url', 'league', 'year', 'split', 'playoffs',
    'date', 'game', 'patch', 'playerid', 'side', 'position', 'playername',
    'teamname', 'champion', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5',
    'gamelength', 'result', 'kills', 'deaths', 'assists', 'teamkills',
    'teamdeaths', 'doublekills', 'triplekills', 'quadrakills', 'pentakills',
    'firstblood', 'firstbloodkill', 'firstbloodassist', 'firstbloodvictim',
    'damagetochampions', 'dpm', 'damageshare', 'damagetakenperminute',
    'damagemitigatedperminute', 'wardsplaced', 'wpm', 'wardskilled',
    'wcpm', 'controlwardsbought', 'visionscore', 'vspm', 'totalgold',
    'earnedgold', 'earned gpm', 'goldspent', 'gspd', 'total cs', 'minionkills',
    'monsterkills', 'monsterkillsownjungle', 'monsterkillsenemyjungle',
    'cspm', 'goldat10', 'xpat10', 'csat10', 'opp_goldat10', 'opp_xpat10',
    'opp_csat10', 'golddiffat10', 'xpdiffat10', 'csdiffat10', 'killsat10',
    'assistsat10', 'deathsat10', 'opp_killsat10', 'opp_assistsat10',
    'opp_deathsat10'
]

# Leaguepedia API settings (for future enrichment)
LEAGUEPEDIA_API_URL = "https://lol.fandom.com/api.php"
MEDIAWIKI_API_URL = "https://en.wikipedia.org/w/api.php"
