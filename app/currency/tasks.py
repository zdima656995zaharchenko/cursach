import requests
from celery import shared_task
from django.conf import settings
from currency import consts
from decimal import Decimal, ROUND_DOWN
from currency.choices import CurrencyChoices
from currency.consts import PRIVATBANK_CODE_NAME, MONOBANK_CODE_NAME
from currency.utils import to_2_places_decimal




@shared_task
def parse_privatbank():
   from currency.models import Rate, Source
   from currency.choices import CurrencyChoices

   source, _ = Source.objects.get_or_create(
      code_name=consts.PRIVATBANK_CODE_NAME,
      defaults={
         'name': 'PrivatBank'
      }
   )

   url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
   response = requests.get(url)

   rates = response.json()

   available_currencies = {
      'USD': CurrencyChoices.USD,
      'EUR': CurrencyChoices.EUR
   }

   for rate in rates:
      buy = to_2_places_decimal(rate['buy'])
      sale = to_2_places_decimal(rate['sale'])
      currency = rate['ccy']

      if currency not in available_currencies:
         continue

      currency = available_currencies[currency]

      last_rate = Rate.objects.filter(source=source, currency=currency).order_by('created').last()

      if last_rate is not None and (last_rate.buy != buy or last_rate.sell != sale):
         Rate.objects.create(
            buy=buy,
            sell=sale,
            source=source,
            currency=currency
         )

@shared_task
def parse_monobank():
   from currency.models import Rate, Source
   from currency.choices import CurrencyChoices

   source, _ = Source.objects.get_or_create(
      code_name=consts.MONOBANK_CODE_NAME,
      defaults={
          'name': 'MonoBank'
      }
   )

   url = 'https://api.monobank.ua/bank/currency'
   response = requests.get(url)

   rates = response.json()

   available_currencies = {
      840: CurrencyChoices.USD,
      978: CurrencyChoices.EUR,
   }

   for rate in rates:
      buy = to_2_places_decimal(rate['rateBuy'])
      sale = to_2_places_decimal(rate['rateSell'])
      currency_code = rate['currencyCodeA']

      if currency_code not in available_currencies:
         continue

      currency = available_currencies[currency_code]

      print("Available Currencies:", available_currencies)
      print("Currency:", currency_code)  # Выводим код валюты

      last_rate = Rate.objects.filter(source=source, currency=currency_code).order_by('created').last()

      if last_rate is not None and (last_rate.buy != buy or last_rate.sell != sale):
         Rate.objects.create(
            buy=buy,
            sell=sale,
            source=source,
            currency=currency
         )

