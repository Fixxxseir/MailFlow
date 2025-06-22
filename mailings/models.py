from django.db import models

from MessageManagement.models import Message
from recipients.models import Recipient
from users.models import User


class Mailing(models.Model):
    STATUS_CHOICES = (("created", "создана"), ("launched", "запущена"), ("completed", "завершена"))
    start_sent_mailing = models.DateTimeField(null=True, blank=True, verbose_name="Начало отправки")
    stop_sent_mailing = models.DateTimeField(null=True, blank=True, verbose_name="Окончание отправки")
    mailing_status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default="created",
        verbose_name="Статус рассылки",
        help_text="Изменить статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
        help_text="Выбрать сообщение",
    )
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели", help_text="Выбрать получателя")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mailings", verbose_name="Создатель рассылки"
    )

    def __str__(self):
        return f"Тема: {self.message.message_subject}, статус: {self.mailing_status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = [
            "mailing_status",
        ]
        permissions = [
            ("can_view_all_mailings", "can view all mailings"),
            ("can_disabling_mailings", "can disabling mailings"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ("successfully", "успешно"),
        ("not_successfully", "не успешно"),
    )
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки отправки сообщения")
    attempt_status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default="not_successfully", verbose_name="статус потки"
    )
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="mailing_attempts")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_attempts")

    def __str__(self):
        return f"Попытка: {self.id} для сообщения: {self.mailing.id}, статус: {self.attempt_status}"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = [
            "attempt_status",
            "attempt_time",
        ]
