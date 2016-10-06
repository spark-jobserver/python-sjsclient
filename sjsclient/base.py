# -*- coding: utf-8 -*-

import collections


class ResourceManager(object):

    base_path = None
    resource_class = None

    def __init__(self, client):
        self.client = client

    def list(self, **kwargs):
        url = self.base_path
        resp = self.client._get(url, params=kwargs).json()
        for data in resp:
            yield self._create_resource(data)

    def _create_resource(self, data):
        return self.resource_class(self, data)


class Resource(collections.MutableMapping):
    base_path = None

    def __init__(self, manager, attrs=None):
        if attrs is None:
            attrs = {}
        self.manager = manager
        self._attrs = attrs
        self.update_attrs(attrs)

    def __getitem__(self, name):
        return self._attrs[name]

    def __setitem__(self, name, value):
        try:
            orig = self._attrs[name]
        except KeyError:
            changed = True
        else:
            changed = orig != value

        if changed:
            self._attrs[name] = value

    def __delitem__(self, name):
        del self._attrs[name]

    def __len__(self):
        return len(self._attrs)

    def __iter__(self):
        return iter(self._attrs)

    def update_attrs(self, *args, **kwargs):
        # ensure setters are called for type coercion
        for key, value in dict(*args).items():
            if key != "id":  # id property is read only
                self._attrs[key] = value
            setattr(self, key, value)

            for key, value in kwargs.items():
                setattr(self, key, value)

    def delete(self):
        return self.manager.delete()
