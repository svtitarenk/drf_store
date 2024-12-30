from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class CreateSuperUser(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Создаем и сохраняем пользователя с username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Пользователь должен быть is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Пользователь должен быть is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=255,
        verbose_name="e-mail",
        help_text="Укажите e-mail",
        unique=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatar",
        **NULLABLE,
        verbose_name="Фотография",
        help_text="Загрузите фотографию",
    )
    phone = PhoneNumberField(
        region="RU", **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CreateSuperUser()
