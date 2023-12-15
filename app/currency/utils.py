from decimal import Decimal, ROUND_DOWN
def to_2_places_decimal(value):
   return Decimal(value).quantize(Decimal('.01'))