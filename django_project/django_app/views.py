from rest_framework import viewsets, permissions
from .models import (
    Competition, Team, Player, Match, MatchStatistics,
    SeasonTeamPerformances, PlayerStatistics, SeasonPlayerStats,
    TeamFormGuide, HeadToHead
)
from .serializers import (
    CompetitionSerializer, TeamSerializer, PlayerSerializer,
    MatchSerializer, MatchStatisticsSerializer, SeasonTeamPerformancesSerializer,
    PlayerStatisticsSerializer, SeasonPlayerStatsSerializer, TeamFormGuideSerializer,
    HeadToHeadSerializer
)

# Generic viewsets for CRUD operations
class CompetitionViewSet(viewsets.ModelViewSet):
    """Viewset for Competition"""
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class TeamViewSet(viewsets.ModelViewSet):
    """Viewset for Team"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

class PlayerViewSet(viewsets.ModelViewSet):
    """Viewset for Player"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.AllowAny]

class MatchViewSet(viewsets.ModelViewSet):
    """Viewset for Match"""
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny]

class MatchStatisticsViewSet(viewsets.ModelViewSet):
    """Viewset for Match Statistics"""
    queryset = MatchStatistics.objects.all()
    serializer_class = MatchStatisticsSerializer
    permission_classes = [permissions.AllowAny]

class SeasonTeamPerformancesViewSet(viewsets.ModelViewSet):
    """Viewset for Season Team Performances"""
    queryset = SeasonTeamPerformances.objects.all()
    serializer_class = SeasonTeamPerformancesSerializer
    permission_classes = [permissions.AllowAny]

class PlayerStatisticsViewSet(viewsets.ModelViewSet):
    """Viewset for Player Statistics"""
    queryset = PlayerStatistics.objects.all()
    serializer_class = PlayerStatisticsSerializer
    permission_classes = [permissions.AllowAny]

class SeasonPlayerStatsViewSet(viewsets.ModelViewSet):
    """Viewset for Season Player Stats"""
    queryset = SeasonPlayerStats.objects.all()
    serializer_class = SeasonPlayerStatsSerializer
    permission_classes = [permissions.AllowAny]

class TeamFormGuideViewSet(viewsets.ModelViewSet):
    """Viewset for Team Form Guide"""
    queryset = TeamFormGuide.objects.all()
    serializer_class = TeamFormGuideSerializer
    permission_classes = [permissions.AllowAny]

class HeadToHeadViewSet(viewsets.ModelViewSet):
    """Viewset for Head to Head"""
    queryset = HeadToHead.objects.all()
    serializer_class = HeadToHeadSerializer
    permission_classes = [permissions.AllowAny]
