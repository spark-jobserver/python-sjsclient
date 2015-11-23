# -*- coding: utf-8 -*-

import requests_mock

from oslotest import base

from sjsclient import client
from sjsclient import context
from sjsclient import exceptions
from sjsclient import utils

context_name = "test-context"
context_create_response = "OK"
context_repr = "<Context: %s>" % context_name
context_get_response = """
[
"%s"
]
""" % context_name


class TestContext(base.BaseTestCase):

    TEST_ENDPOINT = 'http://example.com:8090'

    def setUp(self):
        super(TestContext, self).setUp()
        self.client = client.Client(self.TEST_ENDPOINT)

    def assertContextFields(self, test_ctx):
        self.assertEqual(context_name, test_ctx.name)
        self.assertEqual(context_repr, repr(test_ctx))
        self.assertIsInstance(test_ctx, context.Context)

    @requests_mock.Mocker()
    def test_create(self, mock_req):
        post_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.contexts.base_path,
                                 context_name)

        mock_req.post(post_url, text=context_create_response)

        params = {'num-cpu-cores': '4',
                  'memory-per-node': '512m'}

        test_context = self.client.contexts.create(context_name, params)
        self.assertContextFields(test_context)

    @requests_mock.Mocker()
    def test_list(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)

        mock_req.get(get_url, text=context_get_response)

        ctx_list = self.client.contexts.list()
        self.assertContextFields(next(ctx_list))

    @requests_mock.Mocker()
    def test_get(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)

        mock_req.get(get_url, text=context_get_response)

        test_ctx = self.client.contexts.get(context_name)
        self.assertContextFields(test_ctx)

    @requests_mock.Mocker()
    def test_get_non_existing(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)

        mock_req.get(get_url, text=context_get_response)
        self.assertRaises(exceptions.NotFoundException,
                          self.client.contexts.get, 'does-not-exist')

    @requests_mock.Mocker()
    def test_delete(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path,
                                context_name)

        mock_req.delete(get_url, text=context_create_response)
        self.client.contexts.delete(context_name)

    @requests_mock.Mocker()
    def test_context_instance_delete(self, mock_req):
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path)
        del_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.contexts.base_path,
                                context_name)
        mock_req.get(get_url, text=context_get_response)
        test_ctx = self.client.contexts.get(context_name)
        mock_req.delete(del_url, text=context_create_response)
        test_ctx.delete()
