from datetime import datetime
from typing import Optional

from django.db import models
from django.db import transaction as django_transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from pharmacy.models import PharmacyItem, Drug
from user.models import User


class ExchangeItem(models.Model):
    pharmacy_item = models.ForeignKey('pharmacy.PharmacyItem', on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.IntegerField()


    def __str__(self):
        return self.pharmacy_item.display_name

    def adjust_amount(self, amount):
        if self.amount + amount < 0:
            raise ValidationError('Amount cannot be negative')
        self.amount += amount
        self.save(update_fields=['amount'])

    @staticmethod
    def create(pharmacy_item: PharmacyItem, price: int, amount: int = 0) -> 'ExchangeItem':
        return ExchangeItem.objects.create(pharmacy_item=pharmacy_item, amount=amount, price=price)

    @staticmethod
    def filter_by_drug(drug: Drug) -> QuerySet['ExchangeItem']:
        return ExchangeItem.objects.filter(pharmacy_item__drug_id=drug.id)

    @staticmethod
    def get_by_pharmacy_item(pharmacy_item: PharmacyItem) -> Optional['ExchangeItem']:
        try:
            return ExchangeItem.objects.get(pharmacy_item=pharmacy_item)
        except ExchangeItem.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(item_id: int) -> 'ExchangeItem':
        return ExchangeItem.objects.get(id=item_id)


    @staticmethod
    def add_item_to_store(pharmacy_item: PharmacyItem, amount: int, price: int) -> 'ExchangeItem':
        with django_transaction.atomic():
            pharmacy_item.adjust_amount(-1*amount)
            exchange_item = ExchangeItem.get_by_pharmacy_item(pharmacy_item)
            if not exchange_item:
                exchange_item = ExchangeItem.create(pharmacy_item=pharmacy_item, price=price)

            exchange_item.adjust_amount(amount)
            return exchange_item

    @staticmethod
    def remove_item_from_store(item_id: int) -> None:
        with django_transaction.atomic():
            exchange_item = ExchangeItem.get_by_id(item_id)
            pharmacy_item = exchange_item.pharmacy_item
            pharmacy_item.adjust_amount(exchange_item.amount)
            exchange_item.delete()
