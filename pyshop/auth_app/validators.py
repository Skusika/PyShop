import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class CustomEmailValidator:
    """
    Кастомный валидатор email.
    """

    def __init__(self):
        self.local_part = None
        self.domain_part = None

    def __call__(self, value):
        if not self.validate_email(value):
            raise ValidationError("Введите корректный адрес электронной почты.")

    def validate_email(self, email):
        parts = email.split("@")
        if len(parts) != 2 or len(email) > 50:
            return False

        self.local_part, self.domain_part = parts
        return self.validate_local_part() and self.validate_domain_part()

    def validate_local_part(self):
        local_regex = r"^[a-zA-Z0-9_.+-]+$"
        return (
            bool(self.local_part)
            and bool(re.match(local_regex, self.local_part))
            and not self.local_part.startswith(".")
            and not self.local_part.endswith(".")
            and "-" not in (self.local_part[0], self.local_part[-1])
            and "--" not in self.local_part
        )

    def validate_domain_part(self):
        domain_regex = r"^[a-zA-Z0-9]+(?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.[a-zA-Z]+$"
        return bool(self.domain_part) and bool(re.match(domain_regex, self.domain_part))


class PasswordValidator:
    """
    Валидатор пароля.
    """

    def __init__(self):
        self.password = None

    def __call__(self, value):
        self.validate_password(value)

    def validate_password(self, password):
        regex = r"^(?=.*[0-9])(?=.*[!%&*])[A-Za-z0-9!%&*]{8,}$"
        if not re.match(regex, password):
            raise ValidationError(
                "Пароль должен содержать не менее 8 символов, включая цифру и спецсимволы ! % & * в латинице."
            )


class FIOValidator:
    """
    Кастомный валидатор фамилии, имени и отчества.
    """

    def __init__(self):
        self.fio = None

    def __call__(self, value):
        self.validate_fio(value)

    def validate_fio(self, value):
        pattern = re.compile(r"^[a-zA-Zа-яА-Я\s\'-]+$")
        self.fio = value

        if not pattern.match(self.fio):
            raise ValidationError(
                "Допустимы только буквы (латинские или кириллица), пробелы, дефисы и апострофы."
            )


class CustomUsernameValidator(RegexValidator):
    """
    Кастомный валидатор никнейма.
    """

    regex = r"^[a-zA-Z0-9](?!.*[.]{2,})[a-zA-Z0-9.]{4,48}[a-zA-Z0-9]$"

    message = (
        "Недопустимое имя пользователя. Имя пользователя может содержать только буквы (a-z, A-Z), "
        "цифры (0-9) и точки (.) (за исключением нескольких точек)."
        "Имя пользователя не должно начинаться и заканчиваться точками (.)."
    )

    def __call__(self, value):
        super().__call__(value)

        min_length = getattr(self, "min_length", 3)
        # Получаем значение min_length из экземпляра или используем 3 по умолчанию

        if len(value) < min_length and value.strip() != "":
            raise ValidationError(
                "Убедитесь, что значение содержит не менее %(limit_value)s символов.",
                code="min_length",
                params={"limit_value": min_length},
            )
