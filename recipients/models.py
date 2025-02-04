from django.core.validators import EmailValidator
from django.db import models

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Введите корректный адрес электронной почты")],
        help_text="Введите почту",
        verbose_name="Почтовый адрес получателя",
    )
    first_name = models.CharField(max_length=255, help_text="Введите имя", verbose_name="Имя получателя")
    last_name = models.CharField(max_length=255, help_text="Введите фамилию", verbose_name="Фамилия получателя")
    comment = models.TextField(help_text="Комментарий о получателе", verbose_name="Комментарий о получателе")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name="Создатель получателя рассылки",
    )

    def __str__(self):
        return f" {self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = [
            "last_name",
        ]
        permissions = [
            ("can_view_all_recipients", "can view all recipients"),
        ]
