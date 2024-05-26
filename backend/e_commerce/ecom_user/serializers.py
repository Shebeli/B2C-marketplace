from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from ecom_core.validators import validate_phone, validate_verification_code
from .models import EcomUser


# displaying user profile, updating profile except for phone number
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_fullname", read_only=True)

    class Meta:
        model = EcomUser
        exclude = ["last_login", "is_active", "password"]
        read_only_fields = ["phone", "email", "date_created"]


# registering, updating and authenticating without inputting password are all handled using OTPs via SMS.
class UserPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, validators=[validate_phone])


class UserPhoneVerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField(
        write_only=True, validators=[validate_verification_code]
    )
    phone = serializers.CharField(
        max_length=13,
        validators=[validate_phone, UniqueValidator(queryset=EcomUser.objects.all())],
    )

    def create(self, validated_data):
        user = EcomUser.objects.create_user(phone=validated_data["phone"])
        user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance


class OTPAuthSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, validators=[validate_phone])


class OTPAuthVerificationSerializer(OTPAuthSerializer):
    verification_code = serializers.CharField(validators=[validate_verification_code])


class ChangeCurrentPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=64, write_only=True, required=True)
    new_password = serializers.CharField(max_length=64, write_only=True, required=True)
    new_password_verify = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate_old_password(self, old_password):
        user = self.instance
        if not user:
            raise serializers.ValidationError(
                "An ecomuser instance should be passed to this serializer before validating"
            )
        if not isinstance(user, EcomUser):
            raise serializers.ValidationError(
                "The passed in instance should be an instance of Ecomuser"
            )
        if not user.check_password(old_password):
            raise serializers.ValidationError(_("Current password is incorrect."))
        return old_password

    def validate(self, data):
        if data["new_password"] != data["new_password_verify"]:
            raise serializers.ValidationError(
                _("New Password and its confirmation don't match.")
            )
        try:
            validate_password(data["new_password"], user=self.instance)
        except ValidationError as errors:
            raise serializers.ValidationError(errors)
        return data

    def update(self, user_instance, validated_data):
        user_instance.set_password(validated_data["new_password"])
        user_instance.save()
        return user_instance
