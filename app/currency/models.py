from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from .choices import CurrencyChoices, SourceChoices
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Rate(models.Model):
    buy = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    sell = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    currency = models.PositiveSmallIntegerField(
        _("Currency"),
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
    )

    created = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(
        "currency.Source", on_delete=models.CASCADE, related_name="rates"
    )

    def __str__(self):
        return f"{self.currency}"

    class CustomUserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('The Email field must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)

            return self.create_user(email, password, **extra_fields)




    def __str__(self):
        return f"{self.currency} - {self.rate}"

class ContactUs(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    name = models.CharField(_('Name'), max_length=128)
    reply_to = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=128)
    body = models.CharField(_('Body'), max_length=1024)

class Source(models.Model):
    source_url = models.CharField(max_length=255)
    exchange_address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    name = models.CharField(_('Name'), max_length=64)
    code_name = models.CharField(_('Code_name'), max_length=32, unique=True)
    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')


    def __str__(self):
        return self.name

class RequestResponseLog(models.Model):
    path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    time = models.IntegerField()

    def __str__(self):
        return f"{self.request_method} {self.path}"


