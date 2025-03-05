from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User"""

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Создает и возвращает пользователя."""

        if email is None:
            raise ValueError("Users must have an email address.")

        if first_name is None:
            raise ValueError("Users must have an first_name.")

        if last_name is None:
            raise ValueError("Users must have an last-name.")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """Создает и возвращает пользователя с привилегиями суперпользователя."""

        if password is None:
            raise ValueError("Superusers must have a password.")

        if first_name is None:
            raise ValueError("Users must have an first_name.")

        if last_name is None:
            raise ValueError("Users must have an last-name.")

        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.save()

        return user
