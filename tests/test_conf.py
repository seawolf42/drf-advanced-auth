import sys

from django.test import TestCase

from drf_advanced_auth import conf

if sys.version_info[0] < 3:
    # python 2
    import mock
else:
    # python 3
    from unittest import mock


@mock.patch('drf_advanced_auth.conf._SETTINGS')
class TestConf(TestCase):

    def test_load_class(self, mock_settings):
        self.assertEqual(conf._load_class('tests.test_conf.TestConf'), self.__class__)
