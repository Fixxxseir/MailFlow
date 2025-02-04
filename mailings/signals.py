from django.apps import AppConfig
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from mailings.models import Mailing
from users.models import User


@receiver(post_save, sender=Mailing)
@receiver(post_delete, sender=Mailing)
def clear_mailing_cache(sender, **kwargs):
    # Очищаем кэш для всех рассылок
    cache.delete("all_mailings")
    for user in User.objects.all():
        cache.delete(f"mailings_for_user_{user.id}")


class MailingsConfig(AppConfig):
    name = "mailings"
    scheduler_started = False

    def ready(self):
        if not self.scheduler_started:
            from .tasks import start_scheduler
            start_scheduler()  # Запуск планировщика
            self.scheduler_started = True
