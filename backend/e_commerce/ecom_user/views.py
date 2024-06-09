from django.core.cache import cache
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import get_object_or_404

from ecom_user.throttle import SMSAnonRateThrottle, CodeSubmitAnonRateThrottle
from ecom_user.models import EcomUser
from ecom_user.serializers import (
    UserAccountSerializer,
    UserPhoneSerializer,
    OTPAuthSerializer,
    OTPAuthVerificationSerializer,
    ChangeCurrentPasswordSerializer,
    UserPhoneVerificationSerializer,
    UserPhoneVerificationSerializer,
)
from ecom_user.utils import (
    create_sms_cooldown_cache_key,
    create_phone_verify_cache_key,
    process_phone_verification,
)
from ecom_user.authentication import EcomUserJWTAuthentication
from ecom_user.permissions import IsAnonymous


class UserSignupViewSet(ViewSet):
    """
    Provides the following actions:
    - request_registration: Sends a register verficiation code SMS to user which is to be used in the next action.
    - verify_registration_request: Input the code recieved from previous action 'request_register'
      in order to complete the registration. A pair of access and refresh token will be the sent in a
      succesful response data.
    """

    permission_classes = [IsAnonymous]

    @action(detail=False, methods=["post"], throttle_classes=[SMSAnonRateThrottle])
    def request_registration(self, request):
        serializer = UserPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inputted_phone = serializer.validated_data["phone"]
        sms_cooldown_cache_key = create_sms_cooldown_cache_key(inputted_phone)
        code_cooldown_time = cache.ttl(sms_cooldown_cache_key)
        if code_cooldown_time:
            return Response(
                {"cooldown time to request another code": f"{code_cooldown_time}s"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        process_phone_verification(serializer.validated_data["phone"])
        return Response(
            {
                "success": f"register verification code sent to user for phone {inputted_phone} via SMS"
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(
        detail=False, methods=["post"], throttle_classes=[CodeSubmitAnonRateThrottle]
    )
    def verify_registration_request(self, request):
        serializer = UserPhoneVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(
            create_phone_verify_cache_key(serializer.validated_data["phone"])
        )
        if not cached_code:
            return Response(
                {"error": "server is not expecting a verification code for this phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.validated_data["verification_code"] != cached_code:
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


class UserOnetimeAuthViewSet(ViewSet):
    """
    Should be used when the user forgets their password or they want to login without
    inputting their password, which gives them access to one time authentication using OTP via SMS.
    Provides the following actions:
    - request_auth: sends an OTP via SMS to the inputted phone
      number, which is required in the next action.
    - verify_auth_request: verify the one time authentication using the OTP recieved
      from previous action.
    """

    permission_classes = [IsAnonymous]

    @action(detail=False, methods=["post"], throttle_classes=[SMSAnonRateThrottle])
    def request_auth(self, request):
        serializer = OTPAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(EcomUser, phone=serializer.data["phone"])
        code_cooldown_time = cache.ttl(create_sms_cooldown_cache_key(user.phone))
        if code_cooldown_time:
            return Response(
                {"cooldown time to request another code": f"{code_cooldown_time}s"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        process_phone_verification(serializer.data["phone"])
        return Response(
            {
                "success": f"verification code has been sent via SMS to this phone number: {user.phone}"
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(
        detail=False, methods=["post"], throttle_classes=[CodeSubmitAnonRateThrottle]
    )
    def verify_auth_request(self, request):
        serializer = OTPAuthVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(create_phone_verify_cache_key(serializer.data["phone"]))
        if not cached_code:
            return Response(
                {"error": "server is not expecting a verification code for this phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.data["verification_code"] != cached_code:
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


class UserAccountViewSet(ViewSet):
    """
    Provides the following actions (requires the current user to be authenticated):
    - get_info: retrieves the current user account info.
    - update_info: update the current user account info (except phone, email and password)
    - change_password: for changing current password.
    - change_phone_request: for changing user's current phone password by requesting an OTP via SMS,
      a verification code is sent to the new phone and then used in the next action
      to complete the phone number update process.
    - change_phone_verify: for verifying the new phone number, the verification code from previous action
      should be inputted inorder to complete the phone number update process.
    """

    authentication_classes = [EcomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def get_info(self, request):
        serializer = UserAccountSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["put"])
    def update_info(self, request):
        serializer = UserAccountSerializer(
            self.request.user, request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["put"])
    def change_password(self, request):
        serializer = ChangeCurrentPasswordSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"], throttle_classes=[SMSAnonRateThrottle])
    def change_phone_request(self, request):
        serializer = UserPhoneSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        new_phone = serializer.validated_data["phone"]
        sms_cooldown_cache_key = create_sms_cooldown_cache_key(new_phone)
        if cache.get(create_sms_cooldown_cache_key(new_phone)):
            return Response(
                f"Too many code requests, please try again in {cache.ttl(sms_cooldown_cache_key)} seconds",
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        process_phone_verification(new_phone)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(
        detail=False, methods=["put"], throttle_classes=[CodeSubmitAnonRateThrottle]
    )
    def change_phone_verify(self, request):
        serializer = UserPhoneVerificationSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        cached_code = cache.get(
            create_phone_verify_cache_key(serializer.validated_data["phone"])
        )
        if not cached_code:
            return Response(
                {"error": "server is not expecting a verification code for this phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.validated_data["verification_code"] != cached_code:
            return Response(
                "The inputted code is invalid", status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response("Phone number changed succesfuly", status=status.HTTP_200_OK)
