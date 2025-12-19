"""
Source package for LoL Esports Data Analysis.

This package contains modules for data loading, processing,
and exploratory data analysis of professional League of Legends match data.

Returns:
    module: Source package with data analysis utilities.
"""

from .data_loader import DataLoader
from .eda_analysis import EsportsEDA

__all__ = ['DataLoader', 'EsportsEDA']
