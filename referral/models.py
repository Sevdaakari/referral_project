from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import string
import random

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=6, null=True)
    activated_referral_codes = models.ManyToManyField('ReferralCode', related_name='activated_by_users')
    verification_code = models.CharField(max_length=4, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_users_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users_permissions')
    username = models.CharField(max_length=15) 
    password = models.CharField(max_length=6, default='')
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    @classmethod
    def create_user(cls, phone_number, referral_code=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        user = cls(phone_number=phone_number, **extra_fields)
        if not referral_code:
            referral_code = ReferralCode.generate_referral_code()
        user.referral_code = referral_code
        user.set_password(referral_code)
        user.save(using=cls._default_manager.db)
        return user

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number
        if not self.referral_code:
            self.referral_code = ReferralCode.generate_referral_code()
        if not self.password:
            self.set_password(self.referral_code)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.phone_number

    def verify_verification_code(self, entered_code):
        return self.verification_code == entered_code
        

class ReferralCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_codes')
    
    @classmethod
    def generate_referral_code(cls):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        code = ''.join(random.choices(chars, k=6))
        return code