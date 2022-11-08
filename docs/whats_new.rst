Changelog
============

This page keeps a detailed human friendly rendering of what's new and changed
in specific versions

v1.1.0
-------

New Features
~~~~~~~~~~~~~~
- Add the variable ``File.streamURL`` to get the stream URL of the file

Other
~~~~~~~~~~~~~~
- Optimization

v1.0.6
-------

Bug Fixes
~~~~~~~~~~
- Fix the module was uninstallable on pip

New Features
~~~~~~~~~~~~~~

- Add the function ``Client.download()`` to get the direct link to download something
- Add the function ``Client.upload()`` to upload files on Uptobox
- Add the event ``on_error``

v1.0.0
-------

The first version of the module

New Features
~~~~~~~~~~~~~~

- Add the function ``Client.login()`` to connect to Uptobox
- Add the function ``Client.logout()`` to disconnect to Uptobox
- Add the function ``Client.listen()`` to make events
- Add the class ``Client.user`` to get the account
- Add the function ``Client.fetchFile()`` to get the file object through the file code
- Add the event ``on_connect``
- Add the event ``on_logout``
