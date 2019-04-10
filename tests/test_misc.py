from django.contrib.auth import get_user_model
from django.test import TestCase

from sample_app.models import CustomUser


class TestAssumptions(TestCase):

    def test_user_is_right_user(self):
        self.assertTrue(issubclass(CustomUser, get_user_model()))
