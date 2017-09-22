# -*- coding: utf-8 -*-

from sjsclient import app
from sjsclient import exceptions

from sjsclient.tests.functional import base

import time
import uuid


class TestFunctionalApp(base.TestFunctionalSJS):

    def _create_java_app(self):
        app_name = str(uuid.uuid4())
        test_app = self.client.apps.create(app_name, self.jar_blob)
        return (app_name, test_app)

    def _create_python_app(self):
        app_name = str(uuid.uuid4())
        test_app = self.client.apps.create(app_name, self.egg_blob,
                                           app_type=app.AppType.PYTHON)
        return (app_name, test_app)

    def _delete_app(self, name):
        self.client.apps.delete(name)
        found = True
        while found:
            try:
                time.sleep(2)
                self.client.apps.get(name)
            except exceptions.NotFoundException:
                found = False

    def test_list(self):
        (app_name1, test_app1) = self._create_java_app()
        (app_name2, test_app2) = self._create_java_app()
        app_list = [app.name for app in self.client.apps.list()]
        self.assertTrue(app_name1 in app_list)
        self.assertTrue(app_name2 in app_list)

    def test_create_java_app(self):
        (app_name, test_app) = self._create_java_app()
        self.assertEqual(test_app.name, app_name)
        self.assertIsNotNone(test_app.time)

    def test_create_python_app(self):
        (app_name, test_app) = self._create_python_app()
        self.assertEqual(test_app.name, app_name)
        self.assertIsNotNone(test_app.time)

    def test_get_app(self):
        (app_name, test_app) = self._create_java_app()
        test_app = self.client.apps.get(app_name)
        self.assertEqual(test_app.name, app_name)
        self.assertIsNotNone(test_app.time)

    def test_get_non_existing_app(self):
        self.assertRaises(exceptions.NotFoundException,
                          self.client.apps.get, 'does-not-exist')

    def test_delete_app(self):
        (app_name, test_app) = self._create_java_app()
        self._delete_app(app_name)
        self.assertRaises(exceptions.NotFoundException,
                          self.client.apps.get, app_name)
