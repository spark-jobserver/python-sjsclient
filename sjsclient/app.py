# -*- coding: utf-8 -*-

import time

from sjsclient import base
from sjsclient import exceptions
from sjsclient import utils


class AppType(object):
    """A helper class that contains app types"""

    JAVA = "java"
    PYTHON = "python"
    _APP_TYPES_HEADER_MAP = {
        JAVA: "application/java-archive",
        PYTHON: "application/python-archive"
    }

    @staticmethod
    def get_header(app_type):
        return AppType._APP_TYPES_HEADER_MAP[app_type]


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

    base_path = "binaries"
    resource_class = App

    def create(self, name, app_binary, app_type=AppType.JAVA):
        """Create an app.

        :param name: Descriptive name of application
        :param app_binary: Application binary
        :param app_type: App type, for example java or python, default: java
        :rtype: :class:`App`
        """
        headers = {'Content-Type': AppType.get_header(app_type)}
        url = self.base_path
        url = utils.urljoin(url, name)
        # Strange that it is not JSON
        self.client._post(url, data=app_binary, headers=headers)
        time.sleep(1)
        return self.get(name)

    def delete(self, name):
        """Delete a specific App.

        :param name: The name of the :class:`App` to delete.
        """

        url = self.base_path
        url = utils.urljoin(url, name)
        resp = self.client._delete(url)
        return resp

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
