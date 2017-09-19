# -*- coding: utf-8 -*-
from sjsclient import base
from sjsclient import utils


class JobStatus(object):
    """A Helper class that contains the job status"""

    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class Job(base.Resource):
    """A Spark job."""

    #: Job ID
    jobId = None
    #: Context name
    context = None
    #: Jobs status
    status = None
    #: Time taken by the job to finish
    duration = None
    #: Main java class path
    classpath = None
    #: Response from Spark.
    result = None

    def __repr__(self):
        return "<Job: %s>" % self.jobId

    def delete(self):
        """Delete job."""

        return self.manager.delete(self.jobId)

    def get_config(self):
        """Get job configuration."""

        return self.manager.get_config(self.jobId)


class JobConfig(dict):
    """A Spark job config dictionary."""
    pass


class JobManager(base.ResourceManager):
    """Manage :class:`Job` resources."""

    base_path = "jobs"
    resource_class = Job

    def _create_resource(self, data):
        job = self.resource_class(self, data)
        return job

    def create(self, app, class_path, conf=None, ctx=None, sync=False):
        """Create a Spark job.

        :param app: Instance of :class:`App`
        :param class_path: Main class path of spark job.
        :param conf: Configuration json
        :param ctx: Instance of :class:`Context`
        :param sync: Set to `True` for synchronous job creation
        :rtype: :class:`Job`
        """

        url = self.base_path
        params = {'appName': app.name,
                  'classPath': class_path}
        if ctx:
            params['context'] = ctx.name

        if sync:
            params['sync'] = 'true'

        resp = self.client._post(url, data=conf, params=params).json()
        return self._create_resource(resp)

    def get(self, job_id):
        """Get a specific Job. This returns more information than create.

        :param job_id: The jobId of the :class:`Job` to get.
        :rtype: :class:`Job`
        """

        url = utils.urljoin(self.base_path, job_id)
        resp = self.client._get(url).json()
        return self._create_resource(resp)

    def delete(self, job_id):
        """Delete a specific Job.

        :param job_id: The jobId of the :class:`Job` to get.
        """
        url = self.base_path
        url = utils.urljoin(url, job_id)
        resp = self.client._delete(url)
        return resp

    def get_config(self, job_id):
        """Get job configuration.

        :param job_id: The jobId of the :class:`Job` to get.
        :rtype: :class:`JobConfig`
        """

        url = utils.urljoin(self.base_path, job_id, "config")
        resp = self.client._get(url).json()
        return JobConfig(resp)
