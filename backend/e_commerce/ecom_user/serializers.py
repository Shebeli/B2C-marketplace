from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import EcomUser

# displaying user profile, updating profile except for phone number
class UserSerializer(serializers.ModelSerializer):
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password_verify = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate_old_password(self, old_password):
        user = self.context.get("request").user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                _("Inputed current password is incorrect.")
            )
        return old_password
    
    def validate(self, data):
        if data['new_password'] != data['new_password']:
            raise serializers.ValidationError(_("Passwords doesn't match."))
        return data
        
    def update(self, user_instance, validated_data):
        user_instance.set_password(validated_data['new_password'])
        user_instance.save()
        return user_instance
    
class UpdatePhoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EcomUser
        fields = ['phone','email']
        
    def create(self, validated_data):
        raise Exception("Method create is not allowed on UpdatePhoneSerializer")
    
    def update(self, user_instance, validated_data):
        user_instance.phone = validated_data.get('phone', user_instance.phone)
        user_instance.email = validated_data.get('email', user_instance.email)
        user_instance.save()
        return user_instance