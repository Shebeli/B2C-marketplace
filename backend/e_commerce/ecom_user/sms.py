import requests
import base64
import re
from datetime import datetime

from typing import NewType, Union
from django.conf import settings

PhoneNumber = NewType("PhoneNumber", str)
TimeFormat = NewType("TimeFormat", str)

# auth = f"{settings.SMS_USERNAME}:{settings.SMS_PASSWORD}"
# encoded_auth = base64.b64encode(auth.encode())
# headers = {"Authorization": f"Basic {encoded_auth}"}


def current_time(time_format: TimeFormat = "%H:%M:%S") -> str:
    return datetime.now().strftime(time_format)


def create_verify_register_message(code: Union[str, int]) -> str:
    return f"کد فعالسازی: {code}\nسامانه پیچی کالا\nزمان ارسال {current_time()}"


def create_forgot_password_message(code: Union[str, int]) -> str:
    return f"کد فراموشی رمز عبور: {code}\nسامانه پیچی کالا\nزمان ارسال {current_time()}"


def send_sms(
    reciever_phone_number: PhoneNumber,
    message: str,
    debug: bool = True,
    sender_phone_number: PhoneNumber = settings.SMS_SENDER_PHONE_NUMBER,
) -> None:
    """
    Sends a SMS with provided message to provided phone number. 
    if debug mode is enabled, no real SMS will be sent, instead it will print it in the console
    """
    if debug:
        print(
            f"""
            DEBUG mode is enabled for the function send_sms\n
            The following message is supposed to be sent from the phone number 
            {sender_phone_number} to {reciever_phone_number}:
            \n {message}
            """
        )
        return None
    return None # to be implemented later
