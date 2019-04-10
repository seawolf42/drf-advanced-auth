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


class ChangePasswordSerializer(serializers.Serializer):

    password = PasswordField()
    repeat_password = PasswordField()

    def validate_password(self, value):
        request = self.context.get('request', None)
        user = request.user if request and hasattr(request, 'user') else None
        try:
            validate_password(value, user=user)
        except ModelValidationError as e:
            raise serializers.ValidationError(e)
        return value

    def validate(self, data):
        if data['repeat_password'] != data['password']:
            raise serializers.ValidationError('passwords mismatch')
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.data['password'])
        user.save()


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = PasswordField()


class ResetPasswordCompleteSerializer(ChangePasswordSerializer):

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
        user.set_password(self.data['password'])
        user.save()


class ResetPasswordRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()
