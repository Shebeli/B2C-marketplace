import random
import string

from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EcomUser
from .serializers import (
    UserSerializer,
    PhoneSerializer,
    CreateUserSerializer,
    ChangePasswordSerializer,
)
from .sms import (
    send_sms,
    create_forgot_password_message,
    create_verify_register_message,
)


class UserViewSet(viewsets.ViewSet):
    """
    Provides the following actions:
    - register: Sends a verify register code SMS to user to complete their registration.
    - confirm_register: Input the code recieved from action 'register' by sms 
      to complete registaration (returns a token pair upon success)
    - retrieve: get the user profile info.
    - update: update the user profile data(except phone number)
    - forgot_password: Sends a reset password code to user.
    - confirm_forgot_password: Input the code recieved from action 'reset_password' and
      allows the user to change their password by giving them access to the action called
      change_forgotten_password 
    - change_forgotten_password: user can input their new password and update their password
      which after wards logs them in by returning a token pair.
    """

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_phone = serializer.data['phone']
        register_code = random.choice(string.digits for _ in range(5))
        send_sms(
            reciever_phone_number=user_phone,
            message=create_verify_register_message(register_code),
        )
        cache.set(f"register_{user_phone}", register_code, 60*5)
        return Response(status=status.HTTP_202_ACCEPTED)



