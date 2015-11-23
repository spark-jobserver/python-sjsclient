# -*- coding: utf-8 -*-

from sjsclient import base
from sjsclient import exceptions
from sjsclient import utils


class Context(base.Resource):
    """A Spark context."""

    def __repr__(self):
        return "<Context: %s>" % self.name

    def delete(self):
        """Delete context."""

        return self.manager.delete(self.name)


class ContextManager(base.ResourceManager):
    """Manage :class:`Context` resources."""

    base_path = "contexts"
    resource_class = Context

    def _create_resource(self, data):
        return self.resource_class(self, dict(name=data))

    def create(self, name, params=None):
        """Create a Spark context.

        :param name: Descriptive name of context
        :param params: Dictionary of context parameters
        :rtype: :class:`Context`
        """

        url = utils.urljoin(self.base_path, name)
        self.client._post(url, params=params)
        return self._create_resource(name)

    def delete(self, name):
        """Delete a specific Context.

        :param name: The name of the :class:`Context` to delete.
        """

        url = self.base_path
        url = utils.urljoin(url, name)
        resp = self.client._delete(url)
        return resp

    def get(self, name):
        """Get a specific Context.

        :param name: The name of the :class:`Context` to get.
        :rtype: :class:`Context`
        """

        if name not in [x.name for x in self.list()]:
            msg = "Context {} not found.".format(name)
            raise exceptions.NotFoundException(msg)

        return self._create_resource(name)
