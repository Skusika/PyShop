from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    RegistrationSerializer,
    LogoutSerializer,
    UserSerializer,
    UserPatchSerializer,
    UserSerializerInData,
    CustomTokenObtainPairSerializer
)
from . import schemas

USER_MODEL = get_user_model()


class RegistrationAPIView(GenericAPIView):
    """
    Представление для регистрации пользователя
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @extend_schema(
        summary="Регистрация пользователя.",
        responses={
            status.HTTP_201_CREATED: schemas.get_2xx(
                name="register_201",
                message="Пользователь успешно зарегистрирован. Ссылка для активации направлена на email.",
            ),
            status.HTTP_400_BAD_REQUEST: schemas.get_4xx_many(name="register_400"),
        },
        tags=["registration"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.validated_data["email"]
        return Response(
            {"message": f"Ссылка для активации аккаунта направлена на email {email}."},
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Представление, для получения пары токенов.
    """

    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Вход в систему.",
        responses={
            status.HTTP_200_OK: schemas.login_response_200,
            status.HTTP_400_BAD_REQUEST: schemas.get_4xx_many(name="login_400"),
            status.HTTP_401_UNAUTHORIZED: schemas.get_4xx_single(name="login_401"),
        },
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response_data = {
            "data": {
                "access": response.data["access"],
            },
            "message": "Токен доступа",
        }

        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=response.data['refresh'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.data = response_data

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Представление для обновления токена доступа.
    """

    @extend_schema(
        summary="Обновление токена доступа.",
        description="Создает новый токен доступа, используя действительный токен обновления.",
        responses={
            status.HTTP_200_OK: schemas.refresh_response_200,
            status.HTTP_400_BAD_REQUEST: schemas.get_4xx_many(name="refresh_400"),
            status.HTTP_403_FORBIDDEN: schemas.get_4xx_single(name="refresh_403"),
        },

        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data["data"] = {"access": response.data["access"]}
        response.data["message"] = "Токен доступа"
        del response.data["access"]
        return response


class LogoutAPIView(generics.GenericAPIView):
    """
    Представление, для выхода из системы.
    Refresh token принимает из куки.
    """

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Выход из системы.",
        description="Заносит refresh-токен в чёрный список. Refresh token принимает из куки.",
        request=None,
        responses={
            status.HTTP_200_OK: schemas.get_2xx(
                name="logout_200", message="Выход из системы успешен."
            ),
            status.HTTP_400_BAD_REQUEST: schemas.get_4xx_many(name="logout_400"),
            status.HTTP_401_UNAUTHORIZED: schemas.get_4xx_single(name="logout_401"),
            status.HTTP_403_FORBIDDEN: schemas.get_4xx_single(name="logout_403"),
        },
        tags=["auth"],
    )
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')

        if not refresh_token:
            raise AuthenticationFailed('Токен обновления не предоставлен.')

        serializer = self.serializer_class(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(
            {"message": "Выход из системы успешен."},
            status=status.HTTP_200_OK
        )

        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
        )

        return response


class GetUserView(generics.GenericAPIView):
    """
    Представление для получения данных авторизованного пользователя.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        summary="Данные пользователя.",
        description="Получение данных авторизованного пользователя.",
        responses={
            status.HTTP_200_OK: UserSerializerInData,
            status.HTTP_400_BAD_REQUEST: schemas.get_4xx_many(name="get_user_400"),
            status.HTTP_401_UNAUTHORIZED: schemas.get_4xx_single(name="get_user_401"),
            status.HTTP_403_FORBIDDEN: schemas.get_4xx_single(name="get_user_403"),
        },
        tags=["auth"],
    )
    def get(self, request):
        data = {
            "data": self.serializer_class(request.user).data,
            "message": "Данные пользователя",
        }
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Личный кабинет пользователя.",
        tags=["auth"],
    )
    @extend_schema(
        description="Редактирование профиля.",
        request=UserPatchSerializer,
        responses={
            status.HTTP_200_OK: schemas.get_2xx(
                name="user_patched",
                message="Данные пользователя обновлены."
            ),
            status.HTTP_400_BAD_REQUEST: schemas.get_4xx_many(name="patch_user_lk_400"),
            status.HTTP_401_UNAUTHORIZED: schemas.get_4xx_single(name="patch_user_lk_401"),
            status.HTTP_403_FORBIDDEN: schemas.get_4xx_single(name="patch_user_lk_403"),
        },
    )
    def put(self, request, *args, **kwargs):
        serializer = UserPatchSerializer(request.user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Данные пользователя обновлены."},
            status=status.HTTP_200_OK
        )

    def get_default_renderer(self, view):
        return JSONRenderer()