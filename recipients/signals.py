from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from recipients.models import Recipient
from users.models import User


@receiver(post_save, sender=Recipient)
@receiver(post_delete, sender=Recipient)
def clear_recipients_cache(sender, **kwargs):
    cache.delete("recipients_all")
    for user in User.objects.all():
        cache.delete(f"recipients_for_user_{user.id}")
