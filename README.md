# League of Legends Esports Data Analysis - 2025 Season

A comprehensive data science project for analyzing professional League of Legends esports match data from the 2025 season. This project includes data loading, exploratory data analysis (EDA), statistical analysis, and visualizations to uncover insights about player performance, champion meta, team strategies, and competitive trends.

## 📊 Project Overview

This project provides tools and analyses for understanding professional League of Legends competitive play through data. Using match data from Oracle's Elixir, we examine:

- **Player Performance**: Individual statistics, KDA ratios, and performance metrics
- **Champion Meta**: Pick/ban rates, win rates, and meta trends
- **Team Analysis**: Team performance, win rates, and strategic patterns
- **Position Comparison**: Role-specific statistics and trends
- **Temporal Analysis**: Game duration impact and seasonal trends
- **Statistical Correlations**: Relationships between performance metrics

## 🗂️ Project Structure

```
lol-Esports-Project/
│
├── config/                     # Configuration files
│   ├── __init__.py
│   └── config.py              # Project settings and constants
│
├── data/                      # Data directory (gitignored)
│   ├── raw/                   # Raw CSV files from Oracle's Elixir
│   └── processed/             # Cleaned and processed data
│
├── notebooks/                 # Jupyter notebooks
│   └── 01_exploratory_data_analysis.ipynb
│
├── src/                       # Source code
│   ├── __init__.py
│   ├── data_loader.py        # Data downloading and loading utilities
│   └── eda_analysis.py       # Exploratory data analysis scripts
│
├── output/                    # Analysis outputs (gitignored)
│   ├── figures/              # Visualization outputs
│   └── reports/              # Generated reports
│
├── .gitignore                # Git ignore file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Jupyter Lab/Notebook for interactive analysis

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mattspooner1/lol-Esports-Project.git
cd lol-Esports-Project
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Data Acquisition

The project uses data from **Oracle's Elixir**, which is hosted on Google Drive.

**Option 1: Automatic Download** (uses the data_loader script)
```python
from src.data_loader import DataLoader

loader = DataLoader()
df = loader.load_year_data(2025, download_if_missing=True)
```

**Option 2: Manual Download**
1. Visit the Oracle's Elixir Google Drive: https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH
2. Download the 2025 CSV file
3. Save it to `data/raw/lol_esports_2025.csv`

## 📈 Usage

### Running the Complete EDA Pipeline

Execute the full exploratory data analysis:

```bash
python src/eda_analysis.py
```

This will:
- Load and clean the data
- Generate summary statistics
- Create all visualizations
- Save processed data and figures to output directories

### Using Jupyter Notebooks

For interactive analysis:

```bash
jupyter lab
# Navigate to notebooks/01_exploratory_data_analysis.ipynb
```

### Programmatic Usage

```python
from src.data_loader import DataLoader
from src.eda_analysis import EsportsEDA

# Load data
loader = DataLoader()
df = loader.load_year_data(2025)

# Run EDA
eda = EsportsEDA(df)
eda.run_complete_eda()

# Or run specific analyses
df_clean = eda.clean_data()
player_stats = eda.analyze_player_performance()
champion_stats = eda.analyze_champion_meta()
```

## 📊 Available Analyses

### 1. Player Performance Analysis
- Individual player statistics (KDA, DPM, CSPM, Vision Score)
- Top player rankings
- Performance trends
- Win rates and game counts

**Output**: `data/processed/player_performance.csv`, `output/figures/top_players_kda.png`

### 2. Champion Meta Analysis
- Pick rates and ban rates
- Champion win rates
- Meta trends and popularity
- Champion-specific statistics

**Output**: `data/processed/champion_meta.csv`, `output/figures/champion_pickrate.png`

### 3. Position-Based Analysis
- Role-specific statistics (Top, Jungle, Mid, ADC, Support)
- Average metrics by position
- Position comparison visualizations

**Output**: `data/processed/position_metrics.csv`, `output/figures/position_comparison.png`

### 4. Team Performance Analysis
- Team win rates and rankings
- Aggregate team statistics
- Performance comparisons

**Output**: `data/processed/team_performance.csv`

### 5. Game Duration Impact
- How game length affects performance
- Duration-based metric analysis
- Early vs. late game patterns

**Output**: `output/figures/game_duration_impact.png`

### 6. Statistical Correlations
- Correlation matrix of performance metrics
- Relationship analysis between variables

**Output**: `output/figures/correlation_heatmap.png`

## 🔧 Configuration

Edit `config/config.py` to customize:

- Data source URLs
- Directory paths
- Visualization settings (figure size, DPI, style)
- Analysis parameters (minimum games threshold, etc.)

## 📝 Code Documentation

All code follows a consistent documentation format:

```python
"""
Brief description of what the function/class does.

Returns:
    type: Description of what is returned.
"""
```

Each function includes:
- Comprehensive docstring explaining purpose
- Parameter descriptions with types
- Return value documentation
- Inline comments for complex logic

## 🎯 Key Features

- **Automated Data Pipeline**: Download and load data with a single function call
- **Comprehensive EDA**: Pre-built analyses covering all major aspects of competitive play
- **High-Quality Visualizations**: Publication-ready charts and graphs
- **Flexible Architecture**: Modular code for easy customization and extension
- **Well-Documented**: Clear documentation following best practices
- **Jupyter Integration**: Interactive notebooks for exploratory work

## 📊 Sample Insights

Some questions this project can answer:

- Who are the highest performing players in the 2025 season?
- Which champions dominate the professional meta?
- How do performance metrics vary across different positions?
- What is the correlation between damage dealt and game outcome?
- How does game duration affect player statistics?
- Which teams have the highest win rates?

## 🛠️ Technologies Used

- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical visualizations
- **Jupyter**: Interactive analysis environment
- **gdown**: Google Drive file downloads

## 📚 Data Source

Data provided by **Oracle's Elixir** (https://oracleselixir.com/)
- Professional League of Legends match data
- Updated regularly with new games
- Comprehensive statistics for players, teams, and champions

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Additional analysis modules (e.g., patch-specific analysis)
- Machine learning models for win prediction
- Advanced visualizations and dashboards
- Data enrichment from Leaguepedia API
- Real-time data pipeline integration

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Oracle's Elixir** for providing comprehensive esports data
- **Riot Games** for League of Legends
- Reference pipeline inspiration from [Esports_Data_Pipeline](https://github.com/HerrKurz/Esports_Data_Pipeline)

## 📬 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

**Built with ❤️ for the League of Legends esports community**