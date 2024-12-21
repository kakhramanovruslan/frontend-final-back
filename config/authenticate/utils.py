import random
import smtplib

from django.core.cache import cache
from django.core.mail import send_mail

from .models import User
from config import settings


def generate_random_activation_code() -> int:
    random_number = random.randint(100000, 999999)

    return random_number


def save_generated_activation_code(cache_key, email) -> int or None:
    try:
        user = User.objects.get(email=email)
        user_id = user.id
        activation_code = generate_random_activation_code()
        full_cache_key = f'{cache_key}_{user_id}'
        cache.set(full_cache_key, activation_code, timeout=60*5)  # 5 минут
        print(f'Saving activation code in cache: {full_cache_key} -> {activation_code}')
        return activation_code
    except User.DoesNotExist:
        print(f'User with email {email} does not exist.')
        return None


def check_activation_code(cache_key, email, activation_code) -> bool:
    try:
        user = User.objects.get(email=email)
        user_id = user.id
        full_cache_key = f'{cache_key}_{user_id}'
        saved_activation_code = cache.get(full_cache_key)
        print(f'Checking activation code in cache: {full_cache_key} -> {saved_activation_code}')
        if saved_activation_code and int(saved_activation_code) == int(activation_code):
            return True
        return False
    except User.DoesNotExist:
        print(f'User with email {email} does not exist.')
        return False


def send_activation_code(cache_key, email):
    activation_code = save_generated_activation_code(cache_key, email)
    print("activation_code", activation_code)

    subject = 'User activation code'
    message = f'Your activation code: {activation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
