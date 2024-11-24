import pandas as pd
from kafka import KafkaProducer
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import time



# Configuration
# API_KEY = os.getenv('API_KEY')
API_KEY = ""

KAFKA_BROKER = 'kafka:29092'  # Match the Kafka bootstrap server from the consumer script
# KAFKA_TOPIC = os.getenv('INPUT_TOPIC_NAME')
KAFKA_TOPIC = "input-topic"


class HistoricalFootballCollector:
    def __init__(self, bootstrap_servers=[KAFKA_BROKER]):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def fetch_season_data(self, season: str, competition_id: str, api_key: str) -> List[Dict]:
        """Fetch all matches for a specific season"""
        api_url = f"https://api.football-data.org/v4/competitions/{competition_id}/matches"
        headers = {'X-Auth-Token': api_key}
        params = {'season': season}

        try:
            response = requests.get(api_url, headers=headers, params=params)
            return response.json().get('matches', [])
        except Exception as e:
            print(f"Error fetching season data: {e}")
            return []

    def fetch_team_statistics(self, team_id: str, season: str, api_key: str) -> Dict:
        """Fetch detailed statistics for a team in a specific season"""
        api_url = f"https://api.football-data.org/v4/teams/{team_id}/matches"
        headers = {'X-Auth-Token': api_key}
        params = {'season': season}

        try:
            response = requests.get(api_url, headers=headers, params=params)
            return response.json()
        except Exception as e:
            print(f"Error fetching team statistics: {e}")
            return {}

    def collect_season_data(self, season: str, competition_id: str, api_key: str):
        """Collect and process all data for a season"""
        # Fetch all matches
        matches = self.fetch_season_data(season, competition_id, api_key)

        # Process and send to Kafka
        for match in matches:
            # Match details
            self.producer.send("historical_matches", {
                'match_id': match['id'],
                'season': season,
                'competition_id': competition_id,
                'home_team': match['homeTeam'],
                'away_team': match['awayTeam'],
                'score': match['score'],
                'date': match['utcDate'],
                'status': match['status']
            })

            # Match statistics
            if 'statistics' in match:
                self.producer.send('historical_statistics', {
                    'match_id': match['id'],
                    'season': season,
                    'statistics': match['statistics']
                })

    def collect_team_season_data(self, team_id: str, season: str, api_key: str):
        """Collect all data for a specific team in a season"""
        team_stats = self.fetch_team_statistics(team_id, season, api_key)

        if team_stats:
            self.producer.send('team_season_stats', {
                'team_id': team_id,
                'season': season,
                'matches_played': len(team_stats.get('matches', [])),
                'statistics': team_stats.get('statistics', {}),
                'form': team_stats.get('form', [])
            })

    def process_historical_data(self, seasons: List[str], competition_id: str, api_key: str):
        """Process multiple seasons of data"""
        for season in seasons:
            print(f"Processing season {season}...")
            self.collect_season_data(season, competition_id, api_key)

            # Allow time between requests to respect API rate limits
            time.sleep(6)  # Adjust based on API rate limits

if __name__ == "__main__":
    collector = HistoricalFootballCollector()
    seasons = ['2023', '2022', '2021', '2020']
    collector.process_historical_data(
        seasons=seasons,
        competition_id="PL",  # Premier League
        api_key=API_KEY
    )