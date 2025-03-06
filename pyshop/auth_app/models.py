from django.db import models
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import UserManager
from .validators import CustomUsernameValidator


class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(
        verbose_name="электронная почта", null=False, blank=False, unique=True
    )

    first_name = models.CharField(
        max_length=50,
        verbose_name="имя",
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=2),
        ],
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name="фамилия",
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=2),
        ],
    )

    surname = models.CharField(
        verbose_name="отчество",
        max_length=50,
        null=False,
        blank=True,
        validators=[
            MinLengthValidator(limit_value=2),
        ],
    )

    username = models.CharField(
        max_length=50,
        verbose_name="никнейм",
        null=False,
        blank=True,
        validators=[CustomUsernameValidator(), MinLengthValidator(limit_value=3)],
    )

    is_active = models.BooleanField(verbose_name="активен", default=False)

    is_superuser = models.BooleanField(verbose_name="суперпользователь", default=False)

    is_staff = models.BooleanField(verbose_name="технический персонал", default=False)

    notification = models.BooleanField(verbose_name="уведомление", default=False)

    date_joined = models.DateTimeField(
        verbose_name="дата присоединения", default=timezone.now
    )

    updated_at = models.DateTimeField(verbose_name="дата изменения", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.last_name

    class Meta:
        db_table = "user"
