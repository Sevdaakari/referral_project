from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .models import CustomUser, ReferralCode
from django.contrib import messages
import random
import time 


def login(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        user_exists = CustomUser.objects.filter(phone_number=phone_number).exists()
        if user_exists:
            print('user exists')
            user = get_or_create_custom_user(phone_number, None)
            referral_code = user.referral_code
            print(f"this is user: {user} / referral_code {referral_code}")
            request.session['phone_number'] = phone_number
            request.session['referral_code'] = referral_code
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the authentication backend
            authenticated_user = authenticate(request, phone_number=user, referral_code=referral_code)
            print(f'authenticated_user {authenticated_user}')
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
        else:
            print('creating user')
            referral_code = ReferralCode.generate_referral_code()
            custom_user = get_or_create_custom_user(phone_number, referral_code)
            print(f'referral_code {referral_code} / phone_number {phone_number} ')
            custom_user.backend = 'django.contrib.auth.backends.ModelBackend'
            authenticated_user = authenticate(request, phone_number=phone_number, referral_code=referral_code)
            request.session['phone_number'] = phone_number
            request.session['referral_code'] = referral_code
            print(f'authenticated_user {authenticated_user}')
            if authenticated_user is not None:
                auth_login(request, authenticated_user)        
        
        return redirect('verification_code')  
             
    return render(request, 'referral/login.html')
    
def get_or_create_custom_user(phone_number, referral_code=None):
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
        return user
    except CustomUser.DoesNotExist:
        username = phone_number 
        user = CustomUser.objects.create_user(username=username, phone_number=phone_number, referral_code=referral_code)
        return user
    
def check_duplicate_referral_code(referral_code):
    duplicate_records = ReferralCode.objects.filter(code=referral_code)

    if duplicate_records.exists():
        print("Duplicate referral code found:")
        for record in duplicate_records:
            print(f"ID: {record.id}, Code: {record.code}")
    else:
        print("No duplicate referral codes found.")

def verification_code(request): 
    print('now in def verification_code')
    code = generate_verification_code()
    send_verification_code(code)
    if request.method == "POST": 
        entered_code = request.POST.get('verification_code')
        phone_number = request.session.get('phone_number')
        print(f'entered code: {entered_code} / phone_number {phone_number}')
        if len(entered_code) == 4 and phone_number is not None:               
            return redirect('profile')
        else:
            print('User authentication failed')
    return render(request, 'referral/verification_code.html')
            
def generate_verification_code():
    return ''.join(random.choices('0123456789', k=4))

def send_verification_code(code):
    time.sleep(2)


def profile(request):
    print("in profile")
    phone_number = request.session.get('phone_number')
    referral_code = request.session.get('referral_code')
    check_duplicate_referral_code(referral_code)
    print(f'phone_number: {phone_number} / referral_code: {referral_code}')
    user = get_or_create_custom_user(phone_number, referral_code)
    print(f'user {user}')
    if user.is_authenticated:    
        if request.method == "POST":
            codes = ReferralCode.objects.filter(code=referral_code)
            if codes.exists():
                code_to_activate = codes.first()
                print(f'code_to_activate {code_to_activate}')
                user.activated_referral_codes.add(code_to_activate)
            else:
                print('Referral code does not exist')
                messages.error(request, 'Referral code does not exist')
        context = {'referral_code': referral_code}        
        activated_referral_codes = user.activated_referral_codes.all()
        print(f'activated_referral_codes {activated_referral_codes}')
        return render(request, 'referral/profile.html', context)
    else:
        return redirect('login')

