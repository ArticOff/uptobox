Quickstart
============

This page gives a brief introduction to the library. It assumes you have the library installed,
if you don't check the :ref:`installing` portion.

A Minimal Bot
---------------

Let's make a bot that get the download URL of a file by his code.

.. code-block:: python3

    import uptobox

    client = uptobox.Client(token="token")

    @client.listen()
    async def on_connect():
        print(f'We have logged in as {client.user.name}')
        
        file = client.fetchFile("e9hrkzrylk58")
        url = client.download(file.code)
        print(url)

    client.login()
 
Let's name this file ``mySuperBot.py``. Make sure not to name it ``uptobox.py`` as that'll conflict
with the library.

There's a lot going on here, so let's walk you through it step by step.

1. The first line just imports the library, if this raises a :exc:`ModuleNotFoundError` or :exc:`ImportError`
   then head on over to :ref:`installing` section to properly install.
2. Next, we create an instance of a :class:`Client`. This client is our connection to Uptobox.
3. We then use the :meth:`Client.listen()` decorator to register an event. This library has many events.
4. Since the :func:`on_connect` event triggers when the bot is connected.
5. Afterwards, the bot will get the file object by the file code and get direct download link, due to the API, this action takes 30 seconds.
6. Finally, we run the bot with our login token.

Now that we've made a bot, we have to *run* the bot. Luckily, this is simple since this is just a
Python script, we can run it directly.

On Windows:

.. code-block:: shell

    $ py -3 mySuperBot.py

On other systems:

.. code-block:: shell

    $ python3 mySuperBot.py

Now you can try playing around with your basic bot.
