# -*- coding: utf-8 -*-

from sjsclient import base
from sjsclient import exceptions
from sjsclient import utils


class App(base.Resource):
    """An app is a spark application."""

    #: Name of the App
    name = None
    #: App creation time
    time = None

    def __repr__(self):
        return "<App: %s>" % self.name


class AppManager(base.ResourceManager):
    """Manage :class:`App` resources."""

    base_path = "jars"
    resource_class = App

    def create(self, name, jar_blob):
        """Create an app.

        :param name: Descriptive name of application
        :param jar_blob: Jar binary
        :rtype: :class:`App`
        """

        url = self.base_path
        url = utils.urljoin(url, name)
        # Strange that it is not JSON
        self.client._post(url, data=jar_blob)
        return self.get(name)

    def get(self, name):
        """Get a specific App.

        :param name: The name of the :class:`App` to get.
        :rtype: :class:`App`
        """

        url = self.base_path
        resp = self.client._get(url).json()

        if name not in resp:
            msg = "App {} not found.".format(name)
            raise exceptions.NotFoundException(msg)

        data = {"name": name, "time": resp[name]}
        return self._create_resource(data)

    def list(self):
        """Lists Apps."""

        url = self.base_path
        resp = self.client._get(url).json()
        for k, v in resp.items():
            data_dict = {"name": k, "time": v}
            yield self._create_resource(data_dict)
