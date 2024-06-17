import string
import random
from datetime import datetime
from typing import NewType, Union

from django.conf import settings
from django.core.cache import cache

PhoneNumber = NewType("PhoneNumber", str)
TimeFormat = NewType("TimeFormat", str)

# the following constants are base string templates which are used to construct common cache keys.
VERIFY_PHONE_CACHE_BASE_KEY = "verify:"
SMS_COOLDOWN_CACHE_BASE_KEY = "cooldown:"


def current_time(time_format: TimeFormat = "%H:%M:%S") -> str:
    return datetime.now().strftime(time_format)


def create_verification_msg(code: Union[str, int]) -> str:
    return f"کد فعالسازی: {code}\nسامانه پیچی کالا\nزمان ارسال {current_time()}"


def create_forgot_password_msg(code: Union[str, int]) -> str:
    return f"کد فراموشی رمز عبور: {code}\nسامانه پیچی کالا\nزمان ارسال {current_time()}"


def send_sms(
    reciever_phone_number: PhoneNumber,
    message: str,
    debug: bool = settings.DEBUG,
    sender_phone_number: PhoneNumber = settings.SMS_SENDER_PHONE_NUMBER,
) -> None:
    """
    Sends a SMS with provided message to provided phone number.
    if debug mode is enabled, no real SMS will be sent, instead the message will be printed in the terminal.
    """
    if debug:
        print(
            f"""
            DEBUG mode is enabled for the function send_sms:\n
            The following message is supposed to be sent from the phone number 
            {sender_phone_number} to {reciever_phone_number}:
            \n {message}
            """
        )
        return None
    return None  # to be implemented later


def create_sms_cooldown_cache_key(phone: str) -> str:
    return SMS_COOLDOWN_CACHE_BASE_KEY + phone


def create_phone_verify_cache_key(phone: str) -> str:
    return VERIFY_PHONE_CACHE_BASE_KEY + phone


def generate_random_code(length: int = 6) -> str:
    return "".join(random.choice(string.digits) for _ in range(length))


def process_phone_verification(phone_number: PhoneNumber):
    """
    Generate a verification code, send the verification code via SMS to the provided
    phone number and create caches using the phone number and the generated code.
    """
    verification_code = generate_random_code()
    send_sms(
        reciever_phone_number=phone_number,
        message=create_verification_msg(verification_code),
    )
    cache.set(
        create_phone_verify_cache_key(phone_number),
        verification_code,
        60 * 15,
    )
    cache.set(create_sms_cooldown_cache_key(phone_number), True, 60 * 2)
