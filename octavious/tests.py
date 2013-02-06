import unittest

from octavious.pipeline import Plugin, Pipeline
from utils import init_plugin, init_plugins, create_pipeline


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

    def test_init_plugin(self):
        class_name = 'octavious.tests.Plugin1'
        plugin = init_plugin(class_name)
        self.assertTrue(isinstance(plugin, Plugin))
        self.assertEqual(plugin.__class__.__name__, 'Plugin1')
        class_name = 'octavious.tests.Plugin4'
        with self.assertRaises(TypeError):
            init_plugin(class_name)

    def test_init_plugins(self):
        class_names = [
            'octavious.tests.Plugin1',
            'octavious.tests.Plugin2',
            'octavious.tests.Plugin3',
        ]
        plugins = init_plugins(class_names)
        self.assertTrue(isinstance(plugins, list))
        self.assertTrue(isinstance(plugins[0], Plugin))
        self.assertTrue(isinstance(plugins[1], Plugin))
        self.assertTrue(isinstance(plugins[2], Plugin))
        self.assertEqual(plugins[0].__class__.__name__, 'Plugin1')
        self.assertEqual(plugins[1].__class__.__name__, 'Plugin2')
        self.assertEqual(plugins[2].__class__.__name__, 'Plugin3')
        class_names += ['octavious.tests.Plugin4']
        with self.assertRaises(TypeError):
            init_plugins(class_names)


class TestPipeline(unittest.TestCase):

    def test_create_pipeline(self):
        class_names = [
            'octavious.tests.Plugin1',
            'octavious.tests.Plugin2',
            'octavious.tests.Plugin3',
        ]
        pipeline = create_pipeline(class_names)
        self.assertTrue(isinstance(pipeline, Pipeline))
        self.assertTrue(isinstance(pipeline.plugins[0], Plugin))
        self.assertTrue(isinstance(pipeline.plugins[1], Plugin))
        self.assertTrue(isinstance(pipeline.plugins[2], Plugin))
        self.assertEqual(
            pipeline.plugins[0].__class__.__name__, 'Plugin1')
        self.assertEqual(
            pipeline.plugins[1].__class__.__name__, 'Plugin2')
        self.assertEqual(
            pipeline.plugins[2].__class__.__name__, 'Plugin3')
        class_names += ['octavious.tests.Plugin4']
        with self.assertRaises(TypeError):
            create_pipeline(class_names)

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

if __name__ == '__main__':
    unittest.main()
