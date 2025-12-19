"""
Sample data generator for LoL Esports analysis.

This module creates realistic sample data for testing and demonstration
when the actual Oracle's Elixir data is not available.

Returns:
    pd.DataFrame: Sample esports match data with realistic values.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


class SampleDataGenerator:
    """
    Generates realistic sample LoL esports data for testing.

    Creates synthetic match data with realistic statistics for players,
    teams, champions, and game outcomes.

    Returns:
        SampleDataGenerator: Instance for generating sample data.
    """

    def __init__(self, seed: int = 42):
        """
        Initialize the sample data generator.

        Args:
            seed (int): Random seed for reproducibility.

        Returns:
            None: Initializes the generator.
        """
        np.random.seed(seed)
        random.seed(seed)

        # Sample data
        self.positions = ['top', 'jng', 'mid', 'bot', 'sup']
        self.teams = [
            'T1', 'Gen.G', 'JDG', 'BLG', 'G2', 'FNC', 'C9', 'TL',
            'DK', 'KT', 'HLE', 'DRX', 'WBG', 'LNG', 'MAD', 'FLY'
        ]
        self.leagues = ['LCK', 'LPL', 'LEC', 'LCS']

        self.champions = [
            'Aatrox', 'Ahri', 'Akali', 'Alistar', 'Ashe', 'Azir',
            'Braum', 'Caitlyn', 'Camille', 'Corki', 'Darius', 'Draven',
            'Ekko', 'Elise', 'Ezreal', 'Fiora', 'Gnar', 'Gragas',
            'Graves', 'Gwen', 'Irelia', 'Janna', 'Jarvan IV', 'Jax',
            'Jayce', 'Jhin', 'Jinx', 'Kai\'Sa', 'Kalista', 'Karma',
            'Karthus', 'Kassadin', 'Kennen', 'Khazix', 'Kindred', 'Kog\'Maw',
            'LeBlanc', 'Lee Sin', 'Leona', 'Lissandra', 'Lucian', 'Lulu',
            'Lux', 'Maokai', 'Nautilus', 'Nidalee', 'Nocturne', 'Olaf',
            'Orianna', 'Ornn', 'Poppy', 'Rakan', 'Rell', 'Renekton',
            'Riven', 'Rumble', 'Ryze', 'Sejuani', 'Senna', 'Sett',
            'Shen', 'Sivir', 'Skarner', 'Syndra', 'Tahm Kench', 'Thresh',
            'Tristana', 'Twisted Fate', 'Varus', 'Viego', 'Viktor', 'Vex',
            'Vladimir', 'Volibear', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo',
            'Yone', 'Yuumi', 'Zed', 'Zeri', 'Ziggs', 'Zoe'
        ]

        self.player_names = self._generate_player_names()

    def _generate_player_names(self) -> dict:
        """
        Generates player names for each team.

        Returns:
            dict: Mapping of team names to player rosters.
        """
        first_parts = ['Faker', 'Chovy', 'Ruler', 'Zeus', 'Keria', 'Canyon', 'ShowMaker',
                       'Deft', 'Meiko', 'Knight', 'JackeyLove', 'TheShy', 'Rookie',
                       'Caps', 'Jankos', 'Perkz', 'Rekkles', 'Hylissang', 'Upset',
                       'Impact', 'CoreJJ', 'Blaber', 'Jensen', 'Doublelift']

        additional = ['Alpha', 'Beta', 'Omega', 'Sigma', 'Delta', 'Prime',
                      'Ace', 'King', 'Wolf', 'Tiger', 'Dragon', 'Phoenix']

        all_players = first_parts + [f"{a}{i}" for a in additional for i in range(1, 4)]

        player_dict = {}
        idx = 0
        for team in self.teams:
            team_players = []
            for _ in range(5):
                if idx < len(all_players):
                    team_players.append(all_players[idx])
                else:
                    team_players.append(f"Player{idx}")
                idx += 1
            player_dict[team] = team_players

        return player_dict

    def generate_match_data(self, num_games: int = 500) -> pd.DataFrame:
        """
        Generates complete match data with realistic statistics.

        Creates synthetic game data including player performance metrics,
        champion picks, team compositions, and match outcomes.

        Args:
            num_games (int): Number of games to generate.

        Returns:
            pd.DataFrame: Complete match dataset with all columns.
        """
        data = []
        game_id = 1

        start_date = datetime(2025, 1, 1)

        for _ in range(num_games):
            # Random teams and league
            team1, team2 = random.sample(self.teams, 2)
            league = random.choice(self.leagues)

            # Game metadata
            game_date = start_date + timedelta(days=random.randint(0, 180))
            patch = f"14.{random.randint(1, 12)}"
            game_length = random.randint(1500, 2400)  # 25-40 minutes

            # Determine winner (60/40 split for some realism)
            winner = random.choices([team1, team2], weights=[0.6, 0.4])[0]

            # Generate bans
            bans = random.sample(self.champions, 10)

            # Generate for each player (5 per team)
            for team_idx, team in enumerate([team1, team2]):
                is_winner = (team == winner)
                side = 'Blue' if team_idx == 0 else 'Red'

                for pos_idx, position in enumerate(self.positions):
                    player_name = self.player_names[team][pos_idx]

                    # Pick champion (not in bans)
                    available_champs = [c for c in self.champions if c not in bans]
                    champion = random.choice(available_champs)
                    bans.append(champion)  # Prevent duplicate picks

                    # Generate realistic stats based on position and outcome
                    stats = self._generate_player_stats(position, is_winner, game_length)

                    row = {
                        'gameid': f"GAME_{game_id:04d}",
                        'datacompleteness': 'complete',
                        'url': f'http://example.com/game/{game_id}',
                        'league': league,
                        'year': 2025,
                        'split': 'Spring',
                        'playoffs': random.choice([0, 1]) if random.random() > 0.7 else 0,
                        'date': game_date.strftime('%Y-%m-%d'),
                        'game': 1,
                        'patch': patch,
                        'playerid': f"{player_name}_{team}",
                        'side': side,
                        'position': position,
                        'playername': player_name,
                        'teamname': team,
                        'champion': champion,
                        'ban1': bans[0] if team_idx == 0 else bans[5],
                        'ban2': bans[1] if team_idx == 0 else bans[6],
                        'ban3': bans[2] if team_idx == 0 else bans[7],
                        'ban4': bans[3] if team_idx == 0 else bans[8],
                        'ban5': bans[4] if team_idx == 0 else bans[9],
                        'gamelength': game_length,
                        'result': 1 if is_winner else 0,
                    }

                    row.update(stats)
                    data.append(row)

            game_id += 1

        df = pd.DataFrame(data)
        return df

    def _generate_player_stats(self, position: str, is_winner: bool, game_length: int) -> dict:
        """
        Generates realistic player statistics based on position and outcome.

        Creates performance metrics that vary by role and match result,
        including kills, deaths, assists, gold, damage, and vision stats.

        Args:
            position (str): Player's role (top/jng/mid/bot/sup).
            is_winner (bool): Whether the player's team won.
            game_length (int): Duration of the game in seconds.

        Returns:
            dict: Dictionary of performance statistics.
        """
        game_minutes = game_length / 60

        # Base stats by position
        base_stats = {
            'top': {'k': 3, 'd': 3, 'a': 4, 'cs': 7.5, 'dmg': 550, 'gold': 380},
            'jng': {'k': 4, 'd': 3, 'a': 7, 'cs': 5.5, 'dmg': 480, 'gold': 350},
            'mid': {'k': 4, 'd': 3, 'a': 5, 'cs': 8.0, 'dmg': 600, 'gold': 400},
            'bot': {'k': 5, 'd': 2, 'a': 4, 'cs': 8.5, 'dmg': 650, 'gold': 420},
            'sup': {'k': 1, 'd': 4, 'a': 10, 'cs': 1.5, 'dmg': 220, 'gold': 240}
        }

        stats = base_stats.get(position, base_stats['mid'])

        # Adjust for winner/loser
        win_mult = 1.2 if is_winner else 0.85

        kills = max(0, int(np.random.poisson(stats['k'] * win_mult)))
        deaths = max(1, int(np.random.poisson(stats['d'] / win_mult)))
        assists = max(0, int(np.random.poisson(stats['a'] * win_mult)))

        total_cs = int(stats['cs'] * game_minutes * np.random.uniform(0.85, 1.15))
        cspm = total_cs / game_minutes

        damage = int(stats['dmg'] * game_minutes * np.random.uniform(0.8, 1.2) * win_mult)
        dpm = damage / game_minutes

        total_gold = int(stats['gold'] * game_minutes * np.random.uniform(0.85, 1.15) * win_mult)
        earned_gold = total_gold - 500
        earned_gpm = earned_gold / game_minutes

        vision_score = int(np.random.uniform(1.0, 3.5 if position == 'sup' else 1.8) * game_minutes)
        vspm = vision_score / game_minutes

        # Calculate KDA
        kda = (kills + assists) / max(deaths, 1)

        # Team kills (approximate)
        team_kills = int(np.random.uniform(10, 25) * win_mult)

        return {
            'kills': kills,
            'deaths': deaths,
            'assists': assists,
            'teamkills': team_kills,
            'teamdeaths': int(team_kills / win_mult),
            'doublekills': random.randint(0, 2) if position in ['mid', 'bot'] else 0,
            'triplekills': random.randint(0, 1) if random.random() > 0.8 else 0,
            'quadrakills': 1 if random.random() > 0.95 else 0,
            'pentakills': 1 if random.random() > 0.99 else 0,
            'firstblood': random.choice([0, 1]),
            'firstbloodkill': random.choice([0, 1]),
            'firstbloodassist': random.choice([0, 1]),
            'firstbloodvictim': random.choice([0, 1]),
            'damagetochampions': damage,
            'dpm': dpm,
            'damageshare': np.random.uniform(0.15, 0.35) if position != 'sup' else np.random.uniform(0.05, 0.15),
            'damagetakenperminute': np.random.uniform(300, 800),
            'damagemitigatedperminute': np.random.uniform(200, 600),
            'wardsplaced': int(np.random.uniform(0.5, 2.5 if position == 'sup' else 1.0) * game_minutes),
            'wpm': np.random.uniform(0.4, 2.0),
            'wardskilled': int(np.random.uniform(0.3, 1.2) * game_minutes),
            'wcpm': np.random.uniform(0.2, 1.0),
            'controlwardsbought': int(np.random.uniform(0.1, 0.4) * game_minutes),
            'visionscore': vision_score,
            'vspm': vspm,
            'totalgold': total_gold,
            'earnedgold': earned_gold,
            'earned gpm': earned_gpm,
            'goldspent': int(total_gold * 0.95),
            'gspd': np.random.uniform(0.90, 0.98),
            'total cs': total_cs,
            'minionkills': int(total_cs * 0.7),
            'monsterkills': int(total_cs * 0.3),
            'monsterkillsownjungle': int(total_cs * 0.2) if position == 'jng' else int(total_cs * 0.05),
            'monsterkillsenemyjungle': int(total_cs * 0.1) if position == 'jng' else int(total_cs * 0.02),
            'cspm': cspm,
            'goldat10': int(np.random.uniform(2800, 3500) * win_mult),
            'xpat10': int(np.random.uniform(3200, 4000) * win_mult),
            'csat10': int(np.random.uniform(60, 90) if position != 'sup' else np.random.uniform(5, 15)),
            'opp_goldat10': int(np.random.uniform(2800, 3500) / win_mult),
            'opp_xpat10': int(np.random.uniform(3200, 4000) / win_mult),
            'opp_csat10': int(np.random.uniform(60, 90) if position != 'sup' else np.random.uniform(5, 15)),
            'golddiffat10': int(np.random.uniform(-400, 400) * (1 if is_winner else -1)),
            'xpdiffat10': int(np.random.uniform(-300, 300) * (1 if is_winner else -1)),
            'csdiffat10': int(np.random.uniform(-10, 10) * (1 if is_winner else -1)),
            'killsat10': random.randint(0, 2),
            'assistsat10': random.randint(0, 3),
            'deathsat10': random.randint(0, 2),
            'opp_killsat10': random.randint(0, 2),
            'opp_assistsat10': random.randint(0, 3),
            'opp_deathsat10': random.randint(0, 2),
        }


def generate_sample_data(output_path: str = "data/raw/lol_esports_2025.csv", num_games: int = 500):
    """
    Generates and saves sample LoL esports data to CSV.

    Creates a realistic synthetic dataset for testing and demonstration
    when the actual data is not accessible.

    Args:
        output_path (str): Path where the CSV file should be saved.
        num_games (int): Number of games to generate.

    Returns:
        str: Path to the saved CSV file.
    """
    print(f"Generating sample data with {num_games} games...")

    generator = SampleDataGenerator()
    df = generator.generate_match_data(num_games)

    # Ensure directory exists
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"Sample data saved to: {output_path}")
    print(f"Generated {len(df)} rows ({num_games} games × 10 players)")

    return output_path


if __name__ == "__main__":
    generate_sample_data()
