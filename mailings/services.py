from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from config import settings
from config.settings import CACHE_ENABLED
from mailings.models import Mailing, MailingAttempt


class MailingsService:

    @staticmethod
    def get_mailings_from_cache(user):

        if not CACHE_ENABLED:
            if user.has_perm("mailings.can_view_all_mailings"):
                return Mailing.objects.all()
            return Mailing.objects.filter(owner=user)

        if user.has_perm("mailings.can_view_all_mailings"):
            key = "all_mailings"
        else:
            key = f"mailings_for_user_{user.id}"

        mailing = cache.get(key)

        if mailing is None:
            if user.has_perm("mailings.can_view_all_mailings"):
                mailing = Mailing.objects.all()
            else:
                mailing = Mailing.objects.filter(owner=user)

        cache.set(key, mailing, timeout=60 * 15)
        return mailing


def send_mailing(mailing):
    recipients = mailing.recipients.all()
    subject = mailing.message.message_subject
    message = mailing.message.message_body
    from_email = settings.EMAIL_HOST_USER

    for recipient in recipients:
        try:
            # Отправка письма
            send_mail(
                subject,
                message,
                from_email,
                [recipient.email],
                fail_silently=False,
            )
            # Фиксация успешной попытки
            MailingAttempt.objects.create(
                mailing=mailing,
                attempt_status="successfully",
                attempt_time=timezone.now(),
                server_response="Письмо успешно отправлено",
                owner=mailing.owner,
            )
        except Exception as e:
            # Фиксация неудачной попытки
            MailingAttempt.objects.create(
                mailing=mailing,
                attempt_time=timezone.now(),
                attempt_status="not_successfully",
                server_response=str(e),
                owner=mailing.owner,
            )


def start_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.mailing_status != "launched":
        send_mailing(mailing)
        mailing.mailing_status = "launched"
        mailing.start_sent_mailing = timezone.now()
        mailing.save()
        messages.success(request, "Рассылка успешно запущена.")
    else:
        messages.warning(request, "Рассылка уже запущена.")
    return redirect('mailings:mailings_list')


@permission_required('mailings.can_disabling_mailings')
def disable_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.mailing_status != "completed":
        mailing.mailing_status = "completed"
        mailing.stop_sent_mailing = timezone.now()
        mailing.save()
        messages.success(request, "Рассылка успешно отключена.")
    else:
        messages.warning(request, "Рассылка уже отключена.")
    return redirect('mailings:mailings_list')


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Планирование задач для всех активных рассылок
    for mailing in Mailing.objects.filter(mailing_status="launched"):
        scheduler.add_job(
            send_mailing,
            'interval',
            minutes=1,  # Интервал отправки (например, каждую минуту)
            args=[mailing],
            id=f'mailing_{mailing.id}',
            replace_existing=True,
        )

    scheduler.start()