from django.contrib import admin

from recipients.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "comment",
        "owner",
    )
    list_filter = ("email",)
    search_fields = (
        "email",
        "owner",
    )
