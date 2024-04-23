from django.urls import path
from referral.views import login, verification_code, profile

urlpatterns = [
    path('login/', login, name="login"),
    path('verification_code/', verification_code, name='verification_code'),
    path('profile/', profile, name='profile'),
]