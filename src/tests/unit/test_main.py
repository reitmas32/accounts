from unittest import TestCase


class TestBase(TestCase):
    @classmethod
    def clean_data(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.clean_data()
        super().tearDownClass()

    def test_pagination(self):
        self.assertEqual(3,3)
