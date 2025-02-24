from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from MessageManagement.models import Message
from users.models import User


@receiver(post_save, sender=Message)
@receiver(post_delete, sender=Message)
def clear_messages_cache(sender, **kwargs):
    cache.delete("all_messages")
    for user in User.objects.all():
        cache.delete(f"messages_for_user_{user.id}")
