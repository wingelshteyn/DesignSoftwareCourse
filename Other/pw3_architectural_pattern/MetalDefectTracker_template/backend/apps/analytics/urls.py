"""analytics URL patterns"""

from django.urls import path
from .views import (
    InspectionDetailView,
    InspectionHistoryView,
    MyStatisticsView,
    OverallStatisticsView,
    UserStatisticsView,
)

urlpatterns = [
    path("analytics/history/", InspectionHistoryView.as_view(), name="analytics-history"),
    path("analytics/history/<int:inspection_pk>/", InspectionDetailView.as_view(), name="analytics-history-detail"),
    path("analytics/stats/me/", MyStatisticsView.as_view(), name="analytics-stats-me"),
    path("analytics/stats/", OverallStatisticsView.as_view(), name="analytics-stats-overall"),
    path("analytics/stats/users/<int:user_pk>/", UserStatisticsView.as_view(), name="analytics-stats-user"),
]
