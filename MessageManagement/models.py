from django.db import models

from users.models import User


class Message(models.Model):
    message_subject = models.CharField(max_length=255, verbose_name="Тема рассылки", help_text="Введите тему рассылки")
    message_body = models.TextField(verbose_name="Текст рассылки", help_text="Введите текст рассылки")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages", verbose_name="Создатель рассылки"
    )

    def __str__(self):
        return self.message_subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "message_subject",
        ]
        permissions = [
            ("can_view_all_messages", "can view all messages"),
        ]
