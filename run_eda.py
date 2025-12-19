#!/usr/bin/env python3
"""
Quick start script for running the LoL Esports EDA pipeline.

This script provides a simple command-line interface to run
the complete exploratory data analysis on 2025 LoL esports data.

Usage:
    python run_eda.py

Returns:
    None: Executes the full EDA pipeline and saves results.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.eda_analysis import main

if __name__ == "__main__":
    print("="*70)
    print("League of Legends Esports - 2025 Season EDA")
    print("="*70)
    print()

    main()

    print()
    print("="*70)
    print("Analysis complete!")
    print()
    print("Next steps:")
    print("  - View visualizations in: output/figures/")
    print("  - Check processed data in: data/processed/")
    print("  - Explore interactively: jupyter lab notebooks/")
    print("="*70)
