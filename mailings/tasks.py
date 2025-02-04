from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail

from config import settings
from .models import Mailing, MailingAttempt


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
                server_response="Письмо успешно отправлено",
                owner=mailing.owner,
            )
        except Exception as e:
            # Фиксация неудачной попытки
            MailingAttempt.objects.create(
                mailing=mailing,
                attempt_status="not_successfully",
                server_response=str(e),
                owner=mailing.owner,
            )


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Планирование задач для всех активных рассылок
    for mailing in Mailing.objects.filter(mailing_status="launched"):
        scheduler.add_job(
            send_mailing,
            'interval',
            hours=10,
            args=[mailing],
            id=f'mailing_{mailing.id}',
            replace_existing=True,
        )

    scheduler.start()


def delete_old_job_executions(max_age=604_800):  # 7 дней
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

