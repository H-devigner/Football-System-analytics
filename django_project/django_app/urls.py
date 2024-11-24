from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionViewSet, TeamViewSet, PlayerViewSet, MatchViewSet,
    MatchStatisticsViewSet, SeasonTeamPerformancesViewSet, PlayerStatisticsViewSet,
    SeasonPlayerStatsViewSet, TeamFormGuideViewSet, HeadToHeadViewSet
)

# Initialize the router
router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'match-statistics', MatchStatisticsViewSet)
router.register(r'season-team-performances', SeasonTeamPerformancesViewSet)
router.register(r'player-statistics', PlayerStatisticsViewSet)
router.register(r'season-player-stats', SeasonPlayerStatsViewSet)
router.register(r'team-form-guide', TeamFormGuideViewSet)
router.register(r'head-to-head', HeadToHeadViewSet)

# Wire up the views with the router
urlpatterns = [
    path('', include(router.urls)),
]
