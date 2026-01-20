from typing import Any, Dict, List
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


def _build_user_info(user) -> Dict[str, Any]:
    profile = getattr(user, "profile", None)
    avatar = profile.avatar or None if profile else None
    nickname = (profile.position if profile else None) or user.first_name or user.username
    roles: List[str] = list(user.groups.values_list("name", flat=True))
    permissions: List[str] = list(user.user_permissions.values_list("codename", flat=True))

    return {
        "id": user.id,
        "username": user.username,
        "nickname": nickname,
        "avatar": avatar,
        "roles": roles,
        "permissions": permissions,
    }


def _success(data=None, message="success"):
    return Response({"code": 200, "message": message, "data": data})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access = refresh.access_token

        return {
            "code": 200,
            "message": "success",
            "data": {
                "token": str(access),
                "refresh": str(refresh),
                "userInfo": _build_user_info(self.user),
            },
        }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    token_str = request.data.get("refresh")
    if not token_str:
        return Response({"code": 400, "message": "refresh token required", "data": None}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(token_str)
        access_token = refresh.access_token
        return _success({"token": str(access_token)})
    except Exception:
        return Response({"code": 401, "message": "invalid refresh token", "data": None}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def user_info(request):
    return _success(_build_user_info(request.user))


@api_view(["POST"])
def logout_view(request):
    # Stateless JWT logout, kept for API symmetry
    return _success(None, "logout success")