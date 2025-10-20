from datetime import datetime

from django.db import models
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from user.models import User


class PharmaCompany(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    @staticmethod
    def get_by_name(name: str) -> "PharmaCompany":
        return PharmaCompany.objects.get(name=name)


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return self.name

    @staticmethod
    def create(name: str, address: str, user: User) -> "Pharmacy":
        return Pharmacy.objects.create(name=name, address=address, user=user)


class Drug(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.TextField()
    pharma_company = models.ForeignKey(PharmaCompany, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class PharmacyItem(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    pharma_company = models.ForeignKey(PharmaCompany, on_delete=models.CASCADE)
    explanation = models.TextField()
    expiration = models.DateTimeField()
    amount = models.IntegerField()
    locked = models.IntegerField()
    price = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.drug.name} {self.pharma_company.name}" 
    
    def lock_amount(self, amount: int) -> None:
        if self.amount - self.locked < amount:
            raise ValidationError("Not enough items to lock")
        else:
            self.locked += amount
            self.save(update_fields=["locked"])
    
    def unlock_amount(self, amount: int) -> None:
        if self.locked < amount:
            raise ValidationError("Not enough items to unlock")
        else:
            self.locked -= amount
            self.save(update_fields=["locked"])
    
    def adjust_amount(self, amount: int) -> int:
        if self.amount + amount < 0:
            raise ValidationError("Not enough items")
        else:
            self.amount += amount
            self.save(update_fields=["amount"])
        return self.amount

    @staticmethod
    def create(
            drug: Drug,
            expiration: datetime,
            company: PharmaCompany,
            amount: int, # todo handle box of items!
            pharmacy: Pharmacy,
            price: int,
            locked: int = 0,
            explanation: str = "",
    ) -> "PharmacyItem":
        return PharmacyItem.objects.create(
            drug=drug,
            pharmacy=pharmacy,
            pharma_company=company,
            amount=amount,
            expiration=expiration,
            explanation=explanation,
            locked=locked,
            price=price
        )

    @staticmethod
    def filter_by_drug(drug: Drug) -> QuerySet["PharmacyItem"]:
        return PharmacyItem.objects.filter(drug=drug)

    @staticmethod
    def filter_by_company(company: PharmaCompany) -> QuerySet["PharmacyItem"]:
        return PharmacyItem.objects.filter(pharma_company=company)

    @staticmethod
    def filter_by_pharmacy(pharmacy: Pharmacy) -> QuerySet["PharmacyItem"]:
        return PharmacyItem.objects.filter(pharmacy=pharmacy)