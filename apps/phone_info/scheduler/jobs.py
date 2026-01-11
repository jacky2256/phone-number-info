from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)


def import_phone_ranges_job():
    logger.info("Starting phone ranges import job")
    call_command("import_phone_ranges")
    logger.info("Finished phone ranges import job")
