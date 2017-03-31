# -*- coding: utf-8 -*-

import requests_mock

from oslotest import base

from sjsclient import client
from sjsclient import context
from sjsclient import exceptions
from sjsclient import utils

CONTEXT_NAME = "test-context"
CONTEXT_CREATE_RESPONSE = "OK"
CONTEXT_REPR = "<Context: %s>" % CONTEXT_NAME
CONTEXT_GET_RESPONSE = """
[
"%s"
]
""" % CONTEXT_NAME


class TestContext(base.BaseTestCase):
    """Unit tests for context resource"""

    TEST_ENDPOINT = 'http://example.com:8090'

    def setUp(self):
        """Test suite setup"""
        super(TestContext, self).setUp()
        self.client = client.Client(self.TEST_ENDPOINT)

    def assert_ctx_fields(self, test_ctx):
        """Helper method for asserts"""
        self.assertEqual(CONTEXT_NAME, test_ctx.name)
        self.assertEqual(CONTEXT_REPR, repr(test_ctx))
        self.assertIsInstance(test_ctx, context.Context)

    @requests_mock.Mocker()
    def test_create(self, mock_req):
        """Test create context"""
        post_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.contexts.base_path,
                                 CONTEXT_NAME)

        mock_req.post(post_url, text=CONTEXT_CREATE_RESPONSE)

        params = {'num-cpu-cores': '4',
                  'memory-per-node': '512m'}

        test_context = self.client.contexts.create(CONTEXT_NAME, params)
        self.assert_ctx_fields(test_context)

    @requests_mock.Mocker()
    def test_list(self, mock_req):
        """Test list contexts"""
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)

        mock_req.get(get_url, text=CONTEXT_GET_RESPONSE)

        ctx_list = self.client.contexts.list()
        self.assert_ctx_fields(next(ctx_list))

    @requests_mock.Mocker()
    def test_get(self, mock_req):
        """Test get context"""
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)

        mock_req.get(get_url, text=CONTEXT_GET_RESPONSE)

        test_ctx = self.client.contexts.get(CONTEXT_NAME)
        self.assert_ctx_fields(test_ctx)

    @requests_mock.Mocker()
    def test_get_non_existing(self, mock_req):
        """Test get non existing context"""
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)

        mock_req.get(get_url, text=CONTEXT_GET_RESPONSE)
        self.assertRaises(exceptions.NotFoundException,
                          self.client.contexts.get, 'does-not-exist')

    @requests_mock.Mocker()
    def test_delete(self, mock_req):
        """Test context delete"""
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path,
                                CONTEXT_NAME)

        mock_req.delete(get_url, text=CONTEXT_CREATE_RESPONSE)
        self.client.contexts.delete(CONTEXT_NAME)

    @requests_mock.Mocker()
    def test_context_instance_delete(self, mock_req):
        """Test delete method of context instace"""
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)
        del_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path,
                                CONTEXT_NAME)
        mock_req.get(get_url, text=CONTEXT_GET_RESPONSE)
        test_ctx = self.client.contexts.get(CONTEXT_NAME)
        mock_req.delete(del_url, text=CONTEXT_CREATE_RESPONSE)
        test_ctx.delete()
