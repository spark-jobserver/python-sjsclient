# -*- coding: utf-8 -*-
import sys
import time
import uuid

from sjsclient import app
from sjsclient import exceptions
from sjsclient.tests.functional import base


class TestFunctionalJob(base.TestFunctionalSJS):
    """Job related functional tests"""
    def setUp(self):
        super(TestFunctionalJob, self).setUp()

    def _create_app(self):
        app_name = str(uuid.uuid4())
        test_app = self.client.apps.create(app_name, self.jar_blob)
        return test_app

    def _create_py_app(self):
        app_name = str(uuid.uuid4())
        test_app = self.client.apps.create(app_name, self.egg_blob,
                                           app.AppType.PYTHON)
        return test_app

    def _create_job(self, sjs_app, class_path, conf=None, ctx=None,
                    sync=False):
        job = None
        while not job:
            try:
                job = self.client.jobs.create(sjs_app, class_path,
                                              conf=conf, ctx=ctx, sync=sync)
            except exceptions.HttpException as exc:
                if "NO SLOTS AVAILABLE" in str(exc):
                    raise
        return job

    def test_job_create(self):
        """Test job creation"""
        test_app = self._create_app()
        class_path = "spark.jobserver.VeryShortDoubleJob"
        job = self._create_job(test_app, class_path,
                               ctx=self._get_functional_context())
        time.sleep(3)
        self.assertTrue(len(job.jobId) > 0)
        self.assertTrue(job.status == "STARTED")
        self._wait_till_job_is_done(job)

    def test_py_job_create(self):
        """Test python job creation"""
        test_app = self._create_py_app()
        class_path = "example_jobs.word_count.WordCountSparkSessionJob"
        conf = "input.strings = ['a', 'b', 'a', 'b']"
        job = self._create_job(test_app, class_path, conf,
                               ctx=self._get_functional_py_context())
        time.sleep(3)
        self.assertTrue(len(job.jobId) > 0)
        self.assertTrue(job.status == "STARTED")
        self._wait_till_job_is_done(job)

    def test_job_result(self):
        """Test job result"""
        test_app = self._create_app()
        class_path = "spark.jobserver.VeryShortDoubleJob"
        job = self.client.jobs.create(test_app, class_path,
                                      ctx=self._get_functional_context())
        time.sleep(3)
        self._wait_till_job_is_done(job)
        job = self.client.jobs.get(job.jobId)
        self.assertEqual("FINISHED", job.status)
        self.assertEqual([2, 4, 6], job.result)

    def test_py_job_result(self):
        """Test python job result"""
        test_app = self._create_py_app()
        class_path = "example_jobs.word_count.WordCountSparkSessionJob"
        conf = "input.strings = ['a', 'b', 'a', 'b']"
        job = self._create_job(test_app, class_path, conf,
                               ctx=self._get_functional_py_context())
        time.sleep(3)
        self._wait_till_job_is_done(job)
        job = self.client.jobs.get(job.jobId)
        self.assertEqual("FINISHED", job.status)
        self.assertEqual({"'a'": 2, "'b'": 2}, job.result)

    def test_java_job_result(self):
        """Test java job result"""
        test_app = self._create_app()
        class_path = "spark.jobserver.JavaHelloWorldJob"
        job = self._create_job(test_app, class_path,
                               ctx=self._get_functional_java_context())
        time.sleep(3)
        self._wait_till_job_is_done(job)
        job = self.client.jobs.get(job.jobId)
        self.assertEqual("FINISHED", job.status)
        self.assertEqual("Hi!", job.result)

    def test_job_result_with_conf(self):
        """Test job result with input conf"""
        test_app = self._create_app()
        conf = "stress.test.longpijob.duration = 1"
        class_path = "spark.jobserver.LongPiJob"
        job = self._create_job(test_app, class_path,
                               conf=conf,
                               ctx=self._get_functional_context())
        time.sleep(3)
        created_job = self.client.jobs.get(job.jobId)
        self.assertEqual(job.jobId, created_job.jobId)
        status = created_job.status
        self.assertTrue(status == "RUNNING" or status == "FINISHED")
        self._wait_till_job_is_done(created_job)
        job = self.client.jobs.get(job.jobId)
        self.assertEqual("FINISHED", job.status)
        sys.stderr.write("duration %s" % job.duration)
        self.assertTrue("1." in job.duration)

    def test_job_create_with_sync(self):
        """Test synchronous job creation"""
        test_app = self._create_app()
        class_path = "spark.jobserver.VeryShortDoubleJob"
        job = self._create_job(test_app, class_path,
                               ctx=self._get_functional_context(),
                               sync=True)
        self.assertEqual([2, 4, 6], job.result)

    def _wait_till_job_is_done(self, job):
        while job.status != "FINISHED":
            time.sleep(2)
            job = self.client.jobs.get(job.jobId)

    def test_job_delete(self):
        """Test job delete"""
        test_app = self._create_app()
        conf = "stress.test.longpijob.duration = 5"
        class_path = "spark.jobserver.LongPiJob"
        job = self.client.jobs.create(test_app, class_path,
                                      conf=conf,
                                      ctx=self._get_functional_context())
        time.sleep(3)
        resp = self.client.jobs.delete(job.jobId)
        self.assertEqual(200, resp.status_code)
        resp = resp.json()
        self.assertEqual("KILLED", resp["status"])

    def test_job_delete_non_existing(self):
        """Test job delete non existing job"""
        self.assertRaises(exceptions.NotFoundException,
                          self.client.jobs.delete, 'does-not-exist')

    def test_job_delete_completed_job(self):
        """Test job delete completed job"""
        test_app = self._create_app()
        class_path = "spark.jobserver.VeryShortDoubleJob"
        job = self.client.jobs.create(test_app, class_path,
                                      ctx=self._get_functional_context())
        time.sleep(3)
        self._wait_till_job_is_done(job)
        self.assertRaises(exceptions.NotFoundException,
                          self.client.jobs.delete, job.jobId)

    def test_get_job_config(self):
        """Test get job config"""
        test_app = self._create_app()
        class_path = "spark.jobserver.VeryShortDoubleJob"
        config = {"test_config": "test_config_value"}
        job = self.client.jobs.create(test_app, class_path,
                                      ctx=self._get_functional_context(),
                                      conf=config)
        time.sleep(3)
        self._wait_till_job_is_done(job)
        job = self.client.jobs.get(job.jobId)
        job_config = job.get_config()
        self.assertEqual("FINISHED", job.status)
        self.assertEqual(config["test_config"], job_config["test_config"])
