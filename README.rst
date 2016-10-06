Python client for Spark Jobserver
=================================

.. image:: https://travis-ci.org/spark-jobserver/python-sjsclient.svg?branch=master
  :target:  https://travis-ci.org/spark-jobserver/python-sjsclient
  :align: right

.. image:: https://coveralls.io/repos/spark-jobserver/python-sjsclient/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/spark-jobserver/python-sjsclient?branch=master
  :align: right

.. image:: https://readthedocs.org/projects/python-sjsclient/badge/?version=latest
   :target: http://python-sjsclient.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/python-sjsclient.svg
        :target: https://pypi.python.org/pypi/python-sjsclient
        :alt: Latest version

Features
--------

- Supports Spark Jobserver 0.6.0+


Library Installation
--------------------

::

   $ pip install python-sjsclient


Getting started
---------------

First create a client instance::

    >>> from sjsclient import client
    >>> sjs = client.Client("http://JOB_SERVER_URL:PORT")

Uploading a jar to Spark Jobserver::

    >>> jar_file_path = os.path.join("path", "to", "jar")
    >>> jar_blob = open(jar_file_path, 'rb').read()
    >>> app = sjs.apps.create("test_app", jar_blob)

Listing available apps::

    >>> for app in sjs.apps.list():
    ...     print app.name
    ...
    test_app
    my_streaming_app

Creating an adhoc job::

    >>> test_app = sjs.apps.get("test_app")
    >>> class_path = "spark.jobserver.VeryShortDoubleJob"
    >>> config = {"test_config": "test_config_value"}
    >>> job = sjs.jobs.create(test_app, class_path, conf=config)
    >>> print("Job Status: ", job.status)
    Job Status: STARTED

Polling for job status::

    >>> job = sjs.jobs.create(...)
    >>> while job.status != "FINISHED":
    >>>     time.sleep(2)
    >>>     job = sjs.jobs.get(job.jobId)

Getting job config::

    >>> config = {"test_config": "test_config_value"}
    >>> job = sjs.jobs.create(test_app, class_path, conf=config)
    >>> job_config = job.get_config()
    >>> print("test_config value: ", job_config["test_config"])
    test_config_value: test_config_value

Listing jobs::

    >>> for job in sjs.jobs.list():
    ...     print job.jobId
    ...
    8c5bd52f-6486-44ee-9ac3-a8327ee40494
    24b67573-3115-49c7-983c-d0eff0499b71
    99c8be9e-a0ec-42dd-8a2c-9a8680bc5051
    bb82f712-d4b4-43a4-8e4d-e4bb272e85db

Limiting jobs list::

    >>> for job in sjs.jobs.list(limit=1):
    ...     print job.jobId
    ...
    8c5bd52f-6486-44ee-9ac3-a8327ee40494

Creating a named context::

    >>> ctx_config = {'num-cpu-cores': '1', 'memory-per-node': '512m'}
    >>> ctx = sjs.contexts.create("test_context", ctx_config)

Running a job in a named context::

    >>> test_app = sjs.apps.get("test_app")
    >>> test_ctx = sjs.contexts.get("test_context")
    >>> config = {"test_config": "test_config_value"}
    >>> job = sjs.jobs.create(test_app, class_path, ctx=test_ctx, conf=config)
    >>> print("Job Status: ", job.status)
    Job Status: STARTED


Documentation
-------------

http://python-sjsclient.readthedocs.org


Discussion list
---------------

*spark-jobserver* google group: https://groups.google.com/forum/#!forum/spark-jobserver

Requirements
------------

- Python >= 2.7.0

License
-------

``python-sjsclient`` is offered under the Apache 2 license.

Source code
------------

The latest developer version is available in a github repository:
https://github.com/spark-jobserver/python-sjsclient
