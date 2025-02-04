from django.core.cache import cache

from config.settings import CACHE_ENABLED
from MessageManagement.models import Message


class MessagesService:

    @staticmethod
    def get_messages_from_cache(user):

        if not CACHE_ENABLED:
            if user.has_perm("MessageManagement.can_view_all_messages"):
                return Message.objects.all()
            return Message.objects.filter(owner=user)

        if user.has_perm("MessageManagement.can_view_all_messages"):
            key = "all_messages"
        else:
            key = f"messages_for_user_{user.id}"

        message = cache.get(key)

        if message is not None:
            return message

        if user.has_perm("MessageManagement.can_view_all_messages"):
            message = Message.objects.all()

        else:
            message = Message.objects.filter(owner=user)

        cache.set(key, message, timeout=60 * 15)
        return message
