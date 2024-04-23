from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser, ReferralCode
import random
import string
import time 

def login(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        user_exists = CustomUser.objects.filter(phone_number=phone_number).exists()
        if user_exists:
            print('user exists')
            user = CustomUser.objects.get(phone_number=phone_number)
            referral_code = user.referral_code
            print(f'referral_code {referral_code}')
        else:
            print('creating user')
            print(phone_number)
            referral_code = generate_referral_code()
            custom_user = CustomUser(phone_number=phone_number, referral_code=referral_code)
            custom_user.save()        
        return redirect('verification_code')
    return render(request, 'referral/login.html')


def verification_code(request): 
    print('now in def verification_code')
    code = generate_verification_code()
    send_verification_code(code)
    if request.method == "POST": 
        entered_code = request.POST.get('verification_code')
        print(f'entered code: {entered_code}')
        return render(request, 'referral/profile.html')    
    return render(request, 'referral/verification_code.html')
            
def generate_verification_code():
    return ''.join(random.choices('0123456789', k=4))

def send_verification_code(code):
    time.sleep(2)

def generate_referral_code():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=6))


def profile(request):
    print("in profile")
    user = request.user
    print(f'user {user}')

    activated_referral_codes = user.activated_referral_codes.all()
    
    if request.method == "POST":
        referral_code = request.POST['referral_code']
        try:
            code_to_activate = ReferralCode.objects.get(code=referral_code)
            user.activated_referral_codes.add(code_to_activate)
            activated_referral_codes = user.activated_referral_codes.all()
            return render(request, 'referral/profile.html', {'activated_referral_codes': activated_referral_codes})
        except ReferralCode.DoesNotExist:
            print('referral code does not exist')
            return render(request, 'referral/profile.html', {'activated_referral_codes': activated_referral_codes})

    return render(request, 'referral/profile.html', {'activated_referral_codes': activated_referral_codes})

