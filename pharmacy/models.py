from django.db import models
from user.models import User

class PharmaCompany(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return self.name

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
    count = models.IntegerField()
    locked = models.IntegerField()