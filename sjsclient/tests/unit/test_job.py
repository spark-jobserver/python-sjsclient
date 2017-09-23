# -*- coding: utf-8 -*-

from oslotest import base
import requests_mock

from sjsclient import client
from sjsclient import exceptions
from sjsclient import job
from sjsclient import utils

job_id = "65efab5c-8b75-4454-a42c-882ff4c48786"
start_time = "2015-04-13T12:25:57.691+05:30"
duration = "10.68 secs"
started = "STARTED"
finished = "FINISHED"
running = "RUNNING"
context = "test-context"
class_path = "test.class.path"
result = "[1, 2, 3]"

job_create_response = """
{
  "status": "%s",
  "jobId": "%s",
  "context": "%s"
}
""" % (started, job_id, context)

job_create_with_sync_response = """
{
  "jobId": "%s",
  "result": %s
}
""" % (job_id, result)

job_get_result_response = """
{
  "duration": "%s",
  "classPath": "%s",
  "startTime": "%s",
  "context": "%s",
  "status": "%s",
  "jobId": "%s",
  "result": %s
}
""" % (duration, class_path, start_time, context, finished, job_id, result)

job_get_status_not_found_response = """
{
  "status": "ERROR",
  "result": "No such job ID xxxx"
}
"""

job_status_response = """
{
  "duration": "%s",
  "classPath": "%s",
  "startTime": "%s",
  "context": "%s",
  "status": "%s",
  "jobId": "%s"
}
""" % (duration, class_path, start_time, context, running, job_id)

job_list_response = """
[{
  "duration": "%s",
  "classPath": "%s",
  "startTime": "%s",
  "context": "%s",
  "status": "%s",
  "jobId": "%s"
}]
""" % (duration, class_path, start_time, context, running, job_id)

job_delete_response = """
{
  "status": "KILLED"
}
"""

job_config_response = """
{
   "test_config": "test_value"
}
"""

job_repr = "<Job: %s>" % job_id


class FakeApp(object):
    name = "test_app"


class FakeContext(object):
    name = "test-context"


class TestJob(base.BaseTestCase):
    TEST_ENDPOINT = 'http://example.com:8090'

    def setUp(self):
        super(TestJob, self).setUp()
        self.client = client.Client(self.TEST_ENDPOINT)

    def assertJobFields(self, test_job, status):
        self.assertEqual(job_repr, repr(test_job))
        self.assertIsInstance(test_job, job.Job)
        self.assertEqual(duration, test_job.duration)
        self.assertEqual(class_path, test_job.classPath)
        self.assertEqual(start_time, test_job.startTime)
        self.assertEqual(context, test_job.context)
        self.assertEqual(status, test_job.status)
        self.assertEqual(job_id, test_job.jobId)

    @requests_mock.Mocker()
    def test_job_list(self, mock_req):
        list_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.jobs.base_path)

        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)
        mock_req.get(get_url, text=job_get_result_response)
        mock_req.get(list_url, text=job_list_response)
        job_list = self.client.jobs.list()
        test_job = next(job_list)
        self.assertJobFields(test_job, running)

    @requests_mock.Mocker()
    def test_create(self, mock_req):
        post_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.jobs.base_path)
        query = "?classPath=test.class.path&appName=test_app"
        post_url = "{}{}".format(post_url, query)

        mock_req.post(post_url, text=job_create_response)

        test_job = self.client.jobs.create(FakeApp, "test.class.path")
        self.assertEqual(context, test_job.context)
        self.assertEqual(started, test_job.status)
        self.assertEqual(job_id, test_job.jobId)

        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)
        mock_req.get(get_url, text=job_get_result_response)
        test_job_result = self.client.jobs.get(test_job.jobId)
        self.assertEqual(finished, test_job_result.status)
        self.assertEqual([1, 2, 3], test_job_result.result)

    @requests_mock.Mocker()
    def test_create_with_ctx(self, mock_req):
        post_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.jobs.base_path)
        query = ("?classPath=test.class.path&appName=test_app&"
                 "context=test-context")
        post_url = "{}{}".format(post_url, query)

        mock_req.post(post_url, text=job_create_response)

        test_job = self.client.jobs.create(FakeApp, "test.class.path",
                                           ctx=FakeContext)
        self.assertEqual(context, test_job.context)
        self.assertEqual(started, test_job.status)
        self.assertEqual(job_id, test_job.jobId)

        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)

        mock_req.get(get_url, text=job_get_result_response)
        test_job_result = self.client.jobs.get(test_job.jobId)
        self.assertEqual(finished, test_job_result.status)
        self.assertEqual([1, 2, 3], test_job_result.result)

    @requests_mock.Mocker()
    def test_create_with_sync(self, mock_req):
        post_url = utils.urljoin(self.TEST_ENDPOINT,
                                 self.client.jobs.base_path)
        query = "?classPath=test.class.path&appName=test_app"
        post_url = "{}{}".format(post_url, query)

        mock_req.post(post_url, text=job_create_with_sync_response)

        test_job_result = self.client.jobs.create(FakeApp, "test.class.path",
                                                  sync=True)
        self.assertEqual(job_id, test_job_result.jobId)
        self.assertEqual([1, 2, 3], test_job_result.result)

    @requests_mock.Mocker()
    def test_get(self, mock_req):
        status_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   job_id)
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)
        mock_req.get(get_url, text=job_get_result_response)
        mock_req.get(status_url, text=job_status_response)
        test_job = self.client.jobs.get(job_id)
        self.assertJobFields(test_job, running)

    @requests_mock.Mocker()
    def test_get_after_sjs_restart(self, mock_req):
        status_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   job_id)
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)
        mock_req.get(get_url, status_code=404)
        mock_req.get(status_url, text=job_status_response)
        test_job = self.client.jobs.get(job_id)
        self.assertJobFields(test_job, running)

    @requests_mock.Mocker()
    def test_get_non_existing(self, mock_req):
        status_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   "does-not-exist")
        mock_req.get(status_url, text=job_get_status_not_found_response,
                     status_code=404)
        self.assertRaises(exceptions.NotFoundException,
                          self.client.jobs.get, 'does-not-exist')

    @requests_mock.Mocker()
    def test_delete(self, mock_req):
        delete_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   job_id)
        mock_req.delete(delete_url, text=job_delete_response)
        resp = self.client.jobs.delete(job_id)
        self.assertEqual(200, resp.status_code)
        resp = resp.json()
        self.assertEqual("KILLED", resp["status"])

    @requests_mock.Mocker()
    def test_job_instance_delete(self, mock_req):
        delete_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   job_id)
        status_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   job_id)
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)
        mock_req.get(get_url, text=job_get_result_response)
        mock_req.get(status_url, text=job_status_response)
        mock_req.delete(delete_url, text=job_delete_response)
        test_job = self.client.jobs.get(job_id)
        resp = test_job.delete()
        self.assertEqual(200, resp.status_code)
        resp = resp.json()
        self.assertEqual("KILLED", resp["status"])

    @requests_mock.Mocker()
    def test_get_config(self, mock_req):
        config_url = utils.urljoin(self.TEST_ENDPOINT,
                                   self.client.jobs.base_path,
                                   job_id, "config")
        get_url = utils.urljoin(self.TEST_ENDPOINT,
                                self.client.jobs.base_path,
                                job_id)
        mock_req.get(get_url, text=job_get_result_response)
        mock_req.get(config_url, text=job_config_response)
        jobObj = self.client.jobs.get(job_id)
        job_config = jobObj.get_config()
        self.assertIsInstance(job_config, job.JobConfig)
        self.assertEqual("test_value", job_config["test_config"])
