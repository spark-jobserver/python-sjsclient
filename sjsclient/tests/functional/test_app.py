# -*- coding: utf-8 -*-

from sjsclient import exceptions

from sjsclient.tests.functional import base

import uuid


class TestFunctionalApp(base.TestFunctionalSJS):

    def _create_app(self):
        app_name = str(uuid.uuid4())
        test_app = self.client.apps.create(app_name, self.jar_blob)
        return (app_name, test_app)

    def test_list(self):
        (app_name1, test_app1) = self._create_app()
        (app_name2, test_app2) = self._create_app()
        app_list = [app.name for app in self.client.apps.list()]
        self.assertTrue(app_name1 in app_list)
        self.assertTrue(app_name2 in app_list)

    def test_create_app(self):
        (app_name, test_app) = self._create_app()
        self.assertEqual(test_app.name, app_name)
        self.assertIsNotNone(test_app.time)

    def test_get_app(self):
        (app_name, test_app) = self._create_app()
        test_app = self.client.apps.get(app_name)
        self.assertEqual(test_app.name, app_name)
        self.assertIsNotNone(test_app.time)

    def test_get_non_existing_app(self):
        self.assertRaises(exceptions.NotFoundException,
                          self.client.apps.get, 'does-not-exist')
