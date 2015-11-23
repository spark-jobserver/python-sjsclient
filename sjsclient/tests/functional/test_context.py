# -*- coding: utf-8 -*-

import uuid

from sjsclient import exceptions
from sjsclient.tests.functional import base


class TestFunctionalContext(base.TestFunctionalSJS):

    def setUp(self):
        super(TestFunctionalContext, self).setUp()

    def _create_ctx(self, name=None, params=None):
        if params is None:
            params = {'num-cpu-cores': '1',
                      'memory-per-node': '512m'}
        if name is None:
            name = "ctx_{}".format(str(uuid.uuid4()))

        ctx = self.client.contexts.create(name, params)
        return (name, ctx)

    def test_create_ctx_with_invalid_name(self):
        invalid_name = '1_name_starting_with_number'
        params = {'num-cpu-cores': '4',
                  'memory-per-node': '512m'}
        self.assertRaises(exceptions.HttpException,
                          self.client.contexts.create, invalid_name,
                          params)

    # Commented out because of multiple context issue
    # def test_ctx_create(self):
    #     (ctx_name, test_ctx) = self._create_ctx()
    #     self.assertEqual(test_ctx.name, ctx_name)
    #     self._delete_ctx(ctx_name)

    def test_ctx_delete_non_existing(self):
        self.assertRaises(exceptions.NotFoundException,
                          self.client.contexts.delete, 'does-not-exist')

    # Commented out because of multiple context issue
    # def test_ctx_delete(self):
    #     (ctx_name, test_ctx) = self._create_ctx()
    #     self._delete_ctx(ctx_name)
    #     self.assertRaises(exceptions.NotFoundException,
    #                       self.client.contexts.get, ctx_name)

    def test_ctx_get_non_existing(self):
        self.assertRaises(exceptions.NotFoundException,
                          self.client.contexts.get, 'does-not-exist')

    # Commented out because of multiple context issue
    # def test_ctx_get(self):
    #     (ctx_name, test_ctx) = self._create_ctx()
    #     get_ctx = self.client.contexts.get(ctx_name)
    #     self.assertEqual(get_ctx.name, test_ctx.name)
    #     self._delete_ctx(ctx_name)
