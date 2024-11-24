from rest_framework import serializers
from .models import (
    Competition, Team, Player, Match, MatchStatistics,
    SeasonTeamPerformances, PlayerStatistics, SeasonPlayerStats,
    TeamFormGuide, HeadToHead
)

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    current_team = TeamSerializer()  # Nested serializer for team details

    class Meta:
        model = Player
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer()  # Nested serializer for competition
    home_team = TeamSerializer()
    away_team = TeamSerializer()

    class Meta:
        model = Match
        fields = '__all__'


class MatchStatisticsSerializer(serializers.ModelSerializer):
    match = MatchSerializer()  # Nested serializer for match
    team = TeamSerializer()

    class Meta:
        model = MatchStatistics
        fields = '__all__'


class SeasonTeamPerformancesSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    competition = CompetitionSerializer()

    class Meta:
        model = SeasonTeamPerformances
        fields = '__all__'


class PlayerStatisticsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    match = MatchSerializer()
    team = TeamSerializer()

    class Meta:
        model = PlayerStatistics
        fields = '__all__'


class SeasonPlayerStatsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    team = TeamSerializer()
    competition = CompetitionSerializer()

    class Meta:
        model = SeasonPlayerStats
        fields = '__all__'


class TeamFormGuideSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    competition = CompetitionSerializer()

    class Meta:
        model = TeamFormGuide
        fields = '__all__'


class HeadToHeadSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer()
    team2 = TeamSerializer()
    competition = CompetitionSerializer()

    class Meta:
        model = HeadToHead
        fields = '__all__'
