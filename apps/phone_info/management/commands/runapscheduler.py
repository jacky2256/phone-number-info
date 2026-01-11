import logging
from datetime import datetime, timezone

from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from apps.phone_info.scheduler.jobs import import_phone_ranges_job

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone="UTC")

        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            import_phone_ranges_job,
            trigger=CronTrigger(hour=3, minute=0),  # раз в сутки в 03:00
            # trigger=CronTrigger(second="*/20"),
            id="import_phone_ranges",
            max_instances=1,
            replace_existing=True,
            next_run_time=datetime.now(timezone.utc)
        )

        self.stdout.write(self.style.SUCCESS("APScheduler started"))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Stopping APScheduler..."))
            scheduler.shutdown()
