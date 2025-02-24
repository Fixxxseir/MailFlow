from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )
    phone_number = PhoneNumberField(blank=True, verbose_name="Телефон", help_text="Введите свой телефон")
    country = models.CharField(max_length=20, verbose_name="Страна проживания", help_text="Введите страну проживания")

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_blocking_service_users", "can blocking service users"),
            ("can_view_list_all_users", "can view list all users"),
        ]

    def __str__(self):
        return self.email
