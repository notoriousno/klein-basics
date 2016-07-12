Request Variable: What is it and why is it passed in?
=====================================================

You may have noticed the ``request`` argument which gets passed into every route function.  This variable is a `Request <>`_ object and serves a very important purpose of holding valuable request information.  ``Request`` objects have an abundance of functionality in them, which would be tedious to convey in such a short tutorial.  I will try to demonstrate a few key features that are commonly used.


Write to the Frontend
---------------------

Content can slowly be added to the frontend using the ``Request.write()`` function.  Please note that the parameter must be a bytes type, Python 2.7 users don't have to worry as strings are bytes, however in Python 3, a string is **NOT** a bytes object.

.. code-block:: python

   @app.route('/write')
   def gradualWrite(request):
       request.write(b'<h1>Header</h1>')
       request.write(b'<h2>Header</h2>')
       request.write(b'<h3>Header</h3>')
       request.write(b'<h4>Header</h4>')
       request.write(b'<h5>Header</h5>')

Developers can use this method to gradually build content for the frontend.


Getting Query String or Form Arguments
--------------------------------------

A common use case for any web application would be to handle form data or a query string.  The following will simply display all the form data or query string that's passed along.

.. code-block:: python

   @app.route('/args')
   def arguments(request):
       return '{0}'.format(request.args)

Now lets test this route using ``GET`` with query strings and ``POST`` using form data.

.. code-block:: bash

   curl -X GET curl -X GET localhost:9000/args?Eminem=Superman\&Hoozier=Church
   curl -X POST -d Adele=Hello -d Adele="Fire to the Rain" localhost:9000/args


Cookies
-------

.. code-block:: python

   @app.route('/cookies')
   def cookies(request):
       value = request.args.get(b'cookie', [b'default'])
       request.addCookie('cookie', value[0])


Redirects
---------

.. code-block:: python

   @app.route('/redirect')
   def redirect(request):
       request.redirect('https://www.yahoo.com')


Finished Request
----------------

Interrupted Requests
--------------------

Sessions
--------

Examples
--------

*  `interrupted.py <https://github.com/notoriousno/klein-basics/blob/intro/src/interrupted.py>`_
