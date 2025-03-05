from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinLengthValidator, MaxLengthValidator
from tutorial.quickstart.serializers import UserSerializer

from .validators import PasswordValidator, FIOValidator

USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.

    Переопределено поле password с указанием аргумента write_only,
    предназначенного для записи данных в поле, без возврата значения поля.

    Переопределен метод create() для создания объекта модели User вызывая метод create_user.
    """

    password = serializers.CharField(
        write_only=True, validators=[PasswordValidator()], min_length=8
    )
    first_name = serializers.CharField(
        validators=[FIOValidator()], min_length=2, max_length=50
    )
    last_name = serializers.CharField(
        validators=[FIOValidator()], min_length=2, max_length=50
    )

    class Meta:
        model = USER_MODEL
        fields = ("id", "email", "password", "first_name", "last_name", "surname")

    def validate(self, data):
        surname = data.get("surname", "")
        if surname:
            FIOValidator().validate_fio(surname)

        return data

    def validate_email(self, value):
        email = value.lower()
        if USER_MODEL.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return email

    def create(self, validated_data):
        user = USER_MODEL.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            surname=validated_data["surname"],
        )
        return user


class LogoutSerializer(serializers.Serializer):
    """
    Сериализатор для logout.
    """

    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value):
        try:
            RefreshToken(value).verify()
        except TokenError as e:
            raise TokenError("Invalid refresh token")

        return value

    def save(self, **kwargs):
        RefreshToken(self.validated_data["refresh"]).blacklist()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для TokenObtainPairView с указанием длины полей.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields["password"] = serializers.CharField(
            write_only=True,
            required=True,
            validators=[PasswordValidator()],
            min_length=8,
        )
#
class UserSerializerInData(serializers.Serializer):
    """
    Сериализатор для получения данных пользователя в data.
    """

    data = UserSerializer()
    message = serializers.CharField(default="Данные пользователя")


class UserPatchSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения данных пользователя.
    """

    class Meta:
        model = USER_MODEL
        fields = (
            "id",
            "first_name",
            "last_name",
            "surname",
            "notification",
        )



