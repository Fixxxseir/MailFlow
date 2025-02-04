from django.contrib import admin

from MessageManagement.models import Message


@admin.register(Message)
class RMessageAdmin(admin.ModelAdmin):
    list_display = (
        "message_subject",
        "message_body",
        "owner",
    )
    list_filter = ("owner",)
    search_fields = (
        "owner",
        "message_subject",
    )
