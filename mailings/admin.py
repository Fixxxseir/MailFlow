from django.contrib import admin

from mailings.models import Mailing, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "start_sent_mailing",
        "stop_sent_mailing",
        "mailing_status",
        "message",
        "owner",
    )
    list_filter = (
        "owner",
        "start_sent_mailing",
        "mailing_status",
    )
    search_fields = ("owner", "start_sent_mailing", "mailing_status")


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "attempt_time",
        "attempt_status",
        "server_response",
        "mailing",
        "owner",
    )
    list_filter = (
        "owner",
        "attempt_status",
    )
    search_fields = (
        "owner",
        "attempt_time",
        "attempt_status",
    )
