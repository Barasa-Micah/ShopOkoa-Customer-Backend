from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField('auth.User', null=True, on_delete=models.CASCADE)
    profile_pic_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10)
    accept_terms = models.BooleanField(default=False)

    class UserType(models.TextChoices):
        """
        Enumerated type for the user types
        """
        MERCHANT = "Merchant", _("Merchant")
        ADMIN = "Admin", _("ShopOkoa Admin")
        BUYER = "Buyer", _("Buyer")
    
    user_type = models.CharField(max_length=255, choices=UserType.choices, default=UserType.BUYER)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_permit_url = models.URLField(null=True, blank=True)
    license_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    kra_pin = models.CharField(max_length=50, unique=True, blank=True, null=True)
    national_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user_type == self.UserType.MERCHANT:
            if 'business_name' in kwargs:
                self.business_name = kwargs['business_name']
            if 'business_permit_url' in kwargs:
                self.business_permit_url = kwargs['business_permit_url']
            if 'license_no' in kwargs:
                self.license_no = kwargs['license_no']
            if 'location' in kwargs:
                self.location = kwargs['location']
            if 'kra_pin' in kwargs:
                self.kra_pin = kwargs['kra_pin']
            if 'national_id' in kwargs:
                self.national_id = kwargs['national_id']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
