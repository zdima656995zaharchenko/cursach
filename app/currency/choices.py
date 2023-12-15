from django.db import models
from django.utils.translation import gettext_lazy as _

class CurrencyChoices(models.IntegerChoices):
    USD = 1, _("USD")
    EUR = 2, _("EUR")

class SourceChoices(models.IntegerChoices):
    PRIVAT = 1, _("Privatbank")
    EUR = 2, _("Monobank")