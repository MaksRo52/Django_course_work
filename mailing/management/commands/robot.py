import logging
from logging import exception

import pytz
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing, Message, Attempt

logger = logging.getLogger(__name__)


def my_job():
    print(datetime.now)
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    # создание объекта с применением фильтра
    mailings_off = Mailing.objects.filter(date_of_first_mail__gte=current_datetime).filter(
        status__in=["new", "active"]
    )
    for mailing in mailings_off:
        mailing.status = "complete"
        mailing.save()

    mailings = Mailing.objects.filter(date_of_first_mail__lte=current_datetime).filter(
        status__in=["new", "active"]
    )
    for mailing in mailings:
        try:
            send_mail(
                subject=mailing.message.title,
                message=mailing.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=mailing.clients.values_list("email", flat=True),
            )
            mailing.status = "active"
            mailing.save()
        except Exception as e:
            logger.error(f"Ошибка при отправке рассылки %d: %s {mailing.id}: {str(e)}")
            mailing.attempts.create(status=False, server_response=str(e))
        else:
            mailing.attempts.create(status=True)
            logger.info(f"Рассылка %d {mailing.id} успешно отправлена.")
        finally:
            if mailing.periodicity == "day":
                mailing.date_of_first_mail += relativedelta(days=1)
            elif mailing.periodicity == "week":
                mailing.date_of_first_mail += relativedelta(days=7)
            elif mailing.periodicity == "month":
                mailing.date_of_first_mail += relativedelta(months=1)
            mailing.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Это задание удаляет записи о выполнении заданий APScheduler старше `max_age` из базы данных.
    Это помогает предотвратить заполнение базы данных старыми историческими записями, которые больше не нужны.
     :param max_age: Максимальный срок хранения записей о выполнении исторических заданий. По умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запускает APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено задание 'my_job'.")
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute=" 00 "),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено еженедельное задание: 'delete_old_job_executions'.")
        try:
            logger.info(" Запуск планировщика ... ")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info(" Остановка планировщика ... ")
            scheduler.shutdown()
        logger.info("Планировщик успешно завершен! ")


# def mail_status_change():
#     """Меняет статус рассылки 'запущена' на 'создана' после времени окончания рассылки"""
#     mailings = Mailing.objects.filter(is_active=True)
#     attempt = Attempt.objects.all()
#
#     for mailing in mailings:
#         maillog = attempt.filter(mailing_id=mailing).all().order_by('-time_try').first()
#         if mailing.status == 'new' and mailing.time_end.hour > datetime.now().hour:
#             mailing.status = 'C'
#             mailing.save()
#         elif mailing.status == 'C' and maillog is not None and datetime.now().day > maillog.time_try.day():
#             mailing.status = 'C'
#             mailing.save()
