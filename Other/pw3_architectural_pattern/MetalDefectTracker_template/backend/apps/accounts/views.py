"""
FRQ-1.1  JWT authentication endpoints (login / refresh / logout)
FRQ-2    User management (administrator)
"""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User, Zone


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/  - returns access + refresh JWT tokens."""

    permission_classes = [AllowAny]


class TokenRefreshAPIView(TokenRefreshView):
    """POST /api/auth/refresh/  - exchange refresh token for new access token."""

    permission_classes = [AllowAny]


class MeView(APIView):
    """GET /api/auth/me/  - return currently authenticated user profile."""

    permission_classes = [IsAuthenticated]



class ZoneListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/zones/"""



class UserListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/users/  - list all users
    POST /api/users/  - create new user
    """


class UserDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/users/<pk>/  - retrieve user
    DELETE /api/users/<pk>/  - delete user
    """


class UserRoleUpdateView(generics.UpdateAPIView):
    """PATCH /api/users/<pk>/role/  - update user role"""
