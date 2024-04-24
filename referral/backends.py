from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, referral_code=None):
        # Your authentication logic here
        # Example: Authenticate based on phone number and referral code
        try:
            user = CustomUser.objects.get(phone_number=phone_number, referral_code=referral_code)
            return user
        except CustomUser.DoesNotExist:
            return None
