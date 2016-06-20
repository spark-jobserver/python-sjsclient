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

Then call methods on its managers::

    >>> for app in sjs.apps.list():
    ...     print app.name
    ...
    824d89f1-224d-4083-8129-363b79849939
    36bb9cd3-054a-4ed7-a9f8-956a542c2357


    >>> for job in sjs.jobs.list():
    ...     print job.jobId
    ...
    8c5bd52f-6486-44ee-9ac3-a8327ee40494
    24b67573-3115-49c7-983c-d0eff0499b71
    99c8be9e-a0ec-42dd-8a2c-9a8680bc5051
    bb82f712-d4b4-43a4-8e4d-e4bb272e85db


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
