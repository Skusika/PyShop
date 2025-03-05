from typing import Any
import smtplib
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    NotAuthenticated,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAcceptable,
    UnsupportedMediaType,
    Throttled,
)
from django.http import Http404
from django.core.exceptions import FieldError, ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import TokenError

from auth_app.views import CustomTokenObtainPairView, CustomTokenRefreshView

USER_MODEL = get_user_model()


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """
    Функция вызова встроенного кастомного обработчика исключений DRF
    для предварительной обработки исключения.
    """
    print(exc)
    response = exception_handler(exc, context)
    view = context.get('view')

    if isinstance(exc, ValidationError):
        if isinstance(exc.detail, dict):
            message = [
                message
                for field_errors in exc.detail.values()
                for message in field_errors
            ]
        else:
            message = exc.detail
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, AuthenticationFailed):
        if isinstance(view, CustomTokenRefreshView):
            custom_response_data = {
                "message": "Токен просрочен или не действительный"
            }
            return Response(custom_response_data, status=status.HTTP_403_FORBIDDEN)
        elif isinstance(view, CustomTokenObtainPairView):
            custom_response_data = {
                "message": "Активная учетная запись с указанными учетными "
                "данными не найдена."
            }
            return Response(custom_response_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            custom_response_data = {
                "message": "Ошибка авторизации"
            }
            return Response(custom_response_data, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, PermissionDenied):
        return Response(
            {"message": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN
        )
    elif isinstance(exc, NotAuthenticated):
        return Response(
            {"message": "Необходима аутентификация"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    elif isinstance(exc, USER_MODEL.DoesNotExist):
        return Response(
            {"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"message": f"Объект не найден: {exc.args[0]}"}, status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, (ValueError, TypeError)):
        return Response(
            {"message": "Некорректное значение: " + str(exc)}, status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, Http404):
        return Response(
            {"message": "Страница не найдена"}, status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, smtplib.SMTPException):
        return Response(
            {"message": "Ошибка при отправке почты"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    elif isinstance(exc, TokenError):
        if isinstance(view, CustomTokenRefreshView):
            custom_response_data = {
                "message": "Токен просрочен или не действительный"
            }
            return Response(custom_response_data, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(
                {"message": "Неверный токен"}, status=status.HTTP_400_BAD_REQUEST
            )
    elif isinstance(exc, MethodNotAllowed):
        return Response(
            {"message": "Метод HTTP не разрешен для данного эндпоинта"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    elif isinstance(exc, NotAcceptable):
        return Response(
            {
                "message": "Сервер не может предоставить контент, который удовлетворяет "
                "заголовку Accept в запросе"
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    elif isinstance(exc, UnsupportedMediaType):
        return Response(
            {
                "message": "Сервер не может обработать запрос "
                "из-за неподдерживаемого типа медиа-контента"
            },
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )
    elif isinstance(exc, Throttled):
        return Response(
            {"message": "Превышены ограничения скорости"},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    elif isinstance(exc, IntegrityError):
        return Response(
            {"message": "Произошла ошибка базы данных"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exc, FieldError):
        return Response(
            {"message": "В запрос передан неверное имя поля"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exc, AttributeError):
        return Response(
            {"message": f"Ошибка: При попытке доступа к атрибуту {exc.args[0]}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if response is None:
        return Response(
            {"message": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response