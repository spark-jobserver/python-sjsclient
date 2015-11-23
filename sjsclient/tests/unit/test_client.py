# -*- coding: utf-8 -*-

import json

import mock
from oslotest import base
import requests_mock

from sjsclient import client
from sjsclient import exceptions

fake_response = 'this is a fake response...'
fake_request = 'this is a fake request...'
fake_record = {
    'hello': 'world',
}


class FakeRespone(object):
    def __init__(self, text):
        self.text = text

    def json(self):
        raise ValueError()


class TestClient(base.BaseTestCase):

    TEST_PATH = '/resources'
    TEST_URL = 'http://example.com:8090/resources'
    TEST_ENDPOINT = 'http://example.com:8090'

    def test_parse_error_response(self):
        http_client = client.Client(self.TEST_URL)
        resp = mock.Mock()
        resp.json = mock.Mock()
        resp.json.return_value = {"status": "Not found"}
        self.assertEqual("Not found",
                         http_client._parse_error_response(resp))
        resp = FakeRespone("Not found")
        self.assertEqual("Not found",
                         http_client._parse_error_response(resp))

    @requests_mock.Mocker()
    def test_delete(self, mock_req):
        mock_req.delete(self.TEST_URL, text=fake_response)

        sclient = client.Client(self.TEST_ENDPOINT)
        resp = sclient._delete(self.TEST_PATH)

        self.assertEqual("DELETE", mock_req.last_request.method)
        self.assertResponseOK(resp, body=fake_response)

    @requests_mock.Mocker()
    def test_get(self, mock_req):
        mock_req.get(self.TEST_URL, text=fake_response)

        sclient = client.Client(self.TEST_ENDPOINT)
        resp = sclient._get(self.TEST_PATH)

        self.assertEqual("GET", mock_req.last_request.method)
        self.assertResponseOK(resp, body=fake_response)

    @requests_mock.Mocker()
    def test_post(self, mock_req):
        mock_req.post(self.TEST_URL, text=fake_response)

        sclient = client.Client(self.TEST_ENDPOINT)
        resp = sclient._post(self.TEST_PATH, json=fake_record)

        self.assertEqual("POST", mock_req.last_request.method)
        self.assertEqual(json.dumps(fake_record),
                         mock_req.last_request.body,)
        self.assertResponseOK(resp, body=fake_response)

    @requests_mock.Mocker()
    def test_put(self, mock_req):
        mock_req.put(self.TEST_URL, text=fake_response)

        sclient = client.Client(self.TEST_ENDPOINT)
        resp = sclient._put(self.TEST_PATH, data=fake_request)

        self.assertEqual("PUT", mock_req.last_request.method)
        self.assertEqual(
            fake_request,
            mock_req.last_request.body,
        )
        self.assertResponseOK(resp, body=fake_response)

    @requests_mock.Mocker()
    def test_not_found(self, mock_req):
        sclient = client.Client(self.TEST_ENDPOINT)
        status = 404

        mock_req.get(self.TEST_URL, status_code=status)

        exc = self.assertRaises(exceptions.NotFoundException, sclient._get,
                                self.TEST_PATH)
        self.assertEqual(status, exc.status_code)

    @requests_mock.Mocker()
    def test_server_error(self, mock_req):
        sclient = client.Client(self.TEST_ENDPOINT)
        status = 500

        mock_req.get(self.TEST_URL, status_code=500)

        exc = self.assertRaises(exceptions.HttpException, sclient._get,
                                self.TEST_PATH)
        self.assertEqual(status, exc.status_code)

    def assertResponseOK(self, resp, status=200, body=None):
        self.assertTrue(resp.ok)
        self.assertEqual(status, resp.status_code)
        if body:
            self.assertEqual(body, resp.text)
