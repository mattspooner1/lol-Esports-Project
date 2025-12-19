"""
Data loading and downloading utilities for LoL Esports datasets.

This module handles downloading data from Oracle's Elixir Google Drive,
loading CSV files, and basic data validation.

Returns:
    pd.DataFrame: Loaded and validated esports match data.
"""

import os
import sys
import pandas as pd
import requests
from pathlib import Path
from typing import Optional, List
import gdown

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import (
    RAW_DATA_DIR,
    ORACLE_ELIXIR_FILE_IDS,
    ORACLE_ELIXIR_DIRECT_URLS,
    CURRENT_YEAR
)


class DataLoader:
    """
    Handles downloading and loading of LoL esports match data.

    This class provides methods to download CSV files from Google Drive
    and load them into pandas DataFrames for analysis.

    Returns:
        DataLoader: Instance with methods for data operations.
    """

    def __init__(self, data_dir: str = RAW_DATA_DIR):
        """
        Initialize the DataLoader with specified data directory.

        Args:
            data_dir (str): Directory path for storing raw data files.

        Returns:
            None: Initializes the DataLoader instance.
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_year_data(self, year: int = CURRENT_YEAR, force_download: bool = False) -> str:
        """
        Downloads LoL esports data for a specific year from Google Drive.

        This method uses the gdown library to download CSV files from Oracle's Elixir
        Google Drive repository. It checks if the file already exists before downloading.

        Args:
            year (int): The year of data to download.
            force_download (bool): If True, re-download even if file exists.

        Returns:
            str: Path to the downloaded CSV file.
        """
        file_id = ORACLE_ELIXIR_FILE_IDS.get(year)

        if not file_id:
            raise ValueError(f"No Google Drive file ID configured for year {year}")

        output_path = self.data_dir / f"lol_esports_{year}.csv"

        # Check if file already exists
        if output_path.exists() and not force_download:
            print(f"Data file for {year} already exists at {output_path}")
            return str(output_path)

        try:
            print(f"Downloading {year} LoL esports data from Google Drive...")

            # Try direct URL first if available
            if year in ORACLE_ELIXIR_DIRECT_URLS:
                direct_url = ORACLE_ELIXIR_DIRECT_URLS[year]
                print(f"Using direct download URL...")

                response = requests.get(direct_url, stream=True)
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                chunk_size = 8192

                with open(output_path, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"\rDownloading: {percent:.1f}%", end='', flush=True)
                print()  # New line after progress
            else:
                # Fall back to gdown method
                url = f"https://drive.google.com/uc?id={file_id}"
                gdown.download(url, str(output_path), quiet=False, fuzzy=True)

            print(f"Successfully downloaded data to {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Error downloading data: {e}")
            print(f"\nManual download instructions:")
            print(f"1. Visit: https://drive.google.com/drive/folders/{file_id}")
            print(f"2. Download the {year} CSV file")
            print(f"3. Save it as: {output_path}")
            raise

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Loads a CSV file into a pandas DataFrame with error handling.

        This method reads CSV files with proper encoding and data type inference,
        handling common issues like mixed types and missing values.

        Args:
            file_path (str): Path to the CSV file to load.

        Returns:
            pd.DataFrame: Loaded data as a pandas DataFrame.
        """
        try:
            print(f"Loading data from {file_path}...")

            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1']

            for encoding in encodings:
                try:
                    df = pd.read_csv(
                        file_path,
                        encoding=encoding,
                        low_memory=False,
                        na_values=['', 'NA', 'N/A', 'null', 'NULL']
                    )
                    print(f"Successfully loaded {len(df)} rows with encoding: {encoding}")
                    return df
                except UnicodeDecodeError:
                    continue

            raise ValueError(f"Could not read file with any of these encodings: {encodings}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at {file_path}")
        except Exception as e:
            raise Exception(f"Error loading CSV: {e}")

    def load_year_data(self, year: int = CURRENT_YEAR, download_if_missing: bool = True) -> pd.DataFrame:
        """
        Loads LoL esports data for a specific year, downloading if necessary.

        This is a convenience method that combines download and load operations,
        automatically downloading the data if it's not found locally.

        Args:
            year (int): The year of data to load.
            download_if_missing (bool): If True, download data if not found locally.

        Returns:
            pd.DataFrame: Complete dataset for the specified year.
        """
        file_path = self.data_dir / f"lol_esports_{year}.csv"

        # Download if file doesn't exist and download is enabled
        if not file_path.exists() and download_if_missing:
            print(f"Data file for {year} not found locally.")
            file_path = self.download_year_data(year)
        elif not file_path.exists():
            raise FileNotFoundError(
                f"Data file for {year} not found at {file_path}. "
                f"Set download_if_missing=True to download automatically."
            )

        return self.load_csv(str(file_path))

    def get_data_info(self, df: pd.DataFrame) -> dict:
        """
        Extracts basic information and statistics about the loaded dataset.

        Provides a comprehensive overview of the dataset including shape,
        columns, data types, missing values, and basic statistics.

        Args:
            df (pd.DataFrame): The dataset to analyze.

        Returns:
            dict: Dictionary containing dataset metadata and statistics.
        """
        info = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'numeric_columns': list(df.select_dtypes(include=['number']).columns),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns)
        }

        return info


def main():
    """
    Main function to demonstrate data loading functionality.

    This function serves as an example of how to use the DataLoader class
    to download and load LoL esports data.

    Returns:
        None: Prints information about the loaded dataset.
    """
    print("=== LoL Esports Data Loader ===\n")

    # Initialize loader
    loader = DataLoader()

    # Load 2025 data
    try:
        df = loader.load_year_data(2025, download_if_missing=True)

        # Display basic info
        info = loader.get_data_info(df)

        print(f"\nDataset Shape: {info['shape']}")
        print(f"Memory Usage: {info['memory_usage']:.2f} MB")
        print(f"\nFirst few rows:")
        print(df.head())

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
