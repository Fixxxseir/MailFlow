from django.core.management.base import BaseCommand

from mailings.models import Mailing
from mailings.services import send_mailing


class Command(BaseCommand):
    help = "Запуск всех активных рассылок"

    def handle(self, *args, **kwargs):
        active_mailings = Mailing.objects.filter(status="Запущена")
        for mailing in active_mailings:
            send_mailing(mailing)
            self.stdout.write(f"Рассылка {mailing.id} отправлена")
