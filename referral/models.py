from django.db import models

class CustomUser(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=6, unique=True, null=True)
    activated_referral_codes = models.ManyToManyField('ReferralCode', related_name='activated_by_users')
    

class ReferralCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_codes')