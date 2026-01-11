# apps/phones/models.py
from django.db import models


class PhoneRange(models.Model):
    def_code = models.PositiveSmallIntegerField()
    from_number = models.PositiveIntegerField()
    to_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    operator = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    gar_region = models.CharField(max_length=255)
    inn = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(fields=["def_code", "from_number", "to_number"]),
        ]
        verbose_name = "Phone range"
        verbose_name_plural = "Phone ranges"

    def __str__(self):
        return f"+7{self.def_code} {self.from_number}-{self.to_number}"
