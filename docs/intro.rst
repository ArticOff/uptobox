Introduction
==============

This is the documentation for uptobox, a library for Python to aid
in creating bots that utilise the Uptobox API.

Prerequisites
---------------

uptobox works with Python 3.8 or higher. Support for earlier versions of Python
is not provided. Python 2.7 or lower is not supported. Python 3.7 or lower is not supported.

Installing
-----------

You can get the library directly from PyPI: ::

    python3 -m pip install -U uptobox

If you are using Windows, then the following should be used instead: ::

    py -3 -m pip install -U uptobox
    
Basic Concepts
---------------

uptobox revolves around the concept of events
An event is something you listen to and then respond to. For example, when the bot connect on Uptobox,
you will receive an event about it.

A quick example to showcase how events work:

.. code-block:: python3

    import uptobox

    client = uptobox.Client(token="token")

    @client.listen()
    def on_connect():
        print(f"Logged on as {client.user.name}!")

    client.login()
