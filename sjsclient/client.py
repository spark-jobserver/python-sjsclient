# -*- coding: utf-8 -*-
import requests

from sjsclient import app
from sjsclient import context
from sjsclient import exceptions
from sjsclient import job
from sjsclient import utils


class Client(object):
    """Client for Spark Job Server"""

    def __init__(self, endpoint, auth=None):
        self.endpoint = endpoint
        self.auth = auth
        self.jobs = job.JobManager(self)
        self.apps = app.AppManager(self)
        self.contexts = context.ContextManager(self)

    def _get(self, path, **kwargs):
        """Perform an HTTP GET request."""
        return self._request(path, 'GET', **kwargs)

    def _post(self, path, **kwargs):
        """Perform an HTTP POST request."""
        return self._request(path, 'POST', **kwargs)

    def _put(self, path, **kwargs):
        """Perform an HTTP PUT request."""
        return self._request(path, 'PUT', **kwargs)

    def _delete(self, path, **kwargs):
        """Perform an HTTP DELETE request."""
        return self._request(path, 'DELETE', **kwargs)

    def _request(self, path, method, **kwargs):
        url = utils.urljoin(self.endpoint, path)
        http = requests.Session()
        if self.auth:
            kwargs['auth'] = self.auth
        resp = http.request(method, url, **kwargs)

        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            if resp.status_code == 404:
                exc_type = exceptions.NotFoundException
            else:
                exc_type = exceptions.HttpException
            raise exc_type(str(e),
                           details=self._parse_error_response(resp),
                           status_code=resp.status_code)
        return resp

    def _parse_error_response(self, resp):
        try:
            message = resp.json()['status']
        except ValueError:
            message = resp.text
        return message
