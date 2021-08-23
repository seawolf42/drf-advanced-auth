from django.test import TestCase

from drf_advanced_auth import conf

from .utils import strings

from unittest import mock


@mock.patch('drf_advanced_auth.conf._SETTINGS')
class TestConf(TestCase):

    def test_load_class(self, mock_settings):
        self.assertEqual(conf._load_class('tests.test_conf.TestConf'), self.__class__)

    def test_get_setting_unset_no_default(self, mock_settings):
        conf._SETTINGS = dict()
        self.assertEqual(conf._get_setting(strings[0]), None)

    def test_get_setting_set_no_default(self, mock_settings):
        conf._SETTINGS = {strings[0]: strings[1]}
        self.assertEqual(conf._get_setting(strings[0]), strings[1])

    def test_get_setting_unset_default(self, mock_settings):
        conf._SETTINGS = dict()
        self.assertEqual(conf._get_setting(strings[0], default=strings[-1]), strings[-1])

    def test_get_setting_set_default(self, mock_settings):
        conf._SETTINGS = {strings[0]: strings[1]}
        self.assertEqual(conf._get_setting(strings[0], default=strings[-1]), strings[1])

    @mock.patch('drf_advanced_auth.conf._load_class')
    def test_get_setting_is_class(self, mock_load_class, mock_settings):
        conf._SETTINGS = {strings[0]: strings[1]}
        mock_load_class.return_value = strings
        self.assertEqual(conf._get_setting(strings[0], is_classpath=True), strings)
        mock_load_class.assert_called_once_with(strings[1])
