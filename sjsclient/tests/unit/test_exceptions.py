# -*- coding: utf-8 -*-

from oslotest import base

from sjsclient import exceptions


class TestHttpException(base.BaseTestCase):

    def setUp(self):
        super(TestHttpException, self).setUp()
        self.message = "test message"

    def _do_raise(self, *args, **kwargs):
        raise exceptions.HttpException(*args, **kwargs)

    def test_message_str(self):
        exc = self.assertRaises(exceptions.HttpException,
                                self._do_raise, self.message)
        str_message = "HttpException: {}".format(self.message)
        self.assertEqual(str_message, str(exc))

    def test_details(self):
        details = "some details"
        exc = self.assertRaises(exceptions.HttpException,
                                self._do_raise, self.message,
                                details=details)
        self.assertEqual(details, exc.details)

    def test_details_str(self):
        details = "some details"
        exc = self.assertRaises(exceptions.HttpException,
                                self._do_raise, self.message,
                                details=details)
        str_message_plus_details = "HttpException: {}, {}".format(self.message,
                                                                  details)
        self.assertEqual(str_message_plus_details, str(exc))

    def test_status_code(self):
        status_code = 123
        exc = self.assertRaises(exceptions.HttpException,
                                self._do_raise, self.message,
                                status_code=status_code)
        str_message = "HttpException: {}".format(self.message)
        self.assertEqual(str_message, str(exc))
        self.assertEqual(status_code, exc.status_code)
