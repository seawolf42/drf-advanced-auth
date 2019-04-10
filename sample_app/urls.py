from django.conf.urls import include
from django.conf.urls import url
from django.views import View


class FakeView(View):
    pass


urlpatterns = [
    url(r'^auth/', include('drf_advanced_auth.urls')),
    url(r'^password-reset/update/(?P<uidb64>.*)/(?P<token>.*)', FakeView.as_view(), name='password_reset_confirm')
]
