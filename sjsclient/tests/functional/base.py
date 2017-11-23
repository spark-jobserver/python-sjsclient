# -*- coding: utf-8 -*-

import os
import time

import requests
import testtools

from sjsclient import client
from sjsclient import exceptions

test_ctx = os.getenv("TESTSJS_SPARK_TEST_CTX")
test_py_ctx = "{}_py".format(test_ctx)
test_java_ctx = "{}_java".format(test_ctx)


class TestFunctionalSJS(testtools.TestCase):

    def setUp(self):
        super(TestFunctionalSJS, self).setUp()
        self.client = _get_sjsclient()
        artifact_dir = os.getenv("TESTSJS_SPARKJOB_ARTIFACT_DIR")
        jar_name = os.getenv("TESTSJS_SPARKJOB_JAR_URL").split('/')[-1]
        jar_path = os.path.join(artifact_dir, jar_name)
        self.jar_blob = open(jar_path, 'rb').read()
        egg_name = os.getenv("TESTSJS_SPARKJOB_EGG_URL").split('/')[-1]
        egg_path = os.path.join(artifact_dir, egg_name)
        self.egg_blob = open(egg_path, 'rb').read()

    def _get_functional_context(self):
        return get_functional_context(test_ctx)

    def _get_functional_py_context(self):
        return get_functional_context(test_py_ctx)

    def _get_functional_java_context(self):
        return get_functional_context(test_java_ctx)

    def _delete_ctx(self, name):
        self.client.contexts.delete(name)
        found = True
        while found:
            try:
                time.sleep(2)
                self.client.contexts.get(name)
            except exceptions.NotFoundException:
                found = False


def create_functional_context(ctx, factory=None):
    client = _get_sjsclient()
    try:
        client.contexts.delete(ctx)
    except exceptions.NotFoundException:
        pass
    time.sleep(5)
    if factory is None:
        client.contexts.create(ctx)
    else:
        params = {
            "context-factory": factory
        }
        client.contexts.create(ctx, params)

    time.sleep(2)


def get_functional_context(ctx):
    client = _get_sjsclient()
    return client.contexts.get(ctx)


def _get_sjsclient():
    sjs_url = os.getenv("TESTSJS_SPARKJOB_SERVER_URL")
    sjs_user = os.getenv("TESTSJS_SPARKJOB_SERVER_USERNAME")
    sjs_password = os.getenv("TESTSJS_SPARKJOB_SERVER_PASSWORD")
    auth = None
    if sjs_user or sjs_password:
        auth = requests.auth.HTTPBasicAuth(sjs_user, sjs_password)
    return client.Client(sjs_url, auth)


def bootstrap_testbed():
    create_functional_context(test_ctx)
    py_factory = "spark.jobserver.python.PythonSessionContextFactory"
    create_functional_context(test_py_ctx, py_factory)
    java_factory = "spark.jobserver.context.JavaSparkContextFactory"
    create_functional_context(test_java_ctx, java_factory)
