import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from . import conf


_token_lifetime = datetime.timedelta(days=conf.AUTH_TOKEN_LIFETIME_MINUTES)


def check_token(uidb64, token):
    user = get_user_model().objects.get(pk=urlsafe_base64_decode(uidb64).decode())
    if not default_token_generator.check_token(user, token):
        raise Exception
    return user


def send_mail_to_matching_users(request, email):
    site = get_current_site(request)
    for user in (
        u for u in get_user_model()._default_manager.filter(email__iexact=email, is_active=True)
        if u.has_usable_password()
    ):
        context = dict(
            email=email,
            domain=site.domain,
            site_name=site.name,
            uid=urlsafe_base64_encode(force_bytes(user.pk)),
            user=user,
            token=default_token_generator.make_token(user),
            protocol=request.scheme,
        )
        subject = ''.join(
            loader.render_to_string('registration/password_reset_subject.txt', context).splitlines()
        )
        body = loader.render_to_string('registration/password_reset_email.html', context)
        send_mail(subject, body, settings.SERVER_EMAIL, [email])
