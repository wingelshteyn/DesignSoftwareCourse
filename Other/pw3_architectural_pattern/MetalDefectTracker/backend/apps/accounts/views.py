"""
accounts.views
--------------
FRQ-1.1  JWT authentication endpoints (login / refresh / logout)
FRQ-2    User management (administrator)
"""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User, Zone
from .permissions import IsAdministrator
from .serializers import (
    UserCreateSerializer,
    UserRoleUpdateSerializer,
    UserSerializer,
    ZoneSerializer,
)
from .services import UserService, ZoneService


# ---------------------------------------------------------------------------
# Authentication  (FRQ-1.1)
# ---------------------------------------------------------------------------


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/  - returns access + refresh JWT tokens."""

    permission_classes = [AllowAny]


class TokenRefreshAPIView(TokenRefreshView):
    """POST /api/auth/refresh/  - exchange refresh token for new access token."""

    permission_classes = [AllowAny]


class MeView(APIView):
    """GET /api/auth/me/  - return currently authenticated user profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# Zone management  (FRQ-2.5)
# ---------------------------------------------------------------------------


class ZoneListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/zones/"""

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAdministrator]


# ---------------------------------------------------------------------------
# User management (administrator)  (FRQ-2.1–FRQ-2.4)
# ---------------------------------------------------------------------------


class UserListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/users/  - list all users
    POST /api/users/  - create new user  (FRQ-2.1, FRQ-2.2)
    """

    permission_classes = [IsAdministrator]

    def get_queryset(self):
        return User.objects.select_related("zone").all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/users/<pk>/  - retrieve user
    DELETE /api/users/<pk>/  - delete user  (FRQ-2.4)
    """

    queryset = User.objects.select_related("zone").all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrator]


class UserRoleUpdateView(generics.UpdateAPIView):
    """PATCH /api/users/<pk>/role/  - update user role  (FRQ-2.3)"""

    queryset = User.objects.all()
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [IsAdministrator]
    http_method_names = ["patch"]
