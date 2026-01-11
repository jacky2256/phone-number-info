import csv
import logging
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.phone_info.models import PhoneRange

logger = logging.getLogger(__name__)

CSV_DIR: Path = settings.PHONE_INFO_CSV_DIR
CSV_FILENAME = "DEF-9xx.csv"
CSV_DELIMITER = ";"
BATCH_SIZE = 1000


class Command(BaseCommand):
    help = "Import phone ranges from CSV file in batches"

    def _download_and_update_csv(self, target_path: Path) -> None:
        """
        Downloads/updates CSV from remote server and saves to target_path.
        Сейчас это заглушка: только логирование.
        """
        logger.info("Starting download/update of CSV file")
        logger.info("Target path: %s", target_path)

        # TODO: here will be real download logic (requests/sftp/etc.)
        # e.g. download to temp file -> validate -> atomic replace

        logger.info("CSV download/update finished (stub)")

    def handle(self, *args, **options):
        csv_path = CSV_DIR / CSV_FILENAME

        self._download_and_update_csv(csv_path)

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        batch: list[PhoneRange] = []
        total_created = 0

        with csv_path.open("r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=CSV_DELIMITER)

            for row_number, row in enumerate(reader, start=1):
                batch.append(
                    PhoneRange(
                        def_code=int(row["АВС/ DEF"]),
                        from_number=int(row["От"]),
                        to_number=int(row["До"]),
                        capacity=int(row["Емкость"]),
                        operator=row["Оператор"].strip(),
                        region=row["Регион"].strip(),
                        gar_region=row["Территория ГАР"].strip(),
                        inn=row["ИНН"].strip(),
                    )
                )

                if len(batch) >= BATCH_SIZE:
                    PhoneRange.objects.bulk_create(batch)
                    total_created += len(batch)
                    batch.clear()

                    self.stdout.write(f"Imported {total_created} rows...")

        if batch:
            PhoneRange.objects.bulk_create(batch)
            total_created += len(batch)

        self.stdout.write(
            self.style.SUCCESS(f"Done. Imported {total_created} phone ranges from {csv_path}")
        )
