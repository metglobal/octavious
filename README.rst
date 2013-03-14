=========
Octavious
=========
.. image:: https://github.com/metglobal/octavious/raw/master/dococtopus.gif

Octavious is a very lightweight concurrency framework helps you parallelize
your tasks through a plugin pipeline system.

Currently it supports concurrency technologies such as:

* Multiprocessing (python builtin)
* Threading (python builtin)
* Celery (message Queues)
* Gevent (green threads)

Quick Overview
--------------

Processor
~~~~~~~~~

First of all, you have to define your processor that's going to be working as
parallelized. Let's have look at the example below.

.. code:: python

    # processes/chucknjoke.py
    import urllib
    from octavious.processor import Processor

    class ChuckNJokeProcessor(Processor):
        def process(self, input):
            url = 'http://api.icndb.com/jokes/%s' % input
            return urllib.urlopen(url % input).read()

    processor = ChuckNJokeProcessor

In this example defined, `ChuckNJokeProcessor` joins to given url
and brings the Chuck Norris Jokes as parallelized that are going to be
processed via the plugins.

Plugin
~~~~~~

Plugins already have methods such as `pre-process` and `post-process`. If you
want to make changes on your input data coming from your processor you have to implement the defined `pre-process`, and if you want to make changes on output data
you have to implement the defined `post process`.

As you may see in the example below, this is our first plugin. We are going to
take the RAW JSON data and decode.

.. code:: python

    # plugins/jsondeserializer.py
    import json
    from octavious.pipeline import Plugin

    class JsonDeserializerPlugin(Plugin):
        def post_process(self, input, output):
            return json.loads(output)

    plugin = JsonDeserializerPlugin

And our second plugin

.. code:: python

    # plugins/dictdigger.py
    from octavious.pipeline import Plugin

    class DictDiggerPlugin(Plugin):
        def __init__(self, path):
            self.path = path

        def post_process(self, input, output):
            entry = output
            for component in self.path.split('.'):
                entry = entry.get(component)
            return entry

    plugin = DictDiggerPlugin

This is for getting what data we want from tree structured dictionary.

Pipeline
~~~~~~~~

Pipelines are for running the plugins in the sequence that we desire.
You can create a pipeline with a bunch of plugins just like below.

.. code:: python

    from octavious.utils import pipeline, plugin

    chuck_norris_pipeline = pipeline(
        plugin('chuck_norris.plugins.dictdigger', 'value.joke'),
        plugin('chuck_norris.plugins.jsondeserializer'),
    )

Parallelizer
~~~~~~~~~~~~

As above we have 4 parallelizer options implemented for Octavious. You can set
the parallelizer settings like below

.. code:: python

    chuck_norris_parallellizer = parallelizer(
        'octavious.parallelizer.multiprocessing')

You can also use desired parallelizer backend with choice of

* `octavious.parallelizer.threading`
* `octavious.parallelizer.gevent`
* `octavious.parallelizer.celery`
* `octavious.parallelizer.eventlet`

Convenient Processors
~~~~~~~~~~~~~~~~~~~~~

There are some auxiliary `Processor` implementations help you define
parallelizing workflows.

* `OneToManyProcessor` wraps your processors to work with just one input.
* `ManyToOneProcessor` wraps your processor to works with multiple inputs.

We are going to work with `ManyToOneProcessor` in ChuckNorris example.
This is our last setting below as a summary, that we will make our code work.

.. code:: python

    from octavious.utils import pipeline, processor, plugin, parallelizer
    from octavious.processor import ManyToOneProcessor, PipelineProcessor

    chn_processor = processor('chuck_norris.processes.chucknjoke')
    chn_parallellizer = parallelizer('octavious.parallelizer.gevent')
    chn_pipeline = pipeline(
        plugin('chuck_norris.plugins.dictdigger', 'value.joke'),
        plugin('chuck_norris.plugins.jsondeserializer'),
    )

    manytoone = ManyToOneProcessor(
                  PipelineProcessor(cnj_processor, chn_pipeline),
                  chn_parallelizer)

    for result in manytoone(range(1, 4)):
        print '*', result

Run the example app

.. code:: console

    $ python -m examples.simple
    * Chuck Norris uses ribbed condoms inside out, so he gets the pleasure.
    * Chuck Norris doesn't read books. He stares them down until he gets the information he wants.
    * MacGyver can build an airplane out of gum and paper clips. Chuck Norris can kill him and take it.

Tests
-----

Octavious has a bunch of unit tests. To run them, simply type

.. code:: console

    $ python -m unittest -v octavious.tests
    test_pipeline (octavious.tests.TestPipeline) ... ok
    test_call_symbol (octavious.tests.TestUtils) ... ok
    test_load_symbol (octavious.tests.TestUtils) ... ok

    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    OK

Status
------

Currently in very early stages, please stay tuned!

License
-------

Copyright (c) 2013 Metglobal LLC.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
