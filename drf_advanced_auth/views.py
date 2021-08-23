from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import conf
from . import serializers
from . import utils


_success_response = dict(status='OK')
_user_logged_in_error = dict(error='user logged in')
_user_logged_out_error = dict(error='user logged out')
_invalid_token_error = dict(error='invalid token')


class AuthViewSet(GenericViewSet):

    permission_classes = []

    serializer_for_action = dict(
        login=serializers.LoginSerializer,
        logout=serializers.LogoutSerializer,
        change_password=serializers.ChangePasswordSerializer,
        reset_password_request=serializers.ResetPasswordRequestSerializer,
        reset_password_complete=serializers.ResetPasswordCompleteSerializer,
    )

    def get_serializer_class(self):
        return self.serializer_for_action.get(self.action, serializers.NullSerializer)

    @action(methods=['get', 'post'], detail=False)
    def login(self, request):
        if request.user.is_authenticated:
            return Response(_user_logged_in_error, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'GET':
            serializer = self.get_serializer()
            return Response(serializer.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data['user'])
        if conf.LOGIN_SUCCESS_RESPONSE_SERIALIZER:
            return Response(conf.LOGIN_SUCCESS_RESPONSE_SERIALIZER(request.user, context=dict(request=request)).data)
        return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))

    @action(methods=['get', 'post'], detail=False)
    def logout(self, request):
        if not request.user.is_authenticated:
            return Response(_user_logged_out_error, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'GET':
            serializer = self.get_serializer()
            return Response(serializer.data)
        logout(request)
        return Response(_success_response)

    @action(methods=['get', 'post'], detail=False)
    def change_password(self, request):
        if not request.user.is_authenticated:
            return Response(_user_logged_out_error, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'GET':
            serializer = self.get_serializer()
            return Response(serializer.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        login(request, request.user)
        return Response(_success_response)

    @action(methods=['get', 'post'], detail=False)
    def reset_password_request(self, request):
        if request.user.is_authenticated:
            return Response(_user_logged_in_error, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'GET':
            serializer = self.get_serializer()
            return Response(serializer.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utils.send_mail_to_matching_users(request, serializer.data['email'])
        return Response(_success_response)

    @action(methods=['get', 'post'], detail=False)
    def reset_password_complete(self, request):
        if request.user.is_authenticated:
            return Response(_user_logged_in_error, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'GET':
            serializer = self.get_serializer()
            return Response(serializer.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        login(request, serializer.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
