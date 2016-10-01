# -*- coding: utf-8 -*-

import os
import time

import requests
import testtools

from sjsclient import client
from sjsclient import exceptions

test_ctx = os.getenv("TESTSJS_SPARK_TEST_CTX")


class TestFunctionalSJS(testtools.TestCase):

    def setUp(self):
        super(TestFunctionalSJS, self).setUp()
        self.client = _get_sjsclient()
        jars_dir = os.getenv("TESTSJS_SPARKJOB_JARS_DIR")
        jar_name = os.getenv("TESTSJS_SPARKJOB_JAR_URL").split('/')[-1]
        jar_path = os.path.join(jars_dir, jar_name)
        self.jar_blob = open(jar_path, 'rb').read()

    def _get_functional_context(self):
        return get_functional_context()

    def _delete_ctx(self, name):
        self.client.contexts.delete(name)
        found = True
        while found:
            try:
                time.sleep(2)
                self.client.contexts.get(name)
            except exceptions.NotFoundException:
                found = False


def create_functional_context():
    client = _get_sjsclient()
    try:
        client.contexts.delete(test_ctx)
    except exceptions.NotFoundException:
        pass
    time.sleep(5)
    client.contexts.create(test_ctx)
    time.sleep(2)


def get_functional_context():
    client = _get_sjsclient()
    return client.contexts.get(test_ctx)


def _get_sjsclient():
    sjs_url = os.getenv("TESTSJS_SPARKJOB_SERVER_URL")
    sjs_user = os.getenv("TESTSJS_SPARKJOB_SERVER_USERNAME")
    sjs_password = os.getenv("TESTSJS_SPARKJOB_SERVER_PASSWORD")
    auth = None
    if sjs_user or sjs_password:
        auth = requests.auth.HTTPBasicAuth(sjs_user, sjs_password)
    return client.Client(sjs_url, auth)


def bootstrap_testbed():
    create_functional_context()
