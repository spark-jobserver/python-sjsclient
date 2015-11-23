from oslotest import base

from sjsclient import base as sjs_base


class FakeManager(object):
    def delete(self):
        return True


class TestResource(base.BaseTestCase):
    def test_resource_init(self):
        data = {"id": 1,
                "foo": "bar",
                "bar": "foo"}
        res = sjs_base.Resource(FakeManager, data)
        res["foobar"] = "barfoo"
        res["foobar"] = "foobar"
        self.assertEqual(4, len(res))
        for key in res:
            self.assertTrue(key in res)

    def test_resource_init_with_none_data(self):
        res = sjs_base.Resource(FakeManager)

        def func(x):
            return x.foo
        self.assertRaises(AttributeError, func, res)

    def test_resource_get(self):
        data = {"foo": "bar"}
        res = sjs_base.Resource(FakeManager, data)
        self.assertEqual("bar", res.get('foo'))

    def test_resource_delete(self):
        data = {"foo": "bar"}
        res = sjs_base.Resource(FakeManager(), data)
        self.assertTrue(res.delete())

    def test_resource_del(self):
        data = {"foo": "bar"}
        res = sjs_base.Resource(FakeManager(), data)
        del res["foo"]
        self.assertEqual(0, len(res))

    def test_update_attrs_with_kwargs(self):
        data = {"foo": "bar"}
        res = sjs_base.Resource(FakeManager(), data)
        res.update_attrs(data, bar="foo")
        self.assertEqual(1, len(res))
        self.assertEqual("foo", res.bar)
