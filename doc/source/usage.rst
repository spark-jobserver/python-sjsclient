Usage
-----

First create a client instance::

    >>> from sjsclient import client
    >>> sjs = client.Client("http://JOB_SERVER_URL:PORT")

Then call methods on its managers::

    >>> sjs.apps.list()
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

For more information, see the reference:

.. toctree::
   :maxdepth: 2

   ref/index
