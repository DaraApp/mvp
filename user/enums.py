from django.db import models

class UserRoles(models.IntegerChoices):
    PHARMACIST = 1
    TECHNICIAN = 2