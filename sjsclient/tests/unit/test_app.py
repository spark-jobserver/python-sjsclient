# -*- coding: utf-8 -*-

import requests_mock

from oslotest import base

from sjsclient import app
from sjsclient import client
from sjsclient import exceptions
from sjsclient import utils


app_name = "test-app"
app_repr = "<App: %s>" % app_name
app_create_response = "OK"
app_time = "2015-04-13T12:25:57.691+05:30"
app_get_response = """
{
  "%s":"%s"
}
""" % (app_name, app_time)


class TestApp(base.BaseTestCase):

    TEST_ENDPOINT = 'http://example.com:8090'

    def setUp(self):
        super(TestApp, self).setUp()
        self.client = client.Client(self.TEST_ENDPOINT)

    def assertAppFields(self, test_app):
        self.assertEqual(app_repr, repr(test_app))
        self.assertIsInstance(test_app, app.App)
        self.assertEqual(app_name, test_app.name)
        self.assertEqual(app_time, test_app.time)

    @requests_mock.Mocker()
    def test_create(self, mock_req):
        post_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.apps.base_path,
                                 app_name)
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.apps.base_path)

        mock_req.post(post_url, text=app_create_response)
        mock_req.get(get_url, text=app_get_response)
        test_app = self.client.apps.create(app_name, "fake-data")
        self.assertAppFields(test_app)

    @requests_mock.Mocker()
    def test_get(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.apps.base_path)

        mock_req.get(get_url, text=app_get_response)

        test_app = self.client.apps.get(app_name)
        self.assertAppFields(test_app)

    @requests_mock.Mocker()
    def test_get_non_existing(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.apps.base_path)

        mock_req.get(get_url, text=app_get_response)
        self.assertRaises(exceptions.NotFoundException,
                          self.client.apps.get, 'does-not-exist')

    @requests_mock.Mocker()
    def test_list(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.apps.base_path)

        mock_req.get(get_url, text=app_get_response)

        app_list = self.client.apps.list()
        for tapp in app_list:
            self.assertAppFields(tapp)

    @requests_mock.Mocker()
    def test_delete(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.apps.base_path,
                                app_name)

        mock_req.delete(get_url, text=app_create_response)
        self.client.apps.delete(app_name)
