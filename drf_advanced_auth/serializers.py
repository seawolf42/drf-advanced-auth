from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework import serializers

from . import utils


class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(*args, **kwargs)
        style = self.style
        if 'input_type' in style:
            raise Exception('do not override field_type for password fields')
        self.style['input_type'] = 'password'


NullSerializer = serializers.Serializer


class NewPasswordBase(serializers.Serializer):

    new_password = PasswordField()
    repeat_password = PasswordField()

    def validate_new_password(self, value):
        user = self.context['request'].user
        try:
            validate_password(value, user=user)
        except ModelValidationError as e:
            raise serializers.ValidationError(e)
        return value

    def validate(self, data):
        if data['repeat_password'] != data['new_password']:
            raise serializers.ValidationError('passwords mismatch')
        return data


class ChangePasswordSerializer(NewPasswordBase):

    current_password = PasswordField()

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError('current password incorrect')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.data['new_password'])
        user.save()


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = PasswordField()


class ResetPasswordCompleteSerializer(NewPasswordBase):

    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        data = super(ResetPasswordCompleteSerializer, self).validate(data)
        try:
            self.user = utils.check_token(data['uidb64'], data['token'])
        except Exception as e:
            raise serializers.ValidationError(e)
        return data

    def save(self):
        user = self.user
        user.set_password(self.data['new_password'])
        user.save()


class ResetPasswordRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()
