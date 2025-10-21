from django.db import models

from user.enums import UserRoles


class User(models.Model):
    from pharmacy.models import Pharmacy

    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='users')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    national_code = models.CharField(max_length=11)
    role = models.IntegerField(choices=UserRoles.choices, default=UserRoles.TECHNICIAN)
    
    def __str__(self):
        return f"{self.name} ({self.role})"

    @staticmethod
    def create(
            pharmacy: Pharmacy,
            name: str,
            phone: str,
            email: str,
            address: str,
            national_code: str,
            role: UserRoles
    ) -> "User":
        return User.objects.create(
            pharmacy=pharmacy,
            name=name,
            phone=phone,
            email=email,
            address=address,
            national_code=national_code,
            role=role
        )
