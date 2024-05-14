from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import EcomUser


# displaying user profile, updating profile except for phone number
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_fullname", read_only=True)

    class Meta:
        model = EcomUser
        exclude = ["last_login", "is_active", "password"]
        read_only_fields = ["phone", "email"]


# for creating a user
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcomUser
        fields = ["username", "phone", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if not validated_data["phone"] and not validated_data["username"]:
            raise serializers.ValidationError(
                _("Either phone or username should be provided for user creation.")
            )
        return EcomUser.objects.create_user(
            username=validated_data["username"],
            phone=validated_data["phone"],
            password=validated_data["password"],
        )


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = EcomUser
        fields = ["phone"]

    def create(self, validated_data):
        return EcomUser.objects.create_user(phone=validated_data["phone"])

    def update(self, instance, validated_data):  # instance is Ecomuser object
        instance.phone = validated_data.get("phone")
        instance.save()
        return instance


class ChangeCurrentPasswordSerializer(serializers.Serializer):
    "The request in view should be passed to this serializer through context as 'request'."
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password_verify = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate_old_password(self, old_password):
        user = self.instance
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                _("Inputed current password is incorrect.")
            )
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


class ResetPasswordSerializer(serializers.Serializer):
    """
    For users who have forgotten their password. Also validates the token
    using django's password reset token generator method "check_token()".
    The attribute "user" which is the user instance, becomes available
    after the method 'validate_id' has been called.
    """

    user_id = serializers.IntegerField(label="ID", read_only=True)
    token = serializers.CharField()
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password_verify = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def get_user(self):
        "Should be used after serializer method .is_valid() has been called"
        if not self._user:
            serializers.ValidationError(
                "The serializer should be validated first using the method '.is_valid'. "
            )
        return getattr(self, "_user")

    def validate_id(self, id):
        "Will also set the _user attribute to the user object that has been found using the passed in arguement 'id'."
        try:
            user = EcomUser.objects.get(id=id)
        except EcomUser.DoesNotExist:
            raise serializers.ValidationError(
                _("The provided user object id does not exist")
            )
        self._user = user
        return id

    def validate(self, data):
        if data["new_password"] != data["new_password_verify"]:
            raise serializers.ValidationError(_("Passwords don't match."))
        user = self._user
        try:
            validate_password(data["new_password"], user=user)
        except ValidationError as errors:
            raise serializers.ValidationError(errors)
        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError(_("Provided token does not match"))
        return data

    def save(self):
        user = self._user
        user.set_password(self.validated_data["new_password"])
        user.save()


class VerifyCodeSerializer(PhoneSerializer):
    code = serializers.CharField()

    class Meta:
        model = EcomUser
        fields = ["phone", "code"]

    def validate_code(self, code):
        if len(code) != 5:
            raise serializers.ValidationError(_("The inputed code length isn't 5"))
        if any(digit not in "0123456789" for digit in code):
            raise serializers.ValidationError(
                _("The inputed code cannot contain non-digits")
            )
        return code
