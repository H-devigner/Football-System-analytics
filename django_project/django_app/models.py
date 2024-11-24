# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Competition(models.Model):
    """Competition/League information"""
    competition_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    season = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ('competition_id', 'season')

class Team(models.Model):
    """Team information"""
    team_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    founded = models.IntegerField(null=True)
    venue = models.CharField(max_length=100)
    website = models.URLField(max_length=200, null=True)

class Player(models.Model):
    """Player information"""
    player_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    birth_date = models.DateField()
    current_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

class Match(models.Model):
    """Match information for both live and historical matches"""
    MATCH_STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('LIVE', 'Live'),
        ('FINISHED', 'Finished'),
        ('POSTPONED', 'Postponed'),
        ('CANCELLED', 'Cancelled')
    ]

    match_id = models.CharField(max_length=50, unique=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES)
    matchday = models.IntegerField()
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['season', 'competition']),
            models.Index(fields=['match_date']),
            models.Index(fields=['status'])
        ]

class MatchStatistics(models.Model):
    """Detailed statistics for each match"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='statistics')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    possession = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    corners = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    passes = models.IntegerField(default=0)
    pass_accuracy = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    expected_goals = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('match', 'team')

class SeasonTeamPerformances(models.Model):
    """Aggregated team performance for each season"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    position = models.IntegerField(null=True)
    avg_possession = models.FloatField(default=0.0)
    avg_shots_per_game = models.FloatField(default=0.0)
    avg_shots_on_target = models.FloatField(default=0.0)
    avg_pass_accuracy = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('team', 'competition', 'season')
        indexes = [
            models.Index(fields=['season', 'competition']),
            models.Index(fields=['team', 'season'])
        ]

class PlayerStatistics(models.Model):
    """Player statistics for each match"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    minutes_played = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    passes = models.IntegerField(default=0)
    pass_accuracy = models.FloatField(default=0.0)
    tackles = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('player', 'match')

class SeasonPlayerStats(models.Model):
    """Aggregated player statistics for each season"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    appearances = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('player', 'team', 'competition', 'season')

class TeamFormGuide(models.Model):
    """Rolling form statistics for teams"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    date = models.DateField()
    last_5_results = models.CharField(max_length=9)  # e.g., "W,D,L,W,D"
    form_points = models.IntegerField()
    goals_scored_last_5 = models.IntegerField()
    goals_conceded_last_5 = models.IntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['team', 'date']),
            models.Index(fields=['competition', 'date'])
        ]

    def get_last_5_results(self):
        """Returns last 5 results as a list."""
        return self.last_5_results.split(',')

    def set_last_5_results(self, results):
        """Sets last 5 results from a list."""
        self.last_5_results = ','.join(results)


    """Rolling form statistics for teams"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    date = models.DateField()
    last_5_results = models.CharField(
        max_length=1,  # W, D, or L
    )
    form_points = models.IntegerField()
    goals_scored_last_5 = models.IntegerField()
    goals_conceded_last_5 = models.IntegerField()
    
    class Meta:
        indexes = [
            models.Index(fields=['team', 'date']),
            models.Index(fields=['competition', 'date'])
        ]

class HeadToHead(models.Model):
    """Historical head-to-head records between teams"""
    team1 = models.ForeignKey(Team, related_name='team1_records', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_records', on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    total_matches = models.IntegerField(default=0)
    team1_wins = models.IntegerField(default=0)
    team2_wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    team1_goals = models.IntegerField(default=0)
    team2_goals = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('team1', 'team2', 'competition')