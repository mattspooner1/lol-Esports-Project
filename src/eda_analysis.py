"""
Exploratory Data Analysis (EDA) for LoL Esports 2025 Dataset.

This module performs comprehensive exploratory data analysis including:
- Descriptive statistics
- Data quality assessment
- Player performance metrics
- Champion analytics
- Team comparisons
- Temporal trends
- Statistical visualizations

Returns:
    Analysis: Complete EDA results with visualizations and insights.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Tuple, List, Dict, Optional
import warnings

warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import (
    FIGURES_DIR,
    FIGURE_SIZE,
    DPI,
    STYLE,
    MIN_GAMES_THRESHOLD,
    PROCESSED_DATA_DIR
)
from src.data_loader import DataLoader


class EsportsEDA:
    """
    Comprehensive Exploratory Data Analysis for LoL Esports data.

    This class provides methods for analyzing professional League of Legends
    match data, generating insights, and creating visualizations.

    Returns:
        EsportsEDA: Instance with analysis and visualization methods.
    """

    def __init__(self, df: pd.DataFrame, output_dir: str = FIGURES_DIR):
        """
        Initialize EDA analyzer with dataset and output configuration.

        Args:
            df (pd.DataFrame): The esports dataset to analyze.
            output_dir (str): Directory path for saving visualization outputs.

        Returns:
            None: Initializes the EsportsEDA instance.
        """
        self.df = df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set visualization style
        try:
            plt.style.use(STYLE)
        except:
            plt.style.use('default')

        sns.set_palette("husl")

        # Initialize processed data directory
        self.processed_dir = Path(PROCESSED_DATA_DIR)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def clean_data(self) -> pd.DataFrame:
        """
        Performs data cleaning and preprocessing operations.

        This method handles missing values, converts data types, creates derived
        features, and filters out incomplete or invalid records.

        Returns:
            pd.DataFrame: Cleaned and preprocessed dataset.
        """
        print("Cleaning and preprocessing data...")

        df = self.df.copy()

        # Convert date to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Convert numeric columns
        numeric_cols = [
            'kills', 'deaths', 'assists', 'gamelength', 'totalgold',
            'damagetochampions', 'dpm', 'earnedgold', 'earned gpm',
            'total cs', 'cspm', 'visionscore', 'vspm', 'result'
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Create derived metrics
        if 'kills' in df.columns and 'deaths' in df.columns and 'assists' in df.columns:
            # KDA calculation (avoid division by zero)
            df['kda'] = ((df['kills'] + df['assists']) /
                         df['deaths'].replace(0, 1))

            # Kill participation (if teamkills exists)
            if 'teamkills' in df.columns:
                df['kill_participation'] = (
                    (df['kills'] + df['assists']) / df['teamkills'].replace(0, 1)
                ) * 100

        # Filter player rows only (exclude team summary rows)
        if 'position' in df.columns:
            df = df[df['position'].notna()]
            df = df[df['position'] != 'team']

        # Remove rows with critical missing values
        critical_cols = ['playerid', 'position', 'champion']
        df = df.dropna(subset=[col for col in critical_cols if col in df.columns])

        print(f"Data cleaned: {len(df)} rows remaining")

        self.df_clean = df
        return df

    def generate_summary_statistics(self) -> pd.DataFrame:
        """
        Generates comprehensive summary statistics for the dataset.

        Computes descriptive statistics for all numeric columns including
        mean, median, standard deviation, and quartiles.

        Returns:
            pd.DataFrame: Summary statistics table.
        """
        print("\n=== Summary Statistics ===")

        numeric_cols = self.df_clean.select_dtypes(include=[np.number]).columns
        summary = self.df_clean[numeric_cols].describe()

        print(summary)

        # Save to CSV
        output_path = self.processed_dir / "summary_statistics.csv"
        summary.to_csv(output_path)
        print(f"Summary statistics saved to {output_path}")

        return summary

    def analyze_missing_data(self) -> None:
        """
        Analyzes and visualizes missing data patterns in the dataset.

        Creates a bar chart showing the percentage of missing values
        for each column, helping identify data quality issues.

        Returns:
            None: Saves visualization to output directory.
        """
        print("\n=== Missing Data Analysis ===")

        missing_percent = (self.df.isnull().sum() / len(self.df)) * 100
        missing_percent = missing_percent[missing_percent > 0].sort_values(ascending=False)

        if len(missing_percent) == 0:
            print("No missing data found!")
            return

        print(f"\nColumns with missing data:")
        print(missing_percent)

        # Visualize missing data
        fig, ax = plt.subplots(figsize=(12, max(6, len(missing_percent) * 0.3)))
        missing_percent.plot(kind='barh', ax=ax, color='coral')
        ax.set_xlabel('Missing Percentage (%)', fontsize=12)
        ax.set_ylabel('Column', fontsize=12)
        ax.set_title('Missing Data Analysis', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        save_path = self.output_dir / "missing_data_analysis.png"
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        print(f"Missing data visualization saved to {save_path}")
        plt.close()

    def analyze_player_performance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Analyzes individual player performance metrics across all games.

        Computes aggregate statistics for each player including average KDA,
        damage per minute, CS per minute, and game counts. Filters for players
        with minimum game threshold.

        Args:
            top_n (int): Number of top players to display in rankings.

        Returns:
            pd.DataFrame: Player performance statistics sorted by KDA.
        """
        print(f"\n=== Player Performance Analysis ===")

        df = self.df_clean.copy()

        # Group by player
        player_stats = df.groupby(['playerid', 'playername']).agg({
            'gameid': 'count',
            'kills': 'mean',
            'deaths': 'mean',
            'assists': 'mean',
            'kda': 'mean',
            'dpm': 'mean',
            'cspm': 'mean',
            'vspm': 'mean',
            'result': 'mean'  # Win rate
        }).reset_index()

        player_stats.columns = [
            'player_id', 'player_name', 'games_played', 'avg_kills',
            'avg_deaths', 'avg_assists', 'avg_kda', 'avg_dpm',
            'avg_cspm', 'avg_vspm', 'win_rate'
        ]

        # Filter players with minimum games
        player_stats = player_stats[player_stats['games_played'] >= MIN_GAMES_THRESHOLD]

        # Convert win rate to percentage
        player_stats['win_rate'] = player_stats['win_rate'] * 100

        # Sort by KDA
        player_stats = player_stats.sort_values('avg_kda', ascending=False)

        print(f"\nTop {top_n} Players by KDA:")
        print(player_stats.head(top_n)[['player_name', 'games_played', 'avg_kda', 'win_rate']])

        # Save to CSV
        output_path = self.processed_dir / "player_performance.csv"
        player_stats.to_csv(output_path, index=False)
        print(f"\nPlayer performance data saved to {output_path}")

        return player_stats

    def visualize_top_players_kda(self, top_n: int = 15) -> None:
        """
        Creates a horizontal bar chart of top players by KDA ratio.

        Visualizes the highest performing players based on their average
        KDA (Kill/Death/Assist) ratio across all games played.

        Args:
            top_n (int): Number of top players to include in the chart.

        Returns:
            None: Saves visualization to output directory.
        """
        df = self.df_clean.copy()

        # Calculate player KDA
        player_kda = df.groupby('playername').agg({
            'kda': 'mean',
            'gameid': 'count'
        }).reset_index()
        player_kda.columns = ['player', 'avg_kda', 'games']

        # Filter and sort
        player_kda = player_kda[player_kda['games'] >= MIN_GAMES_THRESHOLD]
        top_players = player_kda.nlargest(top_n, 'avg_kda')

        # Create visualization
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(top_players['player'], top_players['avg_kda'], color='skyblue')

        # Color the top 3 differently
        if len(bars) >= 3:
            bars[0].set_color('gold')
            bars[1].set_color('silver')
            bars[2].set_color('#CD7F32')  # Bronze

        ax.set_xlabel('Average KDA', fontsize=12)
        ax.set_ylabel('Player', fontsize=12)
        ax.set_title(f'Top {top_n} Players by KDA (Min {MIN_GAMES_THRESHOLD} games)',
                     fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, top_players['avg_kda'])):
            ax.text(value, bar.get_y() + bar.get_height()/2,
                   f' {value:.2f}',
                   va='center', fontsize=9)

        plt.tight_layout()
        save_path = self.output_dir / "top_players_kda.png"
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        print(f"Top players KDA visualization saved to {save_path}")
        plt.close()

    def analyze_champion_meta(self, top_n: int = 20) -> pd.DataFrame:
        """
        Analyzes champion pick rates, ban rates, and win rates.

        Examines which champions are most popular in professional play,
        their success rates, and overall meta trends.

        Args:
            top_n (int): Number of top champions to analyze.

        Returns:
            pd.DataFrame: Champion statistics including picks, bans, and win rates.
        """
        print(f"\n=== Champion Meta Analysis ===")

        df = self.df_clean.copy()

        # Champion pick analysis
        champion_stats = df.groupby('champion').agg({
            'gameid': 'count',
            'result': 'mean',
            'kills': 'mean',
            'deaths': 'mean',
            'assists': 'mean',
            'kda': 'mean'
        }).reset_index()

        champion_stats.columns = [
            'champion', 'games_picked', 'win_rate', 'avg_kills',
            'avg_deaths', 'avg_assists', 'avg_kda'
        ]

        # Convert win rate to percentage
        champion_stats['win_rate'] = champion_stats['win_rate'] * 100

        # Calculate pick rate (percentage of total games)
        total_games = len(df['gameid'].unique())
        champion_stats['pick_rate'] = (champion_stats['games_picked'] / total_games) * 100

        # Sort by games picked
        champion_stats = champion_stats.sort_values('games_picked', ascending=False)

        print(f"\nTop {top_n} Most Picked Champions:")
        print(champion_stats.head(top_n)[['champion', 'games_picked', 'pick_rate', 'win_rate']])

        # Save to CSV
        output_path = self.processed_dir / "champion_meta.csv"
        champion_stats.to_csv(output_path, index=False)
        print(f"\nChampion meta data saved to {output_path}")

        return champion_stats

    def visualize_champion_pickrate(self, top_n: int = 20) -> None:
        """
        Creates a bar chart showing the most frequently picked champions.

        Visualizes champion popularity in professional play based on
        the number of games each champion was selected.

        Args:
            top_n (int): Number of top champions to display.

        Returns:
            None: Saves visualization to output directory.
        """
        df = self.df_clean.copy()

        champion_picks = df['champion'].value_counts().head(top_n)

        fig, ax = plt.subplots(figsize=(12, 8))
        champion_picks.plot(kind='barh', ax=ax, color='mediumseagreen')

        ax.set_xlabel('Number of Games Picked', fontsize=12)
        ax.set_ylabel('Champion', fontsize=12)
        ax.set_title(f'Top {top_n} Most Picked Champions',
                     fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, value in enumerate(champion_picks.values):
            ax.text(value, i, f' {value}', va='center', fontsize=9)

        plt.tight_layout()
        save_path = self.output_dir / "champion_pickrate.png"
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        print(f"Champion pick rate visualization saved to {save_path}")
        plt.close()

    def analyze_position_metrics(self) -> pd.DataFrame:
        """
        Analyzes performance metrics broken down by player position (role).

        Compares average statistics across different positions (Top, Jungle,
        Mid, ADC, Support) to understand role-specific performance patterns.

        Returns:
            pd.DataFrame: Position-wise aggregate statistics.
        """
        print(f"\n=== Position-Based Analysis ===")

        df = self.df_clean.copy()

        position_stats = df.groupby('position').agg({
            'gameid': 'count',
            'kills': 'mean',
            'deaths': 'mean',
            'assists': 'mean',
            'kda': 'mean',
            'dpm': 'mean',
            'cspm': 'mean',
            'vspm': 'mean',
            'damagetochampions': 'mean',
            'totalgold': 'mean'
        }).reset_index()

        position_stats.columns = [
            'position', 'games', 'avg_kills', 'avg_deaths', 'avg_assists',
            'avg_kda', 'avg_dpm', 'avg_cspm', 'avg_vspm',
            'avg_damage', 'avg_gold'
        ]

        print("\nAverage Stats by Position:")
        print(position_stats)

        # Save to CSV
        output_path = self.processed_dir / "position_metrics.csv"
        position_stats.to_csv(output_path, index=False)
        print(f"\nPosition metrics saved to {output_path}")

        return position_stats

    def visualize_position_comparison(self) -> None:
        """
        Creates a multi-panel visualization comparing key metrics across positions.

        Generates a grid of box plots showing the distribution of kills, deaths,
        assists, and damage per minute for each position/role.

        Returns:
            None: Saves visualization to output directory.
        """
        df = self.df_clean.copy()

        # Select key metrics
        metrics = ['kills', 'deaths', 'assists', 'dpm']

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.ravel()

        for idx, metric in enumerate(metrics):
            if metric in df.columns:
                sns.boxplot(
                    data=df,
                    x='position',
                    y=metric,
                    ax=axes[idx],
                    palette='Set2'
                )
                axes[idx].set_title(f'{metric.upper()} by Position',
                                   fontsize=12, fontweight='bold')
                axes[idx].set_xlabel('Position', fontsize=10)
                axes[idx].set_ylabel(metric.upper(), fontsize=10)
                axes[idx].grid(axis='y', alpha=0.3)

        plt.suptitle('Performance Metrics Comparison Across Positions',
                     fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()

        save_path = self.output_dir / "position_comparison.png"
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        print(f"Position comparison visualization saved to {save_path}")
        plt.close()

    def analyze_game_duration_impact(self) -> None:
        """
        Analyzes how game duration affects various performance metrics.

        Examines the relationship between game length and statistics like
        kills, gold, and damage to understand pacing and scaling patterns.

        Returns:
            None: Saves correlation visualization to output directory.
        """
        print(f"\n=== Game Duration Impact Analysis ===")

        df = self.df_clean.copy()

        if 'gamelength' not in df.columns:
            print("Game length data not available")
            return

        # Convert game length to minutes
        df['game_minutes'] = df['gamelength'] / 60

        # Create bins for game duration
        df['duration_category'] = pd.cut(
            df['game_minutes'],
            bins=[0, 25, 30, 35, 100],
            labels=['Short (<25m)', 'Medium (25-30m)', 'Long (30-35m)', 'Very Long (35m+)']
        )

        duration_stats = df.groupby('duration_category').agg({
            'gameid': 'count',
            'kills': 'mean',
            'totalgold': 'mean',
            'damagetochampions': 'mean',
            'total cs': 'mean'
        }).reset_index()

        print("\nStats by Game Duration:")
        print(duration_stats)

        # Visualize
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        metrics = ['kills', 'totalgold', 'damagetochampions', 'total cs']
        titles = ['Average Kills', 'Average Total Gold', 'Average Damage', 'Average CS']

        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[idx // 2, idx % 2]
            if metric in duration_stats.columns:
                duration_stats.plot(
                    x='duration_category',
                    y=metric,
                    kind='bar',
                    ax=ax,
                    color='steelblue',
                    legend=False
                )
                ax.set_title(title, fontsize=12, fontweight='bold')
                ax.set_xlabel('Game Duration', fontsize=10)
                ax.set_ylabel(title, fontsize=10)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(axis='y', alpha=0.3)

        plt.suptitle('Impact of Game Duration on Performance Metrics',
                     fontsize=14, fontweight='bold')
        plt.tight_layout()

        save_path = self.output_dir / "game_duration_impact.png"
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        print(f"Game duration analysis saved to {save_path}")
        plt.close()

    def analyze_team_performance(self, top_n: int = 15) -> pd.DataFrame:
        """
        Analyzes team-level performance metrics and standings.

        Aggregates statistics by team including win rates, average game
        statistics, and overall performance rankings.

        Args:
            top_n (int): Number of top teams to display.

        Returns:
            pd.DataFrame: Team performance statistics.
        """
        print(f"\n=== Team Performance Analysis ===")

        df = self.df_clean.copy()

        team_stats = df.groupby('teamname').agg({
            'gameid': 'count',
            'result': 'mean',
            'kills': 'mean',
            'deaths': 'mean',
            'assists': 'mean',
            'totalgold': 'mean',
            'damagetochampions': 'mean'
        }).reset_index()

        team_stats.columns = [
            'team', 'games_played', 'win_rate', 'avg_kills',
            'avg_deaths', 'avg_assists', 'avg_gold', 'avg_damage'
        ]

        # Filter teams with minimum games
        team_stats = team_stats[team_stats['games_played'] >= MIN_GAMES_THRESHOLD]

        # Convert win rate to percentage
        team_stats['win_rate'] = team_stats['win_rate'] * 100

        # Sort by win rate
        team_stats = team_stats.sort_values('win_rate', ascending=False)

        print(f"\nTop {top_n} Teams by Win Rate:")
        print(team_stats.head(top_n)[['team', 'games_played', 'win_rate']])

        # Save to CSV
        output_path = self.processed_dir / "team_performance.csv"
        team_stats.to_csv(output_path, index=False)
        print(f"\nTeam performance data saved to {output_path}")

        return team_stats

    def create_correlation_heatmap(self) -> None:
        """
        Creates a correlation heatmap for numeric performance metrics.

        Visualizes the correlation matrix between different statistical
        categories to identify relationships and patterns in the data.

        Returns:
            None: Saves heatmap visualization to output directory.
        """
        print(f"\n=== Correlation Analysis ===")

        df = self.df_clean.copy()

        # Select key numeric columns
        numeric_cols = [
            'kills', 'deaths', 'assists', 'kda', 'dpm', 'cspm',
            'vspm', 'totalgold', 'damagetochampions', 'gamelength'
        ]

        # Filter only available columns
        available_cols = [col for col in numeric_cols if col in df.columns]

        if len(available_cols) < 2:
            print("Not enough numeric columns for correlation analysis")
            return

        # Calculate correlation matrix
        corr_matrix = df[available_cols].corr()

        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )

        ax.set_title('Correlation Heatmap of Performance Metrics',
                     fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        save_path = self.output_dir / "correlation_heatmap.png"
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        print(f"Correlation heatmap saved to {save_path}")
        plt.close()

    def run_complete_eda(self) -> None:
        """
        Executes the complete exploratory data analysis pipeline.

        Runs all analysis methods in sequence including data cleaning,
        summary statistics, visualizations, and saves all outputs.

        Returns:
            None: Executes full EDA and saves all results.
        """
        print("\n" + "="*60)
        print("STARTING COMPREHENSIVE EDA FOR LOL ESPORTS 2025 DATA")
        print("="*60)

        # Clean data
        self.clean_data()

        # Summary statistics
        self.generate_summary_statistics()

        # Missing data analysis
        self.analyze_missing_data()

        # Player analysis
        self.analyze_player_performance()
        self.visualize_top_players_kda()

        # Champion analysis
        self.analyze_champion_meta()
        self.visualize_champion_pickrate()

        # Position analysis
        self.analyze_position_metrics()
        self.visualize_position_comparison()

        # Game duration analysis
        self.analyze_game_duration_impact()

        # Team analysis
        self.analyze_team_performance()

        # Correlation analysis
        self.create_correlation_heatmap()

        print("\n" + "="*60)
        print("EDA COMPLETE!")
        print(f"All visualizations saved to: {self.output_dir}")
        print(f"All processed data saved to: {self.processed_dir}")
        print("="*60)


def main():
    """
    Main execution function for the EDA pipeline.

    Loads the 2025 LoL esports data and runs comprehensive analysis,
    generating all visualizations and statistical summaries.

    Returns:
        None: Executes the complete analysis pipeline.
    """
    # Load data
    loader = DataLoader()
    print("Loading 2025 LoL Esports data...")

    try:
        df = loader.load_year_data(2025, download_if_missing=True)
    except Exception as e:
        print(f"\nError loading data: {e}")
        print("\nPlease manually download the 2025 CSV file from:")
        print("https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH")
        print(f"And save it to: {loader.data_dir}/lol_esports_2025.csv")
        return

    # Run EDA
    eda = EsportsEDA(df)
    eda.run_complete_eda()


if __name__ == "__main__":
    main()
