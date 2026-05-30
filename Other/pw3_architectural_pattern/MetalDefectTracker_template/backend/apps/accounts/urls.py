"""accounts URL patterns - included under /api/ in config.urls"""

from django.urls import path
from .views import (
    LoginView,
    MeView,
    TokenRefreshAPIView,
    UserDetailView,
    UserListCreateView,
    UserRoleUpdateView,
    ZoneListCreateView,
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshAPIView.as_view(), name="auth-refresh"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("zones/", ZoneListCreateView.as_view(), name="zone-list-create"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/role/", UserRoleUpdateView.as_view(), name="user-role-update"),
]
