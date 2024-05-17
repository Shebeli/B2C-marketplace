from django.core.cache import cache
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import get_object_or_404

from .throttle import SMSAnonRateThrottle, CodeSubmitAnonRateThrottle
from .models import EcomUser
from .serializers import (
    UserProfileSerializer,
    PhoneSerializer,
    CreateUserSerializer,
    ChangeCurrentPasswordSerializer,
    ResetPasswordSerializer,
    VerifyCodeSerializer,
    VerifyCodeSerializer,
)
from .utils import (
    create_sms_cooldown_cache_key,
    create_phone_verify_cache_key,
    create_forgot_password_msg,
    create_verification_msg,
    send_sms,
    generate_random_code,
)


class UserSignupViewSet(viewsets.ViewSet):
    """
    Provides the following actions:
    - request_registration: Sends a register verficiation code SMS to user which is to be used in the next action.
    - confirm_register: Input the code recieved from previous action 'request_register'
      in order to complete the registration. A pair of access and refresh token will be sent
      in a successful response.
    """

    @action(detail=False, methods=["post"], throttle_classes=[SMSAnonRateThrottle])
    def request_registration(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_code = generate_random_code()
        inputted_phone = serializer.data["phone"]
        sms_cooldown_cache_key = create_sms_cooldown_cache_key(inputted_phone)
        code_cooldown_time = cache.get(sms_cooldown_cache_key)
        if code_cooldown_time:
            return Response(
                {"cooldown time to request another code": f"{code_cooldown_time}s"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        send_sms(
            reciever_phone_number=inputted_phone,
            message=create_verification_msg(register_code),
        )
        cache.set(create_phone_verify_cache_key(inputted_phone), register_code, 60 * 15)
        cache.set(sms_cooldown_cache_key, True, 60 * 2)
        return Response(
            {
                "success": f"register verification code sent to user for phone {inputted_phone} by SMS"
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(
        detail=False, methods=["post"], throttle_classes=[CodeSubmitAnonRateThrottle]
    )
    def verify_registration_request(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(
            create_phone_verify_cache_key(serializer.validated_data["phone"])
        )
        if not cached_code:
            return Response(
                {"error": "server is not expecting a verification code for this phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.validated_data["code"] != cached_code:
            return Response(
                {"error": "verification code is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserOnetimeAuthViewSet(viewsets.ViewSet):
    """
    Should be used when the user forgets their password or they want to login without 
    inputting their password, which gives them access to one time authentication.
    Provides the following actions:
    - request_onetime_auth: sends a verification code using SMS to the inputted phone
      number, which is required in the next router action.
    - verify_onetime_auth: verify the one time authentication using the code recieved
      from previous action.
    """

    @action(detail=False, methods=["post"], throttle_classes=[SMSAnonRateThrottle])
    def request_auth(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(EcomUser, phone=serializer.data["phone"])
        code_cooldown_time = cache.get(create_sms_cooldown_cache_key(user.phone))
        if code_cooldown_time:
            return Response(
                {"cooldown time to request another code": f"{code_cooldown_time}s"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        verification_code = generate_random_code()
        send_sms(
            reciever_phone_number=user.phone,
            message=create_forgot_password_msg(verification_code),
        )
        cache.set(create_sms_cooldown_cache_key(user.phone), True, 60 * 2)
        cache.set(create_phone_verify_cache_key(user.phone), verification_code, 60 * 15)

        return Response(
            {
                "success": f"verification code has been sent using SMS to this phone number: {user.phone}"
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["post"], throttle_classes=[CodeSubmitAnonRateThrottle])
    def verify_auth_request(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(create_phone_verify_cache_key(serializer.data["phone"]))
        if not cached_code:
            return Response(
                {"error": "server is not expecting a verification code for this phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.data["code"] != cached_code:
            return Response(
                {"error": "verification code is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = EcomUser.objects.get(phone=serializer.data["phone"])
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserProfileViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    """
    Provides the following actions (assuming the current user is authenticated):
    - retrieve: retrieves the current user profile.
    - update: update the current user profile info (except phone, email and password)
    - change_password: for changing current password.
    - change_phone_request: for requesting to change user's current phone number, a verification code  is sent
      to the new phone and then used in the next action to complete the phone number update process.
    - change_phone_verify: for verifying the new phone number, the verification code from previous action
        should be inputted inorder to complete the phone number update process.
    """

    serializer_class = UserProfileSerializer
    queryset = EcomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=["put"])
    def change_password(self, request):
        serializer = ChangeCurrentPasswordSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], throttle_classes=[SMSAnonRateThrottle])
    def change_phone_request(self, request):
        serializer = PhoneSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        new_phone = serializer.data["phone"]
        sms_cooldown_cache_key = create_sms_cooldown_cache_key(new_phone)
        if cache.get(sms_cooldown_cache_key):
            return Response(
                f"Too many code requests, please try again in {cache.ttl(sms_cooldown_cache_key)} seconds",
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        verification_code = generate_random_code()
        send_sms(
            reciever_phone_number=new_phone,
            message=create_verification_msg(verification_code),
        )
        cache.set(
            create_phone_verify_cache_key(new_phone),
            verification_code,
            60 * 15,
        )
        cache.set(create_sms_cooldown_cache_key(new_phone), True, 60 * 2)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["put"], throttle_classes=[CodeSubmitAnonRateThrottle])
    def change_phone_verify(self, request):
        serializer = VerifyCodeSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(create_phone_verify_cache_key(serializer.data["phone"]))
        if not cached_code:
            return Response(
                {"error": "server is not expecting a verification code for this phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.data["code"] != cached_code:
            return Response(
                "The inputted code is invalid", status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response("Phone number changed succesfuly", status=status.HTTP_200_OK)
