from django.core.cache import cache

from config.settings import CACHE_ENABLED
from recipients.models import Recipient


class RecipientsService:

    @staticmethod
    def get_recipients_from_cache(user):
        if not CACHE_ENABLED:
            if user.has_perm("recipients.can_view_all_recipients"):
                return Recipient.objects.all()
            return Recipient.objects.filter(owner=user)

        # Уникальный ключ кэша для каждого пользователя
        if user.has_perm("recipients.can_view_all_recipients"):
            key = "recipients_all"
        else:
            key = f"recipients_for_user_{user.id}"

        recipients = cache.get(key)

        if recipients is not None:
            return recipients

        if user.has_perm("recipients.can_view_all_recipients"):
            recipients = Recipient.objects.all()
        else:
            recipients = Recipient.objects.filter(owner=user)

        cache.set(key, recipients, timeout=60 * 15)
        return recipients
