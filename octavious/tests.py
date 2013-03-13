import unittest

from mock import patch, Mock

from octavious.pipeline import Plugin, Pipeline
from octavious.utils import load_symbol, call_symbol


class Plugin1(Plugin):

    def pre_process(self, input):
        return {'pre_processed_1': True}

    def post_process(self, input, output):
        output['post_processed_1'] = True
        return output


class Plugin2(Plugin):

    def pre_process(self, input):
        return {'pre_processed_2': True}

    def post_process(self, input, output):
        new_output = output.copy()
        new_output['post_processed_2'] = True
        return new_output


class Plugin3(Plugin):

    def pre_process(self, input):
        return {'pre_processed_3': True}

    def post_process(self, input, output):
        output['post_processed_3'] = True
        return output


class Plugin4(object):
    pass


class TestUtils(unittest.TestCase):

    def test_load_symbol(self):
        plugin_class = load_symbol('octavious.tests', 'Plugin1')
        self.assertEqual(plugin_class.__name__, 'Plugin1')
        with self.assertRaises(ImportError):
            load_symbol('octavious.tests', 'NotAvailableSymbol')

    def test_call_symbol(self):
        plugin = call_symbol('octavious.tests', 'Plugin1')
        self.assertEqual(plugin.__class__.__name__, 'Plugin1')
        self.assertTrue(isinstance(plugin, Plugin1))
        with self.assertRaises(ImportError):
            call_symbol('octavious.tests', 'NotAvailableSymbol')


class TestPipeline(unittest.TestCase):

    def test_pipeline(self):
        plugins = [
            call_symbol('octavious.tests', 'Plugin1'),
            call_symbol('octavious.tests', 'Plugin2'),
            call_symbol('octavious.tests', 'Plugin3'),
        ]
        pipeline = Pipeline(plugins)
        output = pipeline.pre_process({})
        output = pipeline.post_process({}, output)
        self.assertTrue(output['pre_processed_1'])
        self.assertTrue(output['post_processed_1'])
        self.assertTrue(output['post_processed_2'])
        self.assertTrue(output['post_processed_3'])
        with self.assertRaises(KeyError):
            self.assertTrue(output['pre_processed_2'])
        with self.assertRaises(KeyError):
            self.assertTrue(output['pre_processed_3'])


class TestGeventParallelizer(unittest.TestCase):

    def setUp(self):
        try:
            from octavious.parallelizer.gevent import GeventParallelizer
        except ImportError:
            self.skipTest("gevent library is not found.")
        else:
            self.parallelizer_class = GeventParallelizer

    @patch("gevent.monkey.patch_all")
    def test_monkey_patch(self, patch_all):
        self.parallelizer_class()
        patch_all.assert_any_call()

    @patch("gevent.spawn")
    @patch("gevent.joinall")
    def test_parallelizing(self, joinall, spawn):
        input_value = "foo"
        output_value = "bar"

        greenlet = Mock()
        greenlet.value = output_value

        def side_effect(callback):
            callback(greenlet)

        greenlet.link.side_effect = side_effect
        spawn.return_value = greenlet

        processor = Mock()
        parallelizer = self.parallelizer_class(patch_builtins=False)
        results = parallelizer(processors=[processor], input=input_value)

        spawn.assert_called_with(processor, "foo")
        joinall.assert_called_with([greenlet])
        self.assertEqual(results, ["bar"])


class TestEventletParallelizer(unittest.TestCase):

    def setUp(self):
        try:
            from octavious.parallelizer.eventlet import EventletParallelizer
        except ImportError:
            self.skipTest("eventlet library is not found.")
        else:
            self.parallelizer_class = EventletParallelizer

    @patch("eventlet.monkey_patch")
    def test_monkey_patch(self, monkey_patch):
        self.parallelizer_class()
        monkey_patch.assert_any_call()

    @patch("eventlet.GreenPool")
    def test_parallelizer(self, pool_class):
        input_value = "foo"
        output_value = "bar"

        green_thread = Mock()
        green_thread.wait.return_value = output_value

        pool = pool_class()

        def side_effect(callback):
            callback(green_thread)

        green_thread.link.side_effect = side_effect
        pool.spawn.return_value = green_thread

        processor = Mock()
        parallelizer = self.parallelizer_class(patch_builtins=False)
        results = parallelizer(processors=[processor], input=input_value)

        pool.spawn.assert_called_with(processor, "foo")
        pool.waitall.asssert_any_call()
        self.assertEqual(results, ["bar"])


if __name__ == '__main__':
    unittest.main()
