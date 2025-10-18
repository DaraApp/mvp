from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('pharmacist', 'Pharmacist'),
        ('technician', 'Technician')
    ]
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.name} ({self.role})"