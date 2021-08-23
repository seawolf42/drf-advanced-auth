import datetime
import pytz
import re

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail as Mail
from django.core.exceptions import ValidationError as ModelValidationError
from django.shortcuts import resolve_url
from django.shortcuts import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.test import TestCase
from rest_framework.serializers import ModelSerializer
from rest_framework.test import APIClient

from drf_advanced_auth import conf

from .utils import strings

from unittest import mock


User = get_user_model()
timezone = pytz.timezone(settings.TIME_ZONE)


class TestAuthViewBase(TestCase):

    url = ''
    payload = {}
    client = APIClient()
    username = strings[0]
    password = strings[0]

    def _setup_user(self):
        self.user = User.objects.create_user(username=self.username, password=self.password)


class TestLoginView(TestAuthViewBase):

    url = reverse('auth-login')

    class AlternateLoginResponseSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ('username',)

    def setUp(self):
        self.payload = dict(username=self.username, password=self.password)

    def test_get(self):
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)
        self._setup_user()
        self.client.force_login(self.user)
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 405)

    def test_post(self):
        self._setup_user()
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers['location'], resolve_url(settings.LOGIN_REDIRECT_URL))
        self.assertIn('_auth_user_id', self.client.session)

    def test_post_with_login_response_serializer(self):
        with mock.patch('drf_advanced_auth.conf.LOGIN_SUCCESS_RESPONSE_SERIALIZER'):
            conf.LOGIN_SUCCESS_RESPONSE_SERIALIZER = TestLoginView.AlternateLoginResponseSerializer
            self._setup_user()
            self.assertNotIn('_auth_user_id', self.client.session)
            response = self.client.post(self.url, self.payload, format='json')
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.data, dict(username=self.username))

    def test_invalid_username(self):
        self._setup_user()
        self.payload['username'] += strings[0]
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_password(self):
        self._setup_user()
        self.payload['password'] += strings[0]
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_form(self):
        self.payload['password'] = ''
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)


class TestLogoutView(TestAuthViewBase):

    url = reverse('auth-logout')

    def test_get(self):
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 405)
        self._setup_user()
        self.client.force_login(self.user)
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        self._setup_user()
        self.client.force_login(self.user)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class TestChangePasswordView(TestAuthViewBase):

    url = reverse('auth-change-password')
    valid_password = 'abcdefghijklmnopqrstuvwxyz'

    def setUp(self):
        self.payload = dict(
            current_password=self.password,
            new_password=self.valid_password,
        )

    def test_get(self):
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 405)
        self._setup_user()
        self.client.force_login(self.user)
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)

    @mock.patch('drf_advanced_auth.serializers.validate_password')
    def test_post(self, mock_validate_password):
        self._setup_user()
        self.assertIsNotNone(authenticate(username=self.username, password=self.password))
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.payload, format='json')
        mock_validate_password.assert_called_once()
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(authenticate(username=self.username, password=self.password))
        self.assertIsNotNone(authenticate(username=self.username, password=self.valid_password))

    @mock.patch('drf_advanced_auth.serializers.validate_password')
    def test_invalid_password(self, mock_validate_password):
        self._setup_user()
        self.client.force_login(self.user)
        self.payload = dict(password=strings[0])
        mock_validate_password.side_effect = ModelValidationError([])
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)
        self.assertIsNotNone(authenticate(username=self.username, password=self.password))

    @mock.patch('drf_advanced_auth.serializers.validate_password')
    def test_user_not_logged_out_after_password_change(self, mock_validate_password):
        self._setup_user()
        self.assertIsNotNone(authenticate(username=self.username, password=self.password))
        self.client.force_login(self.user)
        self.client.post(self.url, self.payload, format='json')
        response = self.client.get(TestLoginView.url)
        self.assertEquals(response.status_code, 405)


class TestAuthViewResetPasswordBase(TestAuthViewBase):

    valid_email_address = 'test@test.com'
    valid_wrong_email_address = 'tset@test.com'
    invalid_email_address = 'test@test'
    valid_password = 'abcdefghijklmnopqrstuvwxyz'

    def _setup_user(self, include_token=False):
        super(TestAuthViewResetPasswordBase, self)._setup_user()
        self.user.email = self.valid_email_address
        self.user.last_login = timezone.localize(datetime.datetime.now())
        self.user.save()
        if include_token:
            self.client.force_login(self.user)
            self.client.logout()
            self.user = User.objects.get(pk=self.user.pk)
            self.payload = dict(
                uidb64=urlsafe_base64_encode(force_bytes(self.user.pk)),
                token=default_token_generator.make_token(self.user),
            )


class TestAuthViewResetPasswordRequest(TestAuthViewResetPasswordBase):

    url = reverse('auth-reset-password-request')
    reset_link_regex = '(https?://[^/]+{0})'.format(
        reverse('password_reset_confirm', kwargs=dict(uidb64='.*', token='.*'))
    )

    def setUp(self):
        self.payload = dict(email=self.valid_email_address)

    def test_get(self):
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)
        self._setup_user()
        self.client.force_login(self.user)
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 405)

    def test_post(self):
        self._setup_user()
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Mail.outbox), 1)
        mail = Mail.outbox[0]
        self.assertEquals(list(mail.to), [self.valid_email_address])
        self.assertEquals(mail.subject, 'Password reset on testserver')
        self.assertIsNotNone(re.search(self.reset_link_regex, mail.body))

    def test_empty_email(self):
        self._setup_user()
        self.payload['email'] = self.valid_wrong_email_address
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Mail.outbox), 0)

    def test_invalid_email(self):
        self._setup_user()
        self.payload['email'] = self.invalid_email_address
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)


class TestAuthViewResetPasswordComplete(TestAuthViewResetPasswordBase):

    url = reverse('auth-reset-password-complete')

    def _setup_user(self):
        super(TestAuthViewResetPasswordComplete, self)._setup_user(include_token=True)
        self.payload.update(dict(
            new_password=self.valid_password,
        ))

    def test_get(self):
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 200)
        self._setup_user()
        self.client.force_login(self.user)
        response = self.client.get(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 405)

    def test_post(self):
        self._setup_user()
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers['location'], resolve_url(settings.LOGIN_REDIRECT_URL))
        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_token(self):
        self._setup_user()
        self.payload['token'] = strings[0]
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)

    def test_invalid_uidb64(self):
        self._setup_user()
        self.payload['uidb64'] = strings[0]
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)

    @mock.patch('drf_advanced_auth.serializers.validate_password')
    def test_invalid_password(self, mock_validate_password):
        self._setup_user()
        mock_validate_password.side_effect = ModelValidationError([])
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEquals(response.status_code, 400)
        assert authenticate(username=self.user.username, password=self.password) is not None
