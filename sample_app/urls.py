from django.conf.urls import include
from django.conf.urls import url
from django.views import View
from django.views.generic import TemplateView


class FakeView(View):
    pass


urlpatterns = [
    url(r'^auth/', include('drf_advanced_auth.urls')),
    url(r'^password-reset/update/(?P<uidb64>.*)/(?P<token>.*)', FakeView.as_view(), name='password_reset_confirm'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
