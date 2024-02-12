import random
import string

from django.core.cache import cache
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EcomUser
from .serializers import (
    UserProfileSerializer,
    PhoneSerializer,
    CreateUserSerializer,
    ChangePasswordSerializer,
    VerifyCodeSerializer
)
from .sms import (
    send_sms,
    create_forgot_password_message,
    create_verify_register_message,
)


class UserSignUpViewSet(viewsets.ViewSet):
    """
    Provides the following actions:
    - register: Sends a verify register code SMS to user to complete their registration.
    - confirm_register: Input the code recieved from action 'register' by sms
      to complete registaration (returns a token pair upon success)
    """

    def get_register_code_cooldown_time(phone: str) -> str:
        cache_key =f"register_code_cooldown_for_{phone}"
        remaining_time = cache_key.ttl(cache_key) 
        return remaining_time

    # for the sake of consistency, this should be used rather than defining the key explicitly.    
    def _get_register_code_cache_key(self, phone: str) -> str:
        return f"register_code_for_{phone}"


    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_code = random.choice(string.digits for _ in range(5))
        inputed_phone = serializer.data['phone']
        code_cache_key = self._get_register_code_cache_key(inputed_phone)
        code_cooldown_time = self.get_register_code_cooldown_time(inputed_phone)
        if code_cooldown_time:
            return Response({"remaining time": f"{code_cooldown_time}s"},status=status.HTTP_429_TOO_MANY_REQUESTS)
        send_sms(
            reciever_phone_number=inputed_phone,
            message=create_verify_register_message(register_code),
        )
        cache.set(f"register_code_cooldown_for_{inputed_phone}", True, 60*2)
        cache.set(self._get_register_code_cache_key(inputed_phone), register_code, 60 * 15)
        return Response({"success": f"register code SMS sent for phone {inputed_phone}"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["post"])
    def confirm_register(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(self._get_register_code_cache_key(serializer.data['phone'])) 
        if not cached_code:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_201_CREATED,
        )

class UserForgotPasswordViewSet(viewsets.ViewSet):
    """
    Provides the following actions:
    - forgot_password: Sends a reset password code to user.
    - confirm_forgot_password: Input the code recieved from action 'reset_password' and
      allows the user to change their password by giving them access to the action called
      change_forgotten_password
    - change_forgotten_password: user can input their new password and update their password
      which after wards logs them in by returning a token pair.
    """
    pass

class UserProfileViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    """
    Required authentication: UserIsAuthenticated
    Provides the following actions:
    - retrieve: retrieves the current authenticated user profile.
    - update: update the current authenticated user profile info (except phone and email)
    """

    serializer_class = UserProfileSerializer
    queryset = EcomUser.objects.all()
    permission_classes = [IsAuthenticated]
