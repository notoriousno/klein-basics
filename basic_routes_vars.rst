Basics: Routes, Methods, Variables
==================================

.. note::

   This section contains many similarities with Flask.  So if you know how to install pip packages and do basic Flask-style routing, this section can be skipped.  Just keep in mind that a ``request`` parameter must first be passed in all route functions.  Example::

      route('/')
      def example(request):
         ...


Web frameworks have come a long way, especially in Python.  A major contributing factor is the dead simple routing syntax from Flask, Bottle, Hug, etc.  Klein shares syntactical similarities with those frameworks for the most part.  The only key difference is the ``request`` parameter that gets passed into the functions after specifying the route, but we won't worry about that for now.  Let’s dive into Klein with a simple Hello World application.


Routes *aka* Hello World
------------------------

.. code-block:: python

   from klein import Klein

   app = Klein()

   @app.route('/')
   def root(request):
      return 'Welcome'

   @app.route('/hello')
   def hello(request):
      return 'Hello World'

   app.run(host='localhost', port=9000)

To start the Klein application by simply running the file via Python::

   python helloworld.py

This application will create a web server listening on the ``localhost`` interface on port ``9000`` all in the ``app.run()`` function.  Change the host and ports according to your requirements.  ``app.route()`` create the endpoints for your application, so in our snippet, there's the default route and a route for ``/hello``.  A quick test can be done in a web browser by navigating to http://localhost:9000 or by using the ``curl`` utility::

   curl localhost:9000
   curl localhost:9000/hello


Return Types
------------

Klein accepts ``bytes``, ASCII encoded string, a Twisted Resource, or Renderable.


Request Methods
---------------

The HTTP methods ``GET``, ``POST``, ``PUT``, ``DELETE`` are common amongst web applications.  In Klein, routes can be explicitly tied to request methods by passing in a list of the methods names via a parameter aptly called ``methods``.  If no explict method is specified, then all methods will be accepted.

.. code-block:: python

   import json
   from klein import Klein

   app = Klein()
   @app.route('/')
   def root(request):
       return 'Welcome'

   @app.route('/methods', methods=['POST', 'delete'])
   def specificMethods(request):
       return json.dumps({
                          'boolean': True,
                          'int': 1,
                          'list': [1,2,3]
                        })

   app.run(host='localhost', port=9000)

The ``/methods`` endpoint will output JSON data if and only if the endpoint is accessed using the POST or DELETE methods (note that methods are not case sensitive).  Where as the ``/`` can be accessed by any method since no explicit methods are specified.

.. code-block:: bash

   $> curl -X POST localhost:9000/methods
   $> curl -X DELETE localhost:9000/methods
   $> curl -X POST localhost:9000

   # this will fail
   $> curl -X GET localhost:9000/methods

Speaking of “any method”, custom methods can also be used.  For instance, let’s say your application requires a method called “GOOGLE”.  All that needs to be done is to add “GOOGLE” to the list of methods then check using ``curl -X GOOGLE``.

.. code-block:: python

   @app.route('/methods', methods=['POST', 'delete', 'GOOGLE'])
   def specificMethods(request):
       return json.dumps({
                          'boolean': True, 
                          'int': 1, 
                          'list': [1,2,3]
                         })

Variables
---------

Variables works by simply appending a variable name surrounded by angle brackets to the URL string.  Variables allow for your app to take in any string parameter and use it in the function corresponding to the route.  As an example, the following will display a message followed by a name passed in from the URL:

.. code-block:: python
   
   @app.route('/hello/<name>')
   def helloName(request, name):
       return 'Hello %s!' % name

Optionally, a type specifier can be supplied so that the string variable will be cast to a specified type.  This allows variables to be validated without extraneous code.  Out of the box, the specifiers are ``int``, ``float``, and ``path``.

.. code-block:: python
   

   @app.route('/hello/<name>/<int:age>')
   def helloNameAge(request, name, age):
   if age <= 1:
       return '%s is just starting life.' % name
   elif age >= 2 and age <= 29: 
       return '%s is %d years old. You are so young!' % (name, age)
   return '%s is %d years old! You are so old!' % (name, age)


Final Example
-------------

.. code-block:: python

   import json
   from klein import Klein

   app = Klein()

   @app.route('/')
   def root(request):
       return 'Welcome'

   @app.route('/hello')
   def hello(request):
       return 'Hello World'

   @app.route('/hello/<name>')
   def helloName(request, name):
       return 'Hello %s!' % name

   @app.route('/hello/<name>/<int:age>')
   def helloNameAge(request, name, age):
       if age <= 1:
           return '%s is just starting life.' % name
       elif age >= 2 and age <= 29:
           return '%s is %d years old. You are so young!' % (name, age)
       return '%s is %d years old! You are so old!' % (name, age)

   @app.route('/methods', methods=['POST', 'delete', 'Google'])
   def specificMethods(request):
       return json.dumps({
                          'boolean': True,
                          'int': 1,
                          'list': [1,2,3]
                        })

   app.run(host='localhost', port=9000)
