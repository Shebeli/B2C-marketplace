from django.conf import settings

from celery import shared_task


@shared_task()
def send_sms(
    reciever_phone_number: str,
    message: str,
    debug: bool = settings.DEBUG,
    sender_phone_number: str = settings.SMS_SENDER_PHONE_NUMBER,
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